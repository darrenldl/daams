import string
import subprocess
from print_utils import printin
from system_diagnostics import shutdown_error

def get_raw_value(line):
    return line.split()[9]

class DiskController:
    def __init__(self, part, mount_dir):
        self.part = part
        self.disk = part.rstrip(string.digits)
        self.mount_dir = mount_dir

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
        print("Disk controller self check with hard fail, disk :", self.__disk)

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

    def mount_output_lines(self):
        return subprocess.run(["mount"], capture_output=True).stdout.splitlines()

    def mount(self):
        print("Mounting partition", self.part, "to", self.mount_dir)
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
        print("Unmounting directory", self.mount_dir)
        lines = [x for x in self.mount_output_lines() if self.part in str(x)]
        if lines == []:
            printin(1, "Skipped, disk is not mounted")
        else:
            completed = subprocess.run(["umount", self.mount_dir], capture_output=True)
            if completed.returncode == 0:
                printin(1, "Okay")
            else:
                printin(1, "Failed to unmount")
