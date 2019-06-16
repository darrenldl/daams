import string
import subprocess
from print_utils import print_w_time, printin
from system_diagnostics import shutdown_error
from pathlib import Path
import os

def get_raw_value(line):
    return line.split()[9]

class DiskController:
    def __init__(self, part, mount_dir, smart_enabled, warn_temperature, shutdown_temperature):
        self.part = part
        self.disk = part.rstrip(string.digits)
        self.mount_dir = mount_dir
        self.smart_enabled = smart_enabled
        self.warn_temperature = warn_temperature
        self.shutdown_temperature = shutdown_temperature

    def get_smartctl_lines(self):
        return subprocess.run(["smartctl", "-a", self.disk], capture_output=True).stdout.splitlines()

    def get_temperature(self):
        lines = [x for x in self.get_smartctl_lines() if b"Temperature_Celsius" in x]
        if lines == []:
            return None
        else:
            line = lines[0]
            return int(get_raw_value(line))

    def get_reallocated_sector_count(self):
        lines = [x for x in self.get_smartctl_lines() if b"Reallocated_Sector_Ct" in x]
        if lines == []:
            return None
        else:
            line = lines[0]
            return int(get_raw_value(line))

    def self_check_hard_fail(self):
        print_w_time("Disk controller self check with hard fail, disk :", self.disk)

        if self.smart_enabled:
            temp = self.get_temperature()
            reallocated_sector_count = self.get_reallocated_sector_count()

            if temp == None:
                printin(1, "Failed to get temperature")
                shutdown_error()
            elif reallocated_sector_count == None:
                printin(1, "Failed to get reallocated sector count")
                shutdown_error()
            else:
                printin(1, "Okay")
                printin(2, "Temperature :", temp)
                printin(2, "Reallocated sector count :", reallocated_sector_count)
        else:
            printin(1, "SMART monitoring not enabled, check skipped")

    def mount_output_lines(self):
        return subprocess.run(["mount"], capture_output=True).stdout.splitlines()

    def mount(self):
        print_w_time("Mounting partition", self.part, "to", self.mount_dir)
        lines = [x for x in self.mount_output_lines() if self.part in str(x)]
        if lines == []:
            completed = subprocess.run(["mount", self.part, self.mount_dir], capture_output=True)
            if completed.returncode == 0:
                printin(1, "Okay")
            else:
                printin(1, "Failed to mount")
        else:
            printin(1, "Skipped, disk already mounted")

    def unmount(self):
        print_w_time("Unmounting directory", self.mount_dir)
        lines = [x for x in self.mount_output_lines() if self.part in str(x)]
        if lines == []:
            printin(1, "Skipped, disk is not mounted")
        else:
            completed = subprocess.run(["umount", self.mount_dir], capture_output=True)
            if completed.returncode == 0:
                printin(1, "Okay")
            else:
                printin(1, "Failed to unmount")

    def check_if_accessible(self):
        try:
            Path(os.path.join(self.mount_dir, "daams.touch")).touch()
            return True
        except Exception:
            return False

    def health_check(self):
        print_w_time("Disk health check")
        if self.smart_enabled:
            temp = self.get_temperature()
            printin(1, "Temperature :", temp)
            if temp >= self.shutdown_temperature:
                printin(2, "Disk temperature has reached shutdown threshold")
                printin(2, "Shutting down OS")
                raise(OSShutdownRequest)
            elif temp >= self.warn_temperature:
                printin(2, "Disk temperature has reached warning threshold")
                printin(2, "One-off warning registered")
                self.__warning_board.push("Disk temperature at " + str(temp) + ", please check for ventilation status", persist=False)
        else:
            printin(1, "SMART monitoring not enabled, check skipped")
