import os
import blkar
from disk_controller import DiskController

class ECSBXStore(DiskController):
    def __init__(self, config):
        super().__init__(config.partition(), config.mount_dir())
        self.name = config.name()
        self.to_be_repaired = []

    def check(self):
        partial = []
        full_okay = []
        full_failed = []
        unrelated = []
        for d, _, files in os.walk(self.mount_dir):
            for f in files:
                full_path = os.path.join(d, f)
                if full_path.endswith(".ecsbx.part"):
                    print("Ignoring partial copy \"" + full_path + "\"")
                    partial.append(full_path)
                elif full_path.endswith(".ecsbx"):
                    print("Checking \"" + f + "\"")
                    res = blkar.check_file(full_path)
                    print(res)
                else:
                    print("Ignoring unrelated file \"" + full_path + "\"")
                    unrelated.append(full_path)
        self.to_be_repaired = full_failed.copy()

    def repair(self):
        for f in self.to_be_repaired:
            res = blkar.Repaier(f)
            print(res)
