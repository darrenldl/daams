from datetime import datetime
from print_utils import eprint, eprintin

class WarningBoard:
    def __init__(self):
        self.__messages = []

    def push(self, msg, persist=True):
        self.__messages.append((datetime.now(), msg, persist))

    def clear(self):
        self.__messages = filter(lambda (_, _, persist): persist, self.__messages)

    def display(self):
        eprint("Warnings :")
        for (time, msg) in self.__messages:
            eprintin(1, time.strftime("%Y-%m-%d_%H:%M:%S"), "-", msg)
