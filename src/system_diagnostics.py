from print_utils import printin
import blkar
import platform
import os

sys_info = {
    "daams_version" : "0.1.0",
    "acronym" : "D.A.A.M.S.",
    "full_name" : "Data Archive Automatic Maintenance Subsystem"
}

def print_start_up_message():
    print(sys_info["full_name"], "starting")

def check_system_rights():
    print("Checking system rights")
    if os.geteuid() != 0:
        printin(1, sys_info["acronym"], "requires root access")
        shutdown_error()
    printin(1, "Okay")

def check_dependencies():
    print("Checking system dependencies")
    try:
        sys_info["blkar_version"] = blkar.check_for_installation()
    except Exception as e:
        printin(1, e.args[0])
        shutdown_error()
    printin(1, "Okay")

def print_system_info():
    print("System information")
    printin(1, sys_info["acronym"] + " version : " + sys_info["daams_version"])
    printin(1, "OS name            : " + platform.system())
    printin(1, "OS release         : " + platform.release())
    printin(1, "Machine type       : " + platform.machine())
    printin(1, "Python version     : " + platform.python_version())
    printin(1, "blkar version      : " + sys_info["blkar_version"])

def shutdown_error():
    print("Shutting down", sys_info["acronym"])
    exit(1)

def shutdown_normal():
    print("Shutting down", sys_info["acronym"])
    exit(0)
