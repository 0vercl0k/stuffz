import sys

sys.path.append('../')
from goasm import *

def main(argc, argv):
    code  = '\n'.join([
        'call get_ip',

        'get_ip:',
        'pop eax',                    # edx = get_ip
        'lets_go:',
        'add eax, ((end_of_stub - lets_go) + 1)', # eax = address just after the stub

        'decrypt_loop:',
        'mov ebx, D [eax]',           # check if we found the end marker
        'cmp ebx, 0xB196A112',
        'je >end_of_stub',
        'xor B [eax], 0xF1',
        'inc eax',
        'jmp decrypt_loop',

        'end_of_stub:'
    ])

    raw_code = CodeBlock(code)
    c = CodeSection('.text')
    c.add(raw_code)

    e = Executable('decrypt_stub')
    e.add(c)
    e.generate()
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))