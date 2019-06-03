#!/usr/bin/env python3
import argparse
import threading
from datetime import datetime
import os
import random
import string
import sys
import time
import yaml

import blkar
import system_diagnostics
from system_diagnostics import sys_info

def main():
    parser = argparse.ArgumentParser(prog=sys_info["acronym"])

    parser.add_argument("--config", metavar="CONFIG", default=".daams.config", help="Configuration file to use")
    parser.add_argument("--version", action="version", version=sys_info["acronym"] + " " + sys_info["daams_version"])
    parser.add_argument("--version-long", action="version", version=sys_info["full_name"] + " " + sys_info["daams_version"])

    args = parser.parse_args()

    system_diagnostics.check_dependencies()

    system_diagnostics.print_setup_info()

if __name__ == "__main__":
    main()
