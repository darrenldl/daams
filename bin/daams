#!/usr/bin/env python3
import argparse
import shutil
from packaging import version
import re
import subprocess
from subprocess import Popen, PIPE
import threading
import json
from datetime import datetime
import os
import random
import string
import sys
import time

blkar_config = {
    "sbx_version" : 19,
    "rs_data" : 10,
    "rs_parity" : 2,
    "burst" : 10,
    "min_ver" : version.parse("7.0.0"),
    "max_ver_exc" : version.parse("8.0.0")
}

def check_for_blkar_installation():
    if shutil.which("blkar") == None:
        print("blkar" + " not detected, please make sure you have installed blkar correctly")
        exit(1)

    ver_str = re.match("blkar (.*)\n", subprocess.check_output(["blkar", "--version"]).decode("utf-8")).group(1)
    ver = version.parse(ver_str)
    if ver < blkar_config["min_ver"] or ver >= blkar_config["max_ver_exc"]:
        print("Version " + ver_str + " not supported, version must be >=" + blkar_config["min_ver"] + " && < " + blkar_config["max_ver_exc"])
        exit(1)

class Blkar_checker:
    def __init__(self, file_path : str):
        self.proc = Popen(["blkar", "check",
                           "--hash",
                           "--json",
                           file_path],
                          stdin=PIPE,
                          stdout=PIPE)

    def close(self):
        return json.loads(self.proc.stdout.read())

def main():
    check_for_blkar_installation()
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", metavar="CONFIG", default=".daams.config", help="Configuration file to use")

    args = parser.parse_args()

if __name__ == "__main__":
    main()
