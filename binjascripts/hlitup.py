# Axel '0vercl0k' Souchet - 12-May-2018
from binaryninja import *
import itertools

hl_color = enums.HighlightStandardColor.RedHighlightColor
printable_range = range(0x20, 0x7f)
normal_range = range(0, 0x100)
nb_partial_overwrite_bytes = 1

def hlitup(bv):
    # Those are the saved return address that I can overwrite,
    # and I want to visualize every point in the program I can reach
    # with a partial overwrite of those.
    base = 0x56555000
    addresses = (0x56555d29, )
    hled_functions = set()
    for address in addresses:
        log_info('Taking care of: %x(%x)' % (address, address - base))
        # Generate all the combination for a partial overwrite of X bytes.
        # You can also apply restrictions such as if you can only overwrite
        # with printable bytes (which was my case), etc.
        product = itertools.product(
            printable_range,
            repeat = nb_partial_overwrite_bytes
        )

        # Go through every combination and highlight the reachable pieces of code.
        for bytes in product:
            # Right shift the address and incorporate byte by byte the combination.
            address >>= len(bytes) * 8
            for bx in bytes:
                address = (address << 8) | bx

            offset = address - base
            funcs = bv.get_functions_containing(offset)
            if funcs is None:
                log_debug('Cannot find function for %x' % offset)
                continue

            # Highlight the match.
            funcs[0].set_auto_instr_highlight(offset, hl_color)
            log_info('Highlighted %x' % offset)
            # Accumulate the function this match is in.
            hled_functions.add(funcs[0])

    for func in hled_functions:
        print 'Highlighted function:', func.name

hlitup(bv)
