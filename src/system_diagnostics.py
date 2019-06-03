from print_utils import printin
import blkar

sys_info = {
    "version" : "0.1.0"
}

def check_dependencies():
    print("Checking system dependencies")
    try:
        sys_info["blkar_version"] = blkar.check_for_installation()
    except Exception as e:
        printin(1, e.args[0])
        exit(1)

def print_setup_info():
    print("System information reporting")
    printin(1, "D.A.A.M.S. version : " + sys_info["version"])
    printin(1, "blkar version : " + sys_info["blkar_version"])
