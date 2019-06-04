import yaml

from print_utils import printin, indent_str
from shutdown import shutdown

class Config:
    def __init__(self):
        self.config = None

    def load_file(self, file_path):
        print("Loading configuration file")
        try:
            with open(file_path) as f:
                self.config = yaml.safe_load(f.read())
        except IsADirectoryError:
            printin(1, "Configuration file " + '"' + file_path + '"' + " is a directory")
            shutdown()
        except FileNotFoundError:
            printin(1, "Configuration file " + '"' + file_path + '"' + " does not exist")
            shutdown()
        except yaml.YAMLError as e:
            printin(1, "Failed to parse configuration file " + '"' + file_path + '"')
            printin(1, "Error :")
            print(indent_str(2, str(e)))
            shutdown()

    def print_debug(self):
        print(self.config)
