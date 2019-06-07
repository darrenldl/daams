from disk_controller import DiskController

class ECSBXStore(DiskController):
    def __init__(self, config):
        DiskController.__init__(config.partition())
