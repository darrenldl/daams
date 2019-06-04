import yaml
import os
import stat

from print_utils import printin, indent_str

from system_diagnostics import shutdown_error

accepted_root_keys = ["ecsbx_stores",
                      "cpu_health",
                      "disk_health"]

def check_keys(d, accepted):
    for k in d.keys():
        if k not in accepted:
            return k
    return None

def check_root_keys(config):
    printin(1, "Checking root level keys")
    unrecognised_key = check_keys(config, accepted_root_keys)
    if unrecognised_key != None:
        printin(2, "Unrecognised key", '"' + unrecognised_key + '"')
        shutdown_error()
    printin(2, "Okay")

def check_ecsbx_stores(config):
    try:
        printin(1, "Checking ECSBX stores section")
        if "ecsbx_stores" in config:
            ecsbx_stores = config["ecsbx_stores"]
            if not isinstance(ecsbx_stores, list):
                raise Exception("Value following key ecsbx_stores should be a list")
            for store in ecsbx_stores:
                if not isinstance(store, dict):
                    raise Exception("ECSBX store specification should be key value pairs")

                unrecognised_key = check_keys(store, ["partition", "mount_dir"])
                if unrecognised_key != None:
                    printin(2, "Unrecognised key", '"' + unrecognised_key + '"')
                    shutdown_error()

                partition = store["partition"]
                mount_dir = store["mount_dir"]

                try:
                    mode = os.stat(partition).st_mode
                    if not stat.S_ISBLK(mode):
                        raise Exception('"' + partition + '"' + " is not a block device")
                except FileNotFoundError:
                    raise Exception("Partition " + partition + " not found")

                if os.path.isfile(mount_dir):
                    raise Exception(mount_dir + " is not a directory")
                elif os.path.isdir(mount_dir):
                    pass
                else:
                    raise Exception(mount_dir + " does not exist")
            printin(2, "Okay")
        else:
            printin(2, "Section not specified")
    except KeyError as e:
        printin(2, "Key", str(e), "misisng")
        shutdown_error()
    except Exception as e:
        printin(2, str(e))
        shutdown_error()

def check_cpu_health(config):
    try:
        printin(1, "Checking CPU health section")
        if "cpu_health" in config:
            cpu_health = config["cpu_health"]
            if not isinstance(cpu_health, dict):
                raise Exception("Value following key cpu_health should be key value pairs")

            unrecognised_key = check_keys(cpu_health, ["warn_temp", "shutdown_temp"])
            if unrecognised_key != None:
                printin(2, "Unrecognised key", '"' + unrecognised_key + '"')
                shutdown_error()

            warn_temp = cpu_health["warn_temp"]
            if not isinstance(warn_temp, int):
                raise Exception("warn_temp should be an integer")
            if warn_temp < 0:
                raise Exception("warn_temp should be positive")
            shutdown_temp = cpu_health["shutdown_temp"]
            if not isinstance(shutdown_temp, int):
                raise Exception("shutdown_temp should be an integer")
            if shutdown_temp < 0:
                raise Exception("shutdown_temp should be greater than or equal to 0")
            printin(2, "Okay")
        else:
            printin(2, "Section not specified")
    except KeyError as e:
        printin(2, "Key", str(e), "misisng")
        shutdown_error()
    except Exception as e:
        printin(2, str(e))
        shutdown_error()

def check_disk_health(config):
    try:
        printin(1, "Checking disk health section")
        if "disk_health" in config:
            disk_health = config["disk_health"]
            if not isinstance(disk_health, dict):
                raise Exception("Value following key disk_health should be key value pairs")

            unrecognised_key = check_keys(disk_health, ["warn_temp", "shutdown_temp"])
            if unrecognised_key != None:
                printin(2, "Unrecognised key", '"' + unrecognised_key + '"')
                shutdown_error()

            warn_temp = disk_health["warn_temp"]
            if not isinstance(warn_temp, int):
                raise Exception("warn_temp should be an integer")
            if warn_temp < 0:
                raise Exception("warn_temp should be positive")
            shutdown_temp = disk_health["shutdown_temp"]
            if not isinstance(shutdown_temp, int):
                raise Exception("shutdown_temp should be an integer")
            if shutdown_temp < 0:
                raise Exception("shutdown_temp should be greater than or equal to 0")
            printin(2, "Okay")
        else:
            printin(2, "Section not specified")
    except KeyError as e:
        printin(2, "Key", str(e), "misisng")
        shutdown_error()
    except Exception as e:
        printin(2, str(e))
        shutdown_error()

def check_config(config):
    print("Checking configuration file")
    try:
        check_root_keys(config)
        check_ecsbx_stores(config)
        check_cpu_health(config)
        check_disk_health(config)
    except KeyError as e:
        printin(1, "Key", str(e), "misisng")
        shutdown_error()
    except Exception as e:
        printin(1, str(e))
        shutdown_error()

class Config:
    def __init__(self):
        self.config = None

    def load_file(self, file_path):
        print("Loading configuration file")
        try:
            with open(file_path) as f:
                config = yaml.safe_load(f.read())
                check_config(config)
                self.config = config
        except IsADirectoryError:
            printin(1, "Configuration file " + '"' + file_path + '"' + " is a directory")
            shutdown_error()
        except FileNotFoundError:
            printin(1, "Configuration file " + '"' + file_path + '"' + " does not exist")
            shutdown_error()
        except yaml.YAMLError as e:
            printin(1, "Failed to parse configuration file " + '"' + file_path + '"')
            printin(1, "Error :")
            print(indent_str(2, str(e)))
            shutdown_error()

    def print_debug(self):
        print(self.config)
