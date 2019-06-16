from datetime import datetime
from print_utils import eprint, eprintin

class WarningBoard:
    def __init__(self):
        self.__messages = []

    def push(self, msg, persist=True):
        self.__messages.append((datetime.now(), msg, persist))

    def clear(self):
        self.__messages = [(time, msg, persist) for (time, msg, persist) in self.__messages if persist]

    def display(self):
        if self.__messages == []:
            print("No warnings")
        else:
            print("Warnings :")
            for (time, msg, _) in self.__messages:
                printin(1, time.strftime("%Y-%m-%d_%H:%M:%S"), "-", msg)
            self.clear()
