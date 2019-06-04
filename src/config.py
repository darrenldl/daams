import yaml
import os
import stat

from print_utils import printin, indent_str

from system_diagnostics import shutdown_error

def check_ecsbx_stores(config):
    try:
        printin(1, "Checking ECSBX stores")
        if "ecsbx_stores" in config:
            ecsbx_stores = config["ecsbx_stores"]
            if not isinstance(ecsbx_stores, list):
                raise Exception("Value following key ecsbx should be a list")
            for store in ecsbx_stores:
                if not isinstance(store, dict):
                    raise Exception("ECSBX store specification should be key value pairs")
                partition = store["partition"]
                mount_dir = store["mount_dir"]

                try:
                    mode = os.stat(partition).st_mode
                    if not stat.S_ISBLK(mode):
                        raise Exception('"' + partition + '"' + " is not a block device")
                except FileNotFoundError:
                    raise Exception("Partition " + partition + " not found")
            printin(2, "Okay")
        else:
            printin(2, "No ECSBX stores specified")
    except KeyError as e:
        printin(2, "Key", str(e), "misisng")
        shutdown_error()
    except Exception as e:
        printin(2, str(e))
        shutdown_error()

def check_config(config):
    print("Checking configuration file")
    try:
        check_ecsbx_stores(config)
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
