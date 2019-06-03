from print_utils import printin
import blkar
import platform

sys_info = {
    "daams_version" : "0.1.0",
    "acronym" : "D.A.A.M.S.",
    "full_name" : "Data Archive Automatic Maintenance System"
}

def check_dependencies():
    print("Checking system dependencies")
    try:
        sys_info["blkar_version"] = blkar.check_for_installation()
    except Exception as e:
        printin(1, e.args[0])
        exit(1)
    printin(1, "Okay")

def print_setup_info():
    print("System information")
    printin(1, sys_info["acronym"] + " version : " + sys_info["daams_version"])
    printin(1, "OS name            : " + platform.system())
    printin(1, "OS release         : " + platform.release())
    printin(1, "Machine type       : " + platform.machine())
    printin(1, "Python version     : " + platform.python_version())
    printin(1, "blkar version      : " + sys_info["blkar_version"])
