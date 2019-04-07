# Axel '0vercl0k' Souchet - 9 September 2018
from elfesteem.minidump_init import Minidump
from unicorn import *
from unicorn.x86_const import *
import concurrent.futures
import progressbar
import functools

def set_msr(uc, msr, value):
    orax = uc.reg_read(UC_X86_REG_RAX)
    ordx = uc.reg_read(UC_X86_REG_RDX)
    orcx = uc.reg_read(UC_X86_REG_RCX)
    orip = uc.reg_read(UC_X86_REG_RIP)

    # x86: wrmsr
    buf = '\x0f\x30'
    uc.mem_map(0, 0x1000, UC_PROT_READ | UC_PROT_EXEC)
    uc.mem_write(0, buf)

    uc.reg_write(UC_X86_REG_RAX, value & 0xFFFFFFFF)
    uc.reg_write(UC_X86_REG_RDX, (value >> 32) & 0xFFFFFFFF)
    uc.reg_write(UC_X86_REG_RCX, msr & 0xFFFFFFFF)
    uc.emu_start(0, -1, count = 1)

    uc.reg_write(UC_X86_REG_RAX, orax)
    uc.reg_write(UC_X86_REG_RDX, ordx)
    uc.reg_write(UC_X86_REG_RCX, orcx)
    uc.reg_write(UC_X86_REG_RIP, orip)
    uc.mem_unmap(0, 0x1000)

def set_fs(uc, addr):
    FSMSR = 0xC0000100
    set_msr(uc, FSMSR, addr)

def restore_snapshot(uc, ctx, mem):
    # Restore registers
    uc.context_restore(ctx)
    for address, content in mem:
        uc.mem_write(address, content)

def emu_gadget(args):
    dmp_path, start, end = args
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    mdmp = Minidump(open(dmp_path, 'rb').read())
    mem = []
    for m in mdmp.memory.itervalues():
        perms = 0
        if 'WRITE' in m.pretty_protect:
            perms |= UC_PROT_WRITE
        if 'EXECUTE' in m.pretty_protect:
            perms |= UC_PROT_EXEC
        if 'READ' in m.pretty_protect:
            perms |= UC_PROT_READ

        if (perms & UC_PROT_WRITE) != 0:
            mem.append((m.address, m.content))

        uc.mem_map(m.address, len(m.content), perms)
        uc.mem_write(m.address, m.content)

    # teb
    set_fs(uc, 0x000003d98c4c000)

    t = mdmp.threads.Threads[0].ThreadContext
    gprs = {
        UC_X86_REG_RAX : t.Rax[0],
        UC_X86_REG_RBX : t.Rbx[0],
        UC_X86_REG_RCX : t.Rcx[0],
        UC_X86_REG_RDX : t.Rdx[0],
        UC_X86_REG_RSI : t.Rsi[0],
        UC_X86_REG_RDI : t.Rdi[0],
        UC_X86_REG_RBP : t.Rbp[0],
        UC_X86_REG_RSP : t.Rsp[0],
        UC_X86_REG_RIP : t.Rip[0],
        UC_X86_REG_R8 : t.R8[0],
        UC_X86_REG_R9 : t.R9[0],
        UC_X86_REG_R10 : t.R10[0],
        UC_X86_REG_R11 : t.R11[0],
        UC_X86_REG_R12 : t.R12[0],
        UC_X86_REG_R13 : t.R13[0],
        UC_X86_REG_R14 : t.R14[0],
        UC_X86_REG_R15 : t.R15[0],
        UC_X86_REG_EFLAGS : t.EFlags[0]
    }

    for name, val in gprs.iteritems():
        uc.reg_write(name, val)

    ctx = uc.context_save()
    wins = []
    for addr in range(start, end):
        if True:
            uc.reg_write(UC_X86_REG_RAX, addr)
            uc.reg_write(UC_X86_REG_R14, addr)
        try:
            uc.emu_start(addr, -1, count = 30)
        except UcError, e:
            # print str(e), e.errno
            pass

        rsp = uc.reg_read(UC_X86_REG_RSP)
        pc = uc.reg_read(UC_X86_REG_RIP)
        if 0xdeadbeefbaadc000 < rsp < 0xdeadbeefbaadc0ff:# or pc == 0xaaaaaaaaaaaaaaaa:
            wins.append(addr)

        # print '%016x' % rip, '\r',
        restore_snapshot(uc, ctx, mem)
    return wins

