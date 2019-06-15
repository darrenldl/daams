import shutil
import re
from packaging import version
import subprocess
from subprocess import Popen, PIPE
import json

blkar_config = {
    "sbx_version" : 19,
    "rs_data" : 10,
    "rs_parity" : 2,
    "burst" : 10,
    "min_ver" : version.parse("7.0.0"),
    "max_ver_exc" : version.parse("8.0.0")
}

def check_for_installation():
    if shutil.which("blkar") == None:
        raise Exception("blkar" + " not detected, please make sure you have installed blkar correctly")

    ver_str = re.match("blkar (.*)\n", subprocess.check_output(["blkar", "--version"]).decode("utf-8")).group(1)
    ver = version.parse(ver_str)
    if ver < blkar_config["min_ver"] or ver >= blkar_config["max_ver_exc"]:
        raise Exception("Version " + ver_str + " not supported, version must be >=" + blkar_config["min_ver"] + " && < " + blkar_config["max_ver_exc"])

    return ver_str

def check_file(path):
    completed = subprocess.run(["blkar", "check",
                                "--json",
                                path],
                               capture_output=True)

    return json.loads(completed.stdout)

def check_file_hash_only(path):
    completed = subprocess.run(["blkar", "check",
                                "--hash-only",
                                "--json",
                                path],
                               capture_output=True)

    return json.loads(completed.stdout)

def repair_file(path):
    completed = subprocess.run(["blkar", "repair",
                                "--json",
                                path],
                               capture_output=True)

    return json.loads(completed.stdout)
