import os
import blkar
from disk_controller import DiskController

class ECSBXStore(DiskController):
    def __init__(self, config):
        DiskController.__init__(self, config.partition(), config.mount_dir())
        self.__name = config.name()
        self.__to_be_repaired = []

    def check(self):
        partial = []
        full_okay = []
        full_failed = []
        unrelated = []
        for f in os.walk(self.mount_dir):
            if f.endswith(".ecsbx.part"):
                partial.append(f)
            elif f.endswith(".ecsbx"):
                res = blkar.Checker(f)
                print(res)
            else:
                unrelated.append(f)
        self.__to_be_repaired = full_failed.copy()

    def repair(self):

