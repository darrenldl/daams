#!/usr/bin/env python3
import argparse
import threading
from datetime import datetime
import os
import random
import string
import sys
import time

import blkar
import system_diagnostics
from system_diagnostics import sys_info, shutdown_normal
from cpu_diagnostics import CPUMonitor

from ecsbx_store import ECSBXStore

from config import Config

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

    cpu_monitor = CPUMonitor()

    cpu_monitor.self_check_hard_fail()

    ecsbx_stores = map(lambda x: ECSBXStore(x), config.ecsbx_stores())

    for ecsbx_store in ecsbx_stores:
        ecsbx_store.self_check_hard_fail()

    if args.check_only:
        print("All initial checks completed")
        shutdown_normal()

if __name__ == "__main__":
    main()