def dump_gprs(uc, title = 'GPRs'):
    print title.center(62, '=')
    rax = uc.reg_read(UC_X86_REG_RAX)
    rbx = uc.reg_read(UC_X86_REG_RBX)
    rcx = uc.reg_read(UC_X86_REG_RCX)
    print 'rax=%.16x rbx=%.16x rcx=%.16x' % (rax, rbx, rcx)
    rdx = uc.reg_read(UC_X86_REG_RDX)
    rsi = uc.reg_read(UC_X86_REG_RSI)
    rdi = uc.reg_read(UC_X86_REG_RDI)
    print 'rdx=%.16x rsi=%.16x rdi=%.16x' % (rdx, rsi, rdi)
    rip = uc.reg_read(UC_X86_REG_RIP)
    rsp = uc.reg_read(UC_X86_REG_RSP)
    rbp = uc.reg_read(UC_X86_REG_RBP)
    print 'rip=%.16x rsp=%.16x rbp=%.16x' % (rip, rsp, rbp)
    r8 = uc.reg_read(UC_X86_REG_R8)
    r9 = uc.reg_read(UC_X86_REG_R9)
    r10 = uc.reg_read(UC_X86_REG_R10)
    print ' r8=%.16x  r9=%.16x r10=%.16x' % (r8, r9, r10)
    r11 = uc.reg_read(UC_X86_REG_R11)
    r12 = uc.reg_read(UC_X86_REG_R12)
    r13 = uc.reg_read(UC_X86_REG_R13)
    print 'r11=%.16x r12=%.16x r13=%.16x' % (r11, r12, r13)
    r14 = uc.reg_read(UC_X86_REG_R14)
    r15 = uc.reg_read(UC_X86_REG_R15)
    print 'r14=%.16x r15=%.16x' % (r14, r15)
    print 'EOF'.center(62, '=')

def single_step(uc, address, x, y):
    # print address, x, y
    dump_gprs(uc, 'SINGLE STEP')

def emu_test(buf):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    uc.hook_add(UC_HOOK_CODE, single_step)

    teb = 0x000000b25a2c5000
    uc.mem_map(teb, 0x1000, UC_PROT_READ)
    uc.mem_write(teb, 'abcdefgh')
    set_fs(uc, teb)
    addr = 0x1000
    uc.mem_map(addr, 0x1000, UC_PROT_READ | UC_PROT_EXEC)
    uc.mem_write(addr, buf)
    try:
        uc.emu_start(addr, -1, count = 1)
    except UcError, e:
        print str(e), e.errno

def main():
    # mov rax, gs:[0x1000]
    emu_test("\x65\x48\x8b\x04\x25\x00\x10\x00\x00")
    # mov rax, fs:[0]
    emu_test("\x64\x48\x8b\x04\x25\x00\x00\x00\x00")
    # return

    dmp = r'C:\Users\over\Downloads\js_overwrite.dmp'
    mdmp = Minidump(open(dmp, 'rb').read())
    tasks = []
    for m in mdmp.memory.itervalues():
        if 'EXECUTE' not in m.pretty_protect:
            continue

        start = m.address
        end = start + len(m.content)
        #if start in [0x7ff6bdb41000, 0x7ffabab31000]:
        #    continue

        for i in range(start, end, 0x1000):
            t = (dmp, i, i + 0xfff)
            tasks.append(t)

    with concurrent.futures.ProcessPoolExecutor(max_workers = 2) as executor:
        n = 0
        with progressbar.ProgressBar(max_value = len(tasks)) as bar:
            bar.update(n)
            for wins in executor.map(emu_gadget, tasks):
                n += 1
                bar.update(n)
                for win in wins:
                    print hex(win)
                    raw_input('Continue?')

if __name__ == '__main__':
    main()

