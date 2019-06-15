import os
import blkar
from print_utils import printin
from disk_controller import DiskController

class ECSBXStore(DiskController):
    def __init__(self, config):
        super().__init__(config.partition(), config.mount_dir(), config.smart_enabled())
        self.name = config.name()
        self.to_be_repaired = []

    def check(self):
        print("ECBSX store check intitiated, store : " + self.name)
        partial = []
        full_okay = []
        full_failed = []
        unrelated = []
        for d, _, files in os.walk(self.mount_dir):
            for f in files:
                full_path = os.path.join(d, f)
                if full_path.endswith(".ecsbx.part"):
                    printin(1, "Ignoring partial copy " + full_path)
                    partial.append(full_path)
                elif full_path.endswith(".ecsbx"):
                    printin(1, "Checking " + full_path)
                    res = blkar.check_file(full_path)
                    error = res["error"]
                    if error != None:
                        printin(2, error)
                        printin(2, "Ignoring file")
                        continue

                    repair=False

                    failed_block_count = res["stats"]["numberOfBlocksFailedCheck"]
                    if failed_block_count > 0:
                        printin(2, failed_block_count, "blocks failed check")
                        full_failed.append(full_path)
                        repair=True

                    if failed_block_count == 0:
                        printin(2, "No blocks failed check, initiating hash check")

                        res = blkar.check_file_hash_only(full_path)
                        error = res["error"]
                        if error == None:
                            if "recordedHash" in res["stats"]:
                                recorded_hash = res["stats"]["recordedHash"]
                                data_hash = res["stats"]["hashOfStoredData"]
                                if recorded_hash != data_hash:
                                    printin(3, "Hash check failed")
                                    repair=True
                            else:
                                printin(3, "No hash recorded")
                        else:
                            printin(3, error)
                            printin(3, "Ignoring file")

                    if repair:
                        full_failed.append(full_path)
                        printin(2, "Added to repair list")
                else:
                    printin(1, "Ignoring unrelated file " + full_path)
                    unrelated.append(full_path)
        self.to_be_repaired = full_failed.copy()

    def repair(self):
        for f in self.to_be_repaired:
            res = blkar.repair_file(f)
            print(res)
