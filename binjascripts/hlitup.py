# Axel '0vercl0k' Souchet - 12-May-2018
from binaryninja import *
import itertools

hl_color = enums.HighlightStandardColor.RedHighlightColor
printable_range = range(0x20, 0x7f)
normal_range = range(0, 0x100)
nb_partial_overwrite_bytes = 3

def hlitup(bv):
    base = 0x56555000
    # addresses = (0xf7fd8be0, 0xf7fd8000)
    addresses = (0x56555d29, )
    hled_functions = set()
    for address in addresses:
        log_info('Taking care of: %x(%x)' % (address, address - base))
        product = itertools.product(
            printable_range,
            repeat = nb_partial_overwrite_bytes
        )
        for bytes in product:
            # zero the lower n bytes
            address >>= len(bytes) * 8
            for bx in bytes:
                address = (address << 8) | bx  

            offset = address - base
            func = bv.get_function_at(offset)
            if func is None:
                func = bv.get_function_at(bv.get_previous_function_start_before(offset))

            if func is None:
                log_debug('Cannot find function for %x' % offset)
                continue

            instrs = filter(
                lambda ins: ins[1] == offset,
                func.instructions
            )
            
            if len(instrs) != 1:
                log_debug('Cannot find an instruction with this address %x' % offset)
                continue 
            
            _, instr_length = instrs[0]
            func.set_auto_instr_highlight(instr_length, hl_color)
            log_info('Highlighted %x' % offset)
            hled_functions.add(func)

    for func in hled_functions:
        print 'Highlighted function:', func.name

hlitup(bv)
