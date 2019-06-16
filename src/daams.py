#!/usr/bin/env python3
import argparse
import threading
from datetime import datetime
import os
import random
import string
import sys
import time
import sched

import blkar
import system_diagnostics
from system_diagnostics import sys_info, shutdown_normal, shutdown_error, OSShutdownRequest
from cpu_diagnostics import CPUMonitor

from print_utils import print_w_time

from ecsbx_store import ECSBXStore

from config import Config

from warning_board import WarningBoard

def init_tasks(ecsbx_stores):
    for ecsbx_store in ecsbx_stores:
        ecsbx_store.mount()

def check_and_repair_archives(s, ecsbx_stores):
    s.enter(30 * 60, 1, check_and_repair_archives, argument=(s, ecsbx_stores))

    for ecsbx_store in ecsbx_stores:
        ecsbx_store.check_archives()
        ecsbx_store.repair_archives()

def check_ecsbx_stores_health(s, ecsbx_stores):
    s.enter(60, 1, check_ecsbx_stores_health, argument=(s, ecsbx_stores))

    for ecsbx_store in ecsbx_stores:
        ecsbx_store.health_check()

def check_cpu_health(s, cpu_monitor):
    s.enter(30, 1, check_cpu_health, argument=(s, cpu_monitor))

    cpu_monitor.health_check()

def display_warnings(s, warning_board):
    s.enter(60, 1, display_warnings, argument=(s, warning_board))

    warning_board.display()

def schedule_tasks(s, cpu_monitor, ecsbx_stores, warning_board):
    check_cpu_health(s, cpu_monitor)
    check_ecsbx_stores_health(s, ecsbx_stores)
    check_and_repair_archives(s, ecsbx_stores)
    display_warnings(s, warning_board)

def main():
    parser = argparse.ArgumentParser(prog=sys_info["acronym"])

    parser.add_argument("--config", metavar="CONFIG", default="daams.config", help="configuration file to use")
    parser.add_argument("--acronym", action="version", help="show acronym", version=sys_info["acronym"])
    parser.add_argument("--full-name", action="version", help="show full name", version=sys_info["full_name"])
    parser.add_argument("--version", action="version", help="show acrynym and version number", version=sys_info["acronym"] + " " + sys_info["daams_version"])
    parser.add_argument("--version-long", action="version", help="show full name and version number", version=sys_info["full_name"] + " " + sys_info["daams_version"])
    parser.add_argument("--check-only", action="store_true", help="complete all initial checks then exit")

    args = parser.parse_args()

    system_diagnostics.print_start_up_message()
    system_diagnostics.check_system_rights()
    system_diagnostics.check_dependencies()
    system_diagnostics.print_system_info()

    config = Config()

    config.load_file(args.config)

    warning_board = WarningBoard()

    cpu_monitor = CPUMonitor(config.cpu_health(), warning_board)

    cpu_monitor.self_check_hard_fail()

    ecsbx_stores = [ECSBXStore(x, config.disk_health(), warning_board) for x in config.ecsbx_stores()]

    for ecsbx_store in ecsbx_stores:
        ecsbx_store.self_check_hard_fail()

    if args.check_only:
        print("All initial checks completed")
        shutdown_normal()

    try:
        delay_before_sched_sec = config.delay_before_sched_sec()
        print_w_time("Waiting for", str(delay_before_sched_sec), "seconds before scheduling tasks")

        time.sleep(delay_before_sched_sec)

        print_w_time("Scheduling tasks")

        scheduler = sched.scheduler(time.time, time.sleep)

        init_tasks(ecsbx_stores)

        schedule_tasks(scheduler,
                       cpu_monitor,
                       ecsbx_stores,
                       warning_board)

        scheduler.run()
    except KeyboardInterrupt:
        print()
        for ecsbx_store in ecsbx_stores:
            ecsbx_store.unmount()
        shutdown_normal()
    except OSShutdownRequest:
        for ecsbx_store in ecsbx_stores:
            ecsbx_store.unmount()
        shutdown_error()

if __name__ == "__main__":
    main()
