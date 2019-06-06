import os
import string
import subprocess

class Disk:
    def __init__(self, path):
        self.path = path.rstrip(string.digits)

    def get_temperature(self):
        output = subprocess.run(["hddtemp", "-n", self.path], capture_output=True)
        return int(output.stdout)

    def 
