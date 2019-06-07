from disk_controller import DiskController

class ECSBXStore(DiskController):
    def __init__(self, path):
        DiskController.__init__(path)
