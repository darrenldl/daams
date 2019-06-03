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

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", metavar="CONFIG", default=".daams.config", help="Configuration file to use")

    args = parser.parse_args()

    system_diagnostics.check_dependencies()

    system_diagnostics.print_setup_info()

if __name__ == "__main__":
    main()
