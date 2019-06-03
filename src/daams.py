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

def main():
    blkar.check_for_installation()
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", metavar="CONFIG", default=".daams.config", help="Configuration file to use")

    args = parser.parse_args()

if __name__ == "__main__":
    main()
