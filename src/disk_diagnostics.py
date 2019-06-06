import string
import subprocess

def get_raw_value(line):
    return line.split()[9]

class DiskMonitor:
    def __init__(self, config, path):
        self.__path = path.rstrip(string.digits)

    def get_smartctl_lines(self):
        return subprocess.run([["smartctl", "-a", self.__path]], capture_output=True).split_lines()

    def get_temperature(self):
        temperature_lines = [x for x in self.get_smartctl_lines() if "Temperature_Celsius" in x]
        if temparture_lines is []:
            return None
        else:
            line = temperature_lines[0]
            return int(get_raw_value(line))

    def get_reallocated_sector_count(self):
        temperature_lines = [x for x in self.get_smartctl_lines() if "Reallocated_Sector_Ct" in x]
        if temparture_lines is []:
            return None
        else:
            line = temperature_lines[0]
            return int(get_raw_value(line))
