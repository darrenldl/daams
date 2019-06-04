indent_size = 4

def gen_padding(indent):
    return indent * indent_size * " "

def printin(indent, *msgs):
    print((indent * indent_size - 1) * " ", *msgs)

def indent_str(indent, msg):
    l = msg.split('\n')
    padding = gen_padding(indent)
    return padding + ("\n" + padding).join(l)
