# Axel '0vercl0k' Souchet - 3-March-2018
import sys
import socket

host = ('192.168.1.41', 31337)

def recv_until(c, s):
    buff = ''
    while True:
        b = c.recv(1)
        buff += b
        if s in buff:
            return buff

    return None

def addn(c, r_n, n):
    recv_until(c, '8. Exit\n')
    c.send('0\n%d\n%d\n' % (r_n, n))

def readn(c, r_n):
    recv_until(c, '8. Exit\n')
    c.send('1\n%d\n' % r_n)
    recv_until(c, 'Result is ')
    res = c.recv(1024).splitlines()
    return int(res[0], 10)

def main():
    r_key = 18
    r_oracle = 0
    # first step is to find out how many 0's the key starts with,
    # to do so we ask for an encryption where the key is the pkey,
    # and we encrypt until we cannot and we count the number of
    # 'Continue Encryption?'. 32 - this number should give us the
    # number of 0s
    n_zeros = 32
    c = socket.create_connection(host)
    addn(c, r_oracle, 1337)
    recv_until(c, '8. Exit\n')
    c.send('6\n%d\n%d\n' % (r_oracle, r_key))
    recv_until(c, 'Continue Encryption? (y/n)\n')
    for _ in range(32):
        c.send('y\n')
        n_zeros -= 1
        if 'Continue Encryption? (y/n)' not in c.recv(1024):
            break

    if n_zeros > 0:
        print 'Found', n_zeros, '0s at the start of the key'
 
    leaked_key = [ 0 ] * n_zeros
    v_oracle = 3
    # now we can go ahead and leak the key bit by bit (each byte is a bit)
    for i in range(32 - n_zeros):
        which_bit = len(leaked_key) + 1
        bit_idx = which_bit - n_zeros
        c = socket.create_connection(host)
        addn(c, r_oracle, v_oracle)
        # private key encryption
        recv_until(c, '8. Exit\n')
        c.send('6\n%d\n%d\n' % (r_oracle, r_key))
        for _ in range(bit_idx):
            recv_until(c, 'Continue Encryption? (y/n)\n')
            c.send('y\n')

        if which_bit < 32:
            recv_until(c, 'Continue Encryption? (y/n)\n')
            c.send('n\n')

        magic_number = 1
        for b in leaked_key[n_zeros :]:
            magic_number &= 0xffffffff
            magic_number *= magic_number
            if b == 1:
                magic_number *= v_oracle

        magic_number *= magic_number
        magic_number &= 0xffffffff
        n = readn(c, r_oracle)
        bit = 0 if magic_number == n else 1
        leaked_key.append(bit)
        c.close()
        print 'Leaked key: %08x\r' % reduce(lambda x, y: (x * 2) + y, leaked_key),

main()
