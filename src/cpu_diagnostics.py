import subprocess
from system_diagnostics import shutdown_error
from print_utils import print_w_time, printin

class CPUMonitor:
    def get_temperature(self):
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as f:
                temp = int(f.read()) // 1000
                return temp
        except FileNotFoundError:
            return None

    def self_check_hard_fail(self):
        print("CPU monitor self check with hard fail")
        temp = self.get_temperature()
        if temp == None:
            printin(1, "Failed to get temperature")
            shutdown_error()
        else:
            printin(1, "Okay")
            printin(2, "Temperature :", temp)
