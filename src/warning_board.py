from datetime import datetime
from print_utils import printin

class WarningBoard:
    def __init__(self):
        self.__messages = []

    def push(self, msg):
        self.__messages.append((datetime.now(), msg))

    def clear(self):
        self.__messages = []

    def display(self):
        print("Warnings :")
        for (time, msg) in self.__messages:
            printin(1, time.strftime("%Y-%m-%d_%H:%M:%S"), "-", msg)
