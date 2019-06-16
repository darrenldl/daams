import sys
from datetime import datetime

indent_size = 4

def gen_padding(indent):
    return indent * indent_size * " "

def print_w_time(*args, **kwargs):
    time = datetime.now()
    print("{:<60} {}".format("".join(args), "[" + time.strftime("%Y-%m-%d %H:%M:%S")+ "]"), **kwargs)
    # print("[" + time.strftime("%Y-%m-%d_%H:%M:%S")+ "]", 2 * " ", *args, **kwargs)

def printin(indent, *args, **kwargs):
    print((indent * indent_size - 1) * " ", *args, **kwargs)

def indent_str(indent, msg):
    l = msg.split('\n')
    padding = gen_padding(indent)
    return padding + ("\n" + padding).join(l)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def eprintin(indent, *args, **kwargs):
    eprint((indent * indent_size - 1) * " ", *args, **kwargs)
