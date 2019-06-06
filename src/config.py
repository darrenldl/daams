import yaml
import os
import stat

from print_utils import printin, indent_str

from system_diagnostics import shutdown_error

accepted_root_keys = [
    "ecsbx_stores",
    "cpu_health",
    "disk_health",
    "delay_before_sched_sec",
]

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

            unrecognised_key = check_keys(cpu_health, ["warn_temperature", "shutdown_temperature"])
            if unrecognised_key != None:
                printin(2, "Unrecognised key", '"' + unrecognised_key + '"')
                shutdown_error()

            warn_temperature = cpu_health["warn_temperature"]
            if not isinstance(warn_temperature, int):
                raise Exception("warn_temperature should be an integer")
            if warn_temperature < 0:
                raise Exception("warn_temperature should be positive")
            shutdown_temperature = cpu_health["shutdown_temperature"]
            if not isinstance(shutdown_temperature, int):
                raise Exception("shutdown_temperature should be an integer")
            if shutdown_temperature < 0:
                raise Exception("shutdown_temperature should be greater than or equal to 0")
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

            unrecognised_key = check_keys(disk_health, ["warn_temperature", "shutdown_temperature"])
            if unrecognised_key != None:
                printin(2, "Unrecognised key", '"' + unrecognised_key + '"')
                shutdown_error()

            warn_temperature = disk_health["warn_temperature"]
            if not isinstance(warn_temperature, int):
                raise Exception("warn_temperature should be an integer")
            if warn_temperature < 0:
                raise Exception("warn_temperature should be positive")
            shutdown_temperature = disk_health["shutdown_temperature"]
            if not isinstance(shutdown_temperature, int):
                raise Exception("shutdown_temperature should be an integer")
            if shutdown_temperature < 0:
                raise Exception("shutdown_temperature should be greater than or equal to 0")
            printin(2, "Okay")
        else:
            printin(2, "Section not specified")
    except KeyError as e:
        printin(2, "Key", str(e), "misisng")
        shutdown_error()
    except Exception as e:
        printin(2, str(e))
        shutdown_error()

def check_delay_before_sched_sec(config):
    try:
        printin(1, "Checking delay_before_sched_sec")
        if "delay_before_sched_sec" in config:
            delay_before_sched_sec = config["delay_before_sched_sec"]
            if not isinstance(delay_before_sched_sec, int):
                raise Exception("delay_before_sched_sec should be an integer")
            if delay_before_sched_sec < 0:
                raise Exception("delay_before_sched_sec should be greater than or equal to 0")
            printin(2, "Okay")
        else:
            printin(2, "Value not specified")
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
        check_delay_before_sched_sec(config)
    except KeyError as e:
        printin(1, "Key", str(e), "misisng")
        shutdown_error()
    except Exception as e:
        printin(1, str(e))
        shutdown_error()

class ECSBXStoreConfig:
    def __init__(self, partition, mount_dir):
        self.__partition = partition
        self.__mount_dir = mount_dir
        self.__active = True

    def partition(self):
        return self.__partition

    def mount_dir(self):
        return self.__mount_dir

    def mark_inactive(self):
        self.__active = False

    def mark_active(self):
        self.__active = True

class CPUHealthConfig:
    def __init__(self, warn_temperature, shutdown_temperature):
        self.__warn_temperature = warn_temperature
        self.__shutdown_temperature = shutdown_temperature

    def warn_temperature(self):
        return self.__warn_temperature

    def shutdown_temperature(self):
        return self.__shutdown_temperature

class DiskHealthConfig:
    def __init__(self, warn_temperature, shutdown_temperature):
        self.__warn_temperature = warn_temperature
        self.__shutdown_temperature = shutdown_temperature

    def warn_temperature(self):
        return self.__warn_temperature

    def shutdown_temperature(self):
        return self.__shutdown_temperature

class Config:
    def __init__(self):
        self.__config = None
        self.__ecsbx_stores = []
        self.__cpu_health = None
        self.__disk_health = None
        self.__delay_before_sched_sec = None

    def load_file(self, file_path):
        print("Loading configuration file")
        try:
            with open(file_path) as f:
                config = yaml.safe_load(f.read())
                check_config(config)

                self.__config = config

                if "ecsbx_stores" in config:
                    self.__ecsbx_stores = map(lambda d: ECSBXStoreConfig(partition=d["partition"],
                                                                         mount_dir=d["mount_dir"]),
                                              config["ecsbx_stores"])

                if "cpu_health" in config:
                    cpu_health = config["cpu_health"]
                    self.__cpu_health = CPUHealthConfig(warn_temperature=cpu_health["warn_temperature"],
                                                        shutdown_temperature=cpu_health["shutdown_temperature"])

                if "disk_health" in config:
                    disk_health = config["disk_health"]
                    self.__disk_health = DiskHealthConfig(warn_temperature=disk_health["warn_temperature"],
                                                          shutdown_temperature=disk_health["shutdown_temperature"])

                if "delay_before_sched_sec" in config:
                    self.__delay_before_sched_sec = config["delay_before_sched_sec"]
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

    def ecsbx_stores(self):
        return self.__ecsbx_stores

    def cpu_health(self):
        return self.__cpu_health

    def disk_health(self):
        return self.__disk_health

    def delay_before_sched_sec(self):
        return self.__delay_before_sched_sec

    def print_debug(self):
        print(self.__config)
