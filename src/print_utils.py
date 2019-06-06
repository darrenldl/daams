import sys

indent_size = 4

def gen_padding(indent):
    return indent * indent_size * " "

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
