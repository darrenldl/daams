import subprocess
from system_diagnostics import shutdown_error, OSShutdownRequest
from print_utils import print_w_time, printin

class CPUMonitor:
    def __init__(self, config, warning_board):
        self.__warn_temperature = config.warn_temperature()
        self.__shutdown_temperature = config.shutdown_temperature()
        self.__warning_board = warning_board

    def get_temperature(self):
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as f:
                temp = int(f.read()) // 1000
                return temp
        except FileNotFoundError:
            return None

    def self_check_hard_fail(self):
        print_w_time("CPU monitor self check with hard fail")
        temp = self.get_temperature()
        if temp == None:
            printin(1, "Failed to get temperature")
            shutdown_error()
        else:
            printin(1, "Okay")
            printin(2, "Temperature :", temp)

    def health_check(self):
        print_w_time("CPU health check")
        temp = self.get_temperature()
        printin(1, "Temperature :", temp)
        if temp >= self.__shutdown_temperature:
            printin(2, "CPU temperature has reached shutdown threshold")
            printin(2, "Shutting down OS")
            raise(OSShutdownRequest)
        elif temp >= self.__warn_temperature:
            printin(2, "CPU temperature has reached warning threshold")
            printin(2, "One-off warning registered")
            self.__warning_board.push("CPU temperature at " + str(temp) + ", please check for ventilation status", persist=False)
