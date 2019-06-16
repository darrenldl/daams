from print_utils import print_w_time, printin
import blkar
import platform
import os
import shutil

sys_info = {
    "daams_version" : "0.1.0",
    "acronym" : "D.A.A.M.S.",
    "full_name" : "Data Archive Automatic Maintenance Subsystem"
}

def print_start_up_message():
    print(sys_info["full_name"], "starting")

def check_system_rights():
    print_w_time("Checking system rights")
    if os.geteuid() != 0:
        printin(1, sys_info["acronym"], "requires root access")
        shutdown_error()
    printin(1, "Okay")

def check_dependencies():
    print_w_time("Checking system dependencies")
    try:
        sys_info["blkar_version"] = blkar.check_for_installation()
        if shutil.which("hddtemp") == None:
            raise Exception("hddtemp not detected")
    except Exception as e:
        printin(1, e.args[0])
        shutdown_error()
    printin(1, "Okay")

def print_system_info():
    print_w_time("System information")
    printin(1, sys_info["acronym"] + " version : " + sys_info["daams_version"])
    printin(1, "OS name            : " + platform.system())
    printin(1, "OS release         : " + platform.release())
    printin(1, "Machine type       : " + platform.machine())
    printin(1, "Python version     : " + platform.python_version())
    printin(1, "blkar version      : " + sys_info["blkar_version"])

def shutdown_error():
    print_w_time("Shutting down", sys_info["acronym"])
    exit(1)

def shutdown_normal():
    print_w_time("Shutting down", sys_info["acronym"])
    exit(0)
