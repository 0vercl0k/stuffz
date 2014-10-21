#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    code.py - The interesting bits of codes I needed to break the NoSuchCon2014
#    MIPS crackme.
#    Copyright (C) 2014 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

block_generate_magic_from_pc_son = '''.text:00400B8C                 lw      $v0, 0x318+pc_son($fp)  # Load Word
.text:00400B90                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400B94                 la      $v0, loc_400A78  # Load Address
.text:00400B9C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400BA0                 subu    $v0, $v1, $v0    # (regs.pc_father - 400A78)
.text:00400BA4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400BA8                 lw      $v0, 0x318+var_300($fp)  # Load Word
.text:00400BAC                 li      $v1, 0x446F8657  # Load Immediate
.text:00400BB4                 multu   $v0, $v1         # Multiply Unsigned
.text:00400BB8                 mfhi    $v1              # Move From HI
.text:00400BBC                 subu    $v0, $v1         # Subtract Unsigned
.text:00400BC0                 srl     $v0, 1           # Shift Right Logical
.text:00400BC4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400BC8                 srl     $v0, 6           # Shift Right Logical
.text:00400BCC                 sw      $v0, 0x318+var_2F0($fp)  # Store Word
.text:00400BD0                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400BD4                 sll     $v1, $v0, 17     # Shift Left Logical
.text:00400BD8                 srl     $v0, 15          # Shift Right Logical
.text:00400BDC                 or      $v0, $v1, $v0    # OR
.text:00400BE0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400BE4                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400BE8                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00400BEC                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400BF0                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00400BF4                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400BF8                 nor     $v0, $zero, $v0  # NOR
.text:00400BFC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00400C00                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00400C04                 sllv    $v0, $a0, $v0    # Shift Left Logical Variable
.text:00400C08                 or      $v0, $v1, $v0    # OR
.text:00400C0C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400C10                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400C14                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400C18                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:00400C1C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400C20                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400C24                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400C28                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00400C2C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400C30                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400C34                 li      $v0, 0x7FB21515  # Load Immediate
.text:00400C3C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400C40                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400C44                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400C48                 sll     $v1, $v0, 31     # Shift Left Logical
.text:00400C4C                 srl     $v0, 1           # Shift Right Logical
.text:00400C50                 or      $v0, $v1, $v0    # OR
.text:00400C54                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400C58                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400C5C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400C60                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400C64                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400C68                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400C6C                 sll     $v1, $v0, 1      # Shift Left Logical
.text:00400C70                 srl     $v0, 31          # Shift Right Logical
.text:00400C74                 or      $v0, $v1, $v0    # OR
.text:00400C78                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400C7C                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400C80                 sll     $v1, $v0, 22     # Shift Left Logical
.text:00400C84                 srl     $v0, 10          # Shift Right Logical
.text:00400C88                 or      $v0, $v1, $v0    # OR
.text:00400C8C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400C90                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400C94                 nor     $v0, $zero, $v0  # NOR
.text:00400C98                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400C9C                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400CA0                 nor     $v0, $zero, $v0  # NOR
.text:00400CA4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400CA8                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400CAC                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00400CB0                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400CB4                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00400CB8                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400CBC                 nor     $v0, $zero, $v0  # NOR
.text:00400CC0                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00400CC4                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00400CC8                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:00400CCC                 or      $v0, $v1, $v0    # OR
.text:00400CD0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400CD4                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400CD8                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400CDC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400CE0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400CE4                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400CE8                 li      $v0, 0xEAED4623  # Load Immediate
.text:00400CF0                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00400CF4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400CF8                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400CFC                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400D00                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400D04                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400D08                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400D0C                 li      $v0, 0x247DF646  # Load Immediate
.text:00400D14                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400D18                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400D1C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400D20                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400D24                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:00400D28                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400D2C                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400D30                 sll     $v1, $v0, 1      # Shift Left Logical
.text:00400D34                 srl     $v0, 31          # Shift Right Logical
.text:00400D38                 or      $v0, $v1, $v0    # OR
.text:00400D3C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400D40                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400D44                 nor     $v0, $zero, $v0  # NOR
.text:00400D48                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400D4C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400D50                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400D54                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:00400D58                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400D5C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400D60                 li      $v0, 0x66887BA9  # Load Immediate
.text:00400D68                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400D6C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400D70                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400D74                 sll     $v1, $v0, 14     # Shift Left Logical
.text:00400D78                 srl     $v0, 18          # Shift Right Logical
.text:00400D7C                 or      $v0, $v1, $v0    # OR
.text:00400D80                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400D84                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400D88                 li      $v0, 0xA6E6310C  # Load Immediate
.text:00400D90                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400D94                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400D98                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400D9C                 li      $v0, 0x46D63ECE  # Load Immediate
.text:00400DA4                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00400DA8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400DAC                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400DB0                 sll     $v1, $v0, 31     # Shift Left Logical
.text:00400DB4                 srl     $v0, 1           # Shift Right Logical
.text:00400DB8                 or      $v0, $v1, $v0    # OR
.text:00400DBC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400DC0                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400DC4                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400DC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400DCC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400DD0                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400DD4                 nor     $v0, $zero, $v0  # NOR
.text:00400DD8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400DDC                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400DE0                 sll     $v1, $v0, 28     # Shift Left Logical
.text:00400DE4                 srl     $v0, 4           # Shift Right Logical
.text:00400DE8                 or      $v0, $v1, $v0    # OR
.text:00400DEC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400DF0                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400DF4                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400DF8                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:00400DFC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400E00                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400E04                 sll     $v1, $v0, 22     # Shift Left Logical
.text:00400E08                 srl     $v0, 10          # Shift Right Logical
.text:00400E0C                 or      $v0, $v1, $v0    # OR
.text:00400E10                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400E14                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400E18                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400E1C                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:00400E20                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400E24                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400E28                 sll     $v1, $v0, 18     # Shift Left Logical
.text:00400E2C                 srl     $v0, 14          # Shift Right Logical
.text:00400E30                 or      $v0, $v1, $v0    # OR
.text:00400E34                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400E38                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400E3C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400E40                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400E44                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400E48                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400E4C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400E50                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00400E54                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400E58                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400E5C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400E60                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:00400E64                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400E68                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400E6C                 sll     $v1, $v0, 6      # Shift Left Logical
.text:00400E70                 srl     $v0, 26          # Shift Right Logical
.text:00400E74                 or      $v0, $v1, $v0    # OR
.text:00400E78                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400E7C                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400E80                 nor     $v0, $zero, $v0  # NOR
.text:00400E84                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400E88                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400E8C                 li      $v0, 0xB98DDDD6  # Load Immediate
.text:00400E94                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400E98                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400E9C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400EA0                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400EA4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400EA8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400EAC                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400EB0                 nor     $v0, $zero, $v0  # NOR
.text:00400EB4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400EB8                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400EBC                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400EC0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400EC4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400EC8                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400ECC                 sll     $v1, $v0, 14     # Shift Left Logical
.text:00400ED0                 srl     $v0, 18          # Shift Right Logical
.text:00400ED4                 or      $v0, $v1, $v0    # OR
.text:00400ED8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400EDC                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400EE0                 sll     $v1, $v0, 14     # Shift Left Logical
.text:00400EE4                 srl     $v0, 18          # Shift Right Logical
.text:00400EE8                 or      $v0, $v1, $v0    # OR
.text:00400EEC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400EF0                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400EF4                 li      $v0, 0xBED8172B  # Load Immediate
.text:00400EFC                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00400F00                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400F04                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400F08                 sll     $v1, $v0, 11     # Shift Left Logical
.text:00400F0C                 srl     $v0, 21          # Shift Right Logical
.text:00400F10                 or      $v0, $v1, $v0    # OR
.text:00400F14                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400F18                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400F1C                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00400F20                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400F24                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00400F28                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400F2C                 nor     $v0, $zero, $v0  # NOR
.text:00400F30                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00400F34                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00400F38                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:00400F3C                 or      $v0, $v1, $v0    # OR
.text:00400F40                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400F44                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400F48                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400F4C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400F50                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400F54                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400F58                 li      $v0, 0x663D9062  # Load Immediate
.text:00400F60                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00400F64                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400F68                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400F6C                 li      $v0, 0x57B3DFB2  # Load Immediate
.text:00400F74                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400F78                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400F7C                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400F80                 sll     $v1, $v0, 20     # Shift Left Logical
.text:00400F84                 srl     $v0, 12          # Shift Right Logical
.text:00400F88                 or      $v0, $v1, $v0    # OR
.text:00400F8C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400F90                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400F94                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400F98                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400F9C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400FA0                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400FA4                 li      $v0, 0x5345B7B3  # Load Immediate
.text:00400FAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400FB0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400FB4                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00400FB8                 nor     $v0, $zero, $v0  # NOR
.text:00400FBC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400FC0                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400FC4                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400FC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00400FCC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400FD0                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400FD4                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00400FD8                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00400FDC                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00400FE0                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00400FE4                 nor     $v0, $zero, $v0  # NOR
.text:00400FE8                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00400FEC                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00400FF0                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:00400FF4                 or      $v0, $v1, $v0    # OR
.text:00400FF8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00400FFC                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401000                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401004                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:00401008                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040100C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401010                 li      $v0, 0x828E9E5E  # Load Immediate
.text:00401018                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040101C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401020                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401024                 li      $v0, 0x56E376DD  # Load Immediate
.text:0040102C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401030                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401034                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401038                 li      $v0, 0x6407F0AD  # Load Immediate
.text:00401040                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401044                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401048                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:0040104C                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401050                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401054                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00401058                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:0040105C                 nor     $v0, $zero, $v0  # NOR
.text:00401060                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401064                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401068                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:0040106C                 or      $v0, $v1, $v0    # OR
.text:00401070                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401074                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401078                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040107C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401080                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00401084                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401088                 nor     $v0, $zero, $v0  # NOR
.text:0040108C                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401090                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401094                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:00401098                 or      $v0, $v1, $v0    # OR
.text:0040109C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004010A0                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:004010A4                 sll     $v1, $v0, 15     # Shift Left Logical
.text:004010A8                 srl     $v0, 17          # Shift Right Logical
.text:004010AC                 or      $v0, $v1, $v0    # OR
.text:004010B0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004010B4                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004010B8                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004010BC                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004010C0                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:004010C4                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004010C8                 nor     $v0, $zero, $v0  # NOR
.text:004010CC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004010D0                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:004010D4                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:004010D8                 or      $v0, $v1, $v0    # OR
.text:004010DC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004010E0                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004010E4                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004010E8                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004010EC                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:004010F0                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004010F4                 nor     $v0, $zero, $v0  # NOR
.text:004010F8                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004010FC                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401100                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:00401104                 or      $v0, $v1, $v0    # OR
.text:00401108                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040110C                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401110                 nor     $v0, $zero, $v0  # NOR
.text:00401114                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401118                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:0040111C                 li      $v0, 0xFA6407EB  # Load Immediate
.text:00401124                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401128                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040112C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401130                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401134                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401138                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:0040113C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401140                 nor     $v0, $zero, $v0  # NOR
.text:00401144                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401148                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:0040114C                 sllv    $v0, $a0, $v0    # Shift Left Logical Variable
.text:00401150                 or      $v0, $v1, $v0    # OR
.text:00401154                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401158                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:0040115C                 sll     $v1, $v0, 24     # Shift Left Logical
.text:00401160                 srl     $v0, 8           # Shift Right Logical
.text:00401164                 or      $v0, $v1, $v0    # OR
.text:00401168                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040116C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401170                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401174                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401178                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040117C                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401180                 nor     $v0, $zero, $v0  # NOR
.text:00401184                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401188                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:0040118C                 li      $v0, 0xF217F7C2  # Load Immediate
.text:00401194                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401198                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040119C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004011A0                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004011A4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004011A8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004011AC                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004011B0                 li      $v0, 0x3AC80432  # Load Immediate
.text:004011B8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004011BC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004011C0                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004011C4                 li      $v0, 0x155A85B7  # Load Immediate
.text:004011CC                 xor     $v0, $v1, $v0    # Exclusive OR
.text:004011D0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004011D4                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004011D8                 li      $v0, 0xCA0FDC0E  # Load Immediate
.text:004011E0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004011E4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004011E8                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004011EC                 li      $v0, 0x499EA031  # Load Immediate
.text:004011F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004011F8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004011FC                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401200                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401204                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401208                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:0040120C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401210                 nor     $v0, $zero, $v0  # NOR
.text:00401214                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401218                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:0040121C                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:00401220                 or      $v0, $v1, $v0    # OR
.text:00401224                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401228                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:0040122C                 li      $v0, 0x26DB7F0C  # Load Immediate
.text:00401234                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401238                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040123C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401240                 li      $v0, 0xB0E1A02B  # Load Immediate
.text:00401248                 xor     $v0, $v1, $v0    # Exclusive OR
.text:0040124C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401250                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401254                 li      $v0, 0x55DBCB6   # Load Immediate
.text:0040125C                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401260                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401264                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401268                 sll     $v1, $v0, 5      # Shift Left Logical
.text:0040126C                 srl     $v0, 27          # Shift Right Logical
.text:00401270                 or      $v0, $v1, $v0    # OR
.text:00401274                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401278                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:0040127C                 li      $v0, 0x9AA481CD  # Load Immediate
.text:00401284                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401288                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040128C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401290                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401294                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401298                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040129C                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:004012A0                 nor     $v0, $zero, $v0  # NOR
.text:004012A4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004012A8                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004012AC                 li      $v0, 0xF87093BD  # Load Immediate
.text:004012B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004012B8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004012BC                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:004012C0                 sll     $v1, $v0, 4      # Shift Left Logical
.text:004012C4                 srl     $v0, 28          # Shift Right Logical
.text:004012C8                 or      $v0, $v1, $v0    # OR
.text:004012CC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004012D0                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004012D4                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004012D8                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004012DC                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:004012E0                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004012E4                 nor     $v0, $zero, $v0  # NOR
.text:004012E8                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004012EC                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:004012F0                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:004012F4                 or      $v0, $v1, $v0    # OR
.text:004012F8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004012FC                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401300                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401304                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401308                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040130C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401310                 li      $v0, 0x53EC47BB  # Load Immediate
.text:00401318                 xor     $v0, $v1, $v0    # Exclusive OR
.text:0040131C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401320                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401324                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401328                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:0040132C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401330                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401334                 li      $v0, 0x76E63F9C  # Load Immediate
.text:0040133C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401340                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401344                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401348                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040134C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401350                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00401354                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401358                 nor     $v0, $zero, $v0  # NOR
.text:0040135C                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401360                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401364                 sllv    $v0, $a0, $v0    # Shift Left Logical Variable
.text:00401368                 or      $v0, $v1, $v0    # OR
.text:0040136C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401370                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401374                 sll     $v1, $v0, 18     # Shift Left Logical
.text:00401378                 srl     $v0, 14          # Shift Right Logical
.text:0040137C                 or      $v0, $v1, $v0    # OR
.text:00401380                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401384                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401388                 nor     $v0, $zero, $v0  # NOR
.text:0040138C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401390                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401394                 nor     $v0, $zero, $v0  # NOR
.text:00401398                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040139C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004013A0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004013A4                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004013A8                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:004013AC                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004013B0                 nor     $v0, $zero, $v0  # NOR
.text:004013B4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004013B8                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:004013BC                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:004013C0                 or      $v0, $v1, $v0    # OR
.text:004013C4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004013C8                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004013CC                 li      $v0, 0x4660B302  # Load Immediate
.text:004013D4                 xor     $v0, $v1, $v0    # Exclusive OR
.text:004013D8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004013DC                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:004013E0                 nor     $v0, $zero, $v0  # NOR
.text:004013E4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004013E8                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004013EC                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004013F0                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004013F4                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004013F8                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004013FC                 nor     $v0, $zero, $v0  # NOR
.text:00401400                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401404                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401408                 sllv    $v0, $a0, $v0    # Shift Left Logical Variable
.text:0040140C                 or      $v0, $v1, $v0    # OR
.text:00401410                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401414                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401418                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040141C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401420                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00401424                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401428                 nor     $v0, $zero, $v0  # NOR
.text:0040142C                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401430                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401434                 sllv    $v0, $a0, $v0    # Shift Left Logical Variable
.text:00401438                 or      $v0, $v1, $v0    # OR
.text:0040143C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word'''.split('\n')

block_find_magic_in_pcs = '''.text:00401448                 lw      $v0, 0x318+i($fp)  # Load Word
.text:0040144C                 sll     $v1, $v0, 1      # Shift Left Logical
.text:00401450                 lui     $v0, 0x41        # Load Upper Immediate
.text:00401454                 sll     $v1, 2           # Shift Left Logical
.text:00401458                 la      $v0, 0x0414130    # Load Address pcs
.text:0040145C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401460                 lw      $v1, 0($v0)      # Load Word
.text:00401464                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word

.text:00401470                 lw      $v0, 0x318+i($fp)  # Load Word
.text:00401474                 sll     $v0, 1           # Shift Left Logical
.text:00401478                 addiu   $v1, $v0, 1      # Add Immediate Unsigned
.text:0040147C                 lui     $v0, 0x41        # Load Upper Immediate
.text:00401480                 sll     $v1, 2           # Shift Left Logical
.text:00401484                 la      $v0, 0x00414130         # Load Address
.text:00401488                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040148C                 lw      $v0, 0($v0)      # Load Word
'''.split('\n')

block_compute_new_pc_from_magic_high = '''.text:004014F0                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004014F4                 li      $v0, 0xA6F8EB93  # Load Immediate
.text:004014FC                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401500                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401504                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401508                 sll     $v1, $v0, 23     # Shift Left Logical
.text:0040150C                 srl     $v0, 9           # Shift Right Logical
.text:00401510                 or      $v0, $v1, $v0    # OR
.text:00401514                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401518                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:0040151C                 li      $v0, 0x4BEAB6D7  # Load Immediate
.text:00401524                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401528                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040152C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401530                 li      $v0, 0x6FC06733  # Load Immediate
.text:00401538                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040153C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401540                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401544                 li      $v0, 0xB2FC8CCD  # Load Immediate
.text:0040154C                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401550                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401554                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401558                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:0040155C                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401560                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401564                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401568                 li      $v0, 0xF39ADEA8  # Load Immediate
.text:00401570                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401574                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401578                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:0040157C                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401580                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401584                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00401588                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:0040158C                 nor     $v0, $zero, $v0  # NOR
.text:00401590                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401594                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401598                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:0040159C                 or      $v0, $v1, $v0    # OR
.text:004015A0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004015A4                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:004015A8                 nor     $v0, $zero, $v0  # NOR
.text:004015AC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004015B0                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:004015B4                 sll     $v1, $v0, 2      # Shift Left Logical
.text:004015B8                 srl     $v0, 30          # Shift Right Logical
.text:004015BC                 or      $v0, $v1, $v0    # OR
.text:004015C0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004015C4                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004015C8                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004015CC                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:004015D0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004015D4                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004015D8                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004015DC                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:004015E0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004015E4                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:004015E8                 sll     $v1, $v0, 27     # Shift Left Logical
.text:004015EC                 srl     $v0, 5           # Shift Right Logical
.text:004015F0                 or      $v0, $v1, $v0    # OR
.text:004015F4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004015F8                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004015FC                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401600                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401604                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401608                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:0040160C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401610                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:00401614                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401618                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:0040161C                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401620                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401624                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00401628                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:0040162C                 nor     $v0, $zero, $v0  # NOR
.text:00401630                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401634                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401638                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:0040163C                 or      $v0, $v1, $v0    # OR
.text:00401640                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401644                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401648                 sll     $v1, $v0, 19     # Shift Left Logical
.text:0040164C                 srl     $v0, 13          # Shift Right Logical
.text:00401650                 or      $v0, $v1, $v0    # OR
.text:00401654                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401658                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:0040165C                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401660                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401664                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00401668                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:0040166C                 nor     $v0, $zero, $v0  # NOR
.text:00401670                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401674                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401678                 sllv    $v0, $a0, $v0    # Shift Left Logical Variable
.text:0040167C                 or      $v0, $v1, $v0    # OR
.text:00401680                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401684                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401688                 sll     $v1, $v0, 12     # Shift Left Logical
.text:0040168C                 srl     $v0, 20          # Shift Right Logical
.text:00401690                 or      $v0, $v1, $v0    # OR
.text:00401694                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401698                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:0040169C                 li      $v0, 0xDB3B6BCB  # Load Immediate
.text:004016A4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004016A8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004016AC                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004016B0                 li      $v0, 0x21BFC94A  # Load Immediate
.text:004016B8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004016BC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004016C0                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004016C4                 li      $v0, 0x46219385  # Load Immediate
.text:004016CC                 xor     $v0, $v1, $v0    # Exclusive OR
.text:004016D0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004016D4                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004016D8                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004016DC                 xor     $v0, $v1, $v0    # Exclusive OR
.text:004016E0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004016E4                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:004016E8                 sll     $v1, $v0, 18     # Shift Left Logical
.text:004016EC                 srl     $v0, 14          # Shift Right Logical
.text:004016F0                 or      $v0, $v1, $v0    # OR
.text:004016F4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004016F8                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004016FC                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401700                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401704                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00401708                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:0040170C                 nor     $v0, $zero, $v0  # NOR
.text:00401710                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401714                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401718                 sllv    $v0, $a0, $v0    # Shift Left Logical Variable
.text:0040171C                 or      $v0, $v1, $v0    # OR
.text:00401720                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401724                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401728                 sll     $v1, $v0, 29     # Shift Left Logical
.text:0040172C                 srl     $v0, 3           # Shift Right Logical
.text:00401730                 or      $v0, $v1, $v0    # OR
.text:00401734                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401738                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:0040173C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401740                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:00401744                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401748                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:0040174C                 li      $v0, 0xE9D9F9AB  # Load Immediate
.text:00401754                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401758                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040175C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401760                 li      $v0, 0x43D5488F  # Load Immediate
.text:00401768                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040176C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401770                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401774                 li      $v0, 0x193403FA  # Load Immediate
.text:0040177C                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401780                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401784                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401788                 sll     $v1, $v0, 24     # Shift Left Logical
.text:0040178C                 srl     $v0, 8           # Shift Right Logical
.text:00401790                 or      $v0, $v1, $v0    # OR
.text:00401794                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401798                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:0040179C                 sll     $v1, $v0, 18     # Shift Left Logical
.text:004017A0                 srl     $v0, 14          # Shift Right Logical
.text:004017A4                 or      $v0, $v1, $v0    # OR
.text:004017A8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004017AC                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004017B0                 li      $v0, 0x63C954E3  # Load Immediate
.text:004017B8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004017BC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004017C0                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:004017C4                 sll     $v1, $v0, 4      # Shift Left Logical
.text:004017C8                 srl     $v0, 28          # Shift Right Logical
.text:004017CC                 or      $v0, $v1, $v0    # OR
.text:004017D0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004017D4                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:004017D8                 sll     $v1, $v0, 3      # Shift Left Logical
.text:004017DC                 srl     $v0, 29          # Shift Right Logical
.text:004017E0                 or      $v0, $v1, $v0    # OR
.text:004017E4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004017E8                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:004017EC                 sll     $v1, $v0, 6      # Shift Left Logical
.text:004017F0                 srl     $v0, 26          # Shift Right Logical
.text:004017F4                 or      $v0, $v1, $v0    # OR
.text:004017F8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004017FC                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401800                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401804                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401808                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040180C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401810                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401814                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:00401818                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040181C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401820                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401824                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:00401828                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040182C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401830                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401834                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:00401838                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040183C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401840                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401844                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401848                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040184C                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401850                 sll     $v1, $v0, 29     # Shift Left Logical
.text:00401854                 srl     $v0, 3           # Shift Right Logical
.text:00401858                 or      $v0, $v1, $v0    # OR
.text:0040185C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401860                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401864                 li      $v0, 0xED1AFD50  # Load Immediate
.text:0040186C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401870                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401874                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401878                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:0040187C                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:00401880                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401884                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401888                 li      $v0, 0xBE7FD9D7  # Load Immediate
.text:00401890                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401894                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401898                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:0040189C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004018A0                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:004018A4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004018A8                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004018AC                 li      $v0, 0xCEE1CD73  # Load Immediate
.text:004018B4                 xor     $v0, $v1, $v0    # Exclusive OR
.text:004018B8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004018BC                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004018C0                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004018C4                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:004018C8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004018CC                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:004018D0                 sll     $v1, $v0, 11     # Shift Left Logical
.text:004018D4                 srl     $v0, 21          # Shift Right Logical
.text:004018D8                 or      $v0, $v1, $v0    # OR
.text:004018DC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004018E0                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004018E4                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004018E8                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004018EC                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:004018F0                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004018F4                 nor     $v0, $zero, $v0  # NOR
.text:004018F8                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004018FC                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401900                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:00401904                 or      $v0, $v1, $v0    # OR
.text:00401908                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040190C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401910                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401914                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:00401918                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:0040191C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401920                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401924                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401928                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:0040192C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401930                 nor     $v0, $zero, $v0  # NOR
.text:00401934                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401938                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:0040193C                 sllv    $v0, $a0, $v0    # Shift Left Logical Variable
.text:00401940                 or      $v0, $v1, $v0    # OR
.text:00401944                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401948                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:0040194C                 nor     $v0, $zero, $v0  # NOR
.text:00401950                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401954                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401958                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040195C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401960                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00401964                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401968                 nor     $v0, $zero, $v0  # NOR
.text:0040196C                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401970                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401974                 sllv    $v0, $a0, $v0    # Shift Left Logical Variable
.text:00401978                 or      $v0, $v1, $v0    # OR
.text:0040197C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401980                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401984                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401988                 subu    $v0, $v1, $v0    # Subtract Unsigned
.text:0040198C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401990                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401994                 sll     $v1, $v0, 22     # Shift Left Logical
.text:00401998                 srl     $v0, 10          # Shift Right Logical
.text:0040199C                 or      $v0, $v1, $v0    # OR
.text:004019A0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004019A4                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004019A8                 li      $v0, 0xFF135B81  # Load Immediate
.text:004019B0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004019B4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004019B8                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004019BC                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004019C0                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004019C4                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:004019C8                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:004019CC                 nor     $v0, $zero, $v0  # NOR
.text:004019D0                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004019D4                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:004019D8                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:004019DC                 or      $v0, $v1, $v0    # OR
.text:004019E0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004019E4                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:004019E8                 sll     $v1, $v0, 19     # Shift Left Logical
.text:004019EC                 srl     $v0, 13          # Shift Right Logical
.text:004019F0                 or      $v0, $v1, $v0    # OR
.text:004019F4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:004019F8                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:004019FC                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401A00                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401A04                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401A08                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401A0C                 nor     $v0, $zero, $v0  # NOR
.text:00401A10                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401A14                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401A18                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401A1C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401A20                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00401A24                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401A28                 nor     $v0, $zero, $v0  # NOR
.text:00401A2C                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401A30                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401A34                 sllv    $v0, $a0, $v0    # Shift Left Logical Variable
.text:00401A38                 or      $v0, $v1, $v0    # OR
.text:00401A3C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401A40                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401A44                 nor     $v0, $zero, $v0  # NOR
.text:00401A48                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401A4C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401A50                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401A54                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401A58                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00401A5C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401A60                 nor     $v0, $zero, $v0  # NOR
.text:00401A64                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401A68                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401A6C                 sllv    $v0, $a0, $v0    # Shift Left Logical Variable
.text:00401A70                 or      $v0, $v1, $v0    # OR
.text:00401A74                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401A78                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401A7C                 nor     $v0, $zero, $v0  # NOR
.text:00401A80                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401A84                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401A88                 nor     $v0, $zero, $v0  # NOR
.text:00401A8C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401A90                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401A94                 nor     $v0, $zero, $v0  # NOR
.text:00401A98                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401A9C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401AA0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401AA4                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401AA8                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00401AAC                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401AB0                 nor     $v0, $zero, $v0  # NOR
.text:00401AB4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401AB8                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401ABC                 sllv    $v0, $a0, $v0    # Shift Left Logical Variable
.text:00401AC0                 or      $v0, $v1, $v0    # OR
.text:00401AC4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401AC8                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401ACC                 nor     $v0, $zero, $v0  # NOR
.text:00401AD0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401AD4                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401AD8                 li      $v0, 0xD7C43CAF  # Load Immediate
.text:00401AE0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401AE4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401AE8                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401AEC                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401AF0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401AF4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401AF8                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401AFC                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401B00                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401B04                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00401B08                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401B0C                 nor     $v0, $zero, $v0  # NOR
.text:00401B10                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401B14                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401B18                 sllv    $v0, $a0, $v0    # Shift Left Logical Variable
.text:00401B1C                 or      $v0, $v1, $v0    # OR
.text:00401B20                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401B24                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401B28                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401B2C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401B30                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401B34                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401B38                 nor     $v0, $zero, $v0  # NOR
.text:00401B3C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401B40                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401B44                 nor     $v0, $zero, $v0  # NOR
.text:00401B48                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401B4C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401B50                 li      $v0, 0xDEC8E49E  # Load Immediate
.text:00401B58                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401B5C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401B60                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401B64                 li      $v0, 0x759BCDE7  # Load Immediate
.text:00401B6C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401B70                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401B74                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401B78                 sll     $v1, $v0, 6      # Shift Left Logical
.text:00401B7C                 srl     $v0, 26          # Shift Right Logical
.text:00401B80                 or      $v0, $v1, $v0    # OR
.text:00401B84                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401B88                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401B8C                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401B90                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401B94                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401B98                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401B9C                 sll     $v1, $v0, 18     # Shift Left Logical
.text:00401BA0                 srl     $v0, 14          # Shift Right Logical
.text:00401BA4                 or      $v0, $v1, $v0    # OR
.text:00401BA8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401BAC                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401BB0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401BB4                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401BB8                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00401BBC                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401BC0                 nor     $v0, $zero, $v0  # NOR
.text:00401BC4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401BC8                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401BCC                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:00401BD0                 or      $v0, $v1, $v0    # OR
.text:00401BD4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401BD8                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401BDC                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401BE0                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401BE4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401BE8                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401BEC                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401BF0                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401BF4                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00401BF8                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401BFC                 nor     $v0, $zero, $v0  # NOR
.text:00401C00                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401C04                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401C08                 sllv    $v0, $a0, $v0    # Shift Left Logical Variable
.text:00401C0C                 or      $v0, $v1, $v0    # OR
.text:00401C10                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401C14                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401C18                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401C1C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401C20                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401C24                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401C28                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401C2C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401C30                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00401C34                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401C38                 nor     $v0, $zero, $v0  # NOR
.text:00401C3C                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401C40                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401C44                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:00401C48                 or      $v0, $v1, $v0    # OR
.text:00401C4C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401C50                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401C54                 sll     $v1, $v0, 5      # Shift Left Logical
.text:00401C58                 srl     $v0, 27          # Shift Right Logical
.text:00401C5C                 or      $v0, $v1, $v0    # OR
.text:00401C60                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401C64                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401C68                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401C6C                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401C70                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401C74                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401C78                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00401C7C                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401C80                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00401C84                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401C88                 nor     $v0, $zero, $v0  # NOR
.text:00401C8C                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00401C90                 lw      $a0, 0x318+tmp_pc($fp)  # Load Word
.text:00401C94                 srlv    $v0, $a0, $v0    # Shift Right Logical Variable
.text:00401C98                 or      $v0, $v1, $v0    # OR
.text:00401C9C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401CA0                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401CA4                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401CA8                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401CAC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401CB0                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401CB4                 sll     $v1, $v0, 13     # Shift Left Logical
.text:00401CB8                 srl     $v0, 19          # Shift Right Logical
.text:00401CBC                 or      $v0, $v1, $v0    # OR
.text:00401CC0                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401CC4                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401CC8                 li      $v0, 0x1B210CEC  # Load Immediate
.text:00401CD0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401CD4                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401CD8                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401CDC                 sll     $v1, $v0, 23     # Shift Left Logical
.text:00401CE0                 srl     $v0, 9           # Shift Right Logical
.text:00401CE4                 or      $v0, $v1, $v0    # OR
.text:00401CE8                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401CEC                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401CF0                 sll     $v1, $v0, 4      # Shift Left Logical
.text:00401CF4                 srl     $v0, 28          # Shift Right Logical
.text:00401CF8                 or      $v0, $v1, $v0    # OR
.text:00401CFC                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401D00                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401D04                 sll     $v1, $v0, 1      # Shift Left Logical
.text:00401D08                 srl     $v0, 31          # Shift Right Logical
.text:00401D0C                 or      $v0, $v1, $v0    # OR
.text:00401D10                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401D14                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401D18                 nor     $v0, $zero, $v0  # NOR
.text:00401D1C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401D20                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401D24                 lw      $v0, 0x318+var_2F0($fp)  # Load Word
.text:00401D28                 xor     $v0, $v1, $v0    # Exclusive OR
.text:00401D2C                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401D30                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401D34                 li      $v0, 0x438E51AE  # Load Immediate
.text:00401D3C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401D40                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401D44                 lw      $v1, 0x318+tmp_pc($fp)  # Load Word
.text:00401D48                 li      $v0, 0xCF970C79  # Load Immediate
.text:00401D50                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00401D54                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401D58                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401D5C                 sll     $v1, $v0, 4      # Shift Left Logical
.text:00401D60                 srl     $v0, 28          # Shift Right Logical
.text:00401D64                 or      $v0, $v1, $v0    # OR
.text:00401D68                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401D6C                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401D70                 nor     $v0, $zero, $v0  # NOR
.text:00401D74                 sw      $v0, 0x318+tmp_pc($fp)  # Store Word
.text:00401D78                 lui     $v0, 0x40        # Load Upper Immediate
.text:00401D7C                 addiu   $v1, $v0, 0xa78  # Add Immediate Unsigned
.text:00401D80                 lw      $v0, 0x318+tmp_pc($fp)  # Load Word
.text:00401D84                 addu    $v0, $v1, $v0    # Add Unsigned'''.split('\n')

block_code_of_son = '''text:0040228C                 break   0                # Break
.text:00402290                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402294                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402298                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040229C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004022A0                 lw      $a0, 8($v0)      # Load Word
.text:004022A4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022A8                 subu    $a0, $v0         # Subtract Unsigned
.text:004022AC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004022B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004022B8                 sw      $a0, 8($v0)      # Store Word
.text:004022BC                 break   0                # Break
.text:004022C0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004022C4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022C8                 sll     $v0, 2           # Shift Left Logical
.text:004022CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004022D4                 lw      $v0, 8($v0)      # Load Word
.text:004022D8                 srl     $v1, $v0, 1      # Shift Right Logical
.text:004022DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022E0                 sll     $v0, 2           # Shift Left Logical
.text:004022E4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022E8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004022EC                 lw      $v0, 8($v0)      # Load Word
.text:004022F0                 sll     $v0, 31          # Shift Left Logical
.text:004022F4                 or      $v1, $v0         # OR
.text:004022F8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004022FC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402300                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402304                 sw      $v1, 8($v0)      # Store Word
.text:00402308                 break   0                # Break
.text:0040230C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402310                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402314                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402318                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040231C                 lw      $a0, 8($v0)      # Load Word
.text:00402320                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402324                 subu    $a0, $v0         # Subtract Unsigned
.text:00402328                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040232C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402330                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402334                 sw      $a0, 8($v0)      # Store Word
.text:00402338                 break   0                # Break
.text:0040233C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402340                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402344                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402348                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040234C                 lw      $a0, 8($v0)      # Load Word
.text:00402350                 li      $v0, 0x7B4DE789  # Load Immediate
.text:00402358                 xor     $a0, $v0         # Exclusive OR
.text:0040235C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402360                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402364                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402368                 sw      $a0, 8($v0)      # Store Word
.text:0040236C                 break   0                # Break
.text:00402370                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402374                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402378                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040237C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402380                 lw      $a0, 8($v0)      # Load Word
.text:00402384                 li      $v0, 0x87DD2BC5  # Load Immediate
.text:0040238C                 addu    $a0, $v0         # Add Unsigned
.text:00402390                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402394                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402398                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040239C                 sw      $a0, 8($v0)      # Store Word
.text:004023A0                 break   0                # Break
.text:004023A4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004023A8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004023AC                 sll     $v0, 2           # Shift Left Logical
.text:004023B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004023B8                 lw      $v0, 8($v0)      # Load Word
.text:004023BC                 srl     $v1, $v0, 12     # Shift Right Logical
.text:004023C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004023C4                 sll     $v0, 2           # Shift Left Logical
.text:004023C8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023CC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004023D0                 lw      $v0, 8($v0)      # Load Word
.text:004023D4                 sll     $v0, 20          # Shift Left Logical
.text:004023D8                 or      $v1, $v0         # OR
.text:004023DC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004023E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004023E8                 sw      $v1, 8($v0)      # Store Word
.text:004023EC                 break   0                # Break
.text:004023F0                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004023F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004023F8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023FC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402400                 lw      $a0, 8($v0)      # Load Word
.text:00402404                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402408                 addu    $a0, $v0         # Add Unsigned
.text:0040240C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402410                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402414                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402418                 sw      $a0, 8($v0)      # Store Word
.text:0040241C                 break   0                # Break
.text:00402420                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402424                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402428                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040242C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402430                 lw      $a0, 8($v0)      # Load Word
.text:00402434                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402438                 xor     $a0, $v0         # Exclusive OR
.text:0040243C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402440                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402444                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402448                 sw      $a0, 8($v0)      # Store Word
.text:0040244C                 break   0                # Break
.text:00402450                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402454                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402458                 sll     $v0, 2           # Shift Left Logical
.text:0040245C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402460                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402464                 lw      $v0, 8($v0)      # Load Word
.text:00402468                 sll     $v1, $v0, 13     # Shift Left Logical
.text:0040246C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402470                 sll     $v0, 2           # Shift Left Logical
.text:00402474                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402478                 addu    $v0, $a1, $v0    # Add Unsigned
.text:0040247C                 lw      $v0, 8($v0)      # Load Word
.text:00402480                 srl     $v0, 19          # Shift Right Logical
.text:00402484                 or      $v1, $v0         # OR
.text:00402488                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040248C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402490                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402494                 sw      $v1, 8($v0)      # Store Word
.text:00402498                 break   0                # Break
.text:0040249C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004024A0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024A4                 sll     $v0, 2           # Shift Left Logical
.text:004024A8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024AC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004024B0                 lw      $v0, 8($v0)      # Load Word
.text:004024B4                 nor     $v1, $zero, $v0  # NOR
.text:004024B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004024BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004024C4                 sw      $v1, 8($v0)      # Store Word
.text:004024C8                 break   0                # Break
.text:004024CC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004024D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024D4                 sll     $v0, 2           # Shift Left Logical
.text:004024D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004024E0                 lw      $v0, 8($v0)      # Load Word
.text:004024E4                 sll     $v1, $v0, 30     # Shift Left Logical
.text:004024E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024EC                 sll     $v0, 2           # Shift Left Logical
.text:004024F0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024F4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004024F8                 lw      $v0, 8($v0)      # Load Word
.text:004024FC                 srl     $v0, 2           # Shift Right Logical
.text:00402500                 or      $v1, $v0         # OR
.text:00402504                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402508                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040250C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402510                 sw      $v1, 8($v0)      # Store Word
.text:00402514                 break   0                # Break
.text:00402518                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040251C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402520                 sll     $v0, 2           # Shift Left Logical
.text:00402524                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402528                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040252C                 lw      $v0, 8($v0)      # Load Word
.text:00402530                 nor     $v1, $zero, $v0  # NOR
.text:00402534                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402538                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040253C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402540                 sw      $v1, 8($v0)      # Store Word
.text:00402544                 break   0                # Break
.text:00402548                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040254C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402550                 sll     $v0, 2           # Shift Left Logical
.text:00402554                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402558                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040255C                 lw      $v0, 8($v0)      # Load Word
.text:00402560                 nor     $v1, $zero, $v0  # NOR
.text:00402564                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402568                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040256C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402570                 sw      $v1, 8($v0)      # Store Word
.text:00402574                 break   0                # Break
.text:00402578                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040257C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402580                 sll     $v0, 2           # Shift Left Logical
.text:00402584                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402588                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040258C                 lw      $v0, 8($v0)      # Load Word
.text:00402590                 nor     $v1, $zero, $v0  # NOR
.text:00402594                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402598                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040259C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025A0                 sw      $v1, 8($v0)      # Store Word
.text:004025A4                 break   0                # Break
.text:004025A8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004025AC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025B0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025B4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025B8                 lw      $a0, 8($v0)      # Load Word
.text:004025BC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004025C0                 addu    $a0, $v0         # Add Unsigned
.text:004025C4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025C8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025CC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004025D0                 sw      $a0, 8($v0)      # Store Word
.text:004025D4                 break   0                # Break
.text:004025D8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004025DC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025E8                 lw      $a0, 8($v0)      # Load Word
.text:004025EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004025F0                 addu    $a0, $v0         # Add Unsigned
.text:004025F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025F8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025FC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402600                 sw      $a0, 8($v0)      # Store Word
.text:00402604                 break   0                # Break
.text:00402608                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040260C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402610                 sll     $v0, 2           # Shift Left Logical
.text:00402614                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402618                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040261C                 lw      $v0, 8($v0)      # Load Word
.text:00402620                 srl     $v1, $v0, 23     # Shift Right Logical
.text:00402624                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402628                 sll     $v0, 2           # Shift Left Logical
.text:0040262C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402630                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402634                 lw      $v0, 8($v0)      # Load Word
.text:00402638                 sll     $v0, 9           # Shift Left Logical
.text:0040263C                 or      $v1, $v0         # OR
.text:00402640                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402644                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402648                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040264C                 sw      $v1, 8($v0)      # Store Word
.text:00402650                 break   0                # Break
.text:00402654                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402658                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040265C                 sll     $v0, 2           # Shift Left Logical
.text:00402660                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402664                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402668                 lw      $v1, 8($v0)      # Load Word
.text:0040266C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402670                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00402674                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00402678                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040267C                 sll     $v0, 2           # Shift Left Logical
.text:00402680                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402684                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402688                 lw      $a1, 8($v0)      # Load Word
.text:0040268C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402690                 nor     $v0, $zero, $v0  # NOR
.text:00402694                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00402698                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040269C                 or      $v1, $v0         # OR
.text:004026A0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004026A4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026A8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004026AC                 sw      $v1, 8($v0)      # Store Word
.text:004026B0                 break   0                # Break
.text:004026B4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004026B8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026BC                 sll     $v0, 2           # Shift Left Logical
.text:004026C0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026C4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004026C8                 lw      $v1, 8($v0)      # Load Word
.text:004026CC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026D0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004026D4                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004026D8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026DC                 sll     $v0, 2           # Shift Left Logical
.text:004026E0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026E4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004026E8                 lw      $a1, 8($v0)      # Load Word
.text:004026EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026F0                 nor     $v0, $zero, $v0  # NOR
.text:004026F4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004026F8                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004026FC                 or      $v1, $v0         # OR
.text:00402700                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402704                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402708                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040270C                 sw      $v1, 8($v0)      # Store Word
.text:00402710                 break   0                # Break
.text:00402714                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402718                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040271C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402720                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402724                 lw      $a0, 8($v0)      # Load Word
.text:00402728                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040272C                 addu    $a0, $v0         # Add Unsigned
.text:00402730                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402734                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402738                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040273C                 sw      $a0, 8($v0)      # Store Word
.text:00402740                 break   0                # Break
.text:00402744                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402748                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040274C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402750                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402754                 lw      $a0, 8($v0)      # Load Word
.text:00402758                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040275C                 subu    $a0, $v0         # Subtract Unsigned
.text:00402760                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402764                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402768                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040276C                 sw      $a0, 8($v0)      # Store Word
.text:00402770                 break   0                # Break
.text:00402774                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402778                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040277C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402780                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402784                 lw      $a0, 8($v0)      # Load Word
.text:00402788                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040278C                 xor     $a0, $v0         # Exclusive OR
.text:00402790                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402794                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402798                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040279C                 sw      $a0, 8($v0)      # Store Word
.text:004027A0                 break   0                # Break
.text:004027A4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004027A8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027AC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027B0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004027B4                 lw      $a0, 8($v0)      # Load Word
.text:004027B8                 li      $v0, 0xD0970C74  # Load Immediate
.text:004027C0                 addu    $a0, $v0         # Add Unsigned
.text:004027C4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027C8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027CC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004027D0                 sw      $a0, 8($v0)      # Store Word
.text:004027D4                 break   0                # Break
.text:004027D8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004027DC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004027E8                 lw      $a0, 8($v0)      # Load Word
.text:004027EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004027F0                 subu    $a0, $v0         # Subtract Unsigned
.text:004027F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027F8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027FC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402800                 sw      $a0, 8($v0)      # Store Word
.text:00402804                 break   0                # Break
.text:00402808                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040280C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402810                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402814                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402818                 lw      $a0, 8($v0)      # Load Word
.text:0040281C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402820                 subu    $a0, $v0         # Subtract Unsigned
.text:00402824                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402828                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040282C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402830                 sw      $a0, 8($v0)      # Store Word
.text:00402834                 break   0                # Break
.text:00402838                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040283C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402840                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402844                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402848                 lw      $a0, 8($v0)      # Load Word
.text:0040284C                 li      $v0, 0xB65E867F  # Load Immediate
.text:00402854                 addu    $a0, $v0         # Add Unsigned
.text:00402858                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040285C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402860                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402864                 sw      $a0, 8($v0)      # Store Word
.text:00402868                 break   0                # Break
.text:0040286C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402870                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402874                 sll     $v0, 2           # Shift Left Logical
.text:00402878                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040287C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402880                 lw      $v1, 8($v0)      # Load Word
.text:00402884                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402888                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040288C                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00402890                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402894                 sll     $v0, 2           # Shift Left Logical
.text:00402898                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040289C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004028A0                 lw      $a1, 8($v0)      # Load Word
.text:004028A4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004028A8                 nor     $v0, $zero, $v0  # NOR
.text:004028AC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004028B0                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004028B4                 or      $v1, $v0         # OR
.text:004028B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004028BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004028C4                 sw      $v1, 8($v0)      # Store Word
.text:004028C8                 break   0                # Break
.text:004028CC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004028D0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004028D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004028DC                 lw      $a0, 8($v0)      # Load Word
.text:004028E0                 li      $v0, 0x3A2EE307  # Load Immediate
.text:004028E8                 addu    $a0, $v0         # Add Unsigned
.text:004028EC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004028F0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004028F8                 sw      $a0, 8($v0)      # Store Word
.text:004028FC                 break   0                # Break
.text:00402900                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402904                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402908                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040290C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402910                 lw      $a0, 8($v0)      # Load Word
.text:00402914                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402918                 xor     $a0, $v0         # Exclusive OR
.text:0040291C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402920                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402924                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402928                 sw      $a0, 8($v0)      # Store Word
.text:0040292C                 break   0                # Break
.text:00402930                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402934                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402938                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040293C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402940                 lw      $a0, 8($v0)      # Load Word
.text:00402944                 li      $v0, 0x4CC0DC26  # Load Immediate
.text:0040294C                 xor     $a0, $v0         # Exclusive OR
.text:00402950                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402954                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402958                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040295C                 sw      $a0, 8($v0)      # Store Word
.text:00402960                 break   0                # Break
.text:00402964                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402968                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040296C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402970                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402974                 lw      $a0, 8($v0)      # Load Word
.text:00402978                 li      $v0, 0x737F298   # Load Immediate
.text:00402980                 addu    $a0, $v0         # Add Unsigned
.text:00402984                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402988                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040298C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402990                 sw      $a0, 8($v0)      # Store Word
.text:00402994                 break   0                # Break
.text:00402998                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040299C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029A0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029A4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004029A8                 lw      $a0, 8($v0)      # Load Word
.text:004029AC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004029B0                 subu    $a0, $v0         # Subtract Unsigned
.text:004029B4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029B8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029BC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004029C0                 sw      $a0, 8($v0)      # Store Word
.text:004029C4                 break   0                # Break
.text:004029C8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004029CC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029D0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029D4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004029D8                 lw      $a0, 8($v0)      # Load Word
.text:004029DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004029E0                 xor     $a0, $v0         # Exclusive OR
.text:004029E4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029E8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029EC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004029F0                 sw      $a0, 8($v0)      # Store Word
.text:004029F4                 break   0                # Break
.text:004029F8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004029FC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A00                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A04                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402A08                 lw      $a0, 8($v0)      # Load Word
.text:00402A0C                 li      $v0, 0x81674F2B  # Load Immediate
.text:00402A14                 addu    $a0, $v0         # Add Unsigned
.text:00402A18                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A1C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A20                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A24                 sw      $a0, 8($v0)      # Store Word
.text:00402A28                 break   0                # Break
.text:00402A2C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402A30                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A34                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A38                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402A3C                 lw      $a0, 8($v0)      # Load Word
.text:00402A40                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A44                 subu    $a0, $v0         # Subtract Unsigned
.text:00402A48                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A4C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A50                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A54                 sw      $a0, 8($v0)      # Store Word
.text:00402A58                 break   0                # Break
.text:00402A5C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402A60                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A64                 sll     $v0, 2           # Shift Left Logical
.text:00402A68                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A6C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A70                 lw      $v0, 8($v0)      # Load Word
.text:00402A74                 srl     $v1, $v0, 13     # Shift Right Logical
.text:00402A78                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A7C                 sll     $v0, 2           # Shift Left Logical
.text:00402A80                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A84                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402A88                 lw      $v0, 8($v0)      # Load Word
.text:00402A8C                 sll     $v0, 19          # Shift Left Logical
.text:00402A90                 or      $v1, $v0         # OR
.text:00402A94                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402A98                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A9C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402AA0                 sw      $v1, 8($v0)      # Store Word
.text:00402AA4                 break   0                # Break
.text:00402AA8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402AAC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402AB0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AB4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402AB8                 lw      $a0, 8($v0)      # Load Word
.text:00402ABC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402AC0                 xor     $a0, $v0         # Exclusive OR
.text:00402AC4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402AC8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402ACC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402AD0                 sw      $a0, 8($v0)      # Store Word
.text:00402AD4                 break   0                # Break
.text:00402AD8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402ADC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402AE0                 sll     $v0, 2           # Shift Left Logical
.text:00402AE4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AE8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402AEC                 lw      $v0, 8($v0)      # Load Word
.text:00402AF0                 nor     $v1, $zero, $v0  # NOR
.text:00402AF4                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402AF8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AFC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B00                 sw      $v1, 8($v0)      # Store Word
.text:00402B04                 break   0                # Break
.text:00402B08                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402B0C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402B10                 sll     $v0, 2           # Shift Left Logical
.text:00402B14                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B18                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402B1C                 lw      $v0, 8($v0)      # Load Word
.text:00402B20                 srl     $v1, $v0, 26     # Shift Right Logical
.text:00402B24                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402B28                 sll     $v0, 2           # Shift Left Logical
.text:00402B2C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B30                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402B34                 lw      $v0, 8($v0)      # Load Word
.text:00402B38                 sll     $v0, 6           # Shift Left Logical
.text:00402B3C                 or      $v1, $v0         # OR
.text:00402B40                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402B44                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B48                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B4C                 sw      $v1, 8($v0)      # Store Word
.text:00402B50                 break   0                # Break
.text:00402B54                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402B58                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B5C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B60                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B64                 lw      $a0, 8($v0)      # Load Word
.text:00402B68                 li      $v0, 0x79662B5D  # Load Immediate
.text:00402B70                 addu    $a0, $v0         # Add Unsigned
.text:00402B74                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B78                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B7C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402B80                 sw      $a0, 8($v0)      # Store Word
.text:00402B84                 break   0                # Break
.text:00402B88                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402B8C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B90                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B94                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B98                 lw      $a0, 8($v0)      # Load Word
.text:00402B9C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BA0                 subu    $a0, $v0         # Subtract Unsigned
.text:00402BA4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402BA8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402BB0                 sw      $a0, 8($v0)      # Store Word
.text:00402BB4                 break   0                # Break
.text:00402BB8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402BBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BC0                 sll     $v0, 2           # Shift Left Logical
.text:00402BC4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402BCC                 lw      $v0, 8($v0)      # Load Word
.text:00402BD0                 srl     $v1, $v0, 21     # Shift Right Logical
.text:00402BD4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BD8                 sll     $v0, 2           # Shift Left Logical
.text:00402BDC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BE0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402BE4                 lw      $v0, 8($v0)      # Load Word
.text:00402BE8                 sll     $v0, 11          # Shift Left Logical
.text:00402BEC                 or      $v1, $v0         # OR
.text:00402BF0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402BF4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BF8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402BFC                 sw      $v1, 8($v0)      # Store Word
.text:00402C00                 break   0                # Break
.text:00402C04                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402C08                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C0C                 sll     $v0, 2           # Shift Left Logical
.text:00402C10                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C14                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402C18                 lw      $v0, 8($v0)      # Load Word
.text:00402C1C                 srl     $v1, $v0, 4      # Shift Right Logical
.text:00402C20                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C24                 sll     $v0, 2           # Shift Left Logical
.text:00402C28                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C2C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402C30                 lw      $v0, 8($v0)      # Load Word
.text:00402C34                 sll     $v0, 28          # Shift Left Logical
.text:00402C38                 or      $v1, $v0         # OR
.text:00402C3C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402C40                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C44                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402C48                 sw      $v1, 8($v0)      # Store Word
.text:00402C4C                 break   0                # Break
.text:00402C50                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402C54                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C58                 sll     $v0, 2           # Shift Left Logical
.text:00402C5C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C60                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402C64                 lw      $v1, 8($v0)      # Load Word
.text:00402C68                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C6C                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00402C70                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00402C74                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C78                 sll     $v0, 2           # Shift Left Logical
.text:00402C7C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C80                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402C84                 lw      $a1, 8($v0)      # Load Word
.text:00402C88                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C8C                 nor     $v0, $zero, $v0  # NOR
.text:00402C90                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00402C94                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:00402C98                 or      $v1, $v0         # OR
.text:00402C9C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402CA0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CA4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402CA8                 sw      $v1, 8($v0)      # Store Word
.text:00402CAC                 break   0                # Break
.text:00402CB0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402CB4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402CB8                 sll     $v0, 2           # Shift Left Logical
.text:00402CBC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CC0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402CC4                 lw      $v0, 8($v0)      # Load Word
.text:00402CC8                 nor     $v1, $zero, $v0  # NOR
.text:00402CCC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402CD0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CD4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402CD8                 sw      $v1, 8($v0)      # Store Word
.text:00402CDC                 break   0                # Break
.text:00402CE0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402CE4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402CE8                 sll     $v0, 2           # Shift Left Logical
.text:00402CEC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CF0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402CF4                 lw      $v0, 8($v0)      # Load Word
.text:00402CF8                 nor     $v1, $zero, $v0  # NOR
.text:00402CFC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402D00                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D04                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D08                 sw      $v1, 8($v0)      # Store Word
.text:00402D0C                 break   0                # Break
.text:00402D10                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D14                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D18                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D1C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D20                 lw      $a0, 8($v0)      # Load Word
.text:00402D24                 li      $v0, 0xA9BE160D  # Load Immediate
.text:00402D2C                 xor     $a0, $v0         # Exclusive OR
.text:00402D30                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D34                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D38                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402D3C                 sw      $a0, 8($v0)      # Store Word
.text:00402D40                 break   0                # Break
.text:00402D44                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D48                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D4C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D50                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D54                 lw      $a0, 8($v0)      # Load Word
.text:00402D58                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402D5C                 addu    $a0, $v0         # Add Unsigned
.text:00402D60                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D64                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D68                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402D6C                 sw      $a0, 8($v0)      # Store Word
.text:00402D70                 break   0                # Break
.text:00402D74                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D78                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D7C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D80                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D84                 lw      $a0, 8($v0)      # Load Word
.text:00402D88                 li      $v0, 0xD45CEF0A  # Load Immediate
.text:00402D90                 addu    $a0, $v0         # Add Unsigned
.text:00402D94                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D98                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D9C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402DA0                 sw      $a0, 8($v0)      # Store Word
.text:00402DA4                 break   0                # Break
.text:00402DA8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402DAC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DB0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DB4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402DB8                 lw      $a0, 8($v0)      # Load Word
.text:00402DBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402DC0                 xor     $a0, $v0         # Exclusive OR
.text:00402DC4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DC8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DCC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402DD0                 sw      $a0, 8($v0)      # Store Word
.text:00402DD4                 break   0                # Break
.text:00402DD8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402DDC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DE0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DE4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402DE8                 lw      $a0, 8($v0)      # Load Word
.text:00402DEC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402DF0                 subu    $a0, $v0         # Subtract Unsigned
.text:00402DF4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DF8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DFC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E00                 sw      $a0, 8($v0)      # Store Word
.text:00402E04                 break   0                # Break
.text:00402E08                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402E0C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E10                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E14                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E18                 lw      $a0, 8($v0)      # Load Word
.text:00402E1C                 li      $v0, 0x73C69F47  # Load Immediate
.text:00402E24                 addu    $a0, $v0         # Add Unsigned
.text:00402E28                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E2C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E30                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E34                 sw      $a0, 8($v0)      # Store Word
.text:00402E38                 break   0                # Break
.text:00402E3C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402E40                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402E44                 sll     $v0, 2           # Shift Left Logical
.text:00402E48                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E4C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E50                 lw      $v0, 8($v0)      # Load Word
.text:00402E54                 srl     $v1, $v0, 20     # Shift Right Logical
.text:00402E58                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402E5C                 sll     $v0, 2           # Shift Left Logical
.text:00402E60                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E64                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402E68                 lw      $v0, 8($v0)      # Load Word
.text:00402E6C                 sll     $v0, 12          # Shift Left Logical
.text:00402E70                 or      $v1, $v0         # OR
.text:00402E74                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402E78                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E7C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E80                 sw      $v1, 8($v0)      # Store Word
.text:00402E84                 break   0                # Break
.text:00402E88                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402E8C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E90                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E94                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E98                 lw      $a0, 8($v0)      # Load Word
.text:00402E9C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402EA0                 xor     $a0, $v0         # Exclusive OR
.text:00402EA4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402EA8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402EB0                 sw      $a0, 8($v0)      # Store Word
.text:00402EB4                 break   0                # Break
.text:00402EB8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402EBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402EC0                 sll     $v0, 2           # Shift Left Logical
.text:00402EC4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402ECC                 lw      $v0, 8($v0)      # Load Word
.text:00402ED0                 sll     $v1, $v0, 18     # Shift Left Logical
.text:00402ED4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402ED8                 sll     $v0, 2           # Shift Left Logical
.text:00402EDC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EE0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402EE4                 lw      $v0, 8($v0)      # Load Word
.text:00402EE8                 srl     $v0, 14          # Shift Right Logical
.text:00402EEC                 or      $v1, $v0         # OR
.text:00402EF0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402EF4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EF8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402EFC                 sw      $v1, 8($v0)      # Store Word
.text:00402F00                 break   0                # Break
.text:00402F04                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402F08                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402F0C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F10                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402F14                 lw      $a0, 8($v0)      # Load Word
.text:00402F18                 li      $v0, 0x3ECA6F23  # Load Immediate
.text:00402F20                 addu    $a0, $v0         # Add Unsigned
.text:00402F24                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402F28                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F2C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F30                 sw      $a0, 8($v0)      # Store Word
.text:00402F34                 break   0                # Break
.text:00402F38                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402F3C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F40                 sll     $v0, 2           # Shift Left Logical
.text:00402F44                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F48                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F4C                 lw      $v0, 8($v0)      # Load Word
.text:00402F50                 nor     $v1, $zero, $v0  # NOR
.text:00402F54                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402F58                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F5C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402F60                 sw      $v1, 8($v0)      # Store Word
.text:00402F64                 break   0                # Break
.text:00402F68                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402F6C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F70                 sll     $v0, 2           # Shift Left Logical
.text:00402F74                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F78                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F7C                 lw      $v0, 8($v0)      # Load Word
.text:00402F80                 sll     $v1, $v0, 23     # Shift Left Logical
.text:00402F84                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F88                 sll     $v0, 2           # Shift Left Logical
.text:00402F8C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F90                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402F94                 lw      $v0, 8($v0)      # Load Word
.text:00402F98                 srl     $v0, 9           # Shift Right Logical
.text:00402F9C                 or      $v1, $v0         # OR
.text:00402FA0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402FA4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FA8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FAC                 sw      $v1, 8($v0)      # Store Word
.text:00402FB0                 break   0                # Break
.text:00402FB4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402FB8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FBC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FC0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FC4                 lw      $a0, 8($v0)      # Load Word
.text:00402FC8                 li      $v0, 0xCC4E5D94  # Load Immediate
.text:00402FD0                 xor     $a0, $v0         # Exclusive OR
.text:00402FD4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FD8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FDC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402FE0                 sw      $a0, 8($v0)      # Store Word
.text:00402FE4                 break   0                # Break
.text:00402FE8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402FEC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FF0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FF4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FF8                 lw      $a0, 8($v0)      # Load Word
.text:00402FFC                 li      $v0, 0x38C1FEB8  # Load Immediate
.text:00403004                 xor     $a0, $v0         # Exclusive OR
.text:00403008                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040300C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403010                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403014                 sw      $a0, 8($v0)      # Store Word
.text:00403018                 break   0                # Break
.text:0040301C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403020                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403024                 sll     $v0, 2           # Shift Left Logical
.text:00403028                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040302C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403030                 lw      $v0, 8($v0)      # Load Word
.text:00403034                 srl     $v1, $v0, 8      # Shift Right Logical
.text:00403038                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040303C                 sll     $v0, 2           # Shift Left Logical
.text:00403040                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403044                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403048                 lw      $v0, 8($v0)      # Load Word
.text:0040304C                 sll     $v0, 24          # Shift Left Logical
.text:00403050                 or      $v1, $v0         # OR
.text:00403054                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403058                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040305C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403060                 sw      $v1, 8($v0)      # Store Word
.text:00403064                 break   0                # Break
.text:00403068                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040306C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403070                 sll     $v0, 2           # Shift Left Logical
.text:00403074                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403078                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040307C                 lw      $v0, 8($v0)      # Load Word
.text:00403080                 nor     $v1, $zero, $v0  # NOR
.text:00403084                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403088                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040308C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403090                 sw      $v1, 8($v0)      # Store Word
.text:00403094                 break   0                # Break
.text:00403098                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040309C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030A0                 sll     $v0, 2           # Shift Left Logical
.text:004030A4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030A8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004030AC                 lw      $v0, 8($v0)      # Load Word
.text:004030B0                 srl     $v1, $v0, 3      # Shift Right Logical
.text:004030B4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030B8                 sll     $v0, 2           # Shift Left Logical
.text:004030BC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030C0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004030C4                 lw      $v0, 8($v0)      # Load Word
.text:004030C8                 sll     $v0, 29          # Shift Left Logical
.text:004030CC                 or      $v1, $v0         # OR
.text:004030D0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004030D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004030DC                 sw      $v1, 8($v0)      # Store Word
.text:004030E0                 break   0                # Break
.text:004030E4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004030E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030EC                 sll     $v0, 2           # Shift Left Logical
.text:004030F0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004030F8                 lw      $v1, 8($v0)      # Load Word
.text:004030FC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403100                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403104                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403108                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040310C                 sll     $v0, 2           # Shift Left Logical
.text:00403110                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403114                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403118                 lw      $a1, 8($v0)      # Load Word
.text:0040311C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403120                 nor     $v0, $zero, $v0  # NOR
.text:00403124                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403128                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040312C                 or      $v1, $v0         # OR
.text:00403130                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403134                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403138                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040313C                 sw      $v1, 8($v0)      # Store Word
.text:00403140                 break   0                # Break
.text:00403144                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403148                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040314C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403150                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403154                 lw      $a0, 8($v0)      # Load Word
.text:00403158                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040315C                 addu    $a0, $v0         # Add Unsigned
.text:00403160                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403164                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403168                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040316C                 sw      $a0, 8($v0)      # Store Word
.text:00403170                 break   0                # Break
.text:00403174                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403178                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040317C                 sll     $v0, 2           # Shift Left Logical
.text:00403180                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403184                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403188                 lw      $v1, 8($v0)      # Load Word
.text:0040318C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403190                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403194                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403198                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040319C                 sll     $v0, 2           # Shift Left Logical
.text:004031A0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031A4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004031A8                 lw      $a1, 8($v0)      # Load Word
.text:004031AC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004031B0                 nor     $v0, $zero, $v0  # NOR
.text:004031B4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004031B8                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:004031BC                 or      $v1, $v0         # OR
.text:004031C0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004031C4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031C8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004031CC                 sw      $v1, 8($v0)      # Store Word
.text:004031D0                 break   0                # Break
.text:004031D4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004031D8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004031DC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031E0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004031E4                 lw      $a0, 8($v0)      # Load Word
.text:004031E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004031EC                 xor     $a0, $v0         # Exclusive OR
.text:004031F0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004031F4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031F8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004031FC                 sw      $a0, 8($v0)      # Store Word
.text:00403200                 break   0                # Break
.text:00403204                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403208                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040320C                 sll     $v0, 2           # Shift Left Logical
.text:00403210                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403214                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403218                 lw      $v0, 8($v0)      # Load Word
.text:0040321C                 nor     $v1, $zero, $v0  # NOR
.text:00403220                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403224                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403228                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040322C                 sw      $v1, 8($v0)      # Store Word
.text:00403230                 break   0                # Break
.text:00403234                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403238                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040323C                 sll     $v0, 2           # Shift Left Logical
.text:00403240                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403244                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403248                 lw      $v0, 8($v0)      # Load Word
.text:0040324C                 sll     $v1, $v0, 29     # Shift Left Logical
.text:00403250                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403254                 sll     $v0, 2           # Shift Left Logical
.text:00403258                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040325C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403260                 lw      $v0, 8($v0)      # Load Word
.text:00403264                 srl     $v0, 3           # Shift Right Logical
.text:00403268                 or      $v1, $v0         # OR
.text:0040326C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403270                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403274                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403278                 sw      $v1, 8($v0)      # Store Word
.text:0040327C                 break   0                # Break
.text:00403280                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403284                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403288                 sll     $v0, 2           # Shift Left Logical
.text:0040328C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403290                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403294                 lw      $v0, 8($v0)      # Load Word
.text:00403298                 sll     $v1, $v0, 29     # Shift Left Logical
.text:0040329C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004032A0                 sll     $v0, 2           # Shift Left Logical
.text:004032A4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032A8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004032AC                 lw      $v0, 8($v0)      # Load Word
.text:004032B0                 srl     $v0, 3           # Shift Right Logical
.text:004032B4                 or      $v1, $v0         # OR
.text:004032B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004032BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004032C4                 sw      $v1, 8($v0)      # Store Word
.text:004032C8                 break   0                # Break
.text:004032CC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004032D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004032D4                 sll     $v0, 2           # Shift Left Logical
.text:004032D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004032E0                 lw      $v0, 8($v0)      # Load Word
.text:004032E4                 nor     $v1, $zero, $v0  # NOR
.text:004032E8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004032EC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032F0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004032F4                 sw      $v1, 8($v0)      # Store Word
.text:004032F8                 break   0                # Break
.text:004032FC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403300                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403304                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403308                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040330C                 lw      $a0, 8($v0)      # Load Word
.text:00403310                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403314                 xor     $a0, $v0         # Exclusive OR
.text:00403318                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040331C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403320                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403324                 sw      $a0, 8($v0)      # Store Word
.text:00403328                 break   0                # Break
.text:0040332C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403330                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403334                 sll     $v0, 2           # Shift Left Logical
.text:00403338                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040333C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403340                 lw      $v0, 8($v0)      # Load Word
.text:00403344                 sll     $v1, $v0, 31     # Shift Left Logical
.text:00403348                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040334C                 sll     $v0, 2           # Shift Left Logical
.text:00403350                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403354                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403358                 lw      $v0, 8($v0)      # Load Word
.text:0040335C                 srl     $v0, 1           # Shift Right Logical
.text:00403360                 or      $v1, $v0         # OR
.text:00403364                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403368                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040336C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403370                 sw      $v1, 8($v0)      # Store Word
.text:00403374                 break   0                # Break
.text:00403378                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040337C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403380                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403384                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403388                 lw      $a0, 8($v0)      # Load Word
.text:0040338C                 li      $v0, 0xBFD991A0  # Load Immediate
.text:00403394                 xor     $a0, $v0         # Exclusive OR
.text:00403398                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040339C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004033A4                 sw      $a0, 8($v0)      # Store Word
.text:004033A8                 break   0                # Break
.text:004033AC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004033B0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033B4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033B8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004033BC                 lw      $a0, 8($v0)      # Load Word
.text:004033C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004033C4                 addu    $a0, $v0         # Add Unsigned
.text:004033C8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004033D4                 sw      $a0, 8($v0)      # Store Word
.text:004033D8                 break   0                # Break
.text:004033DC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004033E0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033E4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033E8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004033EC                 lw      $a0, 8($v0)      # Load Word
.text:004033F0                 li      $v0, 0xD0358C15  # Load Immediate
.text:004033F8                 addu    $a0, $v0         # Add Unsigned
.text:004033FC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403400                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403404                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403408                 sw      $a0, 8($v0)      # Store Word
.text:0040340C                 break   0                # Break
.text:00403410                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403414                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403418                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040341C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403420                 lw      $a0, 8($v0)      # Load Word
.text:00403424                 li      $v0, 0x192B37D2  # Load Immediate
.text:0040342C                 addu    $a0, $v0         # Add Unsigned
.text:00403430                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403434                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403438                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040343C                 sw      $a0, 8($v0)      # Store Word
.text:00403440                 break   0                # Break
.text:00403444                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403448                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040344C                 sll     $v0, 2           # Shift Left Logical
.text:00403450                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403454                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403458                 lw      $v1, 8($v0)      # Load Word
.text:0040345C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403460                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403464                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403468                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040346C                 sll     $v0, 2           # Shift Left Logical
.text:00403470                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403474                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403478                 lw      $a1, 8($v0)      # Load Word
.text:0040347C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403480                 nor     $v0, $zero, $v0  # NOR
.text:00403484                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403488                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040348C                 or      $v1, $v0         # OR
.text:00403490                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403494                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403498                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040349C                 sw      $v1, 8($v0)      # Store Word
.text:004034A0                 break   0                # Break
.text:004034A4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004034A8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004034AC                 sll     $v0, 2           # Shift Left Logical
.text:004034B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004034B8                 lw      $v0, 8($v0)      # Load Word
.text:004034BC                 srl     $v1, $v0, 17     # Shift Right Logical
.text:004034C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004034C4                 sll     $v0, 2           # Shift Left Logical
.text:004034C8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034CC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004034D0                 lw      $v0, 8($v0)      # Load Word
.text:004034D4                 sll     $v0, 15          # Shift Left Logical
.text:004034D8                 or      $v1, $v0         # OR
.text:004034DC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004034E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004034E8                 sw      $v1, 8($v0)      # Store Word
.text:004034EC                 break   0                # Break
.text:004034F0                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004034F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004034F8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034FC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403500                 lw      $a0, 8($v0)      # Load Word
.text:00403504                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403508                 addu    $a0, $v0         # Add Unsigned
.text:0040350C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403510                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403514                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403518                 sw      $a0, 8($v0)      # Store Word
.text:0040351C                 break   0                # Break
.text:00403520                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403524                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403528                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040352C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403530                 lw      $a0, 8($v0)      # Load Word
.text:00403534                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403538                 xor     $a0, $v0         # Exclusive OR
.text:0040353C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403540                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403544                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403548                 sw      $a0, 8($v0)      # Store Word
.text:0040354C                 break   0                # Break
.text:00403550                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403554                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403558                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040355C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403560                 lw      $a0, 8($v0)      # Load Word
.text:00403564                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403568                 xor     $a0, $v0         # Exclusive OR
.text:0040356C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403570                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403574                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403578                 sw      $a0, 8($v0)      # Store Word
.text:0040357C                 break   0                # Break
.text:00403580                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403584                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403588                 sll     $v0, 2           # Shift Left Logical
.text:0040358C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403590                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403594                 lw      $v0, 8($v0)      # Load Word
.text:00403598                 sll     $v1, $v0, 28     # Shift Left Logical
.text:0040359C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004035A0                 sll     $v0, 2           # Shift Left Logical
.text:004035A4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035A8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004035AC                 lw      $v0, 8($v0)      # Load Word
.text:004035B0                 srl     $v0, 4           # Shift Right Logical
.text:004035B4                 or      $v1, $v0         # OR
.text:004035B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004035BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004035C4                 sw      $v1, 8($v0)      # Store Word
.text:004035C8                 break   0                # Break
.text:004035CC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004035D0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004035D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004035DC                 lw      $a0, 8($v0)      # Load Word
.text:004035E0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004035E4                 addu    $a0, $v0         # Add Unsigned
.text:004035E8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004035EC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035F0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004035F4                 sw      $a0, 8($v0)      # Store Word
.text:004035F8                 break   0                # Break
.text:004035FC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403600                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403604                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403608                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040360C                 lw      $a0, 8($v0)      # Load Word
.text:00403610                 li      $v0, 0x8103D046  # Load Immediate
.text:00403618                 xor     $a0, $v0         # Exclusive OR
.text:0040361C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403620                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403624                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403628                 sw      $a0, 8($v0)      # Store Word
.text:0040362C                 break   0                # Break
.text:00403630                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403634                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403638                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040363C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403640                 lw      $a0, 8($v0)      # Load Word
.text:00403644                 li      $v0, 0x3D68A35C  # Load Immediate
.text:0040364C                 xor     $a0, $v0         # Exclusive OR
.text:00403650                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403654                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403658                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040365C                 sw      $a0, 8($v0)      # Store Word
.text:00403660                 break   0                # Break
.text:00403664                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403668                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040366C                 sll     $v0, 2           # Shift Left Logical
.text:00403670                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403674                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403678                 lw      $v0, 8($v0)      # Load Word
.text:0040367C                 nor     $v1, $zero, $v0  # NOR
.text:00403680                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403684                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403688                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040368C                 sw      $v1, 8($v0)      # Store Word
.text:00403690                 break   0                # Break
.text:00403694                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403698                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040369C                 sll     $v0, 2           # Shift Left Logical
.text:004036A0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036A4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004036A8                 lw      $v0, 8($v0)      # Load Word
.text:004036AC                 sll     $v1, $v0, 6      # Shift Left Logical
.text:004036B0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004036B4                 sll     $v0, 2           # Shift Left Logical
.text:004036B8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036BC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004036C0                 lw      $v0, 8($v0)      # Load Word
.text:004036C4                 srl     $v0, 26          # Shift Right Logical
.text:004036C8                 or      $v1, $v0         # OR
.text:004036CC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004036D0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036D4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004036D8                 sw      $v1, 8($v0)      # Store Word
.text:004036DC                 break   0                # Break
.text:004036E0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004036E4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004036E8                 sll     $v0, 2           # Shift Left Logical
.text:004036EC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036F0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004036F4                 lw      $v0, 8($v0)      # Load Word
.text:004036F8                 sll     $v1, $v0, 5      # Shift Left Logical
.text:004036FC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403700                 sll     $v0, 2           # Shift Left Logical
.text:00403704                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403708                 addu    $v0, $a1, $v0    # Add Unsigned
.text:0040370C                 lw      $v0, 8($v0)      # Load Word
.text:00403710                 srl     $v0, 27          # Shift Right Logical
.text:00403714                 or      $v1, $v0         # OR
.text:00403718                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040371C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403720                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403724                 sw      $v1, 8($v0)      # Store Word
.text:00403728                 break   0                # Break
.text:0040372C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403730                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403734                 sll     $v0, 2           # Shift Left Logical
.text:00403738                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040373C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403740                 lw      $v0, 8($v0)      # Load Word
.text:00403744                 sll     $v1, $v0, 5      # Shift Left Logical
.text:00403748                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040374C                 sll     $v0, 2           # Shift Left Logical
.text:00403750                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403754                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403758                 lw      $v0, 8($v0)      # Load Word
.text:0040375C                 srl     $v0, 27          # Shift Right Logical
.text:00403760                 or      $v1, $v0         # OR
.text:00403764                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403768                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040376C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403770                 sw      $v1, 8($v0)      # Store Word
.text:00403774                 break   0                # Break
.text:00403778                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040377C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403780                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403784                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403788                 lw      $a0, 8($v0)      # Load Word
.text:0040378C                 li      $v0, 0x6EDC032   # Load Immediate
.text:00403794                 addu    $a0, $v0         # Add Unsigned
.text:00403798                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040379C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004037A4                 sw      $a0, 8($v0)      # Store Word
.text:004037A8                 break   0                # Break
.text:004037AC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004037B0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037B4                 sll     $v0, 2           # Shift Left Logical
.text:004037B8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037BC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004037C0                 lw      $v1, 8($v0)      # Load Word
.text:004037C4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037C8                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004037CC                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004037D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037D4                 sll     $v0, 2           # Shift Left Logical
.text:004037D8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037DC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004037E0                 lw      $a1, 8($v0)      # Load Word
.text:004037E4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037E8                 nor     $v0, $zero, $v0  # NOR
.text:004037EC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004037F0                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004037F4                 or      $v1, $v0         # OR
.text:004037F8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004037FC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403800                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403804                 sw      $v1, 8($v0)      # Store Word
.text:00403808                 break   0                # Break
.text:0040380C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403810                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403814                 sll     $v0, 2           # Shift Left Logical
.text:00403818                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040381C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403820                 lw      $v0, 8($v0)      # Load Word
.text:00403824                 sll     $v1, $v0, 16     # Shift Left Logical
.text:00403828                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040382C                 sll     $v0, 2           # Shift Left Logical
.text:00403830                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403834                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403838                 lw      $v0, 8($v0)      # Load Word
.text:0040383C                 srl     $v0, 16          # Shift Right Logical
.text:00403840                 or      $v1, $v0         # OR
.text:00403844                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403848                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040384C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403850                 sw      $v1, 8($v0)      # Store Word
.text:00403854                 break   0                # Break
.text:00403858                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040385C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403860                 sll     $v0, 2           # Shift Left Logical
.text:00403864                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403868                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040386C                 lw      $v0, 8($v0)      # Load Word
.text:00403870                 nor     $v1, $zero, $v0  # NOR
.text:00403874                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403878                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040387C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403880                 sw      $v1, 8($v0)      # Store Word
.text:00403884                 break   0                # Break
.text:00403888                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040388C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403890                 sll     $v0, 2           # Shift Left Logical
.text:00403894                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403898                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040389C                 lw      $v0, 8($v0)      # Load Word
.text:004038A0                 nor     $v1, $zero, $v0  # NOR
.text:004038A4                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004038A8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038AC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038B0                 sw      $v1, 8($v0)      # Store Word
.text:004038B4                 break   0                # Break
.text:004038B8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004038BC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038C0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038C4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038C8                 lw      $a0, 8($v0)      # Load Word
.text:004038CC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004038D0                 subu    $a0, $v0         # Subtract Unsigned
.text:004038D4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004038E0                 sw      $a0, 8($v0)      # Store Word
.text:004038E4                 break   0                # Break
.text:004038E8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004038EC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038F0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038F4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038F8                 lw      $a0, 8($v0)      # Load Word
.text:004038FC                 li      $v0, 0xDBFA3745  # Load Immediate
.text:00403904                 addu    $a0, $v0         # Add Unsigned
.text:00403908                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040390C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403910                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403914                 sw      $a0, 8($v0)      # Store Word
.text:00403918                 break   0                # Break
.text:0040391C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403920                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403924                 sll     $v0, 2           # Shift Left Logical
.text:00403928                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040392C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403930                 lw      $v1, 8($v0)      # Load Word
.text:00403934                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403938                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040393C                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403940                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403944                 sll     $v0, 2           # Shift Left Logical
.text:00403948                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040394C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403950                 lw      $a1, 8($v0)      # Load Word
.text:00403954                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403958                 nor     $v0, $zero, $v0  # NOR
.text:0040395C                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403960                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:00403964                 or      $v1, $v0         # OR
.text:00403968                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040396C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403970                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403974                 sw      $v1, 8($v0)      # Store Word
.text:00403978                 break   0                # Break
.text:0040397C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403980                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403984                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403988                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040398C                 lw      $a0, 8($v0)      # Load Word
.text:00403990                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403994                 xor     $a0, $v0         # Exclusive OR
.text:00403998                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040399C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004039A4                 sw      $a0, 8($v0)      # Store Word
.text:004039A8                 break   0                # Break
.text:004039AC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004039B0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004039B4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039B8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004039BC                 lw      $a0, 8($v0)      # Load Word
.text:004039C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004039C4                 addu    $a0, $v0         # Add Unsigned
.text:004039C8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004039CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004039D4                 sw      $a0, 8($v0)      # Store Word
.text:004039D8                 break   0                # Break
.text:004039DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004039E0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004039E4                 sw      $v0, 0x48+i($fp)  # Store Word'''.split('\n')

block_code_of_son_reordered_loop_unrolled = '''; Found the 0th break (@0040228c) ; new pc will be 00402290
; ========================= BLOCK 0 =========================
.text:00402290                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402294                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402298                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040229C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004022A0                 lw      $a0, 8($v0)      # Load Word
.text:004022A4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022A8                 subu    $a0, $v0         # Subtract Unsigned
.text:004022AC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004022B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004022B8                 sw      $a0, 8($v0)      # Store Word
; Found the 1th break (@004022bc) ; new pc will be 00402ce0
; ========================= BLOCK 1 =========================
.text:00402CE0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402CE4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402CE8                 sll     $v0, 2           # Shift Left Logical
.text:00402CEC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CF0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402CF4                 lw      $v0, 8($v0)      # Load Word
.text:00402CF8                 nor     $v1, $zero, $v0  # NOR
.text:00402CFC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402D00                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D04                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D08                 sw      $v1, 8($v0)      # Store Word
; Found the 2th break (@00402d0c) ; new pc will be 00402da8
; ========================= BLOCK 2 =========================
.text:00402DA8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402DAC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DB0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DB4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402DB8                 lw      $a0, 8($v0)      # Load Word
.text:00402DBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402DC0                 xor     $a0, $v0         # Exclusive OR
.text:00402DC4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DC8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DCC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402DD0                 sw      $a0, 8($v0)      # Store Word
; Found the 3th break (@00402dd4) ; new pc will be 00403550
; ========================= BLOCK 3 =========================
.text:00403550                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403554                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403558                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040355C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403560                 lw      $a0, 8($v0)      # Load Word
.text:00403564                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403568                 xor     $a0, $v0         # Exclusive OR
.text:0040356C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403570                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403574                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403578                 sw      $a0, 8($v0)      # Store Word
; Found the 4th break (@0040357c) ; new pc will be 00402f04
; ========================= BLOCK 4 =========================
.text:00402F04                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402F08                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402F0C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F10                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402F14                 lw      $a0, 8($v0)      # Load Word
.text:00402F18                 li      $v0, 0x3ECA6F23  # Load Immediate
.text:00402F20                 addu    $a0, $v0         # Add Unsigned
.text:00402F24                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402F28                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F2C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F30                 sw      $a0, 8($v0)      # Store Word
; Found the 5th break (@00402f34) ; new pc will be 00403778
; ========================= BLOCK 5 =========================
.text:00403778                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040377C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403780                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403784                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403788                 lw      $a0, 8($v0)      # Load Word
.text:0040378C                 li      $v0, 0x6EDC032   # Load Immediate
.text:00403794                 addu    $a0, $v0         # Add Unsigned
.text:00403798                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040379C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004037A4                 sw      $a0, 8($v0)      # Store Word
; Found the 6th break (@004037a8) ; new pc will be 004036e0
; ========================= BLOCK 6 =========================
.text:004036E0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004036E4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004036E8                 sll     $v0, 2           # Shift Left Logical
.text:004036EC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036F0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004036F4                 lw      $v0, 8($v0)      # Load Word
.text:004036F8                 sll     $v1, $v0, 5      # Shift Left Logical
.text:004036FC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403700                 sll     $v0, 2           # Shift Left Logical
.text:00403704                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403708                 addu    $v0, $a1, $v0    # Add Unsigned
.text:0040370C                 lw      $v0, 8($v0)      # Load Word
.text:00403710                 srl     $v0, 27          # Shift Right Logical
.text:00403714                 or      $v1, $v0         # OR
.text:00403718                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040371C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403720                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403724                 sw      $v1, 8($v0)      # Store Word
; Found the 7th break (@00403728) ; new pc will be 00402420
; ========================= BLOCK 7 =========================
.text:00402420                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402424                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402428                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040242C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402430                 lw      $a0, 8($v0)      # Load Word
.text:00402434                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402438                 xor     $a0, $v0         # Exclusive OR
.text:0040243C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402440                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402444                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402448                 sw      $a0, 8($v0)      # Store Word
; Found the 8th break (@0040244c) ; new pc will be 00403098
; ========================= BLOCK 8 =========================
.text:00403098                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040309C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030A0                 sll     $v0, 2           # Shift Left Logical
.text:004030A4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030A8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004030AC                 lw      $v0, 8($v0)      # Load Word
.text:004030B0                 srl     $v1, $v0, 3      # Shift Right Logical
.text:004030B4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030B8                 sll     $v0, 2           # Shift Left Logical
.text:004030BC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030C0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004030C4                 lw      $v0, 8($v0)      # Load Word
.text:004030C8                 sll     $v0, 29          # Shift Left Logical
.text:004030CC                 or      $v1, $v0         # OR
.text:004030D0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004030D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004030DC                 sw      $v1, 8($v0)      # Store Word
; Found the 9th break (@004030e0) ; new pc will be 004032fc
; ========================= BLOCK 9 =========================
.text:004032FC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403300                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403304                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403308                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040330C                 lw      $a0, 8($v0)      # Load Word
.text:00403310                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403314                 xor     $a0, $v0         # Exclusive OR
.text:00403318                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040331C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403320                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403324                 sw      $a0, 8($v0)      # Store Word
; Found the 10th break (@00403328) ; new pc will be 00402774
; ========================= BLOCK 10 =========================
.text:00402774                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402778                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040277C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402780                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402784                 lw      $a0, 8($v0)      # Load Word
.text:00402788                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040278C                 xor     $a0, $v0         # Exclusive OR
.text:00402790                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402794                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402798                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040279C                 sw      $a0, 8($v0)      # Store Word
; Found the 11th break (@004027a0) ; new pc will be 004033dc
; ========================= BLOCK 11 =========================
.text:004033DC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004033E0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033E4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033E8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004033EC                 lw      $a0, 8($v0)      # Load Word
.text:004033F0                 li      $v0, 0xD0358C15  # Load Immediate
.text:004033F8                 addu    $a0, $v0         # Add Unsigned
.text:004033FC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403400                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403404                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403408                 sw      $a0, 8($v0)      # Store Word
; Found the 12th break (@0040340c) ; new pc will be 004027d8
; ========================= BLOCK 12 =========================
.text:004027D8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004027DC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004027E8                 lw      $a0, 8($v0)      # Load Word
.text:004027EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004027F0                 subu    $a0, $v0         # Subtract Unsigned
.text:004027F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027F8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027FC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402800                 sw      $a0, 8($v0)      # Store Word
; Found the 13th break (@00402804) ; new pc will be 0040380c
; ========================= BLOCK 13 =========================
.text:0040380C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403810                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403814                 sll     $v0, 2           # Shift Left Logical
.text:00403818                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040381C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403820                 lw      $v0, 8($v0)      # Load Word
.text:00403824                 sll     $v1, $v0, 16     # Shift Left Logical
.text:00403828                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040382C                 sll     $v0, 2           # Shift Left Logical
.text:00403830                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403834                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403838                 lw      $v0, 8($v0)      # Load Word
.text:0040383C                 srl     $v0, 16          # Shift Right Logical
.text:00403840                 or      $v1, $v0         # OR
.text:00403844                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403848                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040384C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403850                 sw      $v1, 8($v0)      # Store Word
; Found the 14th break (@00403854) ; new pc will be 00402c50
; ========================= BLOCK 14 =========================
.text:00402C50                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402C54                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C58                 sll     $v0, 2           # Shift Left Logical
.text:00402C5C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C60                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402C64                 lw      $v1, 8($v0)      # Load Word
.text:00402C68                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C6C                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00402C70                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00402C74                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C78                 sll     $v0, 2           # Shift Left Logical
.text:00402C7C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C80                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402C84                 lw      $a1, 8($v0)      # Load Word
.text:00402C88                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C8C                 nor     $v0, $zero, $v0  # NOR
.text:00402C90                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00402C94                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:00402C98                 or      $v1, $v0         # OR
.text:00402C9C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402CA0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CA4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402CA8                 sw      $v1, 8($v0)      # Store Word
; Found the 15th break (@00402cac) ; new pc will be 00402ad8
; ========================= BLOCK 15 =========================
.text:00402AD8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402ADC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402AE0                 sll     $v0, 2           # Shift Left Logical
.text:00402AE4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AE8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402AEC                 lw      $v0, 8($v0)      # Load Word
.text:00402AF0                 nor     $v1, $zero, $v0  # NOR
.text:00402AF4                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402AF8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AFC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B00                 sw      $v1, 8($v0)      # Store Word
; Found the 16th break (@00402b04) ; new pc will be 00402e3c
; ========================= BLOCK 16 =========================
.text:00402E3C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402E40                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402E44                 sll     $v0, 2           # Shift Left Logical
.text:00402E48                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E4C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E50                 lw      $v0, 8($v0)      # Load Word
.text:00402E54                 srl     $v1, $v0, 20     # Shift Right Logical
.text:00402E58                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402E5C                 sll     $v0, 2           # Shift Left Logical
.text:00402E60                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E64                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402E68                 lw      $v0, 8($v0)      # Load Word
.text:00402E6C                 sll     $v0, 12          # Shift Left Logical
.text:00402E70                 or      $v1, $v0         # OR
.text:00402E74                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402E78                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E7C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E80                 sw      $v1, 8($v0)      # Store Word
; Found the 17th break (@00402e84) ; new pc will be 0040230c
; ========================= BLOCK 17 =========================
.text:0040230C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402310                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402314                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402318                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040231C                 lw      $a0, 8($v0)      # Load Word
.text:00402320                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402324                 subu    $a0, $v0         # Subtract Unsigned
.text:00402328                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040232C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402330                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402334                 sw      $a0, 8($v0)      # Store Word
; Found the 18th break (@00402338) ; new pc will be 00402dd8
; ========================= BLOCK 18 =========================
.text:00402DD8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402DDC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DE0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DE4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402DE8                 lw      $a0, 8($v0)      # Load Word
.text:00402DEC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402DF0                 subu    $a0, $v0         # Subtract Unsigned
.text:00402DF4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DF8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DFC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E00                 sw      $a0, 8($v0)      # Store Word
; Found the 19th break (@00402e04) ; new pc will be 004030e4
; ========================= BLOCK 19 =========================
.text:004030E4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004030E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030EC                 sll     $v0, 2           # Shift Left Logical
.text:004030F0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004030F8                 lw      $v1, 8($v0)      # Load Word
.text:004030FC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403100                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403104                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403108                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040310C                 sll     $v0, 2           # Shift Left Logical
.text:00403110                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403114                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403118                 lw      $a1, 8($v0)      # Load Word
.text:0040311C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403120                 nor     $v0, $zero, $v0  # NOR
.text:00403124                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403128                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040312C                 or      $v1, $v0         # OR
.text:00403130                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403134                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403138                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040313C                 sw      $v1, 8($v0)      # Store Word
; Found the 20th break (@00403140) ; new pc will be 00403410
; ========================= BLOCK 20 =========================
.text:00403410                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403414                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403418                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040341C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403420                 lw      $a0, 8($v0)      # Load Word
.text:00403424                 li      $v0, 0x192B37D2  # Load Immediate
.text:0040342C                 addu    $a0, $v0         # Add Unsigned
.text:00403430                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403434                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403438                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040343C                 sw      $a0, 8($v0)      # Store Word
; Found the 21th break (@00403440) ; new pc will be 00402808
; ========================= BLOCK 21 =========================
.text:00402808                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040280C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402810                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402814                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402818                 lw      $a0, 8($v0)      # Load Word
.text:0040281C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402820                 subu    $a0, $v0         # Subtract Unsigned
.text:00402824                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402828                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040282C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402830                 sw      $a0, 8($v0)      # Store Word
; Found the 22th break (@00402834) ; new pc will be 00403068
; ========================= BLOCK 22 =========================
.text:00403068                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040306C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403070                 sll     $v0, 2           # Shift Left Logical
.text:00403074                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403078                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040307C                 lw      $v0, 8($v0)      # Load Word
.text:00403080                 nor     $v1, $zero, $v0  # NOR
.text:00403084                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403088                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040308C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403090                 sw      $v1, 8($v0)      # Store Word
; Found the 23th break (@00403094) ; new pc will be 004025a8
; ========================= BLOCK 23 =========================
.text:004025A8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004025AC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025B0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025B4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025B8                 lw      $a0, 8($v0)      # Load Word
.text:004025BC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004025C0                 addu    $a0, $v0         # Add Unsigned
.text:004025C4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025C8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025CC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004025D0                 sw      $a0, 8($v0)      # Store Word
; Found the 24th break (@004025d4) ; new pc will be 00402608
; ========================= BLOCK 24 =========================
.text:00402608                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040260C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402610                 sll     $v0, 2           # Shift Left Logical
.text:00402614                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402618                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040261C                 lw      $v0, 8($v0)      # Load Word
.text:00402620                 srl     $v1, $v0, 23     # Shift Right Logical
.text:00402624                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402628                 sll     $v0, 2           # Shift Left Logical
.text:0040262C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402630                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402634                 lw      $v0, 8($v0)      # Load Word
.text:00402638                 sll     $v0, 9           # Shift Left Logical
.text:0040263C                 or      $v1, $v0         # OR
.text:00402640                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402644                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402648                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040264C                 sw      $v1, 8($v0)      # Store Word
; Found the 25th break (@00402650) ; new pc will be 00403630
; ========================= BLOCK 25 =========================
.text:00403630                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403634                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403638                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040363C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403640                 lw      $a0, 8($v0)      # Load Word
.text:00403644                 li      $v0, 0x3D68A35C  # Load Immediate
.text:0040364C                 xor     $a0, $v0         # Exclusive OR
.text:00403650                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403654                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403658                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040365C                 sw      $a0, 8($v0)      # Store Word
; Found the 26th break (@00403660) ; new pc will be 00402e08
; ========================= BLOCK 26 =========================
.text:00402E08                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402E0C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E10                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E14                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E18                 lw      $a0, 8($v0)      # Load Word
.text:00402E1C                 li      $v0, 0x73C69F47  # Load Immediate
.text:00402E24                 addu    $a0, $v0         # Add Unsigned
.text:00402E28                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E2C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E30                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E34                 sw      $a0, 8($v0)      # Store Word
; Found the 27th break (@00402e38) ; new pc will be 004038e8
; ========================= BLOCK 27 =========================
.text:004038E8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004038EC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038F0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038F4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038F8                 lw      $a0, 8($v0)      # Load Word
.text:004038FC                 li      $v0, 0xDBFA3745  # Load Immediate
.text:00403904                 addu    $a0, $v0         # Add Unsigned
.text:00403908                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040390C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403910                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403914                 sw      $a0, 8($v0)      # Store Word
; Found the 28th break (@00403918) ; new pc will be 00402c04
; ========================= BLOCK 28 =========================
.text:00402C04                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402C08                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C0C                 sll     $v0, 2           # Shift Left Logical
.text:00402C10                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C14                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402C18                 lw      $v0, 8($v0)      # Load Word
.text:00402C1C                 srl     $v1, $v0, 4      # Shift Right Logical
.text:00402C20                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C24                 sll     $v0, 2           # Shift Left Logical
.text:00402C28                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C2C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402C30                 lw      $v0, 8($v0)      # Load Word
.text:00402C34                 sll     $v0, 28          # Shift Left Logical
.text:00402C38                 or      $v1, $v0         # OR
.text:00402C3C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402C40                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C44                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402C48                 sw      $v1, 8($v0)      # Store Word
; Found the 29th break (@00402c4c) ; new pc will be 00402b54
; ========================= BLOCK 29 =========================
.text:00402B54                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402B58                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B5C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B60                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B64                 lw      $a0, 8($v0)      # Load Word
.text:00402B68                 li      $v0, 0x79662B5D  # Load Immediate
.text:00402B70                 addu    $a0, $v0         # Add Unsigned
.text:00402B74                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B78                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B7C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402B80                 sw      $a0, 8($v0)      # Store Word
; Found the 30th break (@00402b84) ; new pc will be 004034a4
; ========================= BLOCK 30 =========================
.text:004034A4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004034A8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004034AC                 sll     $v0, 2           # Shift Left Logical
.text:004034B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004034B8                 lw      $v0, 8($v0)      # Load Word
.text:004034BC                 srl     $v1, $v0, 17     # Shift Right Logical
.text:004034C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004034C4                 sll     $v0, 2           # Shift Left Logical
.text:004034C8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034CC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004034D0                 lw      $v0, 8($v0)      # Load Word
.text:004034D4                 sll     $v0, 15          # Shift Left Logical
.text:004034D8                 or      $v1, $v0         # OR
.text:004034DC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004034E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004034E8                 sw      $v1, 8($v0)      # Store Word
; Found the 31th break (@004034ec) ; new pc will be 00403204
; ========================= BLOCK 31 =========================
.text:00403204                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403208                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040320C                 sll     $v0, 2           # Shift Left Logical
.text:00403210                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403214                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403218                 lw      $v0, 8($v0)      # Load Word
.text:0040321C                 nor     $v1, $zero, $v0  # NOR
.text:00403220                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403224                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403228                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040322C                 sw      $v1, 8($v0)      # Store Word
; Found the 32th break (@00403230) ; new pc will be 004038b8
; ========================= BLOCK 32 =========================
.text:004038B8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004038BC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038C0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038C4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038C8                 lw      $a0, 8($v0)      # Load Word
.text:004038CC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004038D0                 subu    $a0, $v0         # Subtract Unsigned
.text:004038D4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004038E0                 sw      $a0, 8($v0)      # Store Word
; Found the 33th break (@004038e4) ; new pc will be 00403144
; ========================= BLOCK 33 =========================
.text:00403144                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403148                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040314C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403150                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403154                 lw      $a0, 8($v0)      # Load Word
.text:00403158                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040315C                 addu    $a0, $v0         # Add Unsigned
.text:00403160                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403164                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403168                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040316C                 sw      $a0, 8($v0)      # Store Word
; Found the 34th break (@00403170) ; new pc will be 00402714
; ========================= BLOCK 34 =========================
.text:00402714                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402718                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040271C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402720                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402724                 lw      $a0, 8($v0)      # Load Word
.text:00402728                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040272C                 addu    $a0, $v0         # Add Unsigned
.text:00402730                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402734                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402738                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040273C                 sw      $a0, 8($v0)      # Store Word
; Found the 35th break (@00402740) ; new pc will be 004031d4
; ========================= BLOCK 35 =========================
.text:004031D4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004031D8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004031DC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031E0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004031E4                 lw      $a0, 8($v0)      # Load Word
.text:004031E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004031EC                 xor     $a0, $v0         # Exclusive OR
.text:004031F0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004031F4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031F8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004031FC                 sw      $a0, 8($v0)      # Store Word
; Found the 36th break (@00403200) ; new pc will be 00402d74
; ========================= BLOCK 36 =========================
.text:00402D74                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D78                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D7C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D80                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D84                 lw      $a0, 8($v0)      # Load Word
.text:00402D88                 li      $v0, 0xD45CEF0A  # Load Immediate
.text:00402D90                 addu    $a0, $v0         # Add Unsigned
.text:00402D94                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D98                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D9C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402DA0                 sw      $a0, 8($v0)      # Store Word
; Found the 37th break (@00402da4) ; new pc will be 00402d10
; ========================= BLOCK 37 =========================
.text:00402D10                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D14                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D18                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D1C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D20                 lw      $a0, 8($v0)      # Load Word
.text:00402D24                 li      $v0, 0xA9BE160D  # Load Immediate
.text:00402D2C                 xor     $a0, $v0         # Exclusive OR
.text:00402D30                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D34                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D38                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402D3C                 sw      $a0, 8($v0)      # Store Word
; Found the 38th break (@00402d40) ; new pc will be 004033ac
; ========================= BLOCK 38 =========================
.text:004033AC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004033B0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033B4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033B8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004033BC                 lw      $a0, 8($v0)      # Load Word
.text:004033C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004033C4                 addu    $a0, $v0         # Add Unsigned
.text:004033C8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004033D4                 sw      $a0, 8($v0)      # Store Word
; Found the 39th break (@004033d8) ; new pc will be 00402cb0
; ========================= BLOCK 39 =========================
.text:00402CB0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402CB4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402CB8                 sll     $v0, 2           # Shift Left Logical
.text:00402CBC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CC0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402CC4                 lw      $v0, 8($v0)      # Load Word
.text:00402CC8                 nor     $v1, $zero, $v0  # NOR
.text:00402CCC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402CD0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CD4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402CD8                 sw      $v1, 8($v0)      # Store Word
; Found the 40th break (@00402cdc) ; new pc will be 004028cc
; ========================= BLOCK 40 =========================
.text:004028CC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004028D0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004028D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004028DC                 lw      $a0, 8($v0)      # Load Word
.text:004028E0                 li      $v0, 0x3A2EE307  # Load Immediate
.text:004028E8                 addu    $a0, $v0         # Add Unsigned
.text:004028EC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004028F0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004028F8                 sw      $a0, 8($v0)      # Store Word
; Found the 41th break (@004028fc) ; new pc will be 00402838
; ========================= BLOCK 41 =========================
.text:00402838                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040283C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402840                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402844                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402848                 lw      $a0, 8($v0)      # Load Word
.text:0040284C                 li      $v0, 0xB65E867F  # Load Immediate
.text:00402854                 addu    $a0, $v0         # Add Unsigned
.text:00402858                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040285C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402860                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402864                 sw      $a0, 8($v0)      # Store Word
; Found the 42th break (@00402868) ; new pc will be 00403378
; ========================= BLOCK 42 =========================
.text:00403378                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040337C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403380                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403384                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403388                 lw      $a0, 8($v0)      # Load Word
.text:0040338C                 li      $v0, 0xBFD991A0  # Load Immediate
.text:00403394                 xor     $a0, $v0         # Exclusive OR
.text:00403398                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040339C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004033A4                 sw      $a0, 8($v0)      # Store Word
; Found the 43th break (@004033a8) ; new pc will be 00403234
; ========================= BLOCK 43 =========================
.text:00403234                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403238                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040323C                 sll     $v0, 2           # Shift Left Logical
.text:00403240                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403244                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403248                 lw      $v0, 8($v0)      # Load Word
.text:0040324C                 sll     $v1, $v0, 29     # Shift Left Logical
.text:00403250                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403254                 sll     $v0, 2           # Shift Left Logical
.text:00403258                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040325C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403260                 lw      $v0, 8($v0)      # Load Word
.text:00403264                 srl     $v0, 3           # Shift Right Logical
.text:00403268                 or      $v1, $v0         # OR
.text:0040326C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403270                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403274                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403278                 sw      $v1, 8($v0)      # Store Word
; Found the 44th break (@0040327c) ; new pc will be 00402e88
; ========================= BLOCK 44 =========================
.text:00402E88                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402E8C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E90                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E94                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E98                 lw      $a0, 8($v0)      # Load Word
.text:00402E9C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402EA0                 xor     $a0, $v0         # Exclusive OR
.text:00402EA4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402EA8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402EB0                 sw      $a0, 8($v0)      # Store Word
; Found the 45th break (@00402eb4) ; new pc will be 00403888
; ========================= BLOCK 45 =========================
.text:00403888                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040388C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403890                 sll     $v0, 2           # Shift Left Logical
.text:00403894                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403898                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040389C                 lw      $v0, 8($v0)      # Load Word
.text:004038A0                 nor     $v1, $zero, $v0  # NOR
.text:004038A4                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004038A8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038AC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038B0                 sw      $v1, 8($v0)      # Store Word
; Found the 46th break (@004038b4) ; new pc will be 00402930
; ========================= BLOCK 46 =========================
.text:00402930                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402934                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402938                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040293C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402940                 lw      $a0, 8($v0)      # Load Word
.text:00402944                 li      $v0, 0x4CC0DC26  # Load Immediate
.text:0040294C                 xor     $a0, $v0         # Exclusive OR
.text:00402950                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402954                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402958                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040295C                 sw      $a0, 8($v0)      # Store Word
; Found the 47th break (@00402960) ; new pc will be 00402744
; ========================= BLOCK 47 =========================
.text:00402744                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402748                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040274C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402750                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402754                 lw      $a0, 8($v0)      # Load Word
.text:00402758                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040275C                 subu    $a0, $v0         # Subtract Unsigned
.text:00402760                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402764                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402768                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040276C                 sw      $a0, 8($v0)      # Store Word
; Found the 48th break (@00402770) ; new pc will be 004027a4
; ========================= BLOCK 48 =========================
.text:004027A4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004027A8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027AC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027B0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004027B4                 lw      $a0, 8($v0)      # Load Word
.text:004027B8                 li      $v0, 0xD0970C74  # Load Immediate
.text:004027C0                 addu    $a0, $v0         # Add Unsigned
.text:004027C4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027C8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027CC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004027D0                 sw      $a0, 8($v0)      # Store Word
; Found the 49th break (@004027d4) ; new pc will be 00402b88
; ========================= BLOCK 49 =========================
.text:00402B88                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402B8C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B90                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B94                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B98                 lw      $a0, 8($v0)      # Load Word
.text:00402B9C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BA0                 subu    $a0, $v0         # Subtract Unsigned
.text:00402BA4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402BA8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402BB0                 sw      $a0, 8($v0)      # Store Word
; Found the 50th break (@00402bb4) ; new pc will be 0040233c
; ========================= BLOCK 50 =========================
.text:0040233C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402340                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402344                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402348                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040234C                 lw      $a0, 8($v0)      # Load Word
.text:00402350                 li      $v0, 0x7B4DE789  # Load Immediate
.text:00402358                 xor     $a0, $v0         # Exclusive OR
.text:0040235C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402360                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402364                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402368                 sw      $a0, 8($v0)      # Store Word
; Found the 51th break (@0040236c) ; new pc will be 004035fc
; ========================= BLOCK 51 =========================
.text:004035FC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403600                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403604                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403608                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040360C                 lw      $a0, 8($v0)      # Load Word
.text:00403610                 li      $v0, 0x8103D046  # Load Immediate
.text:00403618                 xor     $a0, $v0         # Exclusive OR
.text:0040361C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403620                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403624                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403628                 sw      $a0, 8($v0)      # Store Word
; Found the 52th break (@0040362c) ; new pc will be 00402fb4
; ========================= BLOCK 52 =========================
.text:00402FB4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402FB8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FBC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FC0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FC4                 lw      $a0, 8($v0)      # Load Word
.text:00402FC8                 li      $v0, 0xCC4E5D94  # Load Immediate
.text:00402FD0                 xor     $a0, $v0         # Exclusive OR
.text:00402FD4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FD8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FDC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402FE0                 sw      $a0, 8($v0)      # Store Word
; Found the 53th break (@00402fe4) ; new pc will be 004034f0
; ========================= BLOCK 53 =========================
.text:004034F0                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004034F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004034F8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034FC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403500                 lw      $a0, 8($v0)      # Load Word
.text:00403504                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403508                 addu    $a0, $v0         # Add Unsigned
.text:0040350C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403510                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403514                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403518                 sw      $a0, 8($v0)      # Store Word
; Found the 54th break (@0040351c) ; new pc will be 0040397c
; ========================= BLOCK 54 =========================
.text:0040397C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403980                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403984                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403988                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040398C                 lw      $a0, 8($v0)      # Load Word
.text:00403990                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403994                 xor     $a0, $v0         # Exclusive OR
.text:00403998                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040399C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004039A4                 sw      $a0, 8($v0)      # Store Word
; Found the 55th break (@004039a8) ; new pc will be 00402aa8
; ========================= BLOCK 55 =========================
.text:00402AA8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402AAC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402AB0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AB4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402AB8                 lw      $a0, 8($v0)      # Load Word
.text:00402ABC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402AC0                 xor     $a0, $v0         # Exclusive OR
.text:00402AC4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402AC8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402ACC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402AD0                 sw      $a0, 8($v0)      # Store Word
; Found the 56th break (@00402ad4) ; new pc will be 00402998
; ========================= BLOCK 56 =========================
.text:00402998                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040299C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029A0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029A4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004029A8                 lw      $a0, 8($v0)      # Load Word
.text:004029AC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004029B0                 subu    $a0, $v0         # Subtract Unsigned
.text:004029B4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029B8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029BC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004029C0                 sw      $a0, 8($v0)      # Store Word
; Found the 57th break (@004029c4) ; new pc will be 00402578
; ========================= BLOCK 57 =========================
.text:00402578                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040257C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402580                 sll     $v0, 2           # Shift Left Logical
.text:00402584                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402588                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040258C                 lw      $v0, 8($v0)      # Load Word
.text:00402590                 nor     $v1, $zero, $v0  # NOR
.text:00402594                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402598                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040259C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025A0                 sw      $v1, 8($v0)      # Store Word
; Found the 58th break (@004025a4) ; new pc will be 00402a5c
; ========================= BLOCK 58 =========================
.text:00402A5C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402A60                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A64                 sll     $v0, 2           # Shift Left Logical
.text:00402A68                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A6C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A70                 lw      $v0, 8($v0)      # Load Word
.text:00402A74                 srl     $v1, $v0, 13     # Shift Right Logical
.text:00402A78                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A7C                 sll     $v0, 2           # Shift Left Logical
.text:00402A80                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A84                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402A88                 lw      $v0, 8($v0)      # Load Word
.text:00402A8C                 sll     $v0, 19          # Shift Left Logical
.text:00402A90                 or      $v1, $v0         # OR
.text:00402A94                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402A98                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A9C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402AA0                 sw      $v1, 8($v0)      # Store Word
; Found the 59th break (@00402aa4) ; new pc will be 004029f8
; ========================= BLOCK 59 =========================
.text:004029F8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004029FC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A00                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A04                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402A08                 lw      $a0, 8($v0)      # Load Word
.text:00402A0C                 li      $v0, 0x81674F2B  # Load Immediate
.text:00402A14                 addu    $a0, $v0         # Add Unsigned
.text:00402A18                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A1C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A20                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A24                 sw      $a0, 8($v0)      # Store Word
; Found the 60th break (@00402a28) ; new pc will be 004023a4
; ========================= BLOCK 60 =========================
.text:004023A4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004023A8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004023AC                 sll     $v0, 2           # Shift Left Logical
.text:004023B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004023B8                 lw      $v0, 8($v0)      # Load Word
.text:004023BC                 srl     $v1, $v0, 12     # Shift Right Logical
.text:004023C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004023C4                 sll     $v0, 2           # Shift Left Logical
.text:004023C8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023CC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004023D0                 lw      $v0, 8($v0)      # Load Word
.text:004023D4                 sll     $v0, 20          # Shift Left Logical
.text:004023D8                 or      $v1, $v0         # OR
.text:004023DC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004023E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004023E8                 sw      $v1, 8($v0)      # Store Word
; Found the 61th break (@004023ec) ; new pc will be 0040286c
; ========================= BLOCK 61 =========================
.text:0040286C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402870                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402874                 sll     $v0, 2           # Shift Left Logical
.text:00402878                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040287C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402880                 lw      $v1, 8($v0)      # Load Word
.text:00402884                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402888                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040288C                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00402890                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402894                 sll     $v0, 2           # Shift Left Logical
.text:00402898                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040289C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004028A0                 lw      $a1, 8($v0)      # Load Word
.text:004028A4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004028A8                 nor     $v0, $zero, $v0  # NOR
.text:004028AC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004028B0                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004028B4                 or      $v1, $v0         # OR
.text:004028B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004028BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004028C4                 sw      $v1, 8($v0)      # Store Word
; Found the 62th break (@004028c8) ; new pc will be 00403520
; ========================= BLOCK 62 =========================
.text:00403520                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403524                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403528                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040352C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403530                 lw      $a0, 8($v0)      # Load Word
.text:00403534                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403538                 xor     $a0, $v0         # Exclusive OR
.text:0040353C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403540                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403544                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403548                 sw      $a0, 8($v0)      # Store Word
; Found the 63th break (@0040354c) ; new pc will be 00403664
; ========================= BLOCK 63 =========================
.text:00403664                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403668                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040366C                 sll     $v0, 2           # Shift Left Logical
.text:00403670                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403674                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403678                 lw      $v0, 8($v0)      # Load Word
.text:0040367C                 nor     $v1, $zero, $v0  # NOR
.text:00403680                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403684                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403688                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040368C                 sw      $v1, 8($v0)      # Store Word
; Found the 64th break (@00403690) ; new pc will be 00402fe8
; ========================= BLOCK 64 =========================
.text:00402FE8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402FEC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FF0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FF4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FF8                 lw      $a0, 8($v0)      # Load Word
.text:00402FFC                 li      $v0, 0x38C1FEB8  # Load Immediate
.text:00403004                 xor     $a0, $v0         # Exclusive OR
.text:00403008                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040300C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403010                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403014                 sw      $a0, 8($v0)      # Store Word
; Found the 65th break (@00403018) ; new pc will be 004039ac
; ========================= BLOCK 65 =========================
.text:004039AC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004039B0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004039B4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039B8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004039BC                 lw      $a0, 8($v0)      # Load Word
.text:004039C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004039C4                 addu    $a0, $v0         # Add Unsigned
.text:004039C8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004039CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004039D4                 sw      $a0, 8($v0)      # Store Word
; Found the 66th break (@004039d8) ; new pc will be 0040332c
; ========================= BLOCK 66 =========================
.text:0040332C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403330                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403334                 sll     $v0, 2           # Shift Left Logical
.text:00403338                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040333C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403340                 lw      $v0, 8($v0)      # Load Word
.text:00403344                 sll     $v1, $v0, 31     # Shift Left Logical
.text:00403348                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040334C                 sll     $v0, 2           # Shift Left Logical
.text:00403350                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403354                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403358                 lw      $v0, 8($v0)      # Load Word
.text:0040335C                 srl     $v0, 1           # Shift Right Logical
.text:00403360                 or      $v1, $v0         # OR
.text:00403364                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403368                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040336C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403370                 sw      $v1, 8($v0)      # Store Word
; Found the 67th break (@00403374) ; new pc will be 00402450
; ========================= BLOCK 67 =========================
.text:00402450                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402454                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402458                 sll     $v0, 2           # Shift Left Logical
.text:0040245C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402460                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402464                 lw      $v0, 8($v0)      # Load Word
.text:00402468                 sll     $v1, $v0, 13     # Shift Left Logical
.text:0040246C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402470                 sll     $v0, 2           # Shift Left Logical
.text:00402474                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402478                 addu    $v0, $a1, $v0    # Add Unsigned
.text:0040247C                 lw      $v0, 8($v0)      # Load Word
.text:00402480                 srl     $v0, 19          # Shift Right Logical
.text:00402484                 or      $v1, $v0         # OR
.text:00402488                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040248C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402490                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402494                 sw      $v1, 8($v0)      # Store Word
; Found the 68th break (@00402498) ; new pc will be 004037ac
; ========================= BLOCK 68 =========================
.text:004037AC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004037B0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037B4                 sll     $v0, 2           # Shift Left Logical
.text:004037B8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037BC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004037C0                 lw      $v1, 8($v0)      # Load Word
.text:004037C4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037C8                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004037CC                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004037D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037D4                 sll     $v0, 2           # Shift Left Logical
.text:004037D8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037DC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004037E0                 lw      $a1, 8($v0)      # Load Word
.text:004037E4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037E8                 nor     $v0, $zero, $v0  # NOR
.text:004037EC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004037F0                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004037F4                 or      $v1, $v0         # OR
.text:004037F8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004037FC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403800                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403804                 sw      $v1, 8($v0)      # Store Word
; Found the 69th break (@00403808) ; new pc will be 00402b08
; ========================= BLOCK 69 =========================
.text:00402B08                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402B0C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402B10                 sll     $v0, 2           # Shift Left Logical
.text:00402B14                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B18                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402B1C                 lw      $v0, 8($v0)      # Load Word
.text:00402B20                 srl     $v1, $v0, 26     # Shift Right Logical
.text:00402B24                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402B28                 sll     $v0, 2           # Shift Left Logical
.text:00402B2C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B30                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402B34                 lw      $v0, 8($v0)      # Load Word
.text:00402B38                 sll     $v0, 6           # Shift Left Logical
.text:00402B3C                 or      $v1, $v0         # OR
.text:00402B40                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402B44                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B48                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B4C                 sw      $v1, 8($v0)      # Store Word
; Found the 70th break (@00402b50) ; new pc will be 0040372c
; ========================= BLOCK 70 =========================
.text:0040372C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403730                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403734                 sll     $v0, 2           # Shift Left Logical
.text:00403738                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040373C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403740                 lw      $v0, 8($v0)      # Load Word
.text:00403744                 sll     $v1, $v0, 5      # Shift Left Logical
.text:00403748                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040374C                 sll     $v0, 2           # Shift Left Logical
.text:00403750                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403754                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403758                 lw      $v0, 8($v0)      # Load Word
.text:0040375C                 srl     $v0, 27          # Shift Right Logical
.text:00403760                 or      $v1, $v0         # OR
.text:00403764                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403768                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040376C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403770                 sw      $v1, 8($v0)      # Store Word
; Found the 71th break (@00403774) ; new pc will be 00403444
; ========================= BLOCK 71 =========================
.text:00403444                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403448                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040344C                 sll     $v0, 2           # Shift Left Logical
.text:00403450                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403454                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403458                 lw      $v1, 8($v0)      # Load Word
.text:0040345C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403460                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403464                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403468                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040346C                 sll     $v0, 2           # Shift Left Logical
.text:00403470                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403474                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403478                 lw      $a1, 8($v0)      # Load Word
.text:0040347C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403480                 nor     $v0, $zero, $v0  # NOR
.text:00403484                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403488                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040348C                 or      $v1, $v0         # OR
.text:00403490                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403494                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403498                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040349C                 sw      $v1, 8($v0)      # Store Word
; Found the 72th break (@004034a0) ; new pc will be 00403694
; ========================= BLOCK 72 =========================
.text:00403694                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403698                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040369C                 sll     $v0, 2           # Shift Left Logical
.text:004036A0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036A4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004036A8                 lw      $v0, 8($v0)      # Load Word
.text:004036AC                 sll     $v1, $v0, 6      # Shift Left Logical
.text:004036B0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004036B4                 sll     $v0, 2           # Shift Left Logical
.text:004036B8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036BC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004036C0                 lw      $v0, 8($v0)      # Load Word
.text:004036C4                 srl     $v0, 26          # Shift Right Logical
.text:004036C8                 or      $v1, $v0         # OR
.text:004036CC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004036D0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036D4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004036D8                 sw      $v1, 8($v0)      # Store Word
; Found the 73th break (@004036dc) ; new pc will be 00403858
; ========================= BLOCK 73 =========================
.text:00403858                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040385C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403860                 sll     $v0, 2           # Shift Left Logical
.text:00403864                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403868                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040386C                 lw      $v0, 8($v0)      # Load Word
.text:00403870                 nor     $v1, $zero, $v0  # NOR
.text:00403874                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403878                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040387C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403880                 sw      $v1, 8($v0)      # Store Word
; Found the 74th break (@00403884) ; new pc will be 0040249c
; ========================= BLOCK 74 =========================
.text:0040249C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004024A0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024A4                 sll     $v0, 2           # Shift Left Logical
.text:004024A8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024AC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004024B0                 lw      $v0, 8($v0)      # Load Word
.text:004024B4                 nor     $v1, $zero, $v0  # NOR
.text:004024B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004024BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004024C4                 sw      $v1, 8($v0)      # Store Word
; Found the 75th break (@004024c8) ; new pc will be 00402d44
; ========================= BLOCK 75 =========================
.text:00402D44                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D48                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D4C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D50                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D54                 lw      $a0, 8($v0)      # Load Word
.text:00402D58                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402D5C                 addu    $a0, $v0         # Add Unsigned
.text:00402D60                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D64                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D68                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402D6C                 sw      $a0, 8($v0)      # Store Word
; Found the 76th break (@00402d70) ; new pc will be 004026b4
; ========================= BLOCK 76 =========================
.text:004026B4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004026B8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026BC                 sll     $v0, 2           # Shift Left Logical
.text:004026C0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026C4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004026C8                 lw      $v1, 8($v0)      # Load Word
.text:004026CC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026D0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004026D4                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004026D8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026DC                 sll     $v0, 2           # Shift Left Logical
.text:004026E0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026E4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004026E8                 lw      $a1, 8($v0)      # Load Word
.text:004026EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026F0                 nor     $v0, $zero, $v0  # NOR
.text:004026F4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004026F8                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004026FC                 or      $v1, $v0         # OR
.text:00402700                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402704                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402708                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040270C                 sw      $v1, 8($v0)      # Store Word
; Found the 77th break (@00402710) ; new pc will be 00402bb8
; ========================= BLOCK 77 =========================
.text:00402BB8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402BBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BC0                 sll     $v0, 2           # Shift Left Logical
.text:00402BC4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402BCC                 lw      $v0, 8($v0)      # Load Word
.text:00402BD0                 srl     $v1, $v0, 21     # Shift Right Logical
.text:00402BD4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BD8                 sll     $v0, 2           # Shift Left Logical
.text:00402BDC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BE0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402BE4                 lw      $v0, 8($v0)      # Load Word
.text:00402BE8                 sll     $v0, 11          # Shift Left Logical
.text:00402BEC                 or      $v1, $v0         # OR
.text:00402BF0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402BF4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BF8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402BFC                 sw      $v1, 8($v0)      # Store Word
; Found the 78th break (@00402c00) ; new pc will be 00403174
; ========================= BLOCK 78 =========================
.text:00403174                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403178                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040317C                 sll     $v0, 2           # Shift Left Logical
.text:00403180                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403184                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403188                 lw      $v1, 8($v0)      # Load Word
.text:0040318C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403190                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403194                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403198                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040319C                 sll     $v0, 2           # Shift Left Logical
.text:004031A0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031A4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004031A8                 lw      $a1, 8($v0)      # Load Word
.text:004031AC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004031B0                 nor     $v0, $zero, $v0  # NOR
.text:004031B4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004031B8                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:004031BC                 or      $v1, $v0         # OR
.text:004031C0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004031C4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031C8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004031CC                 sw      $v1, 8($v0)      # Store Word
; Found the 79th break (@004031d0) ; new pc will be 004029c8
; ========================= BLOCK 79 =========================
.text:004029C8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004029CC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029D0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029D4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004029D8                 lw      $a0, 8($v0)      # Load Word
.text:004029DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004029E0                 xor     $a0, $v0         # Exclusive OR
.text:004029E4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029E8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029EC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004029F0                 sw      $a0, 8($v0)      # Store Word
; Found the 80th break (@004029f4) ; new pc will be 00402f38
; ========================= BLOCK 80 =========================
.text:00402F38                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402F3C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F40                 sll     $v0, 2           # Shift Left Logical
.text:00402F44                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F48                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F4C                 lw      $v0, 8($v0)      # Load Word
.text:00402F50                 nor     $v1, $zero, $v0  # NOR
.text:00402F54                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402F58                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F5C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402F60                 sw      $v1, 8($v0)      # Store Word
; Found the 81th break (@00402f64) ; new pc will be 00402518
; ========================= BLOCK 81 =========================
.text:00402518                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040251C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402520                 sll     $v0, 2           # Shift Left Logical
.text:00402524                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402528                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040252C                 lw      $v0, 8($v0)      # Load Word
.text:00402530                 nor     $v1, $zero, $v0  # NOR
.text:00402534                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402538                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040253C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402540                 sw      $v1, 8($v0)      # Store Word
; Found the 82th break (@00402544) ; new pc will be 00402a2c
; ========================= BLOCK 82 =========================
.text:00402A2C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402A30                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A34                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A38                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402A3C                 lw      $a0, 8($v0)      # Load Word
.text:00402A40                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A44                 subu    $a0, $v0         # Subtract Unsigned
.text:00402A48                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A4C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A50                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A54                 sw      $a0, 8($v0)      # Store Word
; Found the 83th break (@00402a58) ; new pc will be 0040301c
; ========================= BLOCK 83 =========================
.text:0040301C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403020                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403024                 sll     $v0, 2           # Shift Left Logical
.text:00403028                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040302C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403030                 lw      $v0, 8($v0)      # Load Word
.text:00403034                 srl     $v1, $v0, 8      # Shift Right Logical
.text:00403038                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040303C                 sll     $v0, 2           # Shift Left Logical
.text:00403040                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403044                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403048                 lw      $v0, 8($v0)      # Load Word
.text:0040304C                 sll     $v0, 24          # Shift Left Logical
.text:00403050                 or      $v1, $v0         # OR
.text:00403054                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403058                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040305C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403060                 sw      $v1, 8($v0)      # Store Word
; Found the 84th break (@00403064) ; new pc will be 004024cc
; ========================= BLOCK 84 =========================
.text:004024CC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004024D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024D4                 sll     $v0, 2           # Shift Left Logical
.text:004024D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004024E0                 lw      $v0, 8($v0)      # Load Word
.text:004024E4                 sll     $v1, $v0, 30     # Shift Left Logical
.text:004024E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024EC                 sll     $v0, 2           # Shift Left Logical
.text:004024F0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024F4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004024F8                 lw      $v0, 8($v0)      # Load Word
.text:004024FC                 srl     $v0, 2           # Shift Right Logical
.text:00402500                 or      $v1, $v0         # OR
.text:00402504                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402508                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040250C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402510                 sw      $v1, 8($v0)      # Store Word
; Found the 85th break (@00402514) ; new pc will be 004023f0
; ========================= BLOCK 85 =========================
.text:004023F0                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004023F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004023F8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023FC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402400                 lw      $a0, 8($v0)      # Load Word
.text:00402404                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402408                 addu    $a0, $v0         # Add Unsigned
.text:0040240C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402410                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402414                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402418                 sw      $a0, 8($v0)      # Store Word
; Found the 86th break (@0040241c) ; new pc will be 004025d8
; ========================= BLOCK 86 =========================
.text:004025D8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004025DC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025E8                 lw      $a0, 8($v0)      # Load Word
.text:004025EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004025F0                 addu    $a0, $v0         # Add Unsigned
.text:004025F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025F8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025FC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402600                 sw      $a0, 8($v0)      # Store Word
; Found the 87th break (@00402604) ; new pc will be 00402370
; ========================= BLOCK 87 =========================
.text:00402370                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402374                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402378                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040237C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402380                 lw      $a0, 8($v0)      # Load Word
.text:00402384                 li      $v0, 0x87DD2BC5  # Load Immediate
.text:0040238C                 addu    $a0, $v0         # Add Unsigned
.text:00402390                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402394                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402398                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040239C                 sw      $a0, 8($v0)      # Store Word
; Found the 88th break (@004023a0) ; new pc will be 00402964
; ========================= BLOCK 88 =========================
.text:00402964                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402968                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040296C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402970                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402974                 lw      $a0, 8($v0)      # Load Word
.text:00402978                 li      $v0, 0x737F298   # Load Immediate
.text:00402980                 addu    $a0, $v0         # Add Unsigned
.text:00402984                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402988                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040298C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402990                 sw      $a0, 8($v0)      # Store Word
; Found the 89th break (@00402994) ; new pc will be 00402f68
; ========================= BLOCK 89 =========================
.text:00402F68                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402F6C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F70                 sll     $v0, 2           # Shift Left Logical
.text:00402F74                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F78                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F7C                 lw      $v0, 8($v0)      # Load Word
.text:00402F80                 sll     $v1, $v0, 23     # Shift Left Logical
.text:00402F84                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F88                 sll     $v0, 2           # Shift Left Logical
.text:00402F8C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F90                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402F94                 lw      $v0, 8($v0)      # Load Word
.text:00402F98                 srl     $v0, 9           # Shift Right Logical
.text:00402F9C                 or      $v1, $v0         # OR
.text:00402FA0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402FA4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FA8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FAC                 sw      $v1, 8($v0)      # Store Word
; Found the 90th break (@00402fb0) ; new pc will be 00403580
; ========================= BLOCK 90 =========================
.text:00403580                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403584                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403588                 sll     $v0, 2           # Shift Left Logical
.text:0040358C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403590                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403594                 lw      $v0, 8($v0)      # Load Word
.text:00403598                 sll     $v1, $v0, 28     # Shift Left Logical
.text:0040359C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004035A0                 sll     $v0, 2           # Shift Left Logical
.text:004035A4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035A8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004035AC                 lw      $v0, 8($v0)      # Load Word
.text:004035B0                 srl     $v0, 4           # Shift Right Logical
.text:004035B4                 or      $v1, $v0         # OR
.text:004035B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004035BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004035C4                 sw      $v1, 8($v0)      # Store Word
; Found the 91th break (@004035c8) ; new pc will be 00402900
; ========================= BLOCK 91 =========================
.text:00402900                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402904                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402908                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040290C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402910                 lw      $a0, 8($v0)      # Load Word
.text:00402914                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402918                 xor     $a0, $v0         # Exclusive OR
.text:0040291C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402920                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402924                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402928                 sw      $a0, 8($v0)      # Store Word
; Found the 92th break (@0040292c) ; new pc will be 00402654
; ========================= BLOCK 92 =========================
.text:00402654                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402658                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040265C                 sll     $v0, 2           # Shift Left Logical
.text:00402660                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402664                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402668                 lw      $v1, 8($v0)      # Load Word
.text:0040266C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402670                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00402674                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00402678                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040267C                 sll     $v0, 2           # Shift Left Logical
.text:00402680                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402684                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402688                 lw      $a1, 8($v0)      # Load Word
.text:0040268C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402690                 nor     $v0, $zero, $v0  # NOR
.text:00402694                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00402698                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040269C                 or      $v1, $v0         # OR
.text:004026A0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004026A4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026A8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004026AC                 sw      $v1, 8($v0)      # Store Word
; Found the 93th break (@004026b0) ; new pc will be 00403280
; ========================= BLOCK 93 =========================
.text:00403280                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403284                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403288                 sll     $v0, 2           # Shift Left Logical
.text:0040328C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403290                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403294                 lw      $v0, 8($v0)      # Load Word
.text:00403298                 sll     $v1, $v0, 29     # Shift Left Logical
.text:0040329C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004032A0                 sll     $v0, 2           # Shift Left Logical
.text:004032A4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032A8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004032AC                 lw      $v0, 8($v0)      # Load Word
.text:004032B0                 srl     $v0, 3           # Shift Right Logical
.text:004032B4                 or      $v1, $v0         # OR
.text:004032B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004032BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004032C4                 sw      $v1, 8($v0)      # Store Word
; Found the 94th break (@004032c8) ; new pc will be 004035cc
; ========================= BLOCK 94 =========================
.text:004035CC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004035D0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004035D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004035DC                 lw      $a0, 8($v0)      # Load Word
.text:004035E0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004035E4                 addu    $a0, $v0         # Add Unsigned
.text:004035E8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004035EC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035F0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004035F4                 sw      $a0, 8($v0)      # Store Word
; Found the 95th break (@004035f8) ; new pc will be 00402eb8
; ========================= BLOCK 95 =========================
.text:00402EB8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402EBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402EC0                 sll     $v0, 2           # Shift Left Logical
.text:00402EC4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402ECC                 lw      $v0, 8($v0)      # Load Word
.text:00402ED0                 sll     $v1, $v0, 18     # Shift Left Logical
.text:00402ED4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402ED8                 sll     $v0, 2           # Shift Left Logical
.text:00402EDC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EE0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402EE4                 lw      $v0, 8($v0)      # Load Word
.text:00402EE8                 srl     $v0, 14          # Shift Right Logical
.text:00402EEC                 or      $v1, $v0         # OR
.text:00402EF0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402EF4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EF8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402EFC                 sw      $v1, 8($v0)      # Store Word
; Found the 96th break (@00402f00) ; new pc will be 004032cc
; ========================= BLOCK 96 =========================
.text:004032CC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004032D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004032D4                 sll     $v0, 2           # Shift Left Logical
.text:004032D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004032E0                 lw      $v0, 8($v0)      # Load Word
.text:004032E4                 nor     $v1, $zero, $v0  # NOR
.text:004032E8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004032EC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032F0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004032F4                 sw      $v1, 8($v0)      # Store Word
; Found the 97th break (@004032f8) ; new pc will be 004022c0
; ========================= BLOCK 97 =========================
.text:004022C0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004022C4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022C8                 sll     $v0, 2           # Shift Left Logical
.text:004022CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004022D4                 lw      $v0, 8($v0)      # Load Word
.text:004022D8                 srl     $v1, $v0, 1      # Shift Right Logical
.text:004022DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022E0                 sll     $v0, 2           # Shift Left Logical
.text:004022E4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022E8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004022EC                 lw      $v0, 8($v0)      # Load Word
.text:004022F0                 sll     $v0, 31          # Shift Left Logical
.text:004022F4                 or      $v1, $v0         # OR
.text:004022F8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004022FC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402300                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402304                 sw      $v1, 8($v0)      # Store Word
; Found the 98th break (@00402308) ; new pc will be 00402548
; ========================= BLOCK 98 =========================
.text:00402548                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040254C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402550                 sll     $v0, 2           # Shift Left Logical
.text:00402554                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402558                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040255C                 lw      $v0, 8($v0)      # Load Word
.text:00402560                 nor     $v1, $zero, $v0  # NOR
.text:00402564                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402568                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040256C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402570                 sw      $v1, 8($v0)      # Store Word
; Found the 99th break (@00402574) ; new pc will be 0040391c
; ========================= BLOCK 99 =========================
.text:0040391C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403920                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403924                 sll     $v0, 2           # Shift Left Logical
.text:00403928                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040392C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403930                 lw      $v1, 8($v0)      # Load Word
.text:00403934                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403938                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040393C                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403940                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403944                 sll     $v0, 2           # Shift Left Logical
.text:00403948                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040394C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403950                 lw      $a1, 8($v0)      # Load Word
.text:00403954                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403958                 nor     $v0, $zero, $v0  # NOR
.text:0040395C                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403960                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:00403964                 or      $v1, $v0         # OR
.text:00403968                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040396C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403970                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403974                 sw      $v1, 8($v0)      # Store Word
; Found the 100th break (@00403978) ; new pc will be 004039dc
; ========================= BLOCK 100 =========================
.text:004039DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004039E0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004039E4                 sw      $v0, 0x48+i($fp)  # Store Word
; Found the 0th break (@0040228c) ; new pc will be 00402fe8
; ========================= BLOCK 0 =========================
.text:00402FE8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402FEC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FF0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FF4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FF8                 lw      $a0, 8($v0)      # Load Word
.text:00402FFC                 li      $v0, 0x38C1FEB8  # Load Immediate
.text:00403004                 xor     $a0, $v0         # Exclusive OR
.text:00403008                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040300C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403010                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403014                 sw      $a0, 8($v0)      # Store Word
; Found the 1th break (@00403018) ; new pc will be 00402808
; ========================= BLOCK 1 =========================
.text:00402808                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040280C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402810                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402814                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402818                 lw      $a0, 8($v0)      # Load Word
.text:0040281C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402820                 subu    $a0, $v0         # Subtract Unsigned
.text:00402824                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402828                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040282C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402830                 sw      $a0, 8($v0)      # Store Word
; Found the 2th break (@00402834) ; new pc will be 00402838
; ========================= BLOCK 2 =========================
.text:00402838                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040283C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402840                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402844                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402848                 lw      $a0, 8($v0)      # Load Word
.text:0040284C                 li      $v0, 0xB65E867F  # Load Immediate
.text:00402854                 addu    $a0, $v0         # Add Unsigned
.text:00402858                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040285C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402860                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402864                 sw      $a0, 8($v0)      # Store Word
; Found the 3th break (@00402868) ; new pc will be 00403378
; ========================= BLOCK 3 =========================
.text:00403378                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040337C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403380                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403384                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403388                 lw      $a0, 8($v0)      # Load Word
.text:0040338C                 li      $v0, 0xBFD991A0  # Load Immediate
.text:00403394                 xor     $a0, $v0         # Exclusive OR
.text:00403398                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040339C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004033A4                 sw      $a0, 8($v0)      # Store Word
; Found the 4th break (@004033a8) ; new pc will be 004030e4
; ========================= BLOCK 4 =========================
.text:004030E4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004030E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030EC                 sll     $v0, 2           # Shift Left Logical
.text:004030F0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004030F8                 lw      $v1, 8($v0)      # Load Word
.text:004030FC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403100                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403104                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403108                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040310C                 sll     $v0, 2           # Shift Left Logical
.text:00403110                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403114                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403118                 lw      $a1, 8($v0)      # Load Word
.text:0040311C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403120                 nor     $v0, $zero, $v0  # NOR
.text:00403124                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403128                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040312C                 or      $v1, $v0         # OR
.text:00403130                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403134                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403138                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040313C                 sw      $v1, 8($v0)      # Store Word
; Found the 5th break (@00403140) ; new pc will be 00402370
; ========================= BLOCK 5 =========================
.text:00402370                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402374                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402378                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040237C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402380                 lw      $a0, 8($v0)      # Load Word
.text:00402384                 li      $v0, 0x87DD2BC5  # Load Immediate
.text:0040238C                 addu    $a0, $v0         # Add Unsigned
.text:00402390                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402394                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402398                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040239C                 sw      $a0, 8($v0)      # Store Word
; Found the 6th break (@004023a0) ; new pc will be 00402f04
; ========================= BLOCK 6 =========================
.text:00402F04                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402F08                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402F0C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F10                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402F14                 lw      $a0, 8($v0)      # Load Word
.text:00402F18                 li      $v0, 0x3ECA6F23  # Load Immediate
.text:00402F20                 addu    $a0, $v0         # Add Unsigned
.text:00402F24                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402F28                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F2C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F30                 sw      $a0, 8($v0)      # Store Word
; Found the 7th break (@00402f34) ; new pc will be 00402dd8
; ========================= BLOCK 7 =========================
.text:00402DD8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402DDC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DE0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DE4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402DE8                 lw      $a0, 8($v0)      # Load Word
.text:00402DEC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402DF0                 subu    $a0, $v0         # Subtract Unsigned
.text:00402DF4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DF8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DFC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E00                 sw      $a0, 8($v0)      # Store Word
; Found the 8th break (@00402e04) ; new pc will be 0040249c
; ========================= BLOCK 8 =========================
.text:0040249C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004024A0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024A4                 sll     $v0, 2           # Shift Left Logical
.text:004024A8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024AC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004024B0                 lw      $v0, 8($v0)      # Load Word
.text:004024B4                 nor     $v1, $zero, $v0  # NOR
.text:004024B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004024BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004024C4                 sw      $v1, 8($v0)      # Store Word
; Found the 9th break (@004024c8) ; new pc will be 00402964
; ========================= BLOCK 9 =========================
.text:00402964                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402968                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040296C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402970                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402974                 lw      $a0, 8($v0)      # Load Word
.text:00402978                 li      $v0, 0x737F298   # Load Immediate
.text:00402980                 addu    $a0, $v0         # Add Unsigned
.text:00402984                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402988                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040298C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402990                 sw      $a0, 8($v0)      # Store Word
; Found the 10th break (@00402994) ; new pc will be 0040286c
; ========================= BLOCK 10 =========================
.text:0040286C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402870                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402874                 sll     $v0, 2           # Shift Left Logical
.text:00402878                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040287C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402880                 lw      $v1, 8($v0)      # Load Word
.text:00402884                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402888                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040288C                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00402890                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402894                 sll     $v0, 2           # Shift Left Logical
.text:00402898                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040289C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004028A0                 lw      $a1, 8($v0)      # Load Word
.text:004028A4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004028A8                 nor     $v0, $zero, $v0  # NOR
.text:004028AC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004028B0                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004028B4                 or      $v1, $v0         # OR
.text:004028B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004028BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004028C4                 sw      $v1, 8($v0)      # Store Word
; Found the 11th break (@004028c8) ; new pc will be 004037ac
; ========================= BLOCK 11 =========================
.text:004037AC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004037B0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037B4                 sll     $v0, 2           # Shift Left Logical
.text:004037B8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037BC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004037C0                 lw      $v1, 8($v0)      # Load Word
.text:004037C4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037C8                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004037CC                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004037D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037D4                 sll     $v0, 2           # Shift Left Logical
.text:004037D8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037DC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004037E0                 lw      $a1, 8($v0)      # Load Word
.text:004037E4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037E8                 nor     $v0, $zero, $v0  # NOR
.text:004037EC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004037F0                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004037F4                 or      $v1, $v0         # OR
.text:004037F8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004037FC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403800                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403804                 sw      $v1, 8($v0)      # Store Word
; Found the 12th break (@00403808) ; new pc will be 0040301c
; ========================= BLOCK 12 =========================
.text:0040301C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403020                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403024                 sll     $v0, 2           # Shift Left Logical
.text:00403028                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040302C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403030                 lw      $v0, 8($v0)      # Load Word
.text:00403034                 srl     $v1, $v0, 8      # Shift Right Logical
.text:00403038                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040303C                 sll     $v0, 2           # Shift Left Logical
.text:00403040                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403044                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403048                 lw      $v0, 8($v0)      # Load Word
.text:0040304C                 sll     $v0, 24          # Shift Left Logical
.text:00403050                 or      $v1, $v0         # OR
.text:00403054                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403058                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040305C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403060                 sw      $v1, 8($v0)      # Store Word
; Found the 13th break (@00403064) ; new pc will be 00402744
; ========================= BLOCK 13 =========================
.text:00402744                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402748                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040274C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402750                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402754                 lw      $a0, 8($v0)      # Load Word
.text:00402758                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040275C                 subu    $a0, $v0         # Subtract Unsigned
.text:00402760                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402764                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402768                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040276C                 sw      $a0, 8($v0)      # Store Word
; Found the 14th break (@00402770) ; new pc will be 004034a4
; ========================= BLOCK 14 =========================
.text:004034A4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004034A8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004034AC                 sll     $v0, 2           # Shift Left Logical
.text:004034B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004034B8                 lw      $v0, 8($v0)      # Load Word
.text:004034BC                 srl     $v1, $v0, 17     # Shift Right Logical
.text:004034C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004034C4                 sll     $v0, 2           # Shift Left Logical
.text:004034C8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034CC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004034D0                 lw      $v0, 8($v0)      # Load Word
.text:004034D4                 sll     $v0, 15          # Shift Left Logical
.text:004034D8                 or      $v1, $v0         # OR
.text:004034DC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004034E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004034E8                 sw      $v1, 8($v0)      # Store Word
; Found the 15th break (@004034ec) ; new pc will be 004032fc
; ========================= BLOCK 15 =========================
.text:004032FC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403300                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403304                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403308                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040330C                 lw      $a0, 8($v0)      # Load Word
.text:00403310                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403314                 xor     $a0, $v0         # Exclusive OR
.text:00403318                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040331C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403320                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403324                 sw      $a0, 8($v0)      # Store Word
; Found the 16th break (@00403328) ; new pc will be 00403630
; ========================= BLOCK 16 =========================
.text:00403630                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403634                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403638                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040363C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403640                 lw      $a0, 8($v0)      # Load Word
.text:00403644                 li      $v0, 0x3D68A35C  # Load Immediate
.text:0040364C                 xor     $a0, $v0         # Exclusive OR
.text:00403650                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403654                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403658                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040365C                 sw      $a0, 8($v0)      # Store Word
; Found the 17th break (@00403660) ; new pc will be 004027d8
; ========================= BLOCK 17 =========================
.text:004027D8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004027DC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004027E8                 lw      $a0, 8($v0)      # Load Word
.text:004027EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004027F0                 subu    $a0, $v0         # Subtract Unsigned
.text:004027F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027F8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027FC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402800                 sw      $a0, 8($v0)      # Store Word
; Found the 18th break (@00402804) ; new pc will be 00402aa8
; ========================= BLOCK 18 =========================
.text:00402AA8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402AAC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402AB0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AB4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402AB8                 lw      $a0, 8($v0)      # Load Word
.text:00402ABC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402AC0                 xor     $a0, $v0         # Exclusive OR
.text:00402AC4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402AC8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402ACC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402AD0                 sw      $a0, 8($v0)      # Store Word
; Found the 19th break (@00402ad4) ; new pc will be 00402f38
; ========================= BLOCK 19 =========================
.text:00402F38                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402F3C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F40                 sll     $v0, 2           # Shift Left Logical
.text:00402F44                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F48                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F4C                 lw      $v0, 8($v0)      # Load Word
.text:00402F50                 nor     $v1, $zero, $v0  # NOR
.text:00402F54                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402F58                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F5C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402F60                 sw      $v1, 8($v0)      # Store Word
; Found the 20th break (@00402f64) ; new pc will be 00402774
; ========================= BLOCK 20 =========================
.text:00402774                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402778                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040277C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402780                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402784                 lw      $a0, 8($v0)      # Load Word
.text:00402788                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040278C                 xor     $a0, $v0         # Exclusive OR
.text:00402790                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402794                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402798                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040279C                 sw      $a0, 8($v0)      # Store Word
; Found the 21th break (@004027a0) ; new pc will be 0040372c
; ========================= BLOCK 21 =========================
.text:0040372C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403730                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403734                 sll     $v0, 2           # Shift Left Logical
.text:00403738                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040373C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403740                 lw      $v0, 8($v0)      # Load Word
.text:00403744                 sll     $v1, $v0, 5      # Shift Left Logical
.text:00403748                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040374C                 sll     $v0, 2           # Shift Left Logical
.text:00403750                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403754                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403758                 lw      $v0, 8($v0)      # Load Word
.text:0040375C                 srl     $v0, 27          # Shift Right Logical
.text:00403760                 or      $v1, $v0         # OR
.text:00403764                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403768                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040376C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403770                 sw      $v1, 8($v0)      # Store Word
; Found the 22th break (@00403774) ; new pc will be 004036e0
; ========================= BLOCK 22 =========================
.text:004036E0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004036E4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004036E8                 sll     $v0, 2           # Shift Left Logical
.text:004036EC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036F0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004036F4                 lw      $v0, 8($v0)      # Load Word
.text:004036F8                 sll     $v1, $v0, 5      # Shift Left Logical
.text:004036FC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403700                 sll     $v0, 2           # Shift Left Logical
.text:00403704                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403708                 addu    $v0, $a1, $v0    # Add Unsigned
.text:0040370C                 lw      $v0, 8($v0)      # Load Word
.text:00403710                 srl     $v0, 27          # Shift Right Logical
.text:00403714                 or      $v1, $v0         # OR
.text:00403718                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040371C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403720                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403724                 sw      $v1, 8($v0)      # Store Word
; Found the 23th break (@00403728) ; new pc will be 00402b88
; ========================= BLOCK 23 =========================
.text:00402B88                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402B8C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B90                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B94                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B98                 lw      $a0, 8($v0)      # Load Word
.text:00402B9C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BA0                 subu    $a0, $v0         # Subtract Unsigned
.text:00402BA4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402BA8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402BB0                 sw      $a0, 8($v0)      # Store Word
; Found the 24th break (@00402bb4) ; new pc will be 004023f0
; ========================= BLOCK 24 =========================
.text:004023F0                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004023F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004023F8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023FC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402400                 lw      $a0, 8($v0)      # Load Word
.text:00402404                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402408                 addu    $a0, $v0         # Add Unsigned
.text:0040240C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402410                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402414                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402418                 sw      $a0, 8($v0)      # Store Word
; Found the 25th break (@0040241c) ; new pc will be 004026b4
; ========================= BLOCK 25 =========================
.text:004026B4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004026B8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026BC                 sll     $v0, 2           # Shift Left Logical
.text:004026C0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026C4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004026C8                 lw      $v1, 8($v0)      # Load Word
.text:004026CC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026D0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004026D4                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004026D8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026DC                 sll     $v0, 2           # Shift Left Logical
.text:004026E0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026E4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004026E8                 lw      $a1, 8($v0)      # Load Word
.text:004026EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026F0                 nor     $v0, $zero, $v0  # NOR
.text:004026F4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004026F8                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004026FC                 or      $v1, $v0         # OR
.text:00402700                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402704                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402708                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040270C                 sw      $v1, 8($v0)      # Store Word
; Found the 26th break (@00402710) ; new pc will be 00403234
; ========================= BLOCK 26 =========================
.text:00403234                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403238                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040323C                 sll     $v0, 2           # Shift Left Logical
.text:00403240                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403244                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403248                 lw      $v0, 8($v0)      # Load Word
.text:0040324C                 sll     $v1, $v0, 29     # Shift Left Logical
.text:00403250                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403254                 sll     $v0, 2           # Shift Left Logical
.text:00403258                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040325C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403260                 lw      $v0, 8($v0)      # Load Word
.text:00403264                 srl     $v0, 3           # Shift Right Logical
.text:00403268                 or      $v1, $v0         # OR
.text:0040326C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403270                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403274                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403278                 sw      $v1, 8($v0)      # Store Word
; Found the 27th break (@0040327c) ; new pc will be 00403174
; ========================= BLOCK 27 =========================
.text:00403174                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403178                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040317C                 sll     $v0, 2           # Shift Left Logical
.text:00403180                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403184                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403188                 lw      $v1, 8($v0)      # Load Word
.text:0040318C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403190                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403194                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403198                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040319C                 sll     $v0, 2           # Shift Left Logical
.text:004031A0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031A4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004031A8                 lw      $a1, 8($v0)      # Load Word
.text:004031AC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004031B0                 nor     $v0, $zero, $v0  # NOR
.text:004031B4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004031B8                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:004031BC                 or      $v1, $v0         # OR
.text:004031C0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004031C4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031C8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004031CC                 sw      $v1, 8($v0)      # Store Word
; Found the 28th break (@004031d0) ; new pc will be 00402654
; ========================= BLOCK 28 =========================
.text:00402654                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402658                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040265C                 sll     $v0, 2           # Shift Left Logical
.text:00402660                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402664                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402668                 lw      $v1, 8($v0)      # Load Word
.text:0040266C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402670                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00402674                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00402678                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040267C                 sll     $v0, 2           # Shift Left Logical
.text:00402680                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402684                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402688                 lw      $a1, 8($v0)      # Load Word
.text:0040268C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402690                 nor     $v0, $zero, $v0  # NOR
.text:00402694                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00402698                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040269C                 or      $v1, $v0         # OR
.text:004026A0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004026A4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026A8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004026AC                 sw      $v1, 8($v0)      # Store Word
; Found the 29th break (@004026b0) ; new pc will be 00402b54
; ========================= BLOCK 29 =========================
.text:00402B54                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402B58                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B5C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B60                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B64                 lw      $a0, 8($v0)      # Load Word
.text:00402B68                 li      $v0, 0x79662B5D  # Load Immediate
.text:00402B70                 addu    $a0, $v0         # Add Unsigned
.text:00402B74                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B78                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B7C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402B80                 sw      $a0, 8($v0)      # Store Word
; Found the 30th break (@00402b84) ; new pc will be 00403444
; ========================= BLOCK 30 =========================
.text:00403444                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403448                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040344C                 sll     $v0, 2           # Shift Left Logical
.text:00403450                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403454                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403458                 lw      $v1, 8($v0)      # Load Word
.text:0040345C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403460                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403464                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403468                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040346C                 sll     $v0, 2           # Shift Left Logical
.text:00403470                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403474                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403478                 lw      $a1, 8($v0)      # Load Word
.text:0040347C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403480                 nor     $v0, $zero, $v0  # NOR
.text:00403484                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403488                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040348C                 or      $v1, $v0         # OR
.text:00403490                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403494                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403498                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040349C                 sw      $v1, 8($v0)      # Store Word
; Found the 31th break (@004034a0) ; new pc will be 00402bb8
; ========================= BLOCK 31 =========================
.text:00402BB8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402BBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BC0                 sll     $v0, 2           # Shift Left Logical
.text:00402BC4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402BCC                 lw      $v0, 8($v0)      # Load Word
.text:00402BD0                 srl     $v1, $v0, 21     # Shift Right Logical
.text:00402BD4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BD8                 sll     $v0, 2           # Shift Left Logical
.text:00402BDC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BE0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402BE4                 lw      $v0, 8($v0)      # Load Word
.text:00402BE8                 sll     $v0, 11          # Shift Left Logical
.text:00402BEC                 or      $v1, $v0         # OR
.text:00402BF0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402BF4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BF8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402BFC                 sw      $v1, 8($v0)      # Store Word
; Found the 32th break (@00402c00) ; new pc will be 00402b08
; ========================= BLOCK 32 =========================
.text:00402B08                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402B0C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402B10                 sll     $v0, 2           # Shift Left Logical
.text:00402B14                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B18                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402B1C                 lw      $v0, 8($v0)      # Load Word
.text:00402B20                 srl     $v1, $v0, 26     # Shift Right Logical
.text:00402B24                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402B28                 sll     $v0, 2           # Shift Left Logical
.text:00402B2C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B30                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402B34                 lw      $v0, 8($v0)      # Load Word
.text:00402B38                 sll     $v0, 6           # Shift Left Logical
.text:00402B3C                 or      $v1, $v0         # OR
.text:00402B40                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402B44                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B48                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B4C                 sw      $v1, 8($v0)      # Store Word
; Found the 33th break (@00402b50) ; new pc will be 00402998
; ========================= BLOCK 33 =========================
.text:00402998                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040299C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029A0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029A4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004029A8                 lw      $a0, 8($v0)      # Load Word
.text:004029AC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004029B0                 subu    $a0, $v0         # Subtract Unsigned
.text:004029B4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029B8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029BC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004029C0                 sw      $a0, 8($v0)      # Store Word
; Found the 34th break (@004029c4) ; new pc will be 00403694
; ========================= BLOCK 34 =========================
.text:00403694                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403698                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040369C                 sll     $v0, 2           # Shift Left Logical
.text:004036A0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036A4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004036A8                 lw      $v0, 8($v0)      # Load Word
.text:004036AC                 sll     $v1, $v0, 6      # Shift Left Logical
.text:004036B0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004036B4                 sll     $v0, 2           # Shift Left Logical
.text:004036B8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036BC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004036C0                 lw      $v0, 8($v0)      # Load Word
.text:004036C4                 srl     $v0, 26          # Shift Right Logical
.text:004036C8                 or      $v1, $v0         # OR
.text:004036CC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004036D0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036D4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004036D8                 sw      $v1, 8($v0)      # Store Word
; Found the 35th break (@004036dc) ; new pc will be 004035cc
; ========================= BLOCK 35 =========================
.text:004035CC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004035D0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004035D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004035DC                 lw      $a0, 8($v0)      # Load Word
.text:004035E0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004035E4                 addu    $a0, $v0         # Add Unsigned
.text:004035E8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004035EC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035F0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004035F4                 sw      $a0, 8($v0)      # Store Word
; Found the 36th break (@004035f8) ; new pc will be 0040391c
; ========================= BLOCK 36 =========================
.text:0040391C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403920                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403924                 sll     $v0, 2           # Shift Left Logical
.text:00403928                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040392C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403930                 lw      $v1, 8($v0)      # Load Word
.text:00403934                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403938                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040393C                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403940                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403944                 sll     $v0, 2           # Shift Left Logical
.text:00403948                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040394C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403950                 lw      $a1, 8($v0)      # Load Word
.text:00403954                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403958                 nor     $v0, $zero, $v0  # NOR
.text:0040395C                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403960                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:00403964                 or      $v1, $v0         # OR
.text:00403968                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040396C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403970                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403974                 sw      $v1, 8($v0)      # Store Word
; Found the 37th break (@00403978) ; new pc will be 00402a5c
; ========================= BLOCK 37 =========================
.text:00402A5C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402A60                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A64                 sll     $v0, 2           # Shift Left Logical
.text:00402A68                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A6C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A70                 lw      $v0, 8($v0)      # Load Word
.text:00402A74                 srl     $v1, $v0, 13     # Shift Right Logical
.text:00402A78                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A7C                 sll     $v0, 2           # Shift Left Logical
.text:00402A80                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A84                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402A88                 lw      $v0, 8($v0)      # Load Word
.text:00402A8C                 sll     $v0, 19          # Shift Left Logical
.text:00402A90                 or      $v1, $v0         # OR
.text:00402A94                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402A98                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A9C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402AA0                 sw      $v1, 8($v0)      # Store Word
; Found the 38th break (@00402aa4) ; new pc will be 00402eb8
; ========================= BLOCK 38 =========================
.text:00402EB8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402EBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402EC0                 sll     $v0, 2           # Shift Left Logical
.text:00402EC4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402ECC                 lw      $v0, 8($v0)      # Load Word
.text:00402ED0                 sll     $v1, $v0, 18     # Shift Left Logical
.text:00402ED4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402ED8                 sll     $v0, 2           # Shift Left Logical
.text:00402EDC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EE0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402EE4                 lw      $v0, 8($v0)      # Load Word
.text:00402EE8                 srl     $v0, 14          # Shift Right Logical
.text:00402EEC                 or      $v1, $v0         # OR
.text:00402EF0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402EF4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EF8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402EFC                 sw      $v1, 8($v0)      # Store Word
; Found the 39th break (@00402f00) ; new pc will be 00402e08
; ========================= BLOCK 39 =========================
.text:00402E08                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402E0C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E10                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E14                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E18                 lw      $a0, 8($v0)      # Load Word
.text:00402E1C                 li      $v0, 0x73C69F47  # Load Immediate
.text:00402E24                 addu    $a0, $v0         # Add Unsigned
.text:00402E28                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E2C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E30                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E34                 sw      $a0, 8($v0)      # Store Word
; Found the 40th break (@00402e38) ; new pc will be 004035fc
; ========================= BLOCK 40 =========================
.text:004035FC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403600                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403604                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403608                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040360C                 lw      $a0, 8($v0)      # Load Word
.text:00403610                 li      $v0, 0x8103D046  # Load Immediate
.text:00403618                 xor     $a0, $v0         # Exclusive OR
.text:0040361C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403620                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403624                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403628                 sw      $a0, 8($v0)      # Store Word
; Found the 41th break (@0040362c) ; new pc will be 004025d8
; ========================= BLOCK 41 =========================
.text:004025D8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004025DC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025E8                 lw      $a0, 8($v0)      # Load Word
.text:004025EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004025F0                 addu    $a0, $v0         # Add Unsigned
.text:004025F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025F8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025FC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402600                 sw      $a0, 8($v0)      # Store Word
; Found the 42th break (@00402604) ; new pc will be 00402ad8
; ========================= BLOCK 42 =========================
.text:00402AD8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402ADC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402AE0                 sll     $v0, 2           # Shift Left Logical
.text:00402AE4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AE8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402AEC                 lw      $v0, 8($v0)      # Load Word
.text:00402AF0                 nor     $v1, $zero, $v0  # NOR
.text:00402AF4                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402AF8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AFC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B00                 sw      $v1, 8($v0)      # Store Word
; Found the 43th break (@00402b04) ; new pc will be 004034f0
; ========================= BLOCK 43 =========================
.text:004034F0                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004034F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004034F8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034FC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403500                 lw      $a0, 8($v0)      # Load Word
.text:00403504                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403508                 addu    $a0, $v0         # Add Unsigned
.text:0040350C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403510                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403514                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403518                 sw      $a0, 8($v0)      # Store Word
; Found the 44th break (@0040351c) ; new pc will be 00403410
; ========================= BLOCK 44 =========================
.text:00403410                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403414                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403418                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040341C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403420                 lw      $a0, 8($v0)      # Load Word
.text:00403424                 li      $v0, 0x192B37D2  # Load Immediate
.text:0040342C                 addu    $a0, $v0         # Add Unsigned
.text:00403430                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403434                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403438                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040343C                 sw      $a0, 8($v0)      # Store Word
; Found the 45th break (@00403440) ; new pc will be 004038b8
; ========================= BLOCK 45 =========================
.text:004038B8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004038BC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038C0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038C4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038C8                 lw      $a0, 8($v0)      # Load Word
.text:004038CC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004038D0                 subu    $a0, $v0         # Subtract Unsigned
.text:004038D4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004038E0                 sw      $a0, 8($v0)      # Store Word
; Found the 46th break (@004038e4) ; new pc will be 00402290
; ========================= BLOCK 46 =========================
.text:00402290                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402294                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402298                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040229C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004022A0                 lw      $a0, 8($v0)      # Load Word
.text:004022A4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022A8                 subu    $a0, $v0         # Subtract Unsigned
.text:004022AC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004022B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004022B8                 sw      $a0, 8($v0)      # Store Word
; Found the 47th break (@004022bc) ; new pc will be 0040332c
; ========================= BLOCK 47 =========================
.text:0040332C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403330                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403334                 sll     $v0, 2           # Shift Left Logical
.text:00403338                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040333C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403340                 lw      $v0, 8($v0)      # Load Word
.text:00403344                 sll     $v1, $v0, 31     # Shift Left Logical
.text:00403348                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040334C                 sll     $v0, 2           # Shift Left Logical
.text:00403350                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403354                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403358                 lw      $v0, 8($v0)      # Load Word
.text:0040335C                 srl     $v0, 1           # Shift Right Logical
.text:00403360                 or      $v1, $v0         # OR
.text:00403364                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403368                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040336C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403370                 sw      $v1, 8($v0)      # Store Word
; Found the 48th break (@00403374) ; new pc will be 00402da8
; ========================= BLOCK 48 =========================
.text:00402DA8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402DAC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DB0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DB4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402DB8                 lw      $a0, 8($v0)      # Load Word
.text:00402DBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402DC0                 xor     $a0, $v0         # Exclusive OR
.text:00402DC4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DC8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DCC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402DD0                 sw      $a0, 8($v0)      # Store Word
; Found the 49th break (@00402dd4) ; new pc will be 004024cc
; ========================= BLOCK 49 =========================
.text:004024CC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004024D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024D4                 sll     $v0, 2           # Shift Left Logical
.text:004024D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004024E0                 lw      $v0, 8($v0)      # Load Word
.text:004024E4                 sll     $v1, $v0, 30     # Shift Left Logical
.text:004024E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024EC                 sll     $v0, 2           # Shift Left Logical
.text:004024F0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024F4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004024F8                 lw      $v0, 8($v0)      # Load Word
.text:004024FC                 srl     $v0, 2           # Shift Right Logical
.text:00402500                 or      $v1, $v0         # OR
.text:00402504                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402508                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040250C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402510                 sw      $v1, 8($v0)      # Store Word
; Found the 50th break (@00402514) ; new pc will be 0040397c
; ========================= BLOCK 50 =========================
.text:0040397C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403980                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403984                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403988                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040398C                 lw      $a0, 8($v0)      # Load Word
.text:00403990                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403994                 xor     $a0, $v0         # Exclusive OR
.text:00403998                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040399C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004039A4                 sw      $a0, 8($v0)      # Store Word
; Found the 51th break (@004039a8) ; new pc will be 00402e3c
; ========================= BLOCK 51 =========================
.text:00402E3C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402E40                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402E44                 sll     $v0, 2           # Shift Left Logical
.text:00402E48                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E4C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E50                 lw      $v0, 8($v0)      # Load Word
.text:00402E54                 srl     $v1, $v0, 20     # Shift Right Logical
.text:00402E58                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402E5C                 sll     $v0, 2           # Shift Left Logical
.text:00402E60                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E64                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402E68                 lw      $v0, 8($v0)      # Load Word
.text:00402E6C                 sll     $v0, 12          # Shift Left Logical
.text:00402E70                 or      $v1, $v0         # OR
.text:00402E74                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402E78                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E7C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E80                 sw      $v1, 8($v0)      # Store Word
; Found the 52th break (@00402e84) ; new pc will be 004033dc
; ========================= BLOCK 52 =========================
.text:004033DC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004033E0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033E4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033E8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004033EC                 lw      $a0, 8($v0)      # Load Word
.text:004033F0                 li      $v0, 0xD0358C15  # Load Immediate
.text:004033F8                 addu    $a0, $v0         # Add Unsigned
.text:004033FC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403400                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403404                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403408                 sw      $a0, 8($v0)      # Store Word
; Found the 53th break (@0040340c) ; new pc will be 00403664
; ========================= BLOCK 53 =========================
.text:00403664                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403668                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040366C                 sll     $v0, 2           # Shift Left Logical
.text:00403670                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403674                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403678                 lw      $v0, 8($v0)      # Load Word
.text:0040367C                 nor     $v1, $zero, $v0  # NOR
.text:00403680                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403684                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403688                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040368C                 sw      $v1, 8($v0)      # Store Word
; Found the 54th break (@00403690) ; new pc will be 004025a8
; ========================= BLOCK 54 =========================
.text:004025A8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004025AC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025B0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025B4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025B8                 lw      $a0, 8($v0)      # Load Word
.text:004025BC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004025C0                 addu    $a0, $v0         # Add Unsigned
.text:004025C4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025C8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025CC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004025D0                 sw      $a0, 8($v0)      # Store Word
; Found the 55th break (@004025d4) ; new pc will be 004029f8
; ========================= BLOCK 55 =========================
.text:004029F8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004029FC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A00                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A04                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402A08                 lw      $a0, 8($v0)      # Load Word
.text:00402A0C                 li      $v0, 0x81674F2B  # Load Immediate
.text:00402A14                 addu    $a0, $v0         # Add Unsigned
.text:00402A18                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A1C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A20                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A24                 sw      $a0, 8($v0)      # Store Word
; Found the 56th break (@00402a28) ; new pc will be 004032cc
; ========================= BLOCK 56 =========================
.text:004032CC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004032D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004032D4                 sll     $v0, 2           # Shift Left Logical
.text:004032D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004032E0                 lw      $v0, 8($v0)      # Load Word
.text:004032E4                 nor     $v1, $zero, $v0  # NOR
.text:004032E8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004032EC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032F0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004032F4                 sw      $v1, 8($v0)      # Store Word
; Found the 57th break (@004032f8) ; new pc will be 0040233c
; ========================= BLOCK 57 =========================
.text:0040233C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402340                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402344                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402348                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040234C                 lw      $a0, 8($v0)      # Load Word
.text:00402350                 li      $v0, 0x7B4DE789  # Load Immediate
.text:00402358                 xor     $a0, $v0         # Exclusive OR
.text:0040235C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402360                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402364                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402368                 sw      $a0, 8($v0)      # Store Word
; Found the 58th break (@0040236c) ; new pc will be 004031d4
; ========================= BLOCK 58 =========================
.text:004031D4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004031D8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004031DC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031E0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004031E4                 lw      $a0, 8($v0)      # Load Word
.text:004031E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004031EC                 xor     $a0, $v0         # Exclusive OR
.text:004031F0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004031F4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031F8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004031FC                 sw      $a0, 8($v0)      # Store Word
; Found the 59th break (@00403200) ; new pc will be 00403204
; ========================= BLOCK 59 =========================
.text:00403204                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403208                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040320C                 sll     $v0, 2           # Shift Left Logical
.text:00403210                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403214                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403218                 lw      $v0, 8($v0)      # Load Word
.text:0040321C                 nor     $v1, $zero, $v0  # NOR
.text:00403220                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403224                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403228                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040322C                 sw      $v1, 8($v0)      # Store Word
; Found the 60th break (@00403230) ; new pc will be 00402d10
; ========================= BLOCK 60 =========================
.text:00402D10                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D14                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D18                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D1C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D20                 lw      $a0, 8($v0)      # Load Word
.text:00402D24                 li      $v0, 0xA9BE160D  # Load Immediate
.text:00402D2C                 xor     $a0, $v0         # Exclusive OR
.text:00402D30                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D34                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D38                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402D3C                 sw      $a0, 8($v0)      # Store Word
; Found the 61th break (@00402d40) ; new pc will be 00402420
; ========================= BLOCK 61 =========================
.text:00402420                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402424                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402428                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040242C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402430                 lw      $a0, 8($v0)      # Load Word
.text:00402434                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402438                 xor     $a0, $v0         # Exclusive OR
.text:0040243C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402440                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402444                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402448                 sw      $a0, 8($v0)      # Store Word
; Found the 62th break (@0040244c) ; new pc will be 00403280
; ========================= BLOCK 62 =========================
.text:00403280                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403284                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403288                 sll     $v0, 2           # Shift Left Logical
.text:0040328C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403290                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403294                 lw      $v0, 8($v0)      # Load Word
.text:00403298                 sll     $v1, $v0, 29     # Shift Left Logical
.text:0040329C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004032A0                 sll     $v0, 2           # Shift Left Logical
.text:004032A4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032A8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004032AC                 lw      $v0, 8($v0)      # Load Word
.text:004032B0                 srl     $v0, 3           # Shift Right Logical
.text:004032B4                 or      $v1, $v0         # OR
.text:004032B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004032BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004032C4                 sw      $v1, 8($v0)      # Store Word
; Found the 63th break (@004032c8) ; new pc will be 00402450
; ========================= BLOCK 63 =========================
.text:00402450                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402454                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402458                 sll     $v0, 2           # Shift Left Logical
.text:0040245C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402460                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402464                 lw      $v0, 8($v0)      # Load Word
.text:00402468                 sll     $v1, $v0, 13     # Shift Left Logical
.text:0040246C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402470                 sll     $v0, 2           # Shift Left Logical
.text:00402474                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402478                 addu    $v0, $a1, $v0    # Add Unsigned
.text:0040247C                 lw      $v0, 8($v0)      # Load Word
.text:00402480                 srl     $v0, 19          # Shift Right Logical
.text:00402484                 or      $v1, $v0         # OR
.text:00402488                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040248C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402490                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402494                 sw      $v1, 8($v0)      # Store Word
; Found the 64th break (@00402498) ; new pc will be 00402714
; ========================= BLOCK 64 =========================
.text:00402714                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402718                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040271C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402720                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402724                 lw      $a0, 8($v0)      # Load Word
.text:00402728                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040272C                 addu    $a0, $v0         # Add Unsigned
.text:00402730                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402734                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402738                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040273C                 sw      $a0, 8($v0)      # Store Word
; Found the 65th break (@00402740) ; new pc will be 00402cb0
; ========================= BLOCK 65 =========================
.text:00402CB0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402CB4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402CB8                 sll     $v0, 2           # Shift Left Logical
.text:00402CBC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CC0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402CC4                 lw      $v0, 8($v0)      # Load Word
.text:00402CC8                 nor     $v1, $zero, $v0  # NOR
.text:00402CCC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402CD0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CD4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402CD8                 sw      $v1, 8($v0)      # Store Word
; Found the 66th break (@00402cdc) ; new pc will be 00403550
; ========================= BLOCK 66 =========================
.text:00403550                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403554                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403558                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040355C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403560                 lw      $a0, 8($v0)      # Load Word
.text:00403564                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403568                 xor     $a0, $v0         # Exclusive OR
.text:0040356C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403570                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403574                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403578                 sw      $a0, 8($v0)      # Store Word
; Found the 67th break (@0040357c) ; new pc will be 004033ac
; ========================= BLOCK 67 =========================
.text:004033AC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004033B0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033B4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033B8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004033BC                 lw      $a0, 8($v0)      # Load Word
.text:004033C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004033C4                 addu    $a0, $v0         # Add Unsigned
.text:004033C8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004033D4                 sw      $a0, 8($v0)      # Store Word
; Found the 68th break (@004033d8) ; new pc will be 00402a2c
; ========================= BLOCK 68 =========================
.text:00402A2C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402A30                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A34                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A38                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402A3C                 lw      $a0, 8($v0)      # Load Word
.text:00402A40                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A44                 subu    $a0, $v0         # Subtract Unsigned
.text:00402A48                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A4C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A50                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A54                 sw      $a0, 8($v0)      # Store Word
; Found the 69th break (@00402a58) ; new pc will be 004023a4
; ========================= BLOCK 69 =========================
.text:004023A4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004023A8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004023AC                 sll     $v0, 2           # Shift Left Logical
.text:004023B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004023B8                 lw      $v0, 8($v0)      # Load Word
.text:004023BC                 srl     $v1, $v0, 12     # Shift Right Logical
.text:004023C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004023C4                 sll     $v0, 2           # Shift Left Logical
.text:004023C8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023CC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004023D0                 lw      $v0, 8($v0)      # Load Word
.text:004023D4                 sll     $v0, 20          # Shift Left Logical
.text:004023D8                 or      $v1, $v0         # OR
.text:004023DC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004023E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004023E8                 sw      $v1, 8($v0)      # Store Word
; Found the 70th break (@004023ec) ; new pc will be 004022c0
; ========================= BLOCK 70 =========================
.text:004022C0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004022C4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022C8                 sll     $v0, 2           # Shift Left Logical
.text:004022CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004022D4                 lw      $v0, 8($v0)      # Load Word
.text:004022D8                 srl     $v1, $v0, 1      # Shift Right Logical
.text:004022DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022E0                 sll     $v0, 2           # Shift Left Logical
.text:004022E4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022E8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004022EC                 lw      $v0, 8($v0)      # Load Word
.text:004022F0                 sll     $v0, 31          # Shift Left Logical
.text:004022F4                 or      $v1, $v0         # OR
.text:004022F8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004022FC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402300                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402304                 sw      $v1, 8($v0)      # Store Word
; Found the 71th break (@00402308) ; new pc will be 00402518
; ========================= BLOCK 71 =========================
.text:00402518                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040251C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402520                 sll     $v0, 2           # Shift Left Logical
.text:00402524                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402528                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040252C                 lw      $v0, 8($v0)      # Load Word
.text:00402530                 nor     $v1, $zero, $v0  # NOR
.text:00402534                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402538                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040253C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402540                 sw      $v1, 8($v0)      # Store Word
; Found the 72th break (@00402544) ; new pc will be 004028cc
; ========================= BLOCK 72 =========================
.text:004028CC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004028D0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004028D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004028DC                 lw      $a0, 8($v0)      # Load Word
.text:004028E0                 li      $v0, 0x3A2EE307  # Load Immediate
.text:004028E8                 addu    $a0, $v0         # Add Unsigned
.text:004028EC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004028F0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004028F8                 sw      $a0, 8($v0)      # Store Word
; Found the 73th break (@004028fc) ; new pc will be 004038e8
; ========================= BLOCK 73 =========================
.text:004038E8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004038EC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038F0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038F4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038F8                 lw      $a0, 8($v0)      # Load Word
.text:004038FC                 li      $v0, 0xDBFA3745  # Load Immediate
.text:00403904                 addu    $a0, $v0         # Add Unsigned
.text:00403908                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040390C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403910                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403914                 sw      $a0, 8($v0)      # Store Word
; Found the 74th break (@00403918) ; new pc will be 0040380c
; ========================= BLOCK 74 =========================
.text:0040380C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403810                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403814                 sll     $v0, 2           # Shift Left Logical
.text:00403818                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040381C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403820                 lw      $v0, 8($v0)      # Load Word
.text:00403824                 sll     $v1, $v0, 16     # Shift Left Logical
.text:00403828                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040382C                 sll     $v0, 2           # Shift Left Logical
.text:00403830                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403834                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403838                 lw      $v0, 8($v0)      # Load Word
.text:0040383C                 srl     $v0, 16          # Shift Right Logical
.text:00403840                 or      $v1, $v0         # OR
.text:00403844                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403848                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040384C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403850                 sw      $v1, 8($v0)      # Store Word
; Found the 75th break (@00403854) ; new pc will be 00403858
; ========================= BLOCK 75 =========================
.text:00403858                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040385C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403860                 sll     $v0, 2           # Shift Left Logical
.text:00403864                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403868                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040386C                 lw      $v0, 8($v0)      # Load Word
.text:00403870                 nor     $v1, $zero, $v0  # NOR
.text:00403874                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403878                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040387C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403880                 sw      $v1, 8($v0)      # Store Word
; Found the 76th break (@00403884) ; new pc will be 00402d44
; ========================= BLOCK 76 =========================
.text:00402D44                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D48                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D4C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D50                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D54                 lw      $a0, 8($v0)      # Load Word
.text:00402D58                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402D5C                 addu    $a0, $v0         # Add Unsigned
.text:00402D60                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D64                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D68                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402D6C                 sw      $a0, 8($v0)      # Store Word
; Found the 77th break (@00402d70) ; new pc will be 00402608
; ========================= BLOCK 77 =========================
.text:00402608                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040260C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402610                 sll     $v0, 2           # Shift Left Logical
.text:00402614                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402618                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040261C                 lw      $v0, 8($v0)      # Load Word
.text:00402620                 srl     $v1, $v0, 23     # Shift Right Logical
.text:00402624                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402628                 sll     $v0, 2           # Shift Left Logical
.text:0040262C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402630                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402634                 lw      $v0, 8($v0)      # Load Word
.text:00402638                 sll     $v0, 9           # Shift Left Logical
.text:0040263C                 or      $v1, $v0         # OR
.text:00402640                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402644                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402648                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040264C                 sw      $v1, 8($v0)      # Store Word
; Found the 78th break (@00402650) ; new pc will be 00402d74
; ========================= BLOCK 78 =========================
.text:00402D74                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D78                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D7C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D80                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D84                 lw      $a0, 8($v0)      # Load Word
.text:00402D88                 li      $v0, 0xD45CEF0A  # Load Immediate
.text:00402D90                 addu    $a0, $v0         # Add Unsigned
.text:00402D94                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D98                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D9C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402DA0                 sw      $a0, 8($v0)      # Store Word
; Found the 79th break (@00402da4) ; new pc will be 00402e88
; ========================= BLOCK 79 =========================
.text:00402E88                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402E8C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E90                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E94                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E98                 lw      $a0, 8($v0)      # Load Word
.text:00402E9C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402EA0                 xor     $a0, $v0         # Exclusive OR
.text:00402EA4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402EA8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402EB0                 sw      $a0, 8($v0)      # Store Word
; Found the 80th break (@00402eb4) ; new pc will be 0040230c
; ========================= BLOCK 80 =========================
.text:0040230C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402310                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402314                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402318                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040231C                 lw      $a0, 8($v0)      # Load Word
.text:00402320                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402324                 subu    $a0, $v0         # Subtract Unsigned
.text:00402328                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040232C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402330                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402334                 sw      $a0, 8($v0)      # Store Word
; Found the 81th break (@00402338) ; new pc will be 00402f68
; ========================= BLOCK 81 =========================
.text:00402F68                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402F6C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F70                 sll     $v0, 2           # Shift Left Logical
.text:00402F74                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F78                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F7C                 lw      $v0, 8($v0)      # Load Word
.text:00402F80                 sll     $v1, $v0, 23     # Shift Left Logical
.text:00402F84                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F88                 sll     $v0, 2           # Shift Left Logical
.text:00402F8C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F90                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402F94                 lw      $v0, 8($v0)      # Load Word
.text:00402F98                 srl     $v0, 9           # Shift Right Logical
.text:00402F9C                 or      $v1, $v0         # OR
.text:00402FA0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402FA4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FA8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FAC                 sw      $v1, 8($v0)      # Store Word
; Found the 82th break (@00402fb0) ; new pc will be 00403520
; ========================= BLOCK 82 =========================
.text:00403520                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403524                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403528                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040352C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403530                 lw      $a0, 8($v0)      # Load Word
.text:00403534                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403538                 xor     $a0, $v0         # Exclusive OR
.text:0040353C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403540                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403544                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403548                 sw      $a0, 8($v0)      # Store Word
; Found the 83th break (@0040354c) ; new pc will be 00402c04
; ========================= BLOCK 83 =========================
.text:00402C04                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402C08                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C0C                 sll     $v0, 2           # Shift Left Logical
.text:00402C10                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C14                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402C18                 lw      $v0, 8($v0)      # Load Word
.text:00402C1C                 srl     $v1, $v0, 4      # Shift Right Logical
.text:00402C20                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C24                 sll     $v0, 2           # Shift Left Logical
.text:00402C28                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C2C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402C30                 lw      $v0, 8($v0)      # Load Word
.text:00402C34                 sll     $v0, 28          # Shift Left Logical
.text:00402C38                 or      $v1, $v0         # OR
.text:00402C3C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402C40                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C44                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402C48                 sw      $v1, 8($v0)      # Store Word
; Found the 84th break (@00402c4c) ; new pc will be 00403778
; ========================= BLOCK 84 =========================
.text:00403778                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040377C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403780                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403784                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403788                 lw      $a0, 8($v0)      # Load Word
.text:0040378C                 li      $v0, 0x6EDC032   # Load Immediate
.text:00403794                 addu    $a0, $v0         # Add Unsigned
.text:00403798                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040379C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004037A4                 sw      $a0, 8($v0)      # Store Word
; Found the 85th break (@004037a8) ; new pc will be 00402900
; ========================= BLOCK 85 =========================
.text:00402900                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402904                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402908                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040290C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402910                 lw      $a0, 8($v0)      # Load Word
.text:00402914                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402918                 xor     $a0, $v0         # Exclusive OR
.text:0040291C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402920                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402924                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402928                 sw      $a0, 8($v0)      # Store Word
; Found the 86th break (@0040292c) ; new pc will be 004027a4
; ========================= BLOCK 86 =========================
.text:004027A4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004027A8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027AC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027B0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004027B4                 lw      $a0, 8($v0)      # Load Word
.text:004027B8                 li      $v0, 0xD0970C74  # Load Immediate
.text:004027C0                 addu    $a0, $v0         # Add Unsigned
.text:004027C4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027C8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027CC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004027D0                 sw      $a0, 8($v0)      # Store Word
; Found the 87th break (@004027d4) ; new pc will be 00402fb4
; ========================= BLOCK 87 =========================
.text:00402FB4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402FB8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FBC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FC0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FC4                 lw      $a0, 8($v0)      # Load Word
.text:00402FC8                 li      $v0, 0xCC4E5D94  # Load Immediate
.text:00402FD0                 xor     $a0, $v0         # Exclusive OR
.text:00402FD4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FD8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FDC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402FE0                 sw      $a0, 8($v0)      # Store Word
; Found the 88th break (@00402fe4) ; new pc will be 00402578
; ========================= BLOCK 88 =========================
.text:00402578                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040257C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402580                 sll     $v0, 2           # Shift Left Logical
.text:00402584                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402588                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040258C                 lw      $v0, 8($v0)      # Load Word
.text:00402590                 nor     $v1, $zero, $v0  # NOR
.text:00402594                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402598                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040259C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025A0                 sw      $v1, 8($v0)      # Store Word
; Found the 89th break (@004025a4) ; new pc will be 00402548
; ========================= BLOCK 89 =========================
.text:00402548                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040254C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402550                 sll     $v0, 2           # Shift Left Logical
.text:00402554                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402558                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040255C                 lw      $v0, 8($v0)      # Load Word
.text:00402560                 nor     $v1, $zero, $v0  # NOR
.text:00402564                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402568                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040256C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402570                 sw      $v1, 8($v0)      # Store Word
; Found the 90th break (@00402574) ; new pc will be 00402ce0
; ========================= BLOCK 90 =========================
.text:00402CE0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402CE4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402CE8                 sll     $v0, 2           # Shift Left Logical
.text:00402CEC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CF0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402CF4                 lw      $v0, 8($v0)      # Load Word
.text:00402CF8                 nor     $v1, $zero, $v0  # NOR
.text:00402CFC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402D00                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D04                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D08                 sw      $v1, 8($v0)      # Store Word
; Found the 91th break (@00402d0c) ; new pc will be 00403888
; ========================= BLOCK 91 =========================
.text:00403888                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040388C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403890                 sll     $v0, 2           # Shift Left Logical
.text:00403894                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403898                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040389C                 lw      $v0, 8($v0)      # Load Word
.text:004038A0                 nor     $v1, $zero, $v0  # NOR
.text:004038A4                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004038A8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038AC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038B0                 sw      $v1, 8($v0)      # Store Word
; Found the 92th break (@004038b4) ; new pc will be 00402c50
; ========================= BLOCK 92 =========================
.text:00402C50                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402C54                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C58                 sll     $v0, 2           # Shift Left Logical
.text:00402C5C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C60                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402C64                 lw      $v1, 8($v0)      # Load Word
.text:00402C68                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C6C                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00402C70                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00402C74                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C78                 sll     $v0, 2           # Shift Left Logical
.text:00402C7C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C80                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402C84                 lw      $a1, 8($v0)      # Load Word
.text:00402C88                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C8C                 nor     $v0, $zero, $v0  # NOR
.text:00402C90                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00402C94                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:00402C98                 or      $v1, $v0         # OR
.text:00402C9C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402CA0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CA4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402CA8                 sw      $v1, 8($v0)      # Store Word
; Found the 93th break (@00402cac) ; new pc will be 00403144
; ========================= BLOCK 93 =========================
.text:00403144                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403148                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040314C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403150                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403154                 lw      $a0, 8($v0)      # Load Word
.text:00403158                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040315C                 addu    $a0, $v0         # Add Unsigned
.text:00403160                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403164                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403168                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040316C                 sw      $a0, 8($v0)      # Store Word
; Found the 94th break (@00403170) ; new pc will be 004039ac
; ========================= BLOCK 94 =========================
.text:004039AC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004039B0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004039B4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039B8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004039BC                 lw      $a0, 8($v0)      # Load Word
.text:004039C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004039C4                 addu    $a0, $v0         # Add Unsigned
.text:004039C8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004039CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004039D4                 sw      $a0, 8($v0)      # Store Word
; Found the 95th break (@004039d8) ; new pc will be 00403098
; ========================= BLOCK 95 =========================
.text:00403098                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040309C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030A0                 sll     $v0, 2           # Shift Left Logical
.text:004030A4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030A8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004030AC                 lw      $v0, 8($v0)      # Load Word
.text:004030B0                 srl     $v1, $v0, 3      # Shift Right Logical
.text:004030B4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030B8                 sll     $v0, 2           # Shift Left Logical
.text:004030BC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030C0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004030C4                 lw      $v0, 8($v0)      # Load Word
.text:004030C8                 sll     $v0, 29          # Shift Left Logical
.text:004030CC                 or      $v1, $v0         # OR
.text:004030D0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004030D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004030DC                 sw      $v1, 8($v0)      # Store Word
; Found the 96th break (@004030e0) ; new pc will be 004029c8
; ========================= BLOCK 96 =========================
.text:004029C8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004029CC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029D0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029D4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004029D8                 lw      $a0, 8($v0)      # Load Word
.text:004029DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004029E0                 xor     $a0, $v0         # Exclusive OR
.text:004029E4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029E8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029EC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004029F0                 sw      $a0, 8($v0)      # Store Word
; Found the 97th break (@004029f4) ; new pc will be 00402930
; ========================= BLOCK 97 =========================
.text:00402930                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402934                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402938                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040293C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402940                 lw      $a0, 8($v0)      # Load Word
.text:00402944                 li      $v0, 0x4CC0DC26  # Load Immediate
.text:0040294C                 xor     $a0, $v0         # Exclusive OR
.text:00402950                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402954                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402958                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040295C                 sw      $a0, 8($v0)      # Store Word
; Found the 98th break (@00402960) ; new pc will be 00403068
; ========================= BLOCK 98 =========================
.text:00403068                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040306C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403070                 sll     $v0, 2           # Shift Left Logical
.text:00403074                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403078                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040307C                 lw      $v0, 8($v0)      # Load Word
.text:00403080                 nor     $v1, $zero, $v0  # NOR
.text:00403084                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403088                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040308C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403090                 sw      $v1, 8($v0)      # Store Word
; Found the 99th break (@00403094) ; new pc will be 00403580
; ========================= BLOCK 99 =========================
.text:00403580                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403584                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403588                 sll     $v0, 2           # Shift Left Logical
.text:0040358C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403590                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403594                 lw      $v0, 8($v0)      # Load Word
.text:00403598                 sll     $v1, $v0, 28     # Shift Left Logical
.text:0040359C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004035A0                 sll     $v0, 2           # Shift Left Logical
.text:004035A4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035A8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004035AC                 lw      $v0, 8($v0)      # Load Word
.text:004035B0                 srl     $v0, 4           # Shift Right Logical
.text:004035B4                 or      $v1, $v0         # OR
.text:004035B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004035BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004035C4                 sw      $v1, 8($v0)      # Store Word
; Found the 100th break (@004035c8) ; new pc will be 004039dc
; ========================= BLOCK 100 =========================
.text:004039DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004039E0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004039E4                 sw      $v0, 0x48+i($fp)  # Store Word
; Found the 0th break (@0040228c) ; new pc will be 00402548
; ========================= BLOCK 0 =========================
.text:00402548                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040254C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402550                 sll     $v0, 2           # Shift Left Logical
.text:00402554                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402558                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040255C                 lw      $v0, 8($v0)      # Load Word
.text:00402560                 nor     $v1, $zero, $v0  # NOR
.text:00402564                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402568                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040256C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402570                 sw      $v1, 8($v0)      # Store Word
; Found the 1th break (@00402574) ; new pc will be 00402e08
; ========================= BLOCK 1 =========================
.text:00402E08                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402E0C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E10                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E14                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E18                 lw      $a0, 8($v0)      # Load Word
.text:00402E1C                 li      $v0, 0x73C69F47  # Load Immediate
.text:00402E24                 addu    $a0, $v0         # Add Unsigned
.text:00402E28                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E2C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E30                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E34                 sw      $a0, 8($v0)      # Store Word
; Found the 2th break (@00402e38) ; new pc will be 00402290
; ========================= BLOCK 2 =========================
.text:00402290                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402294                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402298                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040229C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004022A0                 lw      $a0, 8($v0)      # Load Word
.text:004022A4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022A8                 subu    $a0, $v0         # Subtract Unsigned
.text:004022AC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004022B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004022B8                 sw      $a0, 8($v0)      # Store Word
; Found the 3th break (@004022bc) ; new pc will be 00402d74
; ========================= BLOCK 3 =========================
.text:00402D74                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D78                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D7C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D80                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D84                 lw      $a0, 8($v0)      # Load Word
.text:00402D88                 li      $v0, 0xD45CEF0A  # Load Immediate
.text:00402D90                 addu    $a0, $v0         # Add Unsigned
.text:00402D94                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D98                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D9C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402DA0                 sw      $a0, 8($v0)      # Store Word
; Found the 4th break (@00402da4) ; new pc will be 00402fe8
; ========================= BLOCK 4 =========================
.text:00402FE8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402FEC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FF0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FF4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FF8                 lw      $a0, 8($v0)      # Load Word
.text:00402FFC                 li      $v0, 0x38C1FEB8  # Load Immediate
.text:00403004                 xor     $a0, $v0         # Exclusive OR
.text:00403008                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040300C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403010                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403014                 sw      $a0, 8($v0)      # Store Word
; Found the 5th break (@00403018) ; new pc will be 00402964
; ========================= BLOCK 5 =========================
.text:00402964                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402968                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040296C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402970                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402974                 lw      $a0, 8($v0)      # Load Word
.text:00402978                 li      $v0, 0x737F298   # Load Immediate
.text:00402980                 addu    $a0, $v0         # Add Unsigned
.text:00402984                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402988                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040298C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402990                 sw      $a0, 8($v0)      # Store Word
; Found the 6th break (@00402994) ; new pc will be 00402420
; ========================= BLOCK 6 =========================
.text:00402420                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402424                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402428                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040242C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402430                 lw      $a0, 8($v0)      # Load Word
.text:00402434                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402438                 xor     $a0, $v0         # Exclusive OR
.text:0040243C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402440                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402444                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402448                 sw      $a0, 8($v0)      # Store Word
; Found the 7th break (@0040244c) ; new pc will be 00402608
; ========================= BLOCK 7 =========================
.text:00402608                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040260C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402610                 sll     $v0, 2           # Shift Left Logical
.text:00402614                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402618                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040261C                 lw      $v0, 8($v0)      # Load Word
.text:00402620                 srl     $v1, $v0, 23     # Shift Right Logical
.text:00402624                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402628                 sll     $v0, 2           # Shift Left Logical
.text:0040262C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402630                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402634                 lw      $v0, 8($v0)      # Load Word
.text:00402638                 sll     $v0, 9           # Shift Left Logical
.text:0040263C                 or      $v1, $v0         # OR
.text:00402640                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402644                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402648                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040264C                 sw      $v1, 8($v0)      # Store Word
; Found the 8th break (@00402650) ; new pc will be 00402654
; ========================= BLOCK 8 =========================
.text:00402654                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402658                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040265C                 sll     $v0, 2           # Shift Left Logical
.text:00402660                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402664                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402668                 lw      $v1, 8($v0)      # Load Word
.text:0040266C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402670                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00402674                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00402678                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040267C                 sll     $v0, 2           # Shift Left Logical
.text:00402680                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402684                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402688                 lw      $a1, 8($v0)      # Load Word
.text:0040268C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402690                 nor     $v0, $zero, $v0  # NOR
.text:00402694                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00402698                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040269C                 or      $v1, $v0         # OR
.text:004026A0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004026A4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026A8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004026AC                 sw      $v1, 8($v0)      # Store Word
; Found the 9th break (@004026b0) ; new pc will be 004025d8
; ========================= BLOCK 9 =========================
.text:004025D8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004025DC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025E8                 lw      $a0, 8($v0)      # Load Word
.text:004025EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004025F0                 addu    $a0, $v0         # Add Unsigned
.text:004025F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025F8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025FC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402600                 sw      $a0, 8($v0)      # Store Word
; Found the 10th break (@00402604) ; new pc will be 00402a2c
; ========================= BLOCK 10 =========================
.text:00402A2C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402A30                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A34                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A38                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402A3C                 lw      $a0, 8($v0)      # Load Word
.text:00402A40                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A44                 subu    $a0, $v0         # Subtract Unsigned
.text:00402A48                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A4C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A50                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A54                 sw      $a0, 8($v0)      # Store Word
; Found the 11th break (@00402a58) ; new pc will be 0040301c
; ========================= BLOCK 11 =========================
.text:0040301C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403020                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403024                 sll     $v0, 2           # Shift Left Logical
.text:00403028                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040302C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403030                 lw      $v0, 8($v0)      # Load Word
.text:00403034                 srl     $v1, $v0, 8      # Shift Right Logical
.text:00403038                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040303C                 sll     $v0, 2           # Shift Left Logical
.text:00403040                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403044                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403048                 lw      $v0, 8($v0)      # Load Word
.text:0040304C                 sll     $v0, 24          # Shift Left Logical
.text:00403050                 or      $v1, $v0         # OR
.text:00403054                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403058                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040305C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403060                 sw      $v1, 8($v0)      # Store Word
; Found the 12th break (@00403064) ; new pc will be 00402dd8
; ========================= BLOCK 12 =========================
.text:00402DD8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402DDC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DE0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DE4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402DE8                 lw      $a0, 8($v0)      # Load Word
.text:00402DEC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402DF0                 subu    $a0, $v0         # Subtract Unsigned
.text:00402DF4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DF8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DFC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E00                 sw      $a0, 8($v0)      # Store Word
; Found the 13th break (@00402e04) ; new pc will be 0040286c
; ========================= BLOCK 13 =========================
.text:0040286C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402870                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402874                 sll     $v0, 2           # Shift Left Logical
.text:00402878                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040287C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402880                 lw      $v1, 8($v0)      # Load Word
.text:00402884                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402888                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040288C                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00402890                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402894                 sll     $v0, 2           # Shift Left Logical
.text:00402898                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040289C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004028A0                 lw      $a1, 8($v0)      # Load Word
.text:004028A4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004028A8                 nor     $v0, $zero, $v0  # NOR
.text:004028AC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004028B0                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004028B4                 or      $v1, $v0         # OR
.text:004028B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004028BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004028C4                 sw      $v1, 8($v0)      # Store Word
; Found the 14th break (@004028c8) ; new pc will be 004029c8
; ========================= BLOCK 14 =========================
.text:004029C8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004029CC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029D0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029D4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004029D8                 lw      $a0, 8($v0)      # Load Word
.text:004029DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004029E0                 xor     $a0, $v0         # Exclusive OR
.text:004029E4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029E8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029EC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004029F0                 sw      $a0, 8($v0)      # Store Word
; Found the 15th break (@004029f4) ; new pc will be 00403888
; ========================= BLOCK 15 =========================
.text:00403888                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040388C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403890                 sll     $v0, 2           # Shift Left Logical
.text:00403894                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403898                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040389C                 lw      $v0, 8($v0)      # Load Word
.text:004038A0                 nor     $v1, $zero, $v0  # NOR
.text:004038A4                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004038A8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038AC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038B0                 sw      $v1, 8($v0)      # Store Word
; Found the 16th break (@004038b4) ; new pc will be 00403280
; ========================= BLOCK 16 =========================
.text:00403280                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403284                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403288                 sll     $v0, 2           # Shift Left Logical
.text:0040328C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403290                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403294                 lw      $v0, 8($v0)      # Load Word
.text:00403298                 sll     $v1, $v0, 29     # Shift Left Logical
.text:0040329C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004032A0                 sll     $v0, 2           # Shift Left Logical
.text:004032A4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032A8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004032AC                 lw      $v0, 8($v0)      # Load Word
.text:004032B0                 srl     $v0, 3           # Shift Right Logical
.text:004032B4                 or      $v1, $v0         # OR
.text:004032B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004032BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004032C4                 sw      $v1, 8($v0)      # Store Word
; Found the 17th break (@004032c8) ; new pc will be 00402c50
; ========================= BLOCK 17 =========================
.text:00402C50                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402C54                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C58                 sll     $v0, 2           # Shift Left Logical
.text:00402C5C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C60                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402C64                 lw      $v1, 8($v0)      # Load Word
.text:00402C68                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C6C                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00402C70                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00402C74                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C78                 sll     $v0, 2           # Shift Left Logical
.text:00402C7C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C80                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402C84                 lw      $a1, 8($v0)      # Load Word
.text:00402C88                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C8C                 nor     $v0, $zero, $v0  # NOR
.text:00402C90                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00402C94                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:00402C98                 or      $v1, $v0         # OR
.text:00402C9C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402CA0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CA4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402CA8                 sw      $v1, 8($v0)      # Store Word
; Found the 18th break (@00402cac) ; new pc will be 00402da8
; ========================= BLOCK 18 =========================
.text:00402DA8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402DAC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DB0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DB4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402DB8                 lw      $a0, 8($v0)      # Load Word
.text:00402DBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402DC0                 xor     $a0, $v0         # Exclusive OR
.text:00402DC4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DC8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DCC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402DD0                 sw      $a0, 8($v0)      # Store Word
; Found the 19th break (@00402dd4) ; new pc will be 00402930
; ========================= BLOCK 19 =========================
.text:00402930                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402934                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402938                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040293C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402940                 lw      $a0, 8($v0)      # Load Word
.text:00402944                 li      $v0, 0x4CC0DC26  # Load Immediate
.text:0040294C                 xor     $a0, $v0         # Exclusive OR
.text:00402950                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402954                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402958                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040295C                 sw      $a0, 8($v0)      # Store Word
; Found the 20th break (@00402960) ; new pc will be 004031d4
; ========================= BLOCK 20 =========================
.text:004031D4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004031D8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004031DC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031E0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004031E4                 lw      $a0, 8($v0)      # Load Word
.text:004031E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004031EC                 xor     $a0, $v0         # Exclusive OR
.text:004031F0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004031F4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031F8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004031FC                 sw      $a0, 8($v0)      # Store Word
; Found the 21th break (@00403200) ; new pc will be 00402578
; ========================= BLOCK 21 =========================
.text:00402578                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040257C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402580                 sll     $v0, 2           # Shift Left Logical
.text:00402584                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402588                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040258C                 lw      $v0, 8($v0)      # Load Word
.text:00402590                 nor     $v1, $zero, $v0  # NOR
.text:00402594                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402598                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040259C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025A0                 sw      $v1, 8($v0)      # Store Word
; Found the 22th break (@004025a4) ; new pc will be 00402f38
; ========================= BLOCK 22 =========================
.text:00402F38                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402F3C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F40                 sll     $v0, 2           # Shift Left Logical
.text:00402F44                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F48                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F4C                 lw      $v0, 8($v0)      # Load Word
.text:00402F50                 nor     $v1, $zero, $v0  # NOR
.text:00402F54                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402F58                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F5C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402F60                 sw      $v1, 8($v0)      # Store Word
; Found the 23th break (@00402f64) ; new pc will be 0040391c
; ========================= BLOCK 23 =========================
.text:0040391C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403920                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403924                 sll     $v0, 2           # Shift Left Logical
.text:00403928                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040392C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403930                 lw      $v1, 8($v0)      # Load Word
.text:00403934                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403938                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040393C                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403940                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403944                 sll     $v0, 2           # Shift Left Logical
.text:00403948                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040394C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403950                 lw      $a1, 8($v0)      # Load Word
.text:00403954                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403958                 nor     $v0, $zero, $v0  # NOR
.text:0040395C                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403960                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:00403964                 or      $v1, $v0         # OR
.text:00403968                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040396C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403970                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403974                 sw      $v1, 8($v0)      # Store Word
; Found the 24th break (@00403978) ; new pc will be 00403234
; ========================= BLOCK 24 =========================
.text:00403234                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403238                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040323C                 sll     $v0, 2           # Shift Left Logical
.text:00403240                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403244                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403248                 lw      $v0, 8($v0)      # Load Word
.text:0040324C                 sll     $v1, $v0, 29     # Shift Left Logical
.text:00403250                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403254                 sll     $v0, 2           # Shift Left Logical
.text:00403258                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040325C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403260                 lw      $v0, 8($v0)      # Load Word
.text:00403264                 srl     $v0, 3           # Shift Right Logical
.text:00403268                 or      $v1, $v0         # OR
.text:0040326C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403270                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403274                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403278                 sw      $v1, 8($v0)      # Store Word
; Found the 25th break (@0040327c) ; new pc will be 00402774
; ========================= BLOCK 25 =========================
.text:00402774                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402778                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040277C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402780                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402784                 lw      $a0, 8($v0)      # Load Word
.text:00402788                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040278C                 xor     $a0, $v0         # Exclusive OR
.text:00402790                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402794                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402798                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040279C                 sw      $a0, 8($v0)      # Store Word
; Found the 26th break (@004027a0) ; new pc will be 004032fc
; ========================= BLOCK 26 =========================
.text:004032FC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403300                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403304                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403308                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040330C                 lw      $a0, 8($v0)      # Load Word
.text:00403310                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403314                 xor     $a0, $v0         # Exclusive OR
.text:00403318                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040331C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403320                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403324                 sw      $a0, 8($v0)      # Store Word
; Found the 27th break (@00403328) ; new pc will be 00402c04
; ========================= BLOCK 27 =========================
.text:00402C04                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402C08                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C0C                 sll     $v0, 2           # Shift Left Logical
.text:00402C10                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C14                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402C18                 lw      $v0, 8($v0)      # Load Word
.text:00402C1C                 srl     $v1, $v0, 4      # Shift Right Logical
.text:00402C20                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C24                 sll     $v0, 2           # Shift Left Logical
.text:00402C28                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C2C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402C30                 lw      $v0, 8($v0)      # Load Word
.text:00402C34                 sll     $v0, 28          # Shift Left Logical
.text:00402C38                 or      $v1, $v0         # OR
.text:00402C3C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402C40                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C44                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402C48                 sw      $v1, 8($v0)      # Store Word
; Found the 28th break (@00402c4c) ; new pc will be 004022c0
; ========================= BLOCK 28 =========================
.text:004022C0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004022C4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022C8                 sll     $v0, 2           # Shift Left Logical
.text:004022CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004022D4                 lw      $v0, 8($v0)      # Load Word
.text:004022D8                 srl     $v1, $v0, 1      # Shift Right Logical
.text:004022DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022E0                 sll     $v0, 2           # Shift Left Logical
.text:004022E4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022E8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004022EC                 lw      $v0, 8($v0)      # Load Word
.text:004022F0                 sll     $v0, 31          # Shift Left Logical
.text:004022F4                 or      $v1, $v0         # OR
.text:004022F8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004022FC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402300                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402304                 sw      $v1, 8($v0)      # Store Word
; Found the 29th break (@00402308) ; new pc will be 0040397c
; ========================= BLOCK 29 =========================
.text:0040397C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403980                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403984                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403988                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040398C                 lw      $a0, 8($v0)      # Load Word
.text:00403990                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403994                 xor     $a0, $v0         # Exclusive OR
.text:00403998                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040399C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004039A4                 sw      $a0, 8($v0)      # Store Word
; Found the 30th break (@004039a8) ; new pc will be 004035fc
; ========================= BLOCK 30 =========================
.text:004035FC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403600                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403604                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403608                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040360C                 lw      $a0, 8($v0)      # Load Word
.text:00403610                 li      $v0, 0x8103D046  # Load Immediate
.text:00403618                 xor     $a0, $v0         # Exclusive OR
.text:0040361C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403620                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403624                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403628                 sw      $a0, 8($v0)      # Store Word
; Found the 31th break (@0040362c) ; new pc will be 004023a4
; ========================= BLOCK 31 =========================
.text:004023A4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004023A8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004023AC                 sll     $v0, 2           # Shift Left Logical
.text:004023B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004023B8                 lw      $v0, 8($v0)      # Load Word
.text:004023BC                 srl     $v1, $v0, 12     # Shift Right Logical
.text:004023C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004023C4                 sll     $v0, 2           # Shift Left Logical
.text:004023C8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023CC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004023D0                 lw      $v0, 8($v0)      # Load Word
.text:004023D4                 sll     $v0, 20          # Shift Left Logical
.text:004023D8                 or      $v1, $v0         # OR
.text:004023DC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004023E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004023E8                 sw      $v1, 8($v0)      # Store Word
; Found the 32th break (@004023ec) ; new pc will be 00402f68
; ========================= BLOCK 32 =========================
.text:00402F68                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402F6C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F70                 sll     $v0, 2           # Shift Left Logical
.text:00402F74                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F78                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F7C                 lw      $v0, 8($v0)      # Load Word
.text:00402F80                 sll     $v1, $v0, 23     # Shift Left Logical
.text:00402F84                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F88                 sll     $v0, 2           # Shift Left Logical
.text:00402F8C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F90                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402F94                 lw      $v0, 8($v0)      # Load Word
.text:00402F98                 srl     $v0, 9           # Shift Right Logical
.text:00402F9C                 or      $v1, $v0         # OR
.text:00402FA0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402FA4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FA8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FAC                 sw      $v1, 8($v0)      # Store Word
; Found the 33th break (@00402fb0) ; new pc will be 004034f0
; ========================= BLOCK 33 =========================
.text:004034F0                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004034F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004034F8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034FC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403500                 lw      $a0, 8($v0)      # Load Word
.text:00403504                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403508                 addu    $a0, $v0         # Add Unsigned
.text:0040350C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403510                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403514                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403518                 sw      $a0, 8($v0)      # Store Word
; Found the 34th break (@0040351c) ; new pc will be 0040249c
; ========================= BLOCK 34 =========================
.text:0040249C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004024A0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024A4                 sll     $v0, 2           # Shift Left Logical
.text:004024A8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024AC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004024B0                 lw      $v0, 8($v0)      # Load Word
.text:004024B4                 nor     $v1, $zero, $v0  # NOR
.text:004024B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004024BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004024C4                 sw      $v1, 8($v0)      # Store Word
; Found the 35th break (@004024c8) ; new pc will be 0040372c
; ========================= BLOCK 35 =========================
.text:0040372C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403730                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403734                 sll     $v0, 2           # Shift Left Logical
.text:00403738                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040373C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403740                 lw      $v0, 8($v0)      # Load Word
.text:00403744                 sll     $v1, $v0, 5      # Shift Left Logical
.text:00403748                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040374C                 sll     $v0, 2           # Shift Left Logical
.text:00403750                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403754                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403758                 lw      $v0, 8($v0)      # Load Word
.text:0040375C                 srl     $v0, 27          # Shift Right Logical
.text:00403760                 or      $v1, $v0         # OR
.text:00403764                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403768                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040376C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403770                 sw      $v1, 8($v0)      # Store Word
; Found the 36th break (@00403774) ; new pc will be 00402b08
; ========================= BLOCK 36 =========================
.text:00402B08                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402B0C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402B10                 sll     $v0, 2           # Shift Left Logical
.text:00402B14                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B18                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402B1C                 lw      $v0, 8($v0)      # Load Word
.text:00402B20                 srl     $v1, $v0, 26     # Shift Right Logical
.text:00402B24                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402B28                 sll     $v0, 2           # Shift Left Logical
.text:00402B2C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B30                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402B34                 lw      $v0, 8($v0)      # Load Word
.text:00402B38                 sll     $v0, 6           # Shift Left Logical
.text:00402B3C                 or      $v1, $v0         # OR
.text:00402B40                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402B44                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B48                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B4C                 sw      $v1, 8($v0)      # Store Word
; Found the 37th break (@00402b50) ; new pc will be 00402cb0
; ========================= BLOCK 37 =========================
.text:00402CB0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402CB4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402CB8                 sll     $v0, 2           # Shift Left Logical
.text:00402CBC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CC0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402CC4                 lw      $v0, 8($v0)      # Load Word
.text:00402CC8                 nor     $v1, $zero, $v0  # NOR
.text:00402CCC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402CD0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CD4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402CD8                 sw      $v1, 8($v0)      # Store Word
; Found the 38th break (@00402cdc) ; new pc will be 004034a4
; ========================= BLOCK 38 =========================
.text:004034A4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004034A8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004034AC                 sll     $v0, 2           # Shift Left Logical
.text:004034B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004034B8                 lw      $v0, 8($v0)      # Load Word
.text:004034BC                 srl     $v1, $v0, 17     # Shift Right Logical
.text:004034C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004034C4                 sll     $v0, 2           # Shift Left Logical
.text:004034C8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034CC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004034D0                 lw      $v0, 8($v0)      # Load Word
.text:004034D4                 sll     $v0, 15          # Shift Left Logical
.text:004034D8                 or      $v1, $v0         # OR
.text:004034DC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004034E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004034E8                 sw      $v1, 8($v0)      # Store Word
; Found the 39th break (@004034ec) ; new pc will be 004037ac
; ========================= BLOCK 39 =========================
.text:004037AC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004037B0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037B4                 sll     $v0, 2           # Shift Left Logical
.text:004037B8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037BC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004037C0                 lw      $v1, 8($v0)      # Load Word
.text:004037C4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037C8                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004037CC                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004037D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037D4                 sll     $v0, 2           # Shift Left Logical
.text:004037D8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037DC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004037E0                 lw      $a1, 8($v0)      # Load Word
.text:004037E4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037E8                 nor     $v0, $zero, $v0  # NOR
.text:004037EC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004037F0                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004037F4                 or      $v1, $v0         # OR
.text:004037F8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004037FC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403800                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403804                 sw      $v1, 8($v0)      # Store Word
; Found the 40th break (@00403808) ; new pc will be 00403550
; ========================= BLOCK 40 =========================
.text:00403550                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403554                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403558                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040355C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403560                 lw      $a0, 8($v0)      # Load Word
.text:00403564                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403568                 xor     $a0, $v0         # Exclusive OR
.text:0040356C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403570                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403574                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403578                 sw      $a0, 8($v0)      # Store Word
; Found the 41th break (@0040357c) ; new pc will be 004030e4
; ========================= BLOCK 41 =========================
.text:004030E4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004030E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030EC                 sll     $v0, 2           # Shift Left Logical
.text:004030F0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004030F8                 lw      $v1, 8($v0)      # Load Word
.text:004030FC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403100                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403104                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403108                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040310C                 sll     $v0, 2           # Shift Left Logical
.text:00403110                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403114                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403118                 lw      $a1, 8($v0)      # Load Word
.text:0040311C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403120                 nor     $v0, $zero, $v0  # NOR
.text:00403124                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403128                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040312C                 or      $v1, $v0         # OR
.text:00403130                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403134                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403138                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040313C                 sw      $v1, 8($v0)      # Store Word
; Found the 42th break (@00403140) ; new pc will be 00402e88
; ========================= BLOCK 42 =========================
.text:00402E88                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402E8C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E90                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E94                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E98                 lw      $a0, 8($v0)      # Load Word
.text:00402E9C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402EA0                 xor     $a0, $v0         # Exclusive OR
.text:00402EA4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402EA8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402EB0                 sw      $a0, 8($v0)      # Store Word
; Found the 43th break (@00402eb4) ; new pc will be 004023f0
; ========================= BLOCK 43 =========================
.text:004023F0                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004023F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004023F8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023FC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402400                 lw      $a0, 8($v0)      # Load Word
.text:00402404                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402408                 addu    $a0, $v0         # Add Unsigned
.text:0040240C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402410                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402414                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402418                 sw      $a0, 8($v0)      # Store Word
; Found the 44th break (@0040241c) ; new pc will be 00402a5c
; ========================= BLOCK 44 =========================
.text:00402A5C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402A60                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A64                 sll     $v0, 2           # Shift Left Logical
.text:00402A68                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A6C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A70                 lw      $v0, 8($v0)      # Load Word
.text:00402A74                 srl     $v1, $v0, 13     # Shift Right Logical
.text:00402A78                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A7C                 sll     $v0, 2           # Shift Left Logical
.text:00402A80                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A84                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402A88                 lw      $v0, 8($v0)      # Load Word
.text:00402A8C                 sll     $v0, 19          # Shift Left Logical
.text:00402A90                 or      $v1, $v0         # OR
.text:00402A94                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402A98                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A9C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402AA0                 sw      $v1, 8($v0)      # Store Word
; Found the 45th break (@00402aa4) ; new pc will be 00402fb4
; ========================= BLOCK 45 =========================
.text:00402FB4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402FB8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FBC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FC0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FC4                 lw      $a0, 8($v0)      # Load Word
.text:00402FC8                 li      $v0, 0xCC4E5D94  # Load Immediate
.text:00402FD0                 xor     $a0, $v0         # Exclusive OR
.text:00402FD4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FD8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FDC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402FE0                 sw      $a0, 8($v0)      # Store Word
; Found the 46th break (@00402fe4) ; new pc will be 00402744
; ========================= BLOCK 46 =========================
.text:00402744                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402748                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040274C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402750                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402754                 lw      $a0, 8($v0)      # Load Word
.text:00402758                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040275C                 subu    $a0, $v0         # Subtract Unsigned
.text:00402760                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402764                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402768                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040276C                 sw      $a0, 8($v0)      # Store Word
; Found the 47th break (@00402770) ; new pc will be 00402518
; ========================= BLOCK 47 =========================
.text:00402518                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040251C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402520                 sll     $v0, 2           # Shift Left Logical
.text:00402524                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402528                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040252C                 lw      $v0, 8($v0)      # Load Word
.text:00402530                 nor     $v1, $zero, $v0  # NOR
.text:00402534                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402538                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040253C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402540                 sw      $v1, 8($v0)      # Store Word
; Found the 48th break (@00402544) ; new pc will be 004025a8
; ========================= BLOCK 48 =========================
.text:004025A8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004025AC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025B0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025B4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025B8                 lw      $a0, 8($v0)      # Load Word
.text:004025BC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004025C0                 addu    $a0, $v0         # Add Unsigned
.text:004025C4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025C8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025CC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004025D0                 sw      $a0, 8($v0)      # Store Word
; Found the 49th break (@004025d4) ; new pc will be 00403778
; ========================= BLOCK 49 =========================
.text:00403778                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040377C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403780                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403784                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403788                 lw      $a0, 8($v0)      # Load Word
.text:0040378C                 li      $v0, 0x6EDC032   # Load Immediate
.text:00403794                 addu    $a0, $v0         # Add Unsigned
.text:00403798                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040379C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004037A4                 sw      $a0, 8($v0)      # Store Word
; Found the 50th break (@004037a8) ; new pc will be 004027d8
; ========================= BLOCK 50 =========================
.text:004027D8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004027DC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004027E8                 lw      $a0, 8($v0)      # Load Word
.text:004027EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004027F0                 subu    $a0, $v0         # Subtract Unsigned
.text:004027F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027F8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027FC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402800                 sw      $a0, 8($v0)      # Store Word
; Found the 51th break (@00402804) ; new pc will be 004028cc
; ========================= BLOCK 51 =========================
.text:004028CC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004028D0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004028D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004028DC                 lw      $a0, 8($v0)      # Load Word
.text:004028E0                 li      $v0, 0x3A2EE307  # Load Immediate
.text:004028E8                 addu    $a0, $v0         # Add Unsigned
.text:004028EC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004028F0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004028F8                 sw      $a0, 8($v0)      # Store Word
; Found the 52th break (@004028fc) ; new pc will be 004033ac
; ========================= BLOCK 52 =========================
.text:004033AC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004033B0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033B4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033B8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004033BC                 lw      $a0, 8($v0)      # Load Word
.text:004033C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004033C4                 addu    $a0, $v0         # Add Unsigned
.text:004033C8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004033D4                 sw      $a0, 8($v0)      # Store Word
; Found the 53th break (@004033d8) ; new pc will be 00402808
; ========================= BLOCK 53 =========================
.text:00402808                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040280C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402810                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402814                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402818                 lw      $a0, 8($v0)      # Load Word
.text:0040281C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402820                 subu    $a0, $v0         # Subtract Unsigned
.text:00402824                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402828                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040282C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402830                 sw      $a0, 8($v0)      # Store Word
; Found the 54th break (@00402834) ; new pc will be 00403098
; ========================= BLOCK 54 =========================
.text:00403098                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040309C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030A0                 sll     $v0, 2           # Shift Left Logical
.text:004030A4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030A8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004030AC                 lw      $v0, 8($v0)      # Load Word
.text:004030B0                 srl     $v1, $v0, 3      # Shift Right Logical
.text:004030B4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030B8                 sll     $v0, 2           # Shift Left Logical
.text:004030BC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030C0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004030C4                 lw      $v0, 8($v0)      # Load Word
.text:004030C8                 sll     $v0, 29          # Shift Left Logical
.text:004030CC                 or      $v1, $v0         # OR
.text:004030D0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004030D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004030DC                 sw      $v1, 8($v0)      # Store Word
; Found the 55th break (@004030e0) ; new pc will be 00402900
; ========================= BLOCK 55 =========================
.text:00402900                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402904                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402908                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040290C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402910                 lw      $a0, 8($v0)      # Load Word
.text:00402914                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402918                 xor     $a0, $v0         # Exclusive OR
.text:0040291C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402920                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402924                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402928                 sw      $a0, 8($v0)      # Store Word
; Found the 56th break (@0040292c) ; new pc will be 00403580
; ========================= BLOCK 56 =========================
.text:00403580                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403584                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403588                 sll     $v0, 2           # Shift Left Logical
.text:0040358C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403590                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403594                 lw      $v0, 8($v0)      # Load Word
.text:00403598                 sll     $v1, $v0, 28     # Shift Left Logical
.text:0040359C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004035A0                 sll     $v0, 2           # Shift Left Logical
.text:004035A4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035A8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004035AC                 lw      $v0, 8($v0)      # Load Word
.text:004035B0                 srl     $v0, 4           # Shift Right Logical
.text:004035B4                 or      $v1, $v0         # OR
.text:004035B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004035BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004035C4                 sw      $v1, 8($v0)      # Store Word
; Found the 57th break (@004035c8) ; new pc will be 0040332c
; ========================= BLOCK 57 =========================
.text:0040332C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403330                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403334                 sll     $v0, 2           # Shift Left Logical
.text:00403338                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040333C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403340                 lw      $v0, 8($v0)      # Load Word
.text:00403344                 sll     $v1, $v0, 31     # Shift Left Logical
.text:00403348                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040334C                 sll     $v0, 2           # Shift Left Logical
.text:00403350                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403354                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403358                 lw      $v0, 8($v0)      # Load Word
.text:0040335C                 srl     $v0, 1           # Shift Right Logical
.text:00403360                 or      $v1, $v0         # OR
.text:00403364                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403368                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040336C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403370                 sw      $v1, 8($v0)      # Store Word
; Found the 58th break (@00403374) ; new pc will be 00403444
; ========================= BLOCK 58 =========================
.text:00403444                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403448                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040344C                 sll     $v0, 2           # Shift Left Logical
.text:00403450                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403454                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403458                 lw      $v1, 8($v0)      # Load Word
.text:0040345C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403460                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403464                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403468                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040346C                 sll     $v0, 2           # Shift Left Logical
.text:00403470                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403474                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403478                 lw      $a1, 8($v0)      # Load Word
.text:0040347C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403480                 nor     $v0, $zero, $v0  # NOR
.text:00403484                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403488                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040348C                 or      $v1, $v0         # OR
.text:00403490                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403494                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403498                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040349C                 sw      $v1, 8($v0)      # Store Word
; Found the 59th break (@004034a0) ; new pc will be 004038b8
; ========================= BLOCK 59 =========================
.text:004038B8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004038BC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038C0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038C4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038C8                 lw      $a0, 8($v0)      # Load Word
.text:004038CC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004038D0                 subu    $a0, $v0         # Subtract Unsigned
.text:004038D4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004038E0                 sw      $a0, 8($v0)      # Store Word
; Found the 60th break (@004038e4) ; new pc will be 00402aa8
; ========================= BLOCK 60 =========================
.text:00402AA8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402AAC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402AB0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AB4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402AB8                 lw      $a0, 8($v0)      # Load Word
.text:00402ABC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402AC0                 xor     $a0, $v0         # Exclusive OR
.text:00402AC4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402AC8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402ACC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402AD0                 sw      $a0, 8($v0)      # Store Word
; Found the 61th break (@00402ad4) ; new pc will be 004029f8
; ========================= BLOCK 61 =========================
.text:004029F8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004029FC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A00                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A04                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402A08                 lw      $a0, 8($v0)      # Load Word
.text:00402A0C                 li      $v0, 0x81674F2B  # Load Immediate
.text:00402A14                 addu    $a0, $v0         # Add Unsigned
.text:00402A18                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A1C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A20                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A24                 sw      $a0, 8($v0)      # Store Word
; Found the 62th break (@00402a28) ; new pc will be 004033dc
; ========================= BLOCK 62 =========================
.text:004033DC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004033E0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033E4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033E8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004033EC                 lw      $a0, 8($v0)      # Load Word
.text:004033F0                 li      $v0, 0xD0358C15  # Load Immediate
.text:004033F8                 addu    $a0, $v0         # Add Unsigned
.text:004033FC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403400                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403404                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403408                 sw      $a0, 8($v0)      # Store Word
; Found the 63th break (@0040340c) ; new pc will be 0040380c
; ========================= BLOCK 63 =========================
.text:0040380C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403810                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403814                 sll     $v0, 2           # Shift Left Logical
.text:00403818                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040381C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403820                 lw      $v0, 8($v0)      # Load Word
.text:00403824                 sll     $v1, $v0, 16     # Shift Left Logical
.text:00403828                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040382C                 sll     $v0, 2           # Shift Left Logical
.text:00403830                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403834                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403838                 lw      $v0, 8($v0)      # Load Word
.text:0040383C                 srl     $v0, 16          # Shift Right Logical
.text:00403840                 or      $v1, $v0         # OR
.text:00403844                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403848                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040384C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403850                 sw      $v1, 8($v0)      # Store Word
; Found the 64th break (@00403854) ; new pc will be 00403520
; ========================= BLOCK 64 =========================
.text:00403520                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403524                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403528                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040352C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403530                 lw      $a0, 8($v0)      # Load Word
.text:00403534                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403538                 xor     $a0, $v0         # Exclusive OR
.text:0040353C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403540                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403544                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403548                 sw      $a0, 8($v0)      # Store Word
; Found the 65th break (@0040354c) ; new pc will be 00402d44
; ========================= BLOCK 65 =========================
.text:00402D44                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D48                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D4C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D50                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D54                 lw      $a0, 8($v0)      # Load Word
.text:00402D58                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402D5C                 addu    $a0, $v0         # Add Unsigned
.text:00402D60                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D64                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D68                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402D6C                 sw      $a0, 8($v0)      # Store Word
; Found the 66th break (@00402d70) ; new pc will be 00402714
; ========================= BLOCK 66 =========================
.text:00402714                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402718                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040271C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402720                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402724                 lw      $a0, 8($v0)      # Load Word
.text:00402728                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040272C                 addu    $a0, $v0         # Add Unsigned
.text:00402730                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402734                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402738                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040273C                 sw      $a0, 8($v0)      # Store Word
; Found the 67th break (@00402740) ; new pc will be 00402ad8
; ========================= BLOCK 67 =========================
.text:00402AD8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402ADC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402AE0                 sll     $v0, 2           # Shift Left Logical
.text:00402AE4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AE8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402AEC                 lw      $v0, 8($v0)      # Load Word
.text:00402AF0                 nor     $v1, $zero, $v0  # NOR
.text:00402AF4                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402AF8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AFC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B00                 sw      $v1, 8($v0)      # Store Word
; Found the 68th break (@00402b04) ; new pc will be 004024cc
; ========================= BLOCK 68 =========================
.text:004024CC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004024D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024D4                 sll     $v0, 2           # Shift Left Logical
.text:004024D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004024E0                 lw      $v0, 8($v0)      # Load Word
.text:004024E4                 sll     $v1, $v0, 30     # Shift Left Logical
.text:004024E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024EC                 sll     $v0, 2           # Shift Left Logical
.text:004024F0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024F4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004024F8                 lw      $v0, 8($v0)      # Load Word
.text:004024FC                 srl     $v0, 2           # Shift Right Logical
.text:00402500                 or      $v1, $v0         # OR
.text:00402504                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402508                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040250C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402510                 sw      $v1, 8($v0)      # Store Word
; Found the 69th break (@00402514) ; new pc will be 004035cc
; ========================= BLOCK 69 =========================
.text:004035CC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004035D0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004035D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004035DC                 lw      $a0, 8($v0)      # Load Word
.text:004035E0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004035E4                 addu    $a0, $v0         # Add Unsigned
.text:004035E8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004035EC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035F0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004035F4                 sw      $a0, 8($v0)      # Store Word
; Found the 70th break (@004035f8) ; new pc will be 00403694
; ========================= BLOCK 70 =========================
.text:00403694                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403698                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040369C                 sll     $v0, 2           # Shift Left Logical
.text:004036A0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036A4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004036A8                 lw      $v0, 8($v0)      # Load Word
.text:004036AC                 sll     $v1, $v0, 6      # Shift Left Logical
.text:004036B0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004036B4                 sll     $v0, 2           # Shift Left Logical
.text:004036B8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036BC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004036C0                 lw      $v0, 8($v0)      # Load Word
.text:004036C4                 srl     $v0, 26          # Shift Right Logical
.text:004036C8                 or      $v1, $v0         # OR
.text:004036CC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004036D0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036D4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004036D8                 sw      $v1, 8($v0)      # Store Word
; Found the 71th break (@004036dc) ; new pc will be 00402eb8
; ========================= BLOCK 71 =========================
.text:00402EB8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402EBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402EC0                 sll     $v0, 2           # Shift Left Logical
.text:00402EC4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402ECC                 lw      $v0, 8($v0)      # Load Word
.text:00402ED0                 sll     $v1, $v0, 18     # Shift Left Logical
.text:00402ED4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402ED8                 sll     $v0, 2           # Shift Left Logical
.text:00402EDC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EE0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402EE4                 lw      $v0, 8($v0)      # Load Word
.text:00402EE8                 srl     $v0, 14          # Shift Right Logical
.text:00402EEC                 or      $v1, $v0         # OR
.text:00402EF0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402EF4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EF8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402EFC                 sw      $v1, 8($v0)      # Store Word
; Found the 72th break (@00402f00) ; new pc will be 00403144
; ========================= BLOCK 72 =========================
.text:00403144                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403148                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040314C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403150                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403154                 lw      $a0, 8($v0)      # Load Word
.text:00403158                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040315C                 addu    $a0, $v0         # Add Unsigned
.text:00403160                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403164                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403168                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040316C                 sw      $a0, 8($v0)      # Store Word
; Found the 73th break (@00403170) ; new pc will be 00402ce0
; ========================= BLOCK 73 =========================
.text:00402CE0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402CE4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402CE8                 sll     $v0, 2           # Shift Left Logical
.text:00402CEC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CF0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402CF4                 lw      $v0, 8($v0)      # Load Word
.text:00402CF8                 nor     $v1, $zero, $v0  # NOR
.text:00402CFC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402D00                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D04                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D08                 sw      $v1, 8($v0)      # Store Word
; Found the 74th break (@00402d0c) ; new pc will be 00403174
; ========================= BLOCK 74 =========================
.text:00403174                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403178                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040317C                 sll     $v0, 2           # Shift Left Logical
.text:00403180                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403184                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403188                 lw      $v1, 8($v0)      # Load Word
.text:0040318C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403190                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403194                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403198                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040319C                 sll     $v0, 2           # Shift Left Logical
.text:004031A0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031A4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004031A8                 lw      $a1, 8($v0)      # Load Word
.text:004031AC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004031B0                 nor     $v0, $zero, $v0  # NOR
.text:004031B4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004031B8                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:004031BC                 or      $v1, $v0         # OR
.text:004031C0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004031C4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031C8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004031CC                 sw      $v1, 8($v0)      # Store Word
; Found the 75th break (@004031d0) ; new pc will be 00403410
; ========================= BLOCK 75 =========================
.text:00403410                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403414                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403418                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040341C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403420                 lw      $a0, 8($v0)      # Load Word
.text:00403424                 li      $v0, 0x192B37D2  # Load Immediate
.text:0040342C                 addu    $a0, $v0         # Add Unsigned
.text:00403430                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403434                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403438                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040343C                 sw      $a0, 8($v0)      # Store Word
; Found the 76th break (@00403440) ; new pc will be 004039ac
; ========================= BLOCK 76 =========================
.text:004039AC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004039B0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004039B4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039B8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004039BC                 lw      $a0, 8($v0)      # Load Word
.text:004039C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004039C4                 addu    $a0, $v0         # Add Unsigned
.text:004039C8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004039CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004039D4                 sw      $a0, 8($v0)      # Store Word
; Found the 77th break (@004039d8) ; new pc will be 00403068
; ========================= BLOCK 77 =========================
.text:00403068                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040306C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403070                 sll     $v0, 2           # Shift Left Logical
.text:00403074                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403078                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040307C                 lw      $v0, 8($v0)      # Load Word
.text:00403080                 nor     $v1, $zero, $v0  # NOR
.text:00403084                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403088                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040308C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403090                 sw      $v1, 8($v0)      # Store Word
; Found the 78th break (@00403094) ; new pc will be 004036e0
; ========================= BLOCK 78 =========================
.text:004036E0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004036E4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004036E8                 sll     $v0, 2           # Shift Left Logical
.text:004036EC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036F0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004036F4                 lw      $v0, 8($v0)      # Load Word
.text:004036F8                 sll     $v1, $v0, 5      # Shift Left Logical
.text:004036FC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403700                 sll     $v0, 2           # Shift Left Logical
.text:00403704                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403708                 addu    $v0, $a1, $v0    # Add Unsigned
.text:0040370C                 lw      $v0, 8($v0)      # Load Word
.text:00403710                 srl     $v0, 27          # Shift Right Logical
.text:00403714                 or      $v1, $v0         # OR
.text:00403718                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040371C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403720                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403724                 sw      $v1, 8($v0)      # Store Word
; Found the 79th break (@00403728) ; new pc will be 00402370
; ========================= BLOCK 79 =========================
.text:00402370                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402374                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402378                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040237C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402380                 lw      $a0, 8($v0)      # Load Word
.text:00402384                 li      $v0, 0x87DD2BC5  # Load Immediate
.text:0040238C                 addu    $a0, $v0         # Add Unsigned
.text:00402390                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402394                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402398                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040239C                 sw      $a0, 8($v0)      # Store Word
; Found the 80th break (@004023a0) ; new pc will be 00402bb8
; ========================= BLOCK 80 =========================
.text:00402BB8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402BBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BC0                 sll     $v0, 2           # Shift Left Logical
.text:00402BC4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402BCC                 lw      $v0, 8($v0)      # Load Word
.text:00402BD0                 srl     $v1, $v0, 21     # Shift Right Logical
.text:00402BD4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BD8                 sll     $v0, 2           # Shift Left Logical
.text:00402BDC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BE0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402BE4                 lw      $v0, 8($v0)      # Load Word
.text:00402BE8                 sll     $v0, 11          # Shift Left Logical
.text:00402BEC                 or      $v1, $v0         # OR
.text:00402BF0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402BF4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BF8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402BFC                 sw      $v1, 8($v0)      # Store Word
; Found the 81th break (@00402c00) ; new pc will be 004027a4
; ========================= BLOCK 81 =========================
.text:004027A4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004027A8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027AC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027B0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004027B4                 lw      $a0, 8($v0)      # Load Word
.text:004027B8                 li      $v0, 0xD0970C74  # Load Immediate
.text:004027C0                 addu    $a0, $v0         # Add Unsigned
.text:004027C4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027C8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027CC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004027D0                 sw      $a0, 8($v0)      # Store Word
; Found the 82th break (@004027d4) ; new pc will be 00403664
; ========================= BLOCK 82 =========================
.text:00403664                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403668                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040366C                 sll     $v0, 2           # Shift Left Logical
.text:00403670                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403674                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403678                 lw      $v0, 8($v0)      # Load Word
.text:0040367C                 nor     $v1, $zero, $v0  # NOR
.text:00403680                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403684                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403688                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040368C                 sw      $v1, 8($v0)      # Store Word
; Found the 83th break (@00403690) ; new pc will be 00402b54
; ========================= BLOCK 83 =========================
.text:00402B54                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402B58                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B5C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B60                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B64                 lw      $a0, 8($v0)      # Load Word
.text:00402B68                 li      $v0, 0x79662B5D  # Load Immediate
.text:00402B70                 addu    $a0, $v0         # Add Unsigned
.text:00402B74                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B78                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B7C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402B80                 sw      $a0, 8($v0)      # Store Word
; Found the 84th break (@00402b84) ; new pc will be 00402e3c
; ========================= BLOCK 84 =========================
.text:00402E3C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402E40                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402E44                 sll     $v0, 2           # Shift Left Logical
.text:00402E48                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E4C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E50                 lw      $v0, 8($v0)      # Load Word
.text:00402E54                 srl     $v1, $v0, 20     # Shift Right Logical
.text:00402E58                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402E5C                 sll     $v0, 2           # Shift Left Logical
.text:00402E60                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E64                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402E68                 lw      $v0, 8($v0)      # Load Word
.text:00402E6C                 sll     $v0, 12          # Shift Left Logical
.text:00402E70                 or      $v1, $v0         # OR
.text:00402E74                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402E78                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E7C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E80                 sw      $v1, 8($v0)      # Store Word
; Found the 85th break (@00402e84) ; new pc will be 00402998
; ========================= BLOCK 85 =========================
.text:00402998                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040299C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029A0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029A4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004029A8                 lw      $a0, 8($v0)      # Load Word
.text:004029AC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004029B0                 subu    $a0, $v0         # Subtract Unsigned
.text:004029B4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029B8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029BC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004029C0                 sw      $a0, 8($v0)      # Store Word
; Found the 86th break (@004029c4) ; new pc will be 004026b4
; ========================= BLOCK 86 =========================
.text:004026B4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004026B8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026BC                 sll     $v0, 2           # Shift Left Logical
.text:004026C0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026C4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004026C8                 lw      $v1, 8($v0)      # Load Word
.text:004026CC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026D0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004026D4                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004026D8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026DC                 sll     $v0, 2           # Shift Left Logical
.text:004026E0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026E4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004026E8                 lw      $a1, 8($v0)      # Load Word
.text:004026EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026F0                 nor     $v0, $zero, $v0  # NOR
.text:004026F4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004026F8                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004026FC                 or      $v1, $v0         # OR
.text:00402700                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402704                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402708                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040270C                 sw      $v1, 8($v0)      # Store Word
; Found the 87th break (@00402710) ; new pc will be 004038e8
; ========================= BLOCK 87 =========================
.text:004038E8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004038EC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038F0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038F4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038F8                 lw      $a0, 8($v0)      # Load Word
.text:004038FC                 li      $v0, 0xDBFA3745  # Load Immediate
.text:00403904                 addu    $a0, $v0         # Add Unsigned
.text:00403908                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040390C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403910                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403914                 sw      $a0, 8($v0)      # Store Word
; Found the 88th break (@00403918) ; new pc will be 00403630
; ========================= BLOCK 88 =========================
.text:00403630                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403634                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403638                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040363C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403640                 lw      $a0, 8($v0)      # Load Word
.text:00403644                 li      $v0, 0x3D68A35C  # Load Immediate
.text:0040364C                 xor     $a0, $v0         # Exclusive OR
.text:00403650                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403654                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403658                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040365C                 sw      $a0, 8($v0)      # Store Word
; Found the 89th break (@00403660) ; new pc will be 00402838
; ========================= BLOCK 89 =========================
.text:00402838                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040283C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402840                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402844                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402848                 lw      $a0, 8($v0)      # Load Word
.text:0040284C                 li      $v0, 0xB65E867F  # Load Immediate
.text:00402854                 addu    $a0, $v0         # Add Unsigned
.text:00402858                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040285C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402860                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402864                 sw      $a0, 8($v0)      # Store Word
; Found the 90th break (@00402868) ; new pc will be 00402f04
; ========================= BLOCK 90 =========================
.text:00402F04                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402F08                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402F0C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F10                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402F14                 lw      $a0, 8($v0)      # Load Word
.text:00402F18                 li      $v0, 0x3ECA6F23  # Load Immediate
.text:00402F20                 addu    $a0, $v0         # Add Unsigned
.text:00402F24                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402F28                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F2C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F30                 sw      $a0, 8($v0)      # Store Word
; Found the 91th break (@00402f34) ; new pc will be 00402450
; ========================= BLOCK 91 =========================
.text:00402450                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402454                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402458                 sll     $v0, 2           # Shift Left Logical
.text:0040245C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402460                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402464                 lw      $v0, 8($v0)      # Load Word
.text:00402468                 sll     $v1, $v0, 13     # Shift Left Logical
.text:0040246C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402470                 sll     $v0, 2           # Shift Left Logical
.text:00402474                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402478                 addu    $v0, $a1, $v0    # Add Unsigned
.text:0040247C                 lw      $v0, 8($v0)      # Load Word
.text:00402480                 srl     $v0, 19          # Shift Right Logical
.text:00402484                 or      $v1, $v0         # OR
.text:00402488                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040248C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402490                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402494                 sw      $v1, 8($v0)      # Store Word
; Found the 92th break (@00402498) ; new pc will be 00403378
; ========================= BLOCK 92 =========================
.text:00403378                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040337C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403380                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403384                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403388                 lw      $a0, 8($v0)      # Load Word
.text:0040338C                 li      $v0, 0xBFD991A0  # Load Immediate
.text:00403394                 xor     $a0, $v0         # Exclusive OR
.text:00403398                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040339C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004033A4                 sw      $a0, 8($v0)      # Store Word
; Found the 93th break (@004033a8) ; new pc will be 0040230c
; ========================= BLOCK 93 =========================
.text:0040230C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402310                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402314                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402318                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040231C                 lw      $a0, 8($v0)      # Load Word
.text:00402320                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402324                 subu    $a0, $v0         # Subtract Unsigned
.text:00402328                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040232C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402330                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402334                 sw      $a0, 8($v0)      # Store Word
; Found the 94th break (@00402338) ; new pc will be 00403858
; ========================= BLOCK 94 =========================
.text:00403858                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040385C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403860                 sll     $v0, 2           # Shift Left Logical
.text:00403864                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403868                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040386C                 lw      $v0, 8($v0)      # Load Word
.text:00403870                 nor     $v1, $zero, $v0  # NOR
.text:00403874                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403878                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040387C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403880                 sw      $v1, 8($v0)      # Store Word
; Found the 95th break (@00403884) ; new pc will be 00402b88
; ========================= BLOCK 95 =========================
.text:00402B88                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402B8C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B90                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B94                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B98                 lw      $a0, 8($v0)      # Load Word
.text:00402B9C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BA0                 subu    $a0, $v0         # Subtract Unsigned
.text:00402BA4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402BA8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402BB0                 sw      $a0, 8($v0)      # Store Word
; Found the 96th break (@00402bb4) ; new pc will be 00402d10
; ========================= BLOCK 96 =========================
.text:00402D10                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D14                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D18                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D1C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D20                 lw      $a0, 8($v0)      # Load Word
.text:00402D24                 li      $v0, 0xA9BE160D  # Load Immediate
.text:00402D2C                 xor     $a0, $v0         # Exclusive OR
.text:00402D30                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D34                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D38                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402D3C                 sw      $a0, 8($v0)      # Store Word
; Found the 97th break (@00402d40) ; new pc will be 0040233c
; ========================= BLOCK 97 =========================
.text:0040233C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402340                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402344                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402348                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040234C                 lw      $a0, 8($v0)      # Load Word
.text:00402350                 li      $v0, 0x7B4DE789  # Load Immediate
.text:00402358                 xor     $a0, $v0         # Exclusive OR
.text:0040235C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402360                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402364                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402368                 sw      $a0, 8($v0)      # Store Word
; Found the 98th break (@0040236c) ; new pc will be 00403204
; ========================= BLOCK 98 =========================
.text:00403204                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403208                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040320C                 sll     $v0, 2           # Shift Left Logical
.text:00403210                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403214                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403218                 lw      $v0, 8($v0)      # Load Word
.text:0040321C                 nor     $v1, $zero, $v0  # NOR
.text:00403220                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403224                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403228                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040322C                 sw      $v1, 8($v0)      # Store Word
; Found the 99th break (@00403230) ; new pc will be 004032cc
; ========================= BLOCK 99 =========================
.text:004032CC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004032D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004032D4                 sll     $v0, 2           # Shift Left Logical
.text:004032D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004032E0                 lw      $v0, 8($v0)      # Load Word
.text:004032E4                 nor     $v1, $zero, $v0  # NOR
.text:004032E8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004032EC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032F0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004032F4                 sw      $v1, 8($v0)      # Store Word
; Found the 100th break (@004032f8) ; new pc will be 004039dc
; ========================= BLOCK 100 =========================
.text:004039DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004039E0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004039E4                 sw      $v0, 0x48+i($fp)  # Store Word
; Found the 0th break (@0040228c) ; new pc will be 00403410
; ========================= BLOCK 0 =========================
.text:00403410                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403414                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403418                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040341C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403420                 lw      $a0, 8($v0)      # Load Word
.text:00403424                 li      $v0, 0x192B37D2  # Load Immediate
.text:0040342C                 addu    $a0, $v0         # Add Unsigned
.text:00403430                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403434                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403438                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040343C                 sw      $a0, 8($v0)      # Store Word
; Found the 1th break (@00403440) ; new pc will be 004032fc
; ========================= BLOCK 1 =========================
.text:004032FC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403300                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403304                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403308                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040330C                 lw      $a0, 8($v0)      # Load Word
.text:00403310                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403314                 xor     $a0, $v0         # Exclusive OR
.text:00403318                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040331C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403320                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403324                 sw      $a0, 8($v0)      # Store Word
; Found the 2th break (@00403328) ; new pc will be 0040391c
; ========================= BLOCK 2 =========================
.text:0040391C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403920                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403924                 sll     $v0, 2           # Shift Left Logical
.text:00403928                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040392C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403930                 lw      $v1, 8($v0)      # Load Word
.text:00403934                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403938                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040393C                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403940                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403944                 sll     $v0, 2           # Shift Left Logical
.text:00403948                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040394C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403950                 lw      $a1, 8($v0)      # Load Word
.text:00403954                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403958                 nor     $v0, $zero, $v0  # NOR
.text:0040395C                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403960                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:00403964                 or      $v1, $v0         # OR
.text:00403968                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040396C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403970                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403974                 sw      $v1, 8($v0)      # Store Word
; Found the 3th break (@00403978) ; new pc will be 00403888
; ========================= BLOCK 3 =========================
.text:00403888                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040388C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403890                 sll     $v0, 2           # Shift Left Logical
.text:00403894                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403898                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040389C                 lw      $v0, 8($v0)      # Load Word
.text:004038A0                 nor     $v1, $zero, $v0  # NOR
.text:004038A4                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004038A8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038AC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038B0                 sw      $v1, 8($v0)      # Store Word
; Found the 4th break (@004038b4) ; new pc will be 0040249c
; ========================= BLOCK 4 =========================
.text:0040249C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004024A0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024A4                 sll     $v0, 2           # Shift Left Logical
.text:004024A8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024AC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004024B0                 lw      $v0, 8($v0)      # Load Word
.text:004024B4                 nor     $v1, $zero, $v0  # NOR
.text:004024B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004024BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004024C4                 sw      $v1, 8($v0)      # Store Word
; Found the 5th break (@004024c8) ; new pc will be 00402714
; ========================= BLOCK 5 =========================
.text:00402714                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402718                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040271C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402720                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402724                 lw      $a0, 8($v0)      # Load Word
.text:00402728                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040272C                 addu    $a0, $v0         # Add Unsigned
.text:00402730                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402734                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402738                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040273C                 sw      $a0, 8($v0)      # Store Word
; Found the 6th break (@00402740) ; new pc will be 00402d44
; ========================= BLOCK 6 =========================
.text:00402D44                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D48                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D4C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D50                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D54                 lw      $a0, 8($v0)      # Load Word
.text:00402D58                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402D5C                 addu    $a0, $v0         # Add Unsigned
.text:00402D60                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D64                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D68                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402D6C                 sw      $a0, 8($v0)      # Store Word
; Found the 7th break (@00402d70) ; new pc will be 00403378
; ========================= BLOCK 7 =========================
.text:00403378                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040337C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403380                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403384                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403388                 lw      $a0, 8($v0)      # Load Word
.text:0040338C                 li      $v0, 0xBFD991A0  # Load Immediate
.text:00403394                 xor     $a0, $v0         # Exclusive OR
.text:00403398                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040339C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004033A4                 sw      $a0, 8($v0)      # Store Word
; Found the 8th break (@004033a8) ; new pc will be 00402654
; ========================= BLOCK 8 =========================
.text:00402654                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402658                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040265C                 sll     $v0, 2           # Shift Left Logical
.text:00402660                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402664                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402668                 lw      $v1, 8($v0)      # Load Word
.text:0040266C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402670                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00402674                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00402678                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040267C                 sll     $v0, 2           # Shift Left Logical
.text:00402680                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402684                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402688                 lw      $a1, 8($v0)      # Load Word
.text:0040268C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402690                 nor     $v0, $zero, $v0  # NOR
.text:00402694                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00402698                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040269C                 or      $v1, $v0         # OR
.text:004026A0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004026A4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026A8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004026AC                 sw      $v1, 8($v0)      # Store Word
; Found the 9th break (@004026b0) ; new pc will be 00402e3c
; ========================= BLOCK 9 =========================
.text:00402E3C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402E40                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402E44                 sll     $v0, 2           # Shift Left Logical
.text:00402E48                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E4C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E50                 lw      $v0, 8($v0)      # Load Word
.text:00402E54                 srl     $v1, $v0, 20     # Shift Right Logical
.text:00402E58                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402E5C                 sll     $v0, 2           # Shift Left Logical
.text:00402E60                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E64                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402E68                 lw      $v0, 8($v0)      # Load Word
.text:00402E6C                 sll     $v0, 12          # Shift Left Logical
.text:00402E70                 or      $v1, $v0         # OR
.text:00402E74                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402E78                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E7C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E80                 sw      $v1, 8($v0)      # Store Word
; Found the 10th break (@00402e84) ; new pc will be 004023f0
; ========================= BLOCK 10 =========================
.text:004023F0                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004023F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004023F8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023FC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402400                 lw      $a0, 8($v0)      # Load Word
.text:00402404                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402408                 addu    $a0, $v0         # Add Unsigned
.text:0040240C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402410                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402414                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402418                 sw      $a0, 8($v0)      # Store Word
; Found the 11th break (@0040241c) ; new pc will be 00402c04
; ========================= BLOCK 11 =========================
.text:00402C04                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402C08                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C0C                 sll     $v0, 2           # Shift Left Logical
.text:00402C10                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C14                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402C18                 lw      $v0, 8($v0)      # Load Word
.text:00402C1C                 srl     $v1, $v0, 4      # Shift Right Logical
.text:00402C20                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C24                 sll     $v0, 2           # Shift Left Logical
.text:00402C28                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C2C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402C30                 lw      $v0, 8($v0)      # Load Word
.text:00402C34                 sll     $v0, 28          # Shift Left Logical
.text:00402C38                 or      $v1, $v0         # OR
.text:00402C3C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402C40                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C44                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402C48                 sw      $v1, 8($v0)      # Store Word
; Found the 12th break (@00402c4c) ; new pc will be 004026b4
; ========================= BLOCK 12 =========================
.text:004026B4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004026B8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026BC                 sll     $v0, 2           # Shift Left Logical
.text:004026C0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026C4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004026C8                 lw      $v1, 8($v0)      # Load Word
.text:004026CC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026D0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004026D4                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004026D8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026DC                 sll     $v0, 2           # Shift Left Logical
.text:004026E0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026E4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004026E8                 lw      $a1, 8($v0)      # Load Word
.text:004026EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026F0                 nor     $v0, $zero, $v0  # NOR
.text:004026F4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004026F8                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004026FC                 or      $v1, $v0         # OR
.text:00402700                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402704                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402708                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040270C                 sw      $v1, 8($v0)      # Store Word
; Found the 13th break (@00402710) ; new pc will be 0040380c
; ========================= BLOCK 13 =========================
.text:0040380C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403810                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403814                 sll     $v0, 2           # Shift Left Logical
.text:00403818                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040381C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403820                 lw      $v0, 8($v0)      # Load Word
.text:00403824                 sll     $v1, $v0, 16     # Shift Left Logical
.text:00403828                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040382C                 sll     $v0, 2           # Shift Left Logical
.text:00403830                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403834                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403838                 lw      $v0, 8($v0)      # Load Word
.text:0040383C                 srl     $v0, 16          # Shift Right Logical
.text:00403840                 or      $v1, $v0         # OR
.text:00403844                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403848                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040384C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403850                 sw      $v1, 8($v0)      # Store Word
; Found the 14th break (@00403854) ; new pc will be 004029c8
; ========================= BLOCK 14 =========================
.text:004029C8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004029CC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029D0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029D4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004029D8                 lw      $a0, 8($v0)      # Load Word
.text:004029DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004029E0                 xor     $a0, $v0         # Exclusive OR
.text:004029E4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029E8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029EC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004029F0                 sw      $a0, 8($v0)      # Store Word
; Found the 15th break (@004029f4) ; new pc will be 00402a5c
; ========================= BLOCK 15 =========================
.text:00402A5C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402A60                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A64                 sll     $v0, 2           # Shift Left Logical
.text:00402A68                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A6C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A70                 lw      $v0, 8($v0)      # Load Word
.text:00402A74                 srl     $v1, $v0, 13     # Shift Right Logical
.text:00402A78                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A7C                 sll     $v0, 2           # Shift Left Logical
.text:00402A80                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A84                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402A88                 lw      $v0, 8($v0)      # Load Word
.text:00402A8C                 sll     $v0, 19          # Shift Left Logical
.text:00402A90                 or      $v1, $v0         # OR
.text:00402A94                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402A98                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A9C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402AA0                 sw      $v1, 8($v0)      # Store Word
; Found the 16th break (@00402aa4) ; new pc will be 004033dc
; ========================= BLOCK 16 =========================
.text:004033DC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004033E0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033E4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033E8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004033EC                 lw      $a0, 8($v0)      # Load Word
.text:004033F0                 li      $v0, 0xD0358C15  # Load Immediate
.text:004033F8                 addu    $a0, $v0         # Add Unsigned
.text:004033FC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403400                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403404                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403408                 sw      $a0, 8($v0)      # Store Word
; Found the 17th break (@0040340c) ; new pc will be 00403234
; ========================= BLOCK 17 =========================
.text:00403234                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403238                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040323C                 sll     $v0, 2           # Shift Left Logical
.text:00403240                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403244                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403248                 lw      $v0, 8($v0)      # Load Word
.text:0040324C                 sll     $v1, $v0, 29     # Shift Left Logical
.text:00403250                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403254                 sll     $v0, 2           # Shift Left Logical
.text:00403258                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040325C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403260                 lw      $v0, 8($v0)      # Load Word
.text:00403264                 srl     $v0, 3           # Shift Right Logical
.text:00403268                 or      $v1, $v0         # OR
.text:0040326C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403270                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403274                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403278                 sw      $v1, 8($v0)      # Store Word
; Found the 18th break (@0040327c) ; new pc will be 00402ce0
; ========================= BLOCK 18 =========================
.text:00402CE0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402CE4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402CE8                 sll     $v0, 2           # Shift Left Logical
.text:00402CEC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CF0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402CF4                 lw      $v0, 8($v0)      # Load Word
.text:00402CF8                 nor     $v1, $zero, $v0  # NOR
.text:00402CFC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402D00                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D04                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D08                 sw      $v1, 8($v0)      # Store Word
; Found the 19th break (@00402d0c) ; new pc will be 0040301c
; ========================= BLOCK 19 =========================
.text:0040301C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403020                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403024                 sll     $v0, 2           # Shift Left Logical
.text:00403028                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040302C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403030                 lw      $v0, 8($v0)      # Load Word
.text:00403034                 srl     $v1, $v0, 8      # Shift Right Logical
.text:00403038                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040303C                 sll     $v0, 2           # Shift Left Logical
.text:00403040                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403044                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403048                 lw      $v0, 8($v0)      # Load Word
.text:0040304C                 sll     $v0, 24          # Shift Left Logical
.text:00403050                 or      $v1, $v0         # OR
.text:00403054                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403058                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040305C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403060                 sw      $v1, 8($v0)      # Store Word
; Found the 20th break (@00403064) ; new pc will be 00403144
; ========================= BLOCK 20 =========================
.text:00403144                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403148                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040314C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403150                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403154                 lw      $a0, 8($v0)      # Load Word
.text:00403158                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040315C                 addu    $a0, $v0         # Add Unsigned
.text:00403160                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403164                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403168                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040316C                 sw      $a0, 8($v0)      # Store Word
; Found the 21th break (@00403170) ; new pc will be 00403098
; ========================= BLOCK 21 =========================
.text:00403098                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040309C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030A0                 sll     $v0, 2           # Shift Left Logical
.text:004030A4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030A8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004030AC                 lw      $v0, 8($v0)      # Load Word
.text:004030B0                 srl     $v1, $v0, 3      # Shift Right Logical
.text:004030B4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030B8                 sll     $v0, 2           # Shift Left Logical
.text:004030BC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030C0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004030C4                 lw      $v0, 8($v0)      # Load Word
.text:004030C8                 sll     $v0, 29          # Shift Left Logical
.text:004030CC                 or      $v1, $v0         # OR
.text:004030D0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004030D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004030DC                 sw      $v1, 8($v0)      # Store Word
; Found the 22th break (@004030e0) ; new pc will be 004028cc
; ========================= BLOCK 22 =========================
.text:004028CC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004028D0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004028D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004028DC                 lw      $a0, 8($v0)      # Load Word
.text:004028E0                 li      $v0, 0x3A2EE307  # Load Immediate
.text:004028E8                 addu    $a0, $v0         # Add Unsigned
.text:004028EC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004028F0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004028F8                 sw      $a0, 8($v0)      # Store Word
; Found the 23th break (@004028fc) ; new pc will be 00402fe8
; ========================= BLOCK 23 =========================
.text:00402FE8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402FEC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FF0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FF4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FF8                 lw      $a0, 8($v0)      # Load Word
.text:00402FFC                 li      $v0, 0x38C1FEB8  # Load Immediate
.text:00403004                 xor     $a0, $v0         # Exclusive OR
.text:00403008                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040300C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403010                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403014                 sw      $a0, 8($v0)      # Store Word
; Found the 24th break (@00403018) ; new pc will be 00403694
; ========================= BLOCK 24 =========================
.text:00403694                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403698                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040369C                 sll     $v0, 2           # Shift Left Logical
.text:004036A0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036A4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004036A8                 lw      $v0, 8($v0)      # Load Word
.text:004036AC                 sll     $v1, $v0, 6      # Shift Left Logical
.text:004036B0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004036B4                 sll     $v0, 2           # Shift Left Logical
.text:004036B8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036BC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004036C0                 lw      $v0, 8($v0)      # Load Word
.text:004036C4                 srl     $v0, 26          # Shift Right Logical
.text:004036C8                 or      $v1, $v0         # OR
.text:004036CC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004036D0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036D4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004036D8                 sw      $v1, 8($v0)      # Store Word
; Found the 25th break (@004036dc) ; new pc will be 00402bb8
; ========================= BLOCK 25 =========================
.text:00402BB8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402BBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BC0                 sll     $v0, 2           # Shift Left Logical
.text:00402BC4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402BCC                 lw      $v0, 8($v0)      # Load Word
.text:00402BD0                 srl     $v1, $v0, 21     # Shift Right Logical
.text:00402BD4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BD8                 sll     $v0, 2           # Shift Left Logical
.text:00402BDC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BE0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402BE4                 lw      $v0, 8($v0)      # Load Word
.text:00402BE8                 sll     $v0, 11          # Shift Left Logical
.text:00402BEC                 or      $v1, $v0         # OR
.text:00402BF0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402BF4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BF8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402BFC                 sw      $v1, 8($v0)      # Store Word
; Found the 26th break (@00402c00) ; new pc will be 00403858
; ========================= BLOCK 26 =========================
.text:00403858                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040385C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403860                 sll     $v0, 2           # Shift Left Logical
.text:00403864                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403868                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040386C                 lw      $v0, 8($v0)      # Load Word
.text:00403870                 nor     $v1, $zero, $v0  # NOR
.text:00403874                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403878                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040387C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403880                 sw      $v1, 8($v0)      # Store Word
; Found the 27th break (@00403884) ; new pc will be 004035cc
; ========================= BLOCK 27 =========================
.text:004035CC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004035D0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004035D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004035DC                 lw      $a0, 8($v0)      # Load Word
.text:004035E0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004035E4                 addu    $a0, $v0         # Add Unsigned
.text:004035E8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004035EC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035F0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004035F4                 sw      $a0, 8($v0)      # Store Word
; Found the 28th break (@004035f8) ; new pc will be 00402370
; ========================= BLOCK 28 =========================
.text:00402370                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402374                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402378                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040237C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402380                 lw      $a0, 8($v0)      # Load Word
.text:00402384                 li      $v0, 0x87DD2BC5  # Load Immediate
.text:0040238C                 addu    $a0, $v0         # Add Unsigned
.text:00402390                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402394                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402398                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040239C                 sw      $a0, 8($v0)      # Store Word
; Found the 29th break (@004023a0) ; new pc will be 00402518
; ========================= BLOCK 29 =========================
.text:00402518                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040251C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402520                 sll     $v0, 2           # Shift Left Logical
.text:00402524                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402528                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040252C                 lw      $v0, 8($v0)      # Load Word
.text:00402530                 nor     $v1, $zero, $v0  # NOR
.text:00402534                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402538                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040253C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402540                 sw      $v1, 8($v0)      # Store Word
; Found the 30th break (@00402544) ; new pc will be 004022c0
; ========================= BLOCK 30 =========================
.text:004022C0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004022C4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022C8                 sll     $v0, 2           # Shift Left Logical
.text:004022CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004022D4                 lw      $v0, 8($v0)      # Load Word
.text:004022D8                 srl     $v1, $v0, 1      # Shift Right Logical
.text:004022DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022E0                 sll     $v0, 2           # Shift Left Logical
.text:004022E4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022E8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004022EC                 lw      $v0, 8($v0)      # Load Word
.text:004022F0                 sll     $v0, 31          # Shift Left Logical
.text:004022F4                 or      $v1, $v0         # OR
.text:004022F8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004022FC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402300                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402304                 sw      $v1, 8($v0)      # Store Word
; Found the 31th break (@00402308) ; new pc will be 00403204
; ========================= BLOCK 31 =========================
.text:00403204                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403208                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040320C                 sll     $v0, 2           # Shift Left Logical
.text:00403210                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403214                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403218                 lw      $v0, 8($v0)      # Load Word
.text:0040321C                 nor     $v1, $zero, $v0  # NOR
.text:00403220                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403224                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403228                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040322C                 sw      $v1, 8($v0)      # Store Word
; Found the 32th break (@00403230) ; new pc will be 00402b88
; ========================= BLOCK 32 =========================
.text:00402B88                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402B8C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B90                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B94                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B98                 lw      $a0, 8($v0)      # Load Word
.text:00402B9C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BA0                 subu    $a0, $v0         # Subtract Unsigned
.text:00402BA4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402BA8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402BB0                 sw      $a0, 8($v0)      # Store Word
; Found the 33th break (@00402bb4) ; new pc will be 004037ac
; ========================= BLOCK 33 =========================
.text:004037AC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004037B0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037B4                 sll     $v0, 2           # Shift Left Logical
.text:004037B8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037BC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004037C0                 lw      $v1, 8($v0)      # Load Word
.text:004037C4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037C8                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004037CC                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004037D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037D4                 sll     $v0, 2           # Shift Left Logical
.text:004037D8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037DC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004037E0                 lw      $a1, 8($v0)      # Load Word
.text:004037E4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037E8                 nor     $v0, $zero, $v0  # NOR
.text:004037EC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004037F0                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004037F4                 or      $v1, $v0         # OR
.text:004037F8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004037FC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403800                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403804                 sw      $v1, 8($v0)      # Store Word
; Found the 34th break (@00403808) ; new pc will be 00402578
; ========================= BLOCK 34 =========================
.text:00402578                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040257C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402580                 sll     $v0, 2           # Shift Left Logical
.text:00402584                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402588                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040258C                 lw      $v0, 8($v0)      # Load Word
.text:00402590                 nor     $v1, $zero, $v0  # NOR
.text:00402594                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402598                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040259C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025A0                 sw      $v1, 8($v0)      # Store Word
; Found the 35th break (@004025a4) ; new pc will be 0040372c
; ========================= BLOCK 35 =========================
.text:0040372C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403730                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403734                 sll     $v0, 2           # Shift Left Logical
.text:00403738                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040373C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403740                 lw      $v0, 8($v0)      # Load Word
.text:00403744                 sll     $v1, $v0, 5      # Shift Left Logical
.text:00403748                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040374C                 sll     $v0, 2           # Shift Left Logical
.text:00403750                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403754                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403758                 lw      $v0, 8($v0)      # Load Word
.text:0040375C                 srl     $v0, 27          # Shift Right Logical
.text:00403760                 or      $v1, $v0         # OR
.text:00403764                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403768                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040376C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403770                 sw      $v1, 8($v0)      # Store Word
; Found the 36th break (@00403774) ; new pc will be 0040332c
; ========================= BLOCK 36 =========================
.text:0040332C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403330                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403334                 sll     $v0, 2           # Shift Left Logical
.text:00403338                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040333C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403340                 lw      $v0, 8($v0)      # Load Word
.text:00403344                 sll     $v1, $v0, 31     # Shift Left Logical
.text:00403348                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040334C                 sll     $v0, 2           # Shift Left Logical
.text:00403350                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403354                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403358                 lw      $v0, 8($v0)      # Load Word
.text:0040335C                 srl     $v0, 1           # Shift Right Logical
.text:00403360                 or      $v1, $v0         # OR
.text:00403364                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403368                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040336C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403370                 sw      $v1, 8($v0)      # Store Word
; Found the 37th break (@00403374) ; new pc will be 00402e08
; ========================= BLOCK 37 =========================
.text:00402E08                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402E0C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E10                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E14                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E18                 lw      $a0, 8($v0)      # Load Word
.text:00402E1C                 li      $v0, 0x73C69F47  # Load Immediate
.text:00402E24                 addu    $a0, $v0         # Add Unsigned
.text:00402E28                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E2C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E30                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E34                 sw      $a0, 8($v0)      # Store Word
; Found the 38th break (@00402e38) ; new pc will be 00402548
; ========================= BLOCK 38 =========================
.text:00402548                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040254C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402550                 sll     $v0, 2           # Shift Left Logical
.text:00402554                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402558                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040255C                 lw      $v0, 8($v0)      # Load Word
.text:00402560                 nor     $v1, $zero, $v0  # NOR
.text:00402564                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402568                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040256C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402570                 sw      $v1, 8($v0)      # Store Word
; Found the 39th break (@00402574) ; new pc will be 004032cc
; ========================= BLOCK 39 =========================
.text:004032CC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004032D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004032D4                 sll     $v0, 2           # Shift Left Logical
.text:004032D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004032E0                 lw      $v0, 8($v0)      # Load Word
.text:004032E4                 nor     $v1, $zero, $v0  # NOR
.text:004032E8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004032EC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032F0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004032F4                 sw      $v1, 8($v0)      # Store Word
; Found the 40th break (@004032f8) ; new pc will be 00402744
; ========================= BLOCK 40 =========================
.text:00402744                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402748                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040274C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402750                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402754                 lw      $a0, 8($v0)      # Load Word
.text:00402758                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040275C                 subu    $a0, $v0         # Subtract Unsigned
.text:00402760                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402764                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402768                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040276C                 sw      $a0, 8($v0)      # Store Word
; Found the 41th break (@00402770) ; new pc will be 00402dd8
; ========================= BLOCK 41 =========================
.text:00402DD8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402DDC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DE0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DE4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402DE8                 lw      $a0, 8($v0)      # Load Word
.text:00402DEC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402DF0                 subu    $a0, $v0         # Subtract Unsigned
.text:00402DF4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DF8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DFC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E00                 sw      $a0, 8($v0)      # Store Word
; Found the 42th break (@00402e04) ; new pc will be 00402838
; ========================= BLOCK 42 =========================
.text:00402838                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040283C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402840                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402844                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402848                 lw      $a0, 8($v0)      # Load Word
.text:0040284C                 li      $v0, 0xB65E867F  # Load Immediate
.text:00402854                 addu    $a0, $v0         # Add Unsigned
.text:00402858                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040285C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402860                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402864                 sw      $a0, 8($v0)      # Store Word
; Found the 43th break (@00402868) ; new pc will be 00402ad8
; ========================= BLOCK 43 =========================
.text:00402AD8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402ADC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402AE0                 sll     $v0, 2           # Shift Left Logical
.text:00402AE4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AE8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402AEC                 lw      $v0, 8($v0)      # Load Word
.text:00402AF0                 nor     $v1, $zero, $v0  # NOR
.text:00402AF4                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402AF8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AFC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B00                 sw      $v1, 8($v0)      # Store Word
; Found the 44th break (@00402b04) ; new pc will be 00402cb0
; ========================= BLOCK 44 =========================
.text:00402CB0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402CB4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402CB8                 sll     $v0, 2           # Shift Left Logical
.text:00402CBC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CC0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402CC4                 lw      $v0, 8($v0)      # Load Word
.text:00402CC8                 nor     $v1, $zero, $v0  # NOR
.text:00402CCC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402CD0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CD4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402CD8                 sw      $v1, 8($v0)      # Store Word
; Found the 45th break (@00402cdc) ; new pc will be 00402964
; ========================= BLOCK 45 =========================
.text:00402964                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402968                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040296C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402970                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402974                 lw      $a0, 8($v0)      # Load Word
.text:00402978                 li      $v0, 0x737F298   # Load Immediate
.text:00402980                 addu    $a0, $v0         # Add Unsigned
.text:00402984                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402988                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040298C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402990                 sw      $a0, 8($v0)      # Store Word
; Found the 46th break (@00402994) ; new pc will be 0040286c
; ========================= BLOCK 46 =========================
.text:0040286C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402870                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402874                 sll     $v0, 2           # Shift Left Logical
.text:00402878                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040287C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402880                 lw      $v1, 8($v0)      # Load Word
.text:00402884                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402888                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040288C                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00402890                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402894                 sll     $v0, 2           # Shift Left Logical
.text:00402898                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040289C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004028A0                 lw      $a1, 8($v0)      # Load Word
.text:004028A4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004028A8                 nor     $v0, $zero, $v0  # NOR
.text:004028AC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004028B0                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004028B4                 or      $v1, $v0         # OR
.text:004028B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004028BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004028C4                 sw      $v1, 8($v0)      # Store Word
; Found the 47th break (@004028c8) ; new pc will be 00402f68
; ========================= BLOCK 47 =========================
.text:00402F68                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402F6C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F70                 sll     $v0, 2           # Shift Left Logical
.text:00402F74                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F78                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F7C                 lw      $v0, 8($v0)      # Load Word
.text:00402F80                 sll     $v1, $v0, 23     # Shift Left Logical
.text:00402F84                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F88                 sll     $v0, 2           # Shift Left Logical
.text:00402F8C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F90                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402F94                 lw      $v0, 8($v0)      # Load Word
.text:00402F98                 srl     $v0, 9           # Shift Right Logical
.text:00402F9C                 or      $v1, $v0         # OR
.text:00402FA0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402FA4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FA8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FAC                 sw      $v1, 8($v0)      # Store Word
; Found the 48th break (@00402fb0) ; new pc will be 00402d10
; ========================= BLOCK 48 =========================
.text:00402D10                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D14                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D18                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D1C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D20                 lw      $a0, 8($v0)      # Load Word
.text:00402D24                 li      $v0, 0xA9BE160D  # Load Immediate
.text:00402D2C                 xor     $a0, $v0         # Exclusive OR
.text:00402D30                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D34                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D38                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402D3C                 sw      $a0, 8($v0)      # Store Word
; Found the 49th break (@00402d40) ; new pc will be 004036e0
; ========================= BLOCK 49 =========================
.text:004036E0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004036E4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004036E8                 sll     $v0, 2           # Shift Left Logical
.text:004036EC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036F0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004036F4                 lw      $v0, 8($v0)      # Load Word
.text:004036F8                 sll     $v1, $v0, 5      # Shift Left Logical
.text:004036FC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403700                 sll     $v0, 2           # Shift Left Logical
.text:00403704                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403708                 addu    $v0, $a1, $v0    # Add Unsigned
.text:0040370C                 lw      $v0, 8($v0)      # Load Word
.text:00403710                 srl     $v0, 27          # Shift Right Logical
.text:00403714                 or      $v1, $v0         # OR
.text:00403718                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040371C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403720                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403724                 sw      $v1, 8($v0)      # Store Word
; Found the 50th break (@00403728) ; new pc will be 0040230c
; ========================= BLOCK 50 =========================
.text:0040230C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402310                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402314                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402318                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040231C                 lw      $a0, 8($v0)      # Load Word
.text:00402320                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402324                 subu    $a0, $v0         # Subtract Unsigned
.text:00402328                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040232C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402330                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402334                 sw      $a0, 8($v0)      # Store Word
; Found the 51th break (@00402338) ; new pc will be 00402450
; ========================= BLOCK 51 =========================
.text:00402450                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402454                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402458                 sll     $v0, 2           # Shift Left Logical
.text:0040245C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402460                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402464                 lw      $v0, 8($v0)      # Load Word
.text:00402468                 sll     $v1, $v0, 13     # Shift Left Logical
.text:0040246C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402470                 sll     $v0, 2           # Shift Left Logical
.text:00402474                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402478                 addu    $v0, $a1, $v0    # Add Unsigned
.text:0040247C                 lw      $v0, 8($v0)      # Load Word
.text:00402480                 srl     $v0, 19          # Shift Right Logical
.text:00402484                 or      $v1, $v0         # OR
.text:00402488                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040248C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402490                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402494                 sw      $v1, 8($v0)      # Store Word
; Found the 52th break (@00402498) ; new pc will be 004027d8
; ========================= BLOCK 52 =========================
.text:004027D8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004027DC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004027E8                 lw      $a0, 8($v0)      # Load Word
.text:004027EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004027F0                 subu    $a0, $v0         # Subtract Unsigned
.text:004027F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027F8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027FC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402800                 sw      $a0, 8($v0)      # Store Word
; Found the 53th break (@00402804) ; new pc will be 00403068
; ========================= BLOCK 53 =========================
.text:00403068                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040306C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403070                 sll     $v0, 2           # Shift Left Logical
.text:00403074                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403078                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040307C                 lw      $v0, 8($v0)      # Load Word
.text:00403080                 nor     $v1, $zero, $v0  # NOR
.text:00403084                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403088                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040308C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403090                 sw      $v1, 8($v0)      # Store Word
; Found the 54th break (@00403094) ; new pc will be 00403580
; ========================= BLOCK 54 =========================
.text:00403580                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403584                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403588                 sll     $v0, 2           # Shift Left Logical
.text:0040358C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403590                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403594                 lw      $v0, 8($v0)      # Load Word
.text:00403598                 sll     $v1, $v0, 28     # Shift Left Logical
.text:0040359C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004035A0                 sll     $v0, 2           # Shift Left Logical
.text:004035A4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035A8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004035AC                 lw      $v0, 8($v0)      # Load Word
.text:004035B0                 srl     $v0, 4           # Shift Right Logical
.text:004035B4                 or      $v1, $v0         # OR
.text:004035B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004035BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004035C4                 sw      $v1, 8($v0)      # Store Word
; Found the 55th break (@004035c8) ; new pc will be 00402808
; ========================= BLOCK 55 =========================
.text:00402808                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040280C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402810                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402814                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402818                 lw      $a0, 8($v0)      # Load Word
.text:0040281C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402820                 subu    $a0, $v0         # Subtract Unsigned
.text:00402824                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402828                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040282C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402830                 sw      $a0, 8($v0)      # Store Word
; Found the 56th break (@00402834) ; new pc will be 00403550
; ========================= BLOCK 56 =========================
.text:00403550                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403554                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403558                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040355C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403560                 lw      $a0, 8($v0)      # Load Word
.text:00403564                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403568                 xor     $a0, $v0         # Exclusive OR
.text:0040356C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403570                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403574                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403578                 sw      $a0, 8($v0)      # Store Word
; Found the 57th break (@0040357c) ; new pc will be 004033ac
; ========================= BLOCK 57 =========================
.text:004033AC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004033B0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033B4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033B8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004033BC                 lw      $a0, 8($v0)      # Load Word
.text:004033C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004033C4                 addu    $a0, $v0         # Add Unsigned
.text:004033C8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004033D4                 sw      $a0, 8($v0)      # Store Word
; Found the 58th break (@004033d8) ; new pc will be 004029f8
; ========================= BLOCK 58 =========================
.text:004029F8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004029FC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A00                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A04                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402A08                 lw      $a0, 8($v0)      # Load Word
.text:00402A0C                 li      $v0, 0x81674F2B  # Load Immediate
.text:00402A14                 addu    $a0, $v0         # Add Unsigned
.text:00402A18                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A1C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A20                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A24                 sw      $a0, 8($v0)      # Store Word
; Found the 59th break (@00402a28) ; new pc will be 0040233c
; ========================= BLOCK 59 =========================
.text:0040233C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402340                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402344                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402348                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040234C                 lw      $a0, 8($v0)      # Load Word
.text:00402350                 li      $v0, 0x7B4DE789  # Load Immediate
.text:00402358                 xor     $a0, $v0         # Exclusive OR
.text:0040235C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402360                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402364                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402368                 sw      $a0, 8($v0)      # Store Word
; Found the 60th break (@0040236c) ; new pc will be 00403174
; ========================= BLOCK 60 =========================
.text:00403174                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403178                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040317C                 sll     $v0, 2           # Shift Left Logical
.text:00403180                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403184                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403188                 lw      $v1, 8($v0)      # Load Word
.text:0040318C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403190                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403194                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403198                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040319C                 sll     $v0, 2           # Shift Left Logical
.text:004031A0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031A4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004031A8                 lw      $a1, 8($v0)      # Load Word
.text:004031AC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004031B0                 nor     $v0, $zero, $v0  # NOR
.text:004031B4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004031B8                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:004031BC                 or      $v1, $v0         # OR
.text:004031C0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004031C4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031C8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004031CC                 sw      $v1, 8($v0)      # Store Word
; Found the 61th break (@004031d0) ; new pc will be 00403630
; ========================= BLOCK 61 =========================
.text:00403630                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403634                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403638                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040363C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403640                 lw      $a0, 8($v0)      # Load Word
.text:00403644                 li      $v0, 0x3D68A35C  # Load Immediate
.text:0040364C                 xor     $a0, $v0         # Exclusive OR
.text:00403650                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403654                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403658                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040365C                 sw      $a0, 8($v0)      # Store Word
; Found the 62th break (@00403660) ; new pc will be 00403778
; ========================= BLOCK 62 =========================
.text:00403778                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040377C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403780                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403784                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403788                 lw      $a0, 8($v0)      # Load Word
.text:0040378C                 li      $v0, 0x6EDC032   # Load Immediate
.text:00403794                 addu    $a0, $v0         # Add Unsigned
.text:00403798                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040379C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004037A4                 sw      $a0, 8($v0)      # Store Word
; Found the 63th break (@004037a8) ; new pc will be 00403520
; ========================= BLOCK 63 =========================
.text:00403520                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403524                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403528                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040352C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403530                 lw      $a0, 8($v0)      # Load Word
.text:00403534                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403538                 xor     $a0, $v0         # Exclusive OR
.text:0040353C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403540                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403544                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403548                 sw      $a0, 8($v0)      # Store Word
; Found the 64th break (@0040354c) ; new pc will be 004034f0
; ========================= BLOCK 64 =========================
.text:004034F0                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004034F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004034F8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034FC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403500                 lw      $a0, 8($v0)      # Load Word
.text:00403504                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403508                 addu    $a0, $v0         # Add Unsigned
.text:0040350C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403510                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403514                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403518                 sw      $a0, 8($v0)      # Store Word
; Found the 65th break (@0040351c) ; new pc will be 004039ac
; ========================= BLOCK 65 =========================
.text:004039AC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004039B0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004039B4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039B8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004039BC                 lw      $a0, 8($v0)      # Load Word
.text:004039C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004039C4                 addu    $a0, $v0         # Add Unsigned
.text:004039C8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004039CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004039D4                 sw      $a0, 8($v0)      # Store Word
; Found the 66th break (@004039d8) ; new pc will be 00402fb4
; ========================= BLOCK 66 =========================
.text:00402FB4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402FB8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FBC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FC0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FC4                 lw      $a0, 8($v0)      # Load Word
.text:00402FC8                 li      $v0, 0xCC4E5D94  # Load Immediate
.text:00402FD0                 xor     $a0, $v0         # Exclusive OR
.text:00402FD4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FD8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FDC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402FE0                 sw      $a0, 8($v0)      # Store Word
; Found the 67th break (@00402fe4) ; new pc will be 004025a8
; ========================= BLOCK 67 =========================
.text:004025A8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004025AC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025B0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025B4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025B8                 lw      $a0, 8($v0)      # Load Word
.text:004025BC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004025C0                 addu    $a0, $v0         # Add Unsigned
.text:004025C4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025C8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025CC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004025D0                 sw      $a0, 8($v0)      # Store Word
; Found the 68th break (@004025d4) ; new pc will be 00402a2c
; ========================= BLOCK 68 =========================
.text:00402A2C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402A30                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A34                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A38                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402A3C                 lw      $a0, 8($v0)      # Load Word
.text:00402A40                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A44                 subu    $a0, $v0         # Subtract Unsigned
.text:00402A48                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A4C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A50                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A54                 sw      $a0, 8($v0)      # Store Word
; Found the 69th break (@00402a58) ; new pc will be 004025d8
; ========================= BLOCK 69 =========================
.text:004025D8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004025DC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025E8                 lw      $a0, 8($v0)      # Load Word
.text:004025EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004025F0                 addu    $a0, $v0         # Add Unsigned
.text:004025F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025F8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025FC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402600                 sw      $a0, 8($v0)      # Store Word
; Found the 70th break (@00402604) ; new pc will be 00402f38
; ========================= BLOCK 70 =========================
.text:00402F38                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402F3C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F40                 sll     $v0, 2           # Shift Left Logical
.text:00402F44                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F48                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F4C                 lw      $v0, 8($v0)      # Load Word
.text:00402F50                 nor     $v1, $zero, $v0  # NOR
.text:00402F54                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402F58                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F5C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402F60                 sw      $v1, 8($v0)      # Store Word
; Found the 71th break (@00402f64) ; new pc will be 00402b08
; ========================= BLOCK 71 =========================
.text:00402B08                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402B0C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402B10                 sll     $v0, 2           # Shift Left Logical
.text:00402B14                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B18                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402B1C                 lw      $v0, 8($v0)      # Load Word
.text:00402B20                 srl     $v1, $v0, 26     # Shift Right Logical
.text:00402B24                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402B28                 sll     $v0, 2           # Shift Left Logical
.text:00402B2C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B30                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402B34                 lw      $v0, 8($v0)      # Load Word
.text:00402B38                 sll     $v0, 6           # Shift Left Logical
.text:00402B3C                 or      $v1, $v0         # OR
.text:00402B40                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402B44                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B48                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B4C                 sw      $v1, 8($v0)      # Store Word
; Found the 72th break (@00402b50) ; new pc will be 00402e88
; ========================= BLOCK 72 =========================
.text:00402E88                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402E8C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E90                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E94                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E98                 lw      $a0, 8($v0)      # Load Word
.text:00402E9C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402EA0                 xor     $a0, $v0         # Exclusive OR
.text:00402EA4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402EA8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402EB0                 sw      $a0, 8($v0)      # Store Word
; Found the 73th break (@00402eb4) ; new pc will be 00402da8
; ========================= BLOCK 73 =========================
.text:00402DA8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402DAC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DB0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DB4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402DB8                 lw      $a0, 8($v0)      # Load Word
.text:00402DBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402DC0                 xor     $a0, $v0         # Exclusive OR
.text:00402DC4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DC8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DCC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402DD0                 sw      $a0, 8($v0)      # Store Word
; Found the 74th break (@00402dd4) ; new pc will be 00402290
; ========================= BLOCK 74 =========================
.text:00402290                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402294                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402298                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040229C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004022A0                 lw      $a0, 8($v0)      # Load Word
.text:004022A4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022A8                 subu    $a0, $v0         # Subtract Unsigned
.text:004022AC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004022B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004022B8                 sw      $a0, 8($v0)      # Store Word
; Found the 75th break (@004022bc) ; new pc will be 00402eb8
; ========================= BLOCK 75 =========================
.text:00402EB8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402EBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402EC0                 sll     $v0, 2           # Shift Left Logical
.text:00402EC4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402ECC                 lw      $v0, 8($v0)      # Load Word
.text:00402ED0                 sll     $v1, $v0, 18     # Shift Left Logical
.text:00402ED4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402ED8                 sll     $v0, 2           # Shift Left Logical
.text:00402EDC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EE0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402EE4                 lw      $v0, 8($v0)      # Load Word
.text:00402EE8                 srl     $v0, 14          # Shift Right Logical
.text:00402EEC                 or      $v1, $v0         # OR
.text:00402EF0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402EF4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EF8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402EFC                 sw      $v1, 8($v0)      # Store Word
; Found the 76th break (@00402f00) ; new pc will be 00402608
; ========================= BLOCK 76 =========================
.text:00402608                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040260C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402610                 sll     $v0, 2           # Shift Left Logical
.text:00402614                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402618                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040261C                 lw      $v0, 8($v0)      # Load Word
.text:00402620                 srl     $v1, $v0, 23     # Shift Right Logical
.text:00402624                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402628                 sll     $v0, 2           # Shift Left Logical
.text:0040262C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402630                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402634                 lw      $v0, 8($v0)      # Load Word
.text:00402638                 sll     $v0, 9           # Shift Left Logical
.text:0040263C                 or      $v1, $v0         # OR
.text:00402640                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402644                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402648                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040264C                 sw      $v1, 8($v0)      # Store Word
; Found the 77th break (@00402650) ; new pc will be 00402f04
; ========================= BLOCK 77 =========================
.text:00402F04                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402F08                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402F0C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F10                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402F14                 lw      $a0, 8($v0)      # Load Word
.text:00402F18                 li      $v0, 0x3ECA6F23  # Load Immediate
.text:00402F20                 addu    $a0, $v0         # Add Unsigned
.text:00402F24                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402F28                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F2C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F30                 sw      $a0, 8($v0)      # Store Word
; Found the 78th break (@00402f34) ; new pc will be 00402c50
; ========================= BLOCK 78 =========================
.text:00402C50                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402C54                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C58                 sll     $v0, 2           # Shift Left Logical
.text:00402C5C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C60                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402C64                 lw      $v1, 8($v0)      # Load Word
.text:00402C68                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C6C                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00402C70                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00402C74                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C78                 sll     $v0, 2           # Shift Left Logical
.text:00402C7C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C80                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402C84                 lw      $a1, 8($v0)      # Load Word
.text:00402C88                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C8C                 nor     $v0, $zero, $v0  # NOR
.text:00402C90                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00402C94                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:00402C98                 or      $v1, $v0         # OR
.text:00402C9C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402CA0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CA4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402CA8                 sw      $v1, 8($v0)      # Store Word
; Found the 79th break (@00402cac) ; new pc will be 004035fc
; ========================= BLOCK 79 =========================
.text:004035FC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403600                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403604                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403608                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040360C                 lw      $a0, 8($v0)      # Load Word
.text:00403610                 li      $v0, 0x8103D046  # Load Immediate
.text:00403618                 xor     $a0, $v0         # Exclusive OR
.text:0040361C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403620                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403624                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403628                 sw      $a0, 8($v0)      # Store Word
; Found the 80th break (@0040362c) ; new pc will be 004038b8
; ========================= BLOCK 80 =========================
.text:004038B8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004038BC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038C0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038C4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038C8                 lw      $a0, 8($v0)      # Load Word
.text:004038CC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004038D0                 subu    $a0, $v0         # Subtract Unsigned
.text:004038D4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004038E0                 sw      $a0, 8($v0)      # Store Word
; Found the 81th break (@004038e4) ; new pc will be 004034a4
; ========================= BLOCK 81 =========================
.text:004034A4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004034A8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004034AC                 sll     $v0, 2           # Shift Left Logical
.text:004034B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004034B8                 lw      $v0, 8($v0)      # Load Word
.text:004034BC                 srl     $v1, $v0, 17     # Shift Right Logical
.text:004034C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004034C4                 sll     $v0, 2           # Shift Left Logical
.text:004034C8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034CC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004034D0                 lw      $v0, 8($v0)      # Load Word
.text:004034D4                 sll     $v0, 15          # Shift Left Logical
.text:004034D8                 or      $v1, $v0         # OR
.text:004034DC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004034E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004034E8                 sw      $v1, 8($v0)      # Store Word
; Found the 82th break (@004034ec) ; new pc will be 004027a4
; ========================= BLOCK 82 =========================
.text:004027A4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004027A8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027AC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027B0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004027B4                 lw      $a0, 8($v0)      # Load Word
.text:004027B8                 li      $v0, 0xD0970C74  # Load Immediate
.text:004027C0                 addu    $a0, $v0         # Add Unsigned
.text:004027C4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027C8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027CC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004027D0                 sw      $a0, 8($v0)      # Store Word
; Found the 83th break (@004027d4) ; new pc will be 00403664
; ========================= BLOCK 83 =========================
.text:00403664                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403668                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040366C                 sll     $v0, 2           # Shift Left Logical
.text:00403670                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403674                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403678                 lw      $v0, 8($v0)      # Load Word
.text:0040367C                 nor     $v1, $zero, $v0  # NOR
.text:00403680                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403684                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403688                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040368C                 sw      $v1, 8($v0)      # Store Word
; Found the 84th break (@00403690) ; new pc will be 004031d4
; ========================= BLOCK 84 =========================
.text:004031D4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004031D8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004031DC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031E0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004031E4                 lw      $a0, 8($v0)      # Load Word
.text:004031E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004031EC                 xor     $a0, $v0         # Exclusive OR
.text:004031F0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004031F4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031F8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004031FC                 sw      $a0, 8($v0)      # Store Word
; Found the 85th break (@00403200) ; new pc will be 00402b54
; ========================= BLOCK 85 =========================
.text:00402B54                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402B58                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B5C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B60                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B64                 lw      $a0, 8($v0)      # Load Word
.text:00402B68                 li      $v0, 0x79662B5D  # Load Immediate
.text:00402B70                 addu    $a0, $v0         # Add Unsigned
.text:00402B74                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B78                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B7C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402B80                 sw      $a0, 8($v0)      # Store Word
; Found the 86th break (@00402b84) ; new pc will be 004023a4
; ========================= BLOCK 86 =========================
.text:004023A4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004023A8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004023AC                 sll     $v0, 2           # Shift Left Logical
.text:004023B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004023B8                 lw      $v0, 8($v0)      # Load Word
.text:004023BC                 srl     $v1, $v0, 12     # Shift Right Logical
.text:004023C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004023C4                 sll     $v0, 2           # Shift Left Logical
.text:004023C8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023CC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004023D0                 lw      $v0, 8($v0)      # Load Word
.text:004023D4                 sll     $v0, 20          # Shift Left Logical
.text:004023D8                 or      $v1, $v0         # OR
.text:004023DC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004023E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004023E8                 sw      $v1, 8($v0)      # Store Word
; Found the 87th break (@004023ec) ; new pc will be 00402998
; ========================= BLOCK 87 =========================
.text:00402998                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040299C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029A0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029A4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004029A8                 lw      $a0, 8($v0)      # Load Word
.text:004029AC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004029B0                 subu    $a0, $v0         # Subtract Unsigned
.text:004029B4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029B8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029BC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004029C0                 sw      $a0, 8($v0)      # Store Word
; Found the 88th break (@004029c4) ; new pc will be 004024cc
; ========================= BLOCK 88 =========================
.text:004024CC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004024D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024D4                 sll     $v0, 2           # Shift Left Logical
.text:004024D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004024E0                 lw      $v0, 8($v0)      # Load Word
.text:004024E4                 sll     $v1, $v0, 30     # Shift Left Logical
.text:004024E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024EC                 sll     $v0, 2           # Shift Left Logical
.text:004024F0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024F4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004024F8                 lw      $v0, 8($v0)      # Load Word
.text:004024FC                 srl     $v0, 2           # Shift Right Logical
.text:00402500                 or      $v1, $v0         # OR
.text:00402504                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402508                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040250C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402510                 sw      $v1, 8($v0)      # Store Word
; Found the 89th break (@00402514) ; new pc will be 004030e4
; ========================= BLOCK 89 =========================
.text:004030E4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004030E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030EC                 sll     $v0, 2           # Shift Left Logical
.text:004030F0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004030F8                 lw      $v1, 8($v0)      # Load Word
.text:004030FC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403100                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403104                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403108                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040310C                 sll     $v0, 2           # Shift Left Logical
.text:00403110                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403114                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403118                 lw      $a1, 8($v0)      # Load Word
.text:0040311C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403120                 nor     $v0, $zero, $v0  # NOR
.text:00403124                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403128                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040312C                 or      $v1, $v0         # OR
.text:00403130                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403134                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403138                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040313C                 sw      $v1, 8($v0)      # Store Word
; Found the 90th break (@00403140) ; new pc will be 00403444
; ========================= BLOCK 90 =========================
.text:00403444                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403448                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040344C                 sll     $v0, 2           # Shift Left Logical
.text:00403450                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403454                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403458                 lw      $v1, 8($v0)      # Load Word
.text:0040345C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403460                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403464                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403468                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040346C                 sll     $v0, 2           # Shift Left Logical
.text:00403470                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403474                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403478                 lw      $a1, 8($v0)      # Load Word
.text:0040347C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403480                 nor     $v0, $zero, $v0  # NOR
.text:00403484                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403488                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040348C                 or      $v1, $v0         # OR
.text:00403490                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403494                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403498                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040349C                 sw      $v1, 8($v0)      # Store Word
; Found the 91th break (@004034a0) ; new pc will be 004038e8
; ========================= BLOCK 91 =========================
.text:004038E8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004038EC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038F0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038F4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038F8                 lw      $a0, 8($v0)      # Load Word
.text:004038FC                 li      $v0, 0xDBFA3745  # Load Immediate
.text:00403904                 addu    $a0, $v0         # Add Unsigned
.text:00403908                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040390C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403910                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403914                 sw      $a0, 8($v0)      # Store Word
; Found the 92th break (@00403918) ; new pc will be 00402d74
; ========================= BLOCK 92 =========================
.text:00402D74                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D78                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D7C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D80                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D84                 lw      $a0, 8($v0)      # Load Word
.text:00402D88                 li      $v0, 0xD45CEF0A  # Load Immediate
.text:00402D90                 addu    $a0, $v0         # Add Unsigned
.text:00402D94                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D98                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D9C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402DA0                 sw      $a0, 8($v0)      # Store Word
; Found the 93th break (@00402da4) ; new pc will be 00402420
; ========================= BLOCK 93 =========================
.text:00402420                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402424                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402428                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040242C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402430                 lw      $a0, 8($v0)      # Load Word
.text:00402434                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402438                 xor     $a0, $v0         # Exclusive OR
.text:0040243C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402440                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402444                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402448                 sw      $a0, 8($v0)      # Store Word
; Found the 94th break (@0040244c) ; new pc will be 00402774
; ========================= BLOCK 94 =========================
.text:00402774                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402778                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040277C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402780                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402784                 lw      $a0, 8($v0)      # Load Word
.text:00402788                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040278C                 xor     $a0, $v0         # Exclusive OR
.text:00402790                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402794                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402798                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040279C                 sw      $a0, 8($v0)      # Store Word
; Found the 95th break (@004027a0) ; new pc will be 00402900
; ========================= BLOCK 95 =========================
.text:00402900                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402904                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402908                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040290C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402910                 lw      $a0, 8($v0)      # Load Word
.text:00402914                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402918                 xor     $a0, $v0         # Exclusive OR
.text:0040291C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402920                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402924                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402928                 sw      $a0, 8($v0)      # Store Word
; Found the 96th break (@0040292c) ; new pc will be 00402aa8
; ========================= BLOCK 96 =========================
.text:00402AA8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402AAC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402AB0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AB4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402AB8                 lw      $a0, 8($v0)      # Load Word
.text:00402ABC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402AC0                 xor     $a0, $v0         # Exclusive OR
.text:00402AC4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402AC8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402ACC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402AD0                 sw      $a0, 8($v0)      # Store Word
; Found the 97th break (@00402ad4) ; new pc will be 00402930
; ========================= BLOCK 97 =========================
.text:00402930                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402934                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402938                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040293C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402940                 lw      $a0, 8($v0)      # Load Word
.text:00402944                 li      $v0, 0x4CC0DC26  # Load Immediate
.text:0040294C                 xor     $a0, $v0         # Exclusive OR
.text:00402950                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402954                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402958                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040295C                 sw      $a0, 8($v0)      # Store Word
; Found the 98th break (@00402960) ; new pc will be 0040397c
; ========================= BLOCK 98 =========================
.text:0040397C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403980                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403984                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403988                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040398C                 lw      $a0, 8($v0)      # Load Word
.text:00403990                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403994                 xor     $a0, $v0         # Exclusive OR
.text:00403998                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040399C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004039A4                 sw      $a0, 8($v0)      # Store Word
; Found the 99th break (@004039a8) ; new pc will be 00403280
; ========================= BLOCK 99 =========================
.text:00403280                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403284                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403288                 sll     $v0, 2           # Shift Left Logical
.text:0040328C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403290                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403294                 lw      $v0, 8($v0)      # Load Word
.text:00403298                 sll     $v1, $v0, 29     # Shift Left Logical
.text:0040329C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004032A0                 sll     $v0, 2           # Shift Left Logical
.text:004032A4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032A8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004032AC                 lw      $v0, 8($v0)      # Load Word
.text:004032B0                 srl     $v0, 3           # Shift Right Logical
.text:004032B4                 or      $v1, $v0         # OR
.text:004032B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004032BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004032C4                 sw      $v1, 8($v0)      # Store Word
; Found the 100th break (@004032c8) ; new pc will be 004039dc
; ========================= BLOCK 100 =========================
.text:004039DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004039E0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004039E4                 sw      $v0, 0x48+i($fp)  # Store Word
; Found the 0th break (@0040228c) ; new pc will be 004039ac
; ========================= BLOCK 0 =========================
.text:004039AC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004039B0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004039B4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039B8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004039BC                 lw      $a0, 8($v0)      # Load Word
.text:004039C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004039C4                 addu    $a0, $v0         # Add Unsigned
.text:004039C8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004039CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004039D4                 sw      $a0, 8($v0)      # Store Word
; Found the 1th break (@004039d8) ; new pc will be 004031d4
; ========================= BLOCK 1 =========================
.text:004031D4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004031D8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004031DC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031E0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004031E4                 lw      $a0, 8($v0)      # Load Word
.text:004031E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004031EC                 xor     $a0, $v0         # Exclusive OR
.text:004031F0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004031F4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031F8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004031FC                 sw      $a0, 8($v0)      # Store Word
; Found the 2th break (@00403200) ; new pc will be 0040301c
; ========================= BLOCK 2 =========================
.text:0040301C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403020                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403024                 sll     $v0, 2           # Shift Left Logical
.text:00403028                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040302C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403030                 lw      $v0, 8($v0)      # Load Word
.text:00403034                 srl     $v1, $v0, 8      # Shift Right Logical
.text:00403038                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040303C                 sll     $v0, 2           # Shift Left Logical
.text:00403040                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403044                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403048                 lw      $v0, 8($v0)      # Load Word
.text:0040304C                 sll     $v0, 24          # Shift Left Logical
.text:00403050                 or      $v1, $v0         # OR
.text:00403054                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403058                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040305C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403060                 sw      $v1, 8($v0)      # Store Word
; Found the 3th break (@00403064) ; new pc will be 00402744
; ========================= BLOCK 3 =========================
.text:00402744                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402748                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040274C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402750                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402754                 lw      $a0, 8($v0)      # Load Word
.text:00402758                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040275C                 subu    $a0, $v0         # Subtract Unsigned
.text:00402760                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402764                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402768                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040276C                 sw      $a0, 8($v0)      # Store Word
; Found the 4th break (@00402770) ; new pc will be 00402518
; ========================= BLOCK 4 =========================
.text:00402518                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040251C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402520                 sll     $v0, 2           # Shift Left Logical
.text:00402524                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402528                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040252C                 lw      $v0, 8($v0)      # Load Word
.text:00402530                 nor     $v1, $zero, $v0  # NOR
.text:00402534                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402538                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040253C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402540                 sw      $v1, 8($v0)      # Store Word
; Found the 5th break (@00402544) ; new pc will be 00403858
; ========================= BLOCK 5 =========================
.text:00403858                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040385C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403860                 sll     $v0, 2           # Shift Left Logical
.text:00403864                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403868                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040386C                 lw      $v0, 8($v0)      # Load Word
.text:00403870                 nor     $v1, $zero, $v0  # NOR
.text:00403874                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403878                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040387C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403880                 sw      $v1, 8($v0)      # Store Word
; Found the 6th break (@00403884) ; new pc will be 004032cc
; ========================= BLOCK 6 =========================
.text:004032CC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004032D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004032D4                 sll     $v0, 2           # Shift Left Logical
.text:004032D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004032E0                 lw      $v0, 8($v0)      # Load Word
.text:004032E4                 nor     $v1, $zero, $v0  # NOR
.text:004032E8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004032EC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032F0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004032F4                 sw      $v1, 8($v0)      # Store Word
; Found the 7th break (@004032f8) ; new pc will be 004038b8
; ========================= BLOCK 7 =========================
.text:004038B8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004038BC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038C0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038C4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038C8                 lw      $a0, 8($v0)      # Load Word
.text:004038CC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004038D0                 subu    $a0, $v0         # Subtract Unsigned
.text:004038D4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004038E0                 sw      $a0, 8($v0)      # Store Word
; Found the 8th break (@004038e4) ; new pc will be 004027a4
; ========================= BLOCK 8 =========================
.text:004027A4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004027A8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027AC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027B0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004027B4                 lw      $a0, 8($v0)      # Load Word
.text:004027B8                 li      $v0, 0xD0970C74  # Load Immediate
.text:004027C0                 addu    $a0, $v0         # Add Unsigned
.text:004027C4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027C8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027CC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004027D0                 sw      $a0, 8($v0)      # Store Word
; Found the 9th break (@004027d4) ; new pc will be 00403410
; ========================= BLOCK 9 =========================
.text:00403410                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403414                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403418                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040341C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403420                 lw      $a0, 8($v0)      # Load Word
.text:00403424                 li      $v0, 0x192B37D2  # Load Immediate
.text:0040342C                 addu    $a0, $v0         # Add Unsigned
.text:00403430                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403434                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403438                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040343C                 sw      $a0, 8($v0)      # Store Word
; Found the 10th break (@00403440) ; new pc will be 0040332c
; ========================= BLOCK 10 =========================
.text:0040332C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403330                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403334                 sll     $v0, 2           # Shift Left Logical
.text:00403338                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040333C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403340                 lw      $v0, 8($v0)      # Load Word
.text:00403344                 sll     $v1, $v0, 31     # Shift Left Logical
.text:00403348                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040334C                 sll     $v0, 2           # Shift Left Logical
.text:00403350                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403354                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403358                 lw      $v0, 8($v0)      # Load Word
.text:0040335C                 srl     $v0, 1           # Shift Right Logical
.text:00403360                 or      $v1, $v0         # OR
.text:00403364                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403368                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040336C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403370                 sw      $v1, 8($v0)      # Store Word
; Found the 11th break (@00403374) ; new pc will be 0040391c
; ========================= BLOCK 11 =========================
.text:0040391C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403920                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403924                 sll     $v0, 2           # Shift Left Logical
.text:00403928                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040392C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403930                 lw      $v1, 8($v0)      # Load Word
.text:00403934                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403938                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040393C                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403940                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403944                 sll     $v0, 2           # Shift Left Logical
.text:00403948                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040394C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403950                 lw      $a1, 8($v0)      # Load Word
.text:00403954                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403958                 nor     $v0, $zero, $v0  # NOR
.text:0040395C                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403960                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:00403964                 or      $v1, $v0         # OR
.text:00403968                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040396C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403970                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403974                 sw      $v1, 8($v0)      # Store Word
; Found the 12th break (@00403978) ; new pc will be 00402fe8
; ========================= BLOCK 12 =========================
.text:00402FE8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402FEC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FF0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FF4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FF8                 lw      $a0, 8($v0)      # Load Word
.text:00402FFC                 li      $v0, 0x38C1FEB8  # Load Immediate
.text:00403004                 xor     $a0, $v0         # Exclusive OR
.text:00403008                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040300C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403010                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403014                 sw      $a0, 8($v0)      # Store Word
; Found the 13th break (@00403018) ; new pc will be 004034f0
; ========================= BLOCK 13 =========================
.text:004034F0                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004034F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004034F8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034FC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403500                 lw      $a0, 8($v0)      # Load Word
.text:00403504                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403508                 addu    $a0, $v0         # Add Unsigned
.text:0040350C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403510                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403514                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403518                 sw      $a0, 8($v0)      # Store Word
; Found the 14th break (@0040351c) ; new pc will be 00403550
; ========================= BLOCK 14 =========================
.text:00403550                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403554                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403558                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040355C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403560                 lw      $a0, 8($v0)      # Load Word
.text:00403564                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403568                 xor     $a0, $v0         # Exclusive OR
.text:0040356C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403570                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403574                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403578                 sw      $a0, 8($v0)      # Store Word
; Found the 15th break (@0040357c) ; new pc will be 00402290
; ========================= BLOCK 15 =========================
.text:00402290                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402294                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402298                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040229C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004022A0                 lw      $a0, 8($v0)      # Load Word
.text:004022A4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022A8                 subu    $a0, $v0         # Subtract Unsigned
.text:004022AC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004022B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004022B8                 sw      $a0, 8($v0)      # Store Word
; Found the 16th break (@004022bc) ; new pc will be 00402aa8
; ========================= BLOCK 16 =========================
.text:00402AA8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402AAC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402AB0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AB4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402AB8                 lw      $a0, 8($v0)      # Load Word
.text:00402ABC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402AC0                 xor     $a0, $v0         # Exclusive OR
.text:00402AC4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402AC8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402ACC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402AD0                 sw      $a0, 8($v0)      # Store Word
; Found the 17th break (@00402ad4) ; new pc will be 00403204
; ========================= BLOCK 17 =========================
.text:00403204                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403208                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040320C                 sll     $v0, 2           # Shift Left Logical
.text:00403210                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403214                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403218                 lw      $v0, 8($v0)      # Load Word
.text:0040321C                 nor     $v1, $zero, $v0  # NOR
.text:00403220                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403224                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403228                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040322C                 sw      $v1, 8($v0)      # Store Word
; Found the 18th break (@00403230) ; new pc will be 004022c0
; ========================= BLOCK 18 =========================
.text:004022C0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004022C4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022C8                 sll     $v0, 2           # Shift Left Logical
.text:004022CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004022D4                 lw      $v0, 8($v0)      # Load Word
.text:004022D8                 srl     $v1, $v0, 1      # Shift Right Logical
.text:004022DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022E0                 sll     $v0, 2           # Shift Left Logical
.text:004022E4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022E8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004022EC                 lw      $v0, 8($v0)      # Load Word
.text:004022F0                 sll     $v0, 31          # Shift Left Logical
.text:004022F4                 or      $v1, $v0         # OR
.text:004022F8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004022FC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402300                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402304                 sw      $v1, 8($v0)      # Store Word
; Found the 19th break (@00402308) ; new pc will be 004025a8
; ========================= BLOCK 19 =========================
.text:004025A8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004025AC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025B0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025B4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025B8                 lw      $a0, 8($v0)      # Load Word
.text:004025BC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004025C0                 addu    $a0, $v0         # Add Unsigned
.text:004025C4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025C8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025CC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004025D0                 sw      $a0, 8($v0)      # Store Word
; Found the 20th break (@004025d4) ; new pc will be 00402450
; ========================= BLOCK 20 =========================
.text:00402450                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402454                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402458                 sll     $v0, 2           # Shift Left Logical
.text:0040245C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402460                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402464                 lw      $v0, 8($v0)      # Load Word
.text:00402468                 sll     $v1, $v0, 13     # Shift Left Logical
.text:0040246C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402470                 sll     $v0, 2           # Shift Left Logical
.text:00402474                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402478                 addu    $v0, $a1, $v0    # Add Unsigned
.text:0040247C                 lw      $v0, 8($v0)      # Load Word
.text:00402480                 srl     $v0, 19          # Shift Right Logical
.text:00402484                 or      $v1, $v0         # OR
.text:00402488                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040248C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402490                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402494                 sw      $v1, 8($v0)      # Store Word
; Found the 21th break (@00402498) ; new pc will be 00402964
; ========================= BLOCK 21 =========================
.text:00402964                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402968                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040296C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402970                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402974                 lw      $a0, 8($v0)      # Load Word
.text:00402978                 li      $v0, 0x737F298   # Load Immediate
.text:00402980                 addu    $a0, $v0         # Add Unsigned
.text:00402984                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402988                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040298C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402990                 sw      $a0, 8($v0)      # Store Word
; Found the 22th break (@00402994) ; new pc will be 004025d8
; ========================= BLOCK 22 =========================
.text:004025D8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004025DC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025E8                 lw      $a0, 8($v0)      # Load Word
.text:004025EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004025F0                 addu    $a0, $v0         # Add Unsigned
.text:004025F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025F8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025FC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402600                 sw      $a0, 8($v0)      # Store Word
; Found the 23th break (@00402604) ; new pc will be 00402f68
; ========================= BLOCK 23 =========================
.text:00402F68                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402F6C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F70                 sll     $v0, 2           # Shift Left Logical
.text:00402F74                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F78                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F7C                 lw      $v0, 8($v0)      # Load Word
.text:00402F80                 sll     $v1, $v0, 23     # Shift Left Logical
.text:00402F84                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F88                 sll     $v0, 2           # Shift Left Logical
.text:00402F8C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F90                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402F94                 lw      $v0, 8($v0)      # Load Word
.text:00402F98                 srl     $v0, 9           # Shift Right Logical
.text:00402F9C                 or      $v1, $v0         # OR
.text:00402FA0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402FA4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FA8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FAC                 sw      $v1, 8($v0)      # Store Word
; Found the 24th break (@00402fb0) ; new pc will be 00402b54
; ========================= BLOCK 24 =========================
.text:00402B54                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402B58                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B5C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B60                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B64                 lw      $a0, 8($v0)      # Load Word
.text:00402B68                 li      $v0, 0x79662B5D  # Load Immediate
.text:00402B70                 addu    $a0, $v0         # Add Unsigned
.text:00402B74                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B78                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B7C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402B80                 sw      $a0, 8($v0)      # Store Word
; Found the 25th break (@00402b84) ; new pc will be 00402d10
; ========================= BLOCK 25 =========================
.text:00402D10                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D14                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D18                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D1C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D20                 lw      $a0, 8($v0)      # Load Word
.text:00402D24                 li      $v0, 0xA9BE160D  # Load Immediate
.text:00402D2C                 xor     $a0, $v0         # Exclusive OR
.text:00402D30                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D34                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D38                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402D3C                 sw      $a0, 8($v0)      # Store Word
; Found the 26th break (@00402d40) ; new pc will be 004037ac
; ========================= BLOCK 26 =========================
.text:004037AC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004037B0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037B4                 sll     $v0, 2           # Shift Left Logical
.text:004037B8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037BC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004037C0                 lw      $v1, 8($v0)      # Load Word
.text:004037C4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037C8                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004037CC                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004037D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037D4                 sll     $v0, 2           # Shift Left Logical
.text:004037D8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037DC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004037E0                 lw      $a1, 8($v0)      # Load Word
.text:004037E4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037E8                 nor     $v0, $zero, $v0  # NOR
.text:004037EC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004037F0                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004037F4                 or      $v1, $v0         # OR
.text:004037F8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004037FC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403800                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403804                 sw      $v1, 8($v0)      # Store Word
; Found the 27th break (@00403808) ; new pc will be 0040372c
; ========================= BLOCK 27 =========================
.text:0040372C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403730                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403734                 sll     $v0, 2           # Shift Left Logical
.text:00403738                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040373C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403740                 lw      $v0, 8($v0)      # Load Word
.text:00403744                 sll     $v1, $v0, 5      # Shift Left Logical
.text:00403748                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040374C                 sll     $v0, 2           # Shift Left Logical
.text:00403750                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403754                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403758                 lw      $v0, 8($v0)      # Load Word
.text:0040375C                 srl     $v0, 27          # Shift Right Logical
.text:00403760                 or      $v1, $v0         # OR
.text:00403764                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403768                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040376C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403770                 sw      $v1, 8($v0)      # Store Word
; Found the 28th break (@00403774) ; new pc will be 00402a2c
; ========================= BLOCK 28 =========================
.text:00402A2C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402A30                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A34                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A38                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402A3C                 lw      $a0, 8($v0)      # Load Word
.text:00402A40                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A44                 subu    $a0, $v0         # Subtract Unsigned
.text:00402A48                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A4C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A50                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A54                 sw      $a0, 8($v0)      # Store Word
; Found the 29th break (@00402a58) ; new pc will be 004030e4
; ========================= BLOCK 29 =========================
.text:004030E4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004030E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030EC                 sll     $v0, 2           # Shift Left Logical
.text:004030F0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004030F8                 lw      $v1, 8($v0)      # Load Word
.text:004030FC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403100                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403104                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403108                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040310C                 sll     $v0, 2           # Shift Left Logical
.text:00403110                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403114                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403118                 lw      $a1, 8($v0)      # Load Word
.text:0040311C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403120                 nor     $v0, $zero, $v0  # NOR
.text:00403124                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403128                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040312C                 or      $v1, $v0         # OR
.text:00403130                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403134                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403138                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040313C                 sw      $v1, 8($v0)      # Store Word
; Found the 30th break (@00403140) ; new pc will be 0040286c
; ========================= BLOCK 30 =========================
.text:0040286C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402870                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402874                 sll     $v0, 2           # Shift Left Logical
.text:00402878                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040287C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402880                 lw      $v1, 8($v0)      # Load Word
.text:00402884                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402888                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040288C                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00402890                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402894                 sll     $v0, 2           # Shift Left Logical
.text:00402898                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040289C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004028A0                 lw      $a1, 8($v0)      # Load Word
.text:004028A4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004028A8                 nor     $v0, $zero, $v0  # NOR
.text:004028AC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004028B0                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004028B4                 or      $v1, $v0         # OR
.text:004028B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004028BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004028C4                 sw      $v1, 8($v0)      # Store Word
; Found the 31th break (@004028c8) ; new pc will be 00402eb8
; ========================= BLOCK 31 =========================
.text:00402EB8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402EBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402EC0                 sll     $v0, 2           # Shift Left Logical
.text:00402EC4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402ECC                 lw      $v0, 8($v0)      # Load Word
.text:00402ED0                 sll     $v1, $v0, 18     # Shift Left Logical
.text:00402ED4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402ED8                 sll     $v0, 2           # Shift Left Logical
.text:00402EDC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EE0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402EE4                 lw      $v0, 8($v0)      # Load Word
.text:00402EE8                 srl     $v0, 14          # Shift Right Logical
.text:00402EEC                 or      $v1, $v0         # OR
.text:00402EF0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402EF4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EF8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402EFC                 sw      $v1, 8($v0)      # Store Word
; Found the 32th break (@00402f00) ; new pc will be 00402c50
; ========================= BLOCK 32 =========================
.text:00402C50                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402C54                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C58                 sll     $v0, 2           # Shift Left Logical
.text:00402C5C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C60                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402C64                 lw      $v1, 8($v0)      # Load Word
.text:00402C68                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C6C                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00402C70                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00402C74                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C78                 sll     $v0, 2           # Shift Left Logical
.text:00402C7C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C80                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402C84                 lw      $a1, 8($v0)      # Load Word
.text:00402C88                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C8C                 nor     $v0, $zero, $v0  # NOR
.text:00402C90                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00402C94                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:00402C98                 or      $v1, $v0         # OR
.text:00402C9C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402CA0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CA4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402CA8                 sw      $v1, 8($v0)      # Store Word
; Found the 33th break (@00402cac) ; new pc will be 004038e8
; ========================= BLOCK 33 =========================
.text:004038E8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004038EC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038F0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038F4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038F8                 lw      $a0, 8($v0)      # Load Word
.text:004038FC                 li      $v0, 0xDBFA3745  # Load Immediate
.text:00403904                 addu    $a0, $v0         # Add Unsigned
.text:00403908                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040390C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403910                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403914                 sw      $a0, 8($v0)      # Store Word
; Found the 34th break (@00403918) ; new pc will be 00402a5c
; ========================= BLOCK 34 =========================
.text:00402A5C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402A60                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A64                 sll     $v0, 2           # Shift Left Logical
.text:00402A68                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A6C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A70                 lw      $v0, 8($v0)      # Load Word
.text:00402A74                 srl     $v1, $v0, 13     # Shift Right Logical
.text:00402A78                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A7C                 sll     $v0, 2           # Shift Left Logical
.text:00402A80                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A84                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402A88                 lw      $v0, 8($v0)      # Load Word
.text:00402A8C                 sll     $v0, 19          # Shift Left Logical
.text:00402A90                 or      $v1, $v0         # OR
.text:00402A94                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402A98                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A9C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402AA0                 sw      $v1, 8($v0)      # Store Word
; Found the 35th break (@00402aa4) ; new pc will be 00402608
; ========================= BLOCK 35 =========================
.text:00402608                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040260C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402610                 sll     $v0, 2           # Shift Left Logical
.text:00402614                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402618                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040261C                 lw      $v0, 8($v0)      # Load Word
.text:00402620                 srl     $v1, $v0, 23     # Shift Right Logical
.text:00402624                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402628                 sll     $v0, 2           # Shift Left Logical
.text:0040262C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402630                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402634                 lw      $v0, 8($v0)      # Load Word
.text:00402638                 sll     $v0, 9           # Shift Left Logical
.text:0040263C                 or      $v1, $v0         # OR
.text:00402640                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402644                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402648                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040264C                 sw      $v1, 8($v0)      # Store Word
; Found the 36th break (@00402650) ; new pc will be 00402c04
; ========================= BLOCK 36 =========================
.text:00402C04                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402C08                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C0C                 sll     $v0, 2           # Shift Left Logical
.text:00402C10                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C14                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402C18                 lw      $v0, 8($v0)      # Load Word
.text:00402C1C                 srl     $v1, $v0, 4      # Shift Right Logical
.text:00402C20                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C24                 sll     $v0, 2           # Shift Left Logical
.text:00402C28                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C2C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402C30                 lw      $v0, 8($v0)      # Load Word
.text:00402C34                 sll     $v0, 28          # Shift Left Logical
.text:00402C38                 or      $v1, $v0         # OR
.text:00402C3C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402C40                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C44                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402C48                 sw      $v1, 8($v0)      # Store Word
; Found the 37th break (@00402c4c) ; new pc will be 004029f8
; ========================= BLOCK 37 =========================
.text:004029F8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004029FC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A00                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A04                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402A08                 lw      $a0, 8($v0)      # Load Word
.text:00402A0C                 li      $v0, 0x81674F2B  # Load Immediate
.text:00402A14                 addu    $a0, $v0         # Add Unsigned
.text:00402A18                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A1C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A20                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A24                 sw      $a0, 8($v0)      # Store Word
; Found the 38th break (@00402a28) ; new pc will be 00402b88
; ========================= BLOCK 38 =========================
.text:00402B88                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402B8C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B90                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B94                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B98                 lw      $a0, 8($v0)      # Load Word
.text:00402B9C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BA0                 subu    $a0, $v0         # Subtract Unsigned
.text:00402BA4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402BA8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402BB0                 sw      $a0, 8($v0)      # Store Word
; Found the 39th break (@00402bb4) ; new pc will be 00402f38
; ========================= BLOCK 39 =========================
.text:00402F38                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402F3C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F40                 sll     $v0, 2           # Shift Left Logical
.text:00402F44                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F48                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F4C                 lw      $v0, 8($v0)      # Load Word
.text:00402F50                 nor     $v1, $zero, $v0  # NOR
.text:00402F54                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402F58                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F5C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402F60                 sw      $v1, 8($v0)      # Store Word
; Found the 40th break (@00402f64) ; new pc will be 00402714
; ========================= BLOCK 40 =========================
.text:00402714                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402718                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040271C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402720                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402724                 lw      $a0, 8($v0)      # Load Word
.text:00402728                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040272C                 addu    $a0, $v0         # Add Unsigned
.text:00402730                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402734                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402738                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040273C                 sw      $a0, 8($v0)      # Store Word
; Found the 41th break (@00402740) ; new pc will be 00403664
; ========================= BLOCK 41 =========================
.text:00403664                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403668                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040366C                 sll     $v0, 2           # Shift Left Logical
.text:00403670                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403674                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403678                 lw      $v0, 8($v0)      # Load Word
.text:0040367C                 nor     $v1, $zero, $v0  # NOR
.text:00403680                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403684                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403688                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040368C                 sw      $v1, 8($v0)      # Store Word
; Found the 42th break (@00403690) ; new pc will be 00403520
; ========================= BLOCK 42 =========================
.text:00403520                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403524                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403528                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040352C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403530                 lw      $a0, 8($v0)      # Load Word
.text:00403534                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403538                 xor     $a0, $v0         # Exclusive OR
.text:0040353C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403540                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403544                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403548                 sw      $a0, 8($v0)      # Store Word
; Found the 43th break (@0040354c) ; new pc will be 00402998
; ========================= BLOCK 43 =========================
.text:00402998                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040299C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029A0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029A4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004029A8                 lw      $a0, 8($v0)      # Load Word
.text:004029AC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004029B0                 subu    $a0, $v0         # Subtract Unsigned
.text:004029B4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029B8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029BC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004029C0                 sw      $a0, 8($v0)      # Store Word
; Found the 44th break (@004029c4) ; new pc will be 00402dd8
; ========================= BLOCK 44 =========================
.text:00402DD8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402DDC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DE0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DE4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402DE8                 lw      $a0, 8($v0)      # Load Word
.text:00402DEC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402DF0                 subu    $a0, $v0         # Subtract Unsigned
.text:00402DF4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DF8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DFC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E00                 sw      $a0, 8($v0)      # Store Word
; Found the 45th break (@00402e04) ; new pc will be 00403174
; ========================= BLOCK 45 =========================
.text:00403174                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403178                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040317C                 sll     $v0, 2           # Shift Left Logical
.text:00403180                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403184                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403188                 lw      $v1, 8($v0)      # Load Word
.text:0040318C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403190                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403194                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403198                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040319C                 sll     $v0, 2           # Shift Left Logical
.text:004031A0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031A4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004031A8                 lw      $a1, 8($v0)      # Load Word
.text:004031AC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004031B0                 nor     $v0, $zero, $v0  # NOR
.text:004031B4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004031B8                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:004031BC                 or      $v1, $v0         # OR
.text:004031C0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004031C4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031C8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004031CC                 sw      $v1, 8($v0)      # Store Word
; Found the 46th break (@004031d0) ; new pc will be 00402d44
; ========================= BLOCK 46 =========================
.text:00402D44                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D48                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D4C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D50                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D54                 lw      $a0, 8($v0)      # Load Word
.text:00402D58                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402D5C                 addu    $a0, $v0         # Add Unsigned
.text:00402D60                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D64                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D68                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402D6C                 sw      $a0, 8($v0)      # Store Word
; Found the 47th break (@00402d70) ; new pc will be 00402838
; ========================= BLOCK 47 =========================
.text:00402838                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040283C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402840                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402844                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402848                 lw      $a0, 8($v0)      # Load Word
.text:0040284C                 li      $v0, 0xB65E867F  # Load Immediate
.text:00402854                 addu    $a0, $v0         # Add Unsigned
.text:00402858                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040285C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402860                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402864                 sw      $a0, 8($v0)      # Store Word
; Found the 48th break (@00402868) ; new pc will be 00403378
; ========================= BLOCK 48 =========================
.text:00403378                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040337C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403380                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403384                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403388                 lw      $a0, 8($v0)      # Load Word
.text:0040338C                 li      $v0, 0xBFD991A0  # Load Immediate
.text:00403394                 xor     $a0, $v0         # Exclusive OR
.text:00403398                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040339C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004033A4                 sw      $a0, 8($v0)      # Store Word
; Found the 49th break (@004033a8) ; new pc will be 00403778
; ========================= BLOCK 49 =========================
.text:00403778                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040377C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403780                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403784                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403788                 lw      $a0, 8($v0)      # Load Word
.text:0040378C                 li      $v0, 0x6EDC032   # Load Immediate
.text:00403794                 addu    $a0, $v0         # Add Unsigned
.text:00403798                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040379C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004037A4                 sw      $a0, 8($v0)      # Store Word
; Found the 50th break (@004037a8) ; new pc will be 004033ac
; ========================= BLOCK 50 =========================
.text:004033AC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004033B0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033B4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033B8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004033BC                 lw      $a0, 8($v0)      # Load Word
.text:004033C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004033C4                 addu    $a0, $v0         # Add Unsigned
.text:004033C8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004033D4                 sw      $a0, 8($v0)      # Store Word
; Found the 51th break (@004033d8) ; new pc will be 00402808
; ========================= BLOCK 51 =========================
.text:00402808                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040280C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402810                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402814                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402818                 lw      $a0, 8($v0)      # Load Word
.text:0040281C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402820                 subu    $a0, $v0         # Subtract Unsigned
.text:00402824                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402828                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040282C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402830                 sw      $a0, 8($v0)      # Store Word
; Found the 52th break (@00402834) ; new pc will be 004035cc
; ========================= BLOCK 52 =========================
.text:004035CC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004035D0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004035D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004035DC                 lw      $a0, 8($v0)      # Load Word
.text:004035E0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004035E4                 addu    $a0, $v0         # Add Unsigned
.text:004035E8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004035EC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035F0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004035F4                 sw      $a0, 8($v0)      # Store Word
; Found the 53th break (@004035f8) ; new pc will be 004026b4
; ========================= BLOCK 53 =========================
.text:004026B4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004026B8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026BC                 sll     $v0, 2           # Shift Left Logical
.text:004026C0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026C4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004026C8                 lw      $v1, 8($v0)      # Load Word
.text:004026CC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026D0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004026D4                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004026D8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026DC                 sll     $v0, 2           # Shift Left Logical
.text:004026E0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026E4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004026E8                 lw      $a1, 8($v0)      # Load Word
.text:004026EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026F0                 nor     $v0, $zero, $v0  # NOR
.text:004026F4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004026F8                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004026FC                 or      $v1, $v0         # OR
.text:00402700                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402704                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402708                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040270C                 sw      $v1, 8($v0)      # Store Word
; Found the 54th break (@00402710) ; new pc will be 00402ce0
; ========================= BLOCK 54 =========================
.text:00402CE0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402CE4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402CE8                 sll     $v0, 2           # Shift Left Logical
.text:00402CEC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CF0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402CF4                 lw      $v0, 8($v0)      # Load Word
.text:00402CF8                 nor     $v1, $zero, $v0  # NOR
.text:00402CFC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402D00                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D04                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D08                 sw      $v1, 8($v0)      # Store Word
; Found the 55th break (@00402d0c) ; new pc will be 00402e08
; ========================= BLOCK 55 =========================
.text:00402E08                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402E0C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E10                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E14                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E18                 lw      $a0, 8($v0)      # Load Word
.text:00402E1C                 li      $v0, 0x73C69F47  # Load Immediate
.text:00402E24                 addu    $a0, $v0         # Add Unsigned
.text:00402E28                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E2C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E30                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E34                 sw      $a0, 8($v0)      # Store Word
; Found the 56th break (@00402e38) ; new pc will be 004029c8
; ========================= BLOCK 56 =========================
.text:004029C8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004029CC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029D0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029D4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004029D8                 lw      $a0, 8($v0)      # Load Word
.text:004029DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004029E0                 xor     $a0, $v0         # Exclusive OR
.text:004029E4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029E8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029EC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004029F0                 sw      $a0, 8($v0)      # Store Word
; Found the 57th break (@004029f4) ; new pc will be 00402654
; ========================= BLOCK 57 =========================
.text:00402654                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402658                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040265C                 sll     $v0, 2           # Shift Left Logical
.text:00402660                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402664                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402668                 lw      $v1, 8($v0)      # Load Word
.text:0040266C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402670                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00402674                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00402678                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040267C                 sll     $v0, 2           # Shift Left Logical
.text:00402680                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402684                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402688                 lw      $a1, 8($v0)      # Load Word
.text:0040268C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402690                 nor     $v0, $zero, $v0  # NOR
.text:00402694                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00402698                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040269C                 or      $v1, $v0         # OR
.text:004026A0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004026A4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026A8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004026AC                 sw      $v1, 8($v0)      # Store Word
; Found the 58th break (@004026b0) ; new pc will be 00403068
; ========================= BLOCK 58 =========================
.text:00403068                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040306C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403070                 sll     $v0, 2           # Shift Left Logical
.text:00403074                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403078                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040307C                 lw      $v0, 8($v0)      # Load Word
.text:00403080                 nor     $v1, $zero, $v0  # NOR
.text:00403084                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403088                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040308C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403090                 sw      $v1, 8($v0)      # Store Word
; Found the 59th break (@00403094) ; new pc will be 00402b08
; ========================= BLOCK 59 =========================
.text:00402B08                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402B0C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402B10                 sll     $v0, 2           # Shift Left Logical
.text:00402B14                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B18                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402B1C                 lw      $v0, 8($v0)      # Load Word
.text:00402B20                 srl     $v1, $v0, 26     # Shift Right Logical
.text:00402B24                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402B28                 sll     $v0, 2           # Shift Left Logical
.text:00402B2C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B30                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402B34                 lw      $v0, 8($v0)      # Load Word
.text:00402B38                 sll     $v0, 6           # Shift Left Logical
.text:00402B3C                 or      $v1, $v0         # OR
.text:00402B40                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402B44                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B48                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B4C                 sw      $v1, 8($v0)      # Store Word
; Found the 60th break (@00402b50) ; new pc will be 004036e0
; ========================= BLOCK 60 =========================
.text:004036E0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004036E4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004036E8                 sll     $v0, 2           # Shift Left Logical
.text:004036EC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036F0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004036F4                 lw      $v0, 8($v0)      # Load Word
.text:004036F8                 sll     $v1, $v0, 5      # Shift Left Logical
.text:004036FC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403700                 sll     $v0, 2           # Shift Left Logical
.text:00403704                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403708                 addu    $v0, $a1, $v0    # Add Unsigned
.text:0040370C                 lw      $v0, 8($v0)      # Load Word
.text:00403710                 srl     $v0, 27          # Shift Right Logical
.text:00403714                 or      $v1, $v0         # OR
.text:00403718                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040371C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403720                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403724                 sw      $v1, 8($v0)      # Store Word
; Found the 61th break (@00403728) ; new pc will be 00403280
; ========================= BLOCK 61 =========================
.text:00403280                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403284                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403288                 sll     $v0, 2           # Shift Left Logical
.text:0040328C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403290                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403294                 lw      $v0, 8($v0)      # Load Word
.text:00403298                 sll     $v1, $v0, 29     # Shift Left Logical
.text:0040329C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004032A0                 sll     $v0, 2           # Shift Left Logical
.text:004032A4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032A8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004032AC                 lw      $v0, 8($v0)      # Load Word
.text:004032B0                 srl     $v0, 3           # Shift Right Logical
.text:004032B4                 or      $v1, $v0         # OR
.text:004032B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004032BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004032C4                 sw      $v1, 8($v0)      # Store Word
; Found the 62th break (@004032c8) ; new pc will be 00402bb8
; ========================= BLOCK 62 =========================
.text:00402BB8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402BBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BC0                 sll     $v0, 2           # Shift Left Logical
.text:00402BC4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402BCC                 lw      $v0, 8($v0)      # Load Word
.text:00402BD0                 srl     $v1, $v0, 21     # Shift Right Logical
.text:00402BD4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BD8                 sll     $v0, 2           # Shift Left Logical
.text:00402BDC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BE0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402BE4                 lw      $v0, 8($v0)      # Load Word
.text:00402BE8                 sll     $v0, 11          # Shift Left Logical
.text:00402BEC                 or      $v1, $v0         # OR
.text:00402BF0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402BF4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BF8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402BFC                 sw      $v1, 8($v0)      # Store Word
; Found the 63th break (@00402c00) ; new pc will be 0040380c
; ========================= BLOCK 63 =========================
.text:0040380C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403810                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403814                 sll     $v0, 2           # Shift Left Logical
.text:00403818                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040381C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403820                 lw      $v0, 8($v0)      # Load Word
.text:00403824                 sll     $v1, $v0, 16     # Shift Left Logical
.text:00403828                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040382C                 sll     $v0, 2           # Shift Left Logical
.text:00403830                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403834                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403838                 lw      $v0, 8($v0)      # Load Word
.text:0040383C                 srl     $v0, 16          # Shift Right Logical
.text:00403840                 or      $v1, $v0         # OR
.text:00403844                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403848                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040384C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403850                 sw      $v1, 8($v0)      # Store Word
; Found the 64th break (@00403854) ; new pc will be 00402e88
; ========================= BLOCK 64 =========================
.text:00402E88                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402E8C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E90                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E94                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E98                 lw      $a0, 8($v0)      # Load Word
.text:00402E9C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402EA0                 xor     $a0, $v0         # Exclusive OR
.text:00402EA4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402EA8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402EB0                 sw      $a0, 8($v0)      # Store Word
; Found the 65th break (@00402eb4) ; new pc will be 00402370
; ========================= BLOCK 65 =========================
.text:00402370                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402374                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402378                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040237C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402380                 lw      $a0, 8($v0)      # Load Word
.text:00402384                 li      $v0, 0x87DD2BC5  # Load Immediate
.text:0040238C                 addu    $a0, $v0         # Add Unsigned
.text:00402390                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402394                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402398                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040239C                 sw      $a0, 8($v0)      # Store Word
; Found the 66th break (@004023a0) ; new pc will be 004028cc
; ========================= BLOCK 66 =========================
.text:004028CC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004028D0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004028D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004028DC                 lw      $a0, 8($v0)      # Load Word
.text:004028E0                 li      $v0, 0x3A2EE307  # Load Immediate
.text:004028E8                 addu    $a0, $v0         # Add Unsigned
.text:004028EC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004028F0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004028F8                 sw      $a0, 8($v0)      # Store Word
; Found the 67th break (@004028fc) ; new pc will be 00402578
; ========================= BLOCK 67 =========================
.text:00402578                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040257C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402580                 sll     $v0, 2           # Shift Left Logical
.text:00402584                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402588                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040258C                 lw      $v0, 8($v0)      # Load Word
.text:00402590                 nor     $v1, $zero, $v0  # NOR
.text:00402594                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402598                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040259C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025A0                 sw      $v1, 8($v0)      # Store Word
; Found the 68th break (@004025a4) ; new pc will be 004032fc
; ========================= BLOCK 68 =========================
.text:004032FC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403300                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403304                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403308                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040330C                 lw      $a0, 8($v0)      # Load Word
.text:00403310                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403314                 xor     $a0, $v0         # Exclusive OR
.text:00403318                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040331C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403320                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403324                 sw      $a0, 8($v0)      # Store Word
; Found the 69th break (@00403328) ; new pc will be 00402420
; ========================= BLOCK 69 =========================
.text:00402420                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402424                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402428                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040242C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402430                 lw      $a0, 8($v0)      # Load Word
.text:00402434                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402438                 xor     $a0, $v0         # Exclusive OR
.text:0040243C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402440                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402444                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402448                 sw      $a0, 8($v0)      # Store Word
; Found the 70th break (@0040244c) ; new pc will be 00402ad8
; ========================= BLOCK 70 =========================
.text:00402AD8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402ADC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402AE0                 sll     $v0, 2           # Shift Left Logical
.text:00402AE4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AE8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402AEC                 lw      $v0, 8($v0)      # Load Word
.text:00402AF0                 nor     $v1, $zero, $v0  # NOR
.text:00402AF4                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402AF8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AFC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B00                 sw      $v1, 8($v0)      # Store Word
; Found the 71th break (@00402b04) ; new pc will be 00402900
; ========================= BLOCK 71 =========================
.text:00402900                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402904                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402908                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040290C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402910                 lw      $a0, 8($v0)      # Load Word
.text:00402914                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402918                 xor     $a0, $v0         # Exclusive OR
.text:0040291C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402920                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402924                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402928                 sw      $a0, 8($v0)      # Store Word
; Found the 72th break (@0040292c) ; new pc will be 00403234
; ========================= BLOCK 72 =========================
.text:00403234                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403238                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040323C                 sll     $v0, 2           # Shift Left Logical
.text:00403240                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403244                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403248                 lw      $v0, 8($v0)      # Load Word
.text:0040324C                 sll     $v1, $v0, 29     # Shift Left Logical
.text:00403250                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403254                 sll     $v0, 2           # Shift Left Logical
.text:00403258                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040325C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403260                 lw      $v0, 8($v0)      # Load Word
.text:00403264                 srl     $v0, 3           # Shift Right Logical
.text:00403268                 or      $v1, $v0         # OR
.text:0040326C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403270                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403274                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403278                 sw      $v1, 8($v0)      # Store Word
; Found the 73th break (@0040327c) ; new pc will be 00402774
; ========================= BLOCK 73 =========================
.text:00402774                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402778                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040277C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402780                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402784                 lw      $a0, 8($v0)      # Load Word
.text:00402788                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040278C                 xor     $a0, $v0         # Exclusive OR
.text:00402790                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402794                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402798                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040279C                 sw      $a0, 8($v0)      # Store Word
; Found the 74th break (@004027a0) ; new pc will be 00403694
; ========================= BLOCK 74 =========================
.text:00403694                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403698                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040369C                 sll     $v0, 2           # Shift Left Logical
.text:004036A0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036A4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004036A8                 lw      $v0, 8($v0)      # Load Word
.text:004036AC                 sll     $v1, $v0, 6      # Shift Left Logical
.text:004036B0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004036B4                 sll     $v0, 2           # Shift Left Logical
.text:004036B8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036BC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004036C0                 lw      $v0, 8($v0)      # Load Word
.text:004036C4                 srl     $v0, 26          # Shift Right Logical
.text:004036C8                 or      $v1, $v0         # OR
.text:004036CC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004036D0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036D4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004036D8                 sw      $v1, 8($v0)      # Store Word
; Found the 75th break (@004036dc) ; new pc will be 00403098
; ========================= BLOCK 75 =========================
.text:00403098                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040309C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030A0                 sll     $v0, 2           # Shift Left Logical
.text:004030A4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030A8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004030AC                 lw      $v0, 8($v0)      # Load Word
.text:004030B0                 srl     $v1, $v0, 3      # Shift Right Logical
.text:004030B4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030B8                 sll     $v0, 2           # Shift Left Logical
.text:004030BC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030C0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004030C4                 lw      $v0, 8($v0)      # Load Word
.text:004030C8                 sll     $v0, 29          # Shift Left Logical
.text:004030CC                 or      $v1, $v0         # OR
.text:004030D0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004030D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004030DC                 sw      $v1, 8($v0)      # Store Word
; Found the 76th break (@004030e0) ; new pc will be 00403888
; ========================= BLOCK 76 =========================
.text:00403888                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040388C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403890                 sll     $v0, 2           # Shift Left Logical
.text:00403894                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403898                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040389C                 lw      $v0, 8($v0)      # Load Word
.text:004038A0                 nor     $v1, $zero, $v0  # NOR
.text:004038A4                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004038A8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038AC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038B0                 sw      $v1, 8($v0)      # Store Word
; Found the 77th break (@004038b4) ; new pc will be 00403144
; ========================= BLOCK 77 =========================
.text:00403144                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403148                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040314C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403150                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403154                 lw      $a0, 8($v0)      # Load Word
.text:00403158                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040315C                 addu    $a0, $v0         # Add Unsigned
.text:00403160                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403164                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403168                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040316C                 sw      $a0, 8($v0)      # Store Word
; Found the 78th break (@00403170) ; new pc will be 00402cb0
; ========================= BLOCK 78 =========================
.text:00402CB0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402CB4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402CB8                 sll     $v0, 2           # Shift Left Logical
.text:00402CBC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CC0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402CC4                 lw      $v0, 8($v0)      # Load Word
.text:00402CC8                 nor     $v1, $zero, $v0  # NOR
.text:00402CCC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402CD0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CD4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402CD8                 sw      $v1, 8($v0)      # Store Word
; Found the 79th break (@00402cdc) ; new pc will be 004023a4
; ========================= BLOCK 79 =========================
.text:004023A4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004023A8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004023AC                 sll     $v0, 2           # Shift Left Logical
.text:004023B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004023B8                 lw      $v0, 8($v0)      # Load Word
.text:004023BC                 srl     $v1, $v0, 12     # Shift Right Logical
.text:004023C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004023C4                 sll     $v0, 2           # Shift Left Logical
.text:004023C8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023CC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004023D0                 lw      $v0, 8($v0)      # Load Word
.text:004023D4                 sll     $v0, 20          # Shift Left Logical
.text:004023D8                 or      $v1, $v0         # OR
.text:004023DC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004023E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004023E8                 sw      $v1, 8($v0)      # Store Word
; Found the 80th break (@004023ec) ; new pc will be 00402fb4
; ========================= BLOCK 80 =========================
.text:00402FB4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402FB8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FBC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FC0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FC4                 lw      $a0, 8($v0)      # Load Word
.text:00402FC8                 li      $v0, 0xCC4E5D94  # Load Immediate
.text:00402FD0                 xor     $a0, $v0         # Exclusive OR
.text:00402FD4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FD8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FDC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402FE0                 sw      $a0, 8($v0)      # Store Word
; Found the 81th break (@00402fe4) ; new pc will be 00403444
; ========================= BLOCK 81 =========================
.text:00403444                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403448                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040344C                 sll     $v0, 2           # Shift Left Logical
.text:00403450                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403454                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403458                 lw      $v1, 8($v0)      # Load Word
.text:0040345C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403460                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403464                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403468                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040346C                 sll     $v0, 2           # Shift Left Logical
.text:00403470                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403474                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403478                 lw      $a1, 8($v0)      # Load Word
.text:0040347C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403480                 nor     $v0, $zero, $v0  # NOR
.text:00403484                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403488                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040348C                 or      $v1, $v0         # OR
.text:00403490                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403494                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403498                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040349C                 sw      $v1, 8($v0)      # Store Word
; Found the 82th break (@004034a0) ; new pc will be 004027d8
; ========================= BLOCK 82 =========================
.text:004027D8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004027DC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004027E8                 lw      $a0, 8($v0)      # Load Word
.text:004027EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004027F0                 subu    $a0, $v0         # Subtract Unsigned
.text:004027F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027F8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027FC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402800                 sw      $a0, 8($v0)      # Store Word
; Found the 83th break (@00402804) ; new pc will be 00402930
; ========================= BLOCK 83 =========================
.text:00402930                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402934                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402938                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040293C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402940                 lw      $a0, 8($v0)      # Load Word
.text:00402944                 li      $v0, 0x4CC0DC26  # Load Immediate
.text:0040294C                 xor     $a0, $v0         # Exclusive OR
.text:00402950                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402954                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402958                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040295C                 sw      $a0, 8($v0)      # Store Word
; Found the 84th break (@00402960) ; new pc will be 00402da8
; ========================= BLOCK 84 =========================
.text:00402DA8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402DAC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DB0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DB4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402DB8                 lw      $a0, 8($v0)      # Load Word
.text:00402DBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402DC0                 xor     $a0, $v0         # Exclusive OR
.text:00402DC4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DC8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DCC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402DD0                 sw      $a0, 8($v0)      # Store Word
; Found the 85th break (@00402dd4) ; new pc will be 004034a4
; ========================= BLOCK 85 =========================
.text:004034A4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004034A8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004034AC                 sll     $v0, 2           # Shift Left Logical
.text:004034B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004034B8                 lw      $v0, 8($v0)      # Load Word
.text:004034BC                 srl     $v1, $v0, 17     # Shift Right Logical
.text:004034C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004034C4                 sll     $v0, 2           # Shift Left Logical
.text:004034C8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034CC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004034D0                 lw      $v0, 8($v0)      # Load Word
.text:004034D4                 sll     $v0, 15          # Shift Left Logical
.text:004034D8                 or      $v1, $v0         # OR
.text:004034DC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004034E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004034E8                 sw      $v1, 8($v0)      # Store Word
; Found the 86th break (@004034ec) ; new pc will be 00402d74
; ========================= BLOCK 86 =========================
.text:00402D74                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D78                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D7C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D80                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D84                 lw      $a0, 8($v0)      # Load Word
.text:00402D88                 li      $v0, 0xD45CEF0A  # Load Immediate
.text:00402D90                 addu    $a0, $v0         # Add Unsigned
.text:00402D94                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D98                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D9C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402DA0                 sw      $a0, 8($v0)      # Store Word
; Found the 87th break (@00402da4) ; new pc will be 00402e3c
; ========================= BLOCK 87 =========================
.text:00402E3C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402E40                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402E44                 sll     $v0, 2           # Shift Left Logical
.text:00402E48                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E4C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E50                 lw      $v0, 8($v0)      # Load Word
.text:00402E54                 srl     $v1, $v0, 20     # Shift Right Logical
.text:00402E58                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402E5C                 sll     $v0, 2           # Shift Left Logical
.text:00402E60                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E64                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402E68                 lw      $v0, 8($v0)      # Load Word
.text:00402E6C                 sll     $v0, 12          # Shift Left Logical
.text:00402E70                 or      $v1, $v0         # OR
.text:00402E74                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402E78                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E7C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E80                 sw      $v1, 8($v0)      # Store Word
; Found the 88th break (@00402e84) ; new pc will be 004024cc
; ========================= BLOCK 88 =========================
.text:004024CC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004024D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024D4                 sll     $v0, 2           # Shift Left Logical
.text:004024D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004024E0                 lw      $v0, 8($v0)      # Load Word
.text:004024E4                 sll     $v1, $v0, 30     # Shift Left Logical
.text:004024E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024EC                 sll     $v0, 2           # Shift Left Logical
.text:004024F0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024F4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004024F8                 lw      $v0, 8($v0)      # Load Word
.text:004024FC                 srl     $v0, 2           # Shift Right Logical
.text:00402500                 or      $v1, $v0         # OR
.text:00402504                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402508                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040250C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402510                 sw      $v1, 8($v0)      # Store Word
; Found the 89th break (@00402514) ; new pc will be 00402548
; ========================= BLOCK 89 =========================
.text:00402548                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040254C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402550                 sll     $v0, 2           # Shift Left Logical
.text:00402554                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402558                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040255C                 lw      $v0, 8($v0)      # Load Word
.text:00402560                 nor     $v1, $zero, $v0  # NOR
.text:00402564                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402568                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040256C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402570                 sw      $v1, 8($v0)      # Store Word
; Found the 90th break (@00402574) ; new pc will be 004023f0
; ========================= BLOCK 90 =========================
.text:004023F0                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004023F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004023F8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023FC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402400                 lw      $a0, 8($v0)      # Load Word
.text:00402404                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402408                 addu    $a0, $v0         # Add Unsigned
.text:0040240C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402410                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402414                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402418                 sw      $a0, 8($v0)      # Store Word
; Found the 91th break (@0040241c) ; new pc will be 0040230c
; ========================= BLOCK 91 =========================
.text:0040230C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402310                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402314                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402318                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040231C                 lw      $a0, 8($v0)      # Load Word
.text:00402320                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402324                 subu    $a0, $v0         # Subtract Unsigned
.text:00402328                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040232C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402330                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402334                 sw      $a0, 8($v0)      # Store Word
; Found the 92th break (@00402338) ; new pc will be 0040233c
; ========================= BLOCK 92 =========================
.text:0040233C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402340                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402344                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402348                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040234C                 lw      $a0, 8($v0)      # Load Word
.text:00402350                 li      $v0, 0x7B4DE789  # Load Immediate
.text:00402358                 xor     $a0, $v0         # Exclusive OR
.text:0040235C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402360                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402364                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402368                 sw      $a0, 8($v0)      # Store Word
; Found the 93th break (@0040236c) ; new pc will be 00402f04
; ========================= BLOCK 93 =========================
.text:00402F04                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402F08                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402F0C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F10                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402F14                 lw      $a0, 8($v0)      # Load Word
.text:00402F18                 li      $v0, 0x3ECA6F23  # Load Immediate
.text:00402F20                 addu    $a0, $v0         # Add Unsigned
.text:00402F24                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402F28                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F2C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F30                 sw      $a0, 8($v0)      # Store Word
; Found the 94th break (@00402f34) ; new pc will be 00403630
; ========================= BLOCK 94 =========================
.text:00403630                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403634                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403638                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040363C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403640                 lw      $a0, 8($v0)      # Load Word
.text:00403644                 li      $v0, 0x3D68A35C  # Load Immediate
.text:0040364C                 xor     $a0, $v0         # Exclusive OR
.text:00403650                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403654                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403658                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040365C                 sw      $a0, 8($v0)      # Store Word
; Found the 95th break (@00403660) ; new pc will be 004033dc
; ========================= BLOCK 95 =========================
.text:004033DC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004033E0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033E4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033E8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004033EC                 lw      $a0, 8($v0)      # Load Word
.text:004033F0                 li      $v0, 0xD0358C15  # Load Immediate
.text:004033F8                 addu    $a0, $v0         # Add Unsigned
.text:004033FC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403400                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403404                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403408                 sw      $a0, 8($v0)      # Store Word
; Found the 96th break (@0040340c) ; new pc will be 0040249c
; ========================= BLOCK 96 =========================
.text:0040249C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004024A0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024A4                 sll     $v0, 2           # Shift Left Logical
.text:004024A8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024AC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004024B0                 lw      $v0, 8($v0)      # Load Word
.text:004024B4                 nor     $v1, $zero, $v0  # NOR
.text:004024B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004024BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004024C4                 sw      $v1, 8($v0)      # Store Word
; Found the 97th break (@004024c8) ; new pc will be 004035fc
; ========================= BLOCK 97 =========================
.text:004035FC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403600                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403604                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403608                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040360C                 lw      $a0, 8($v0)      # Load Word
.text:00403610                 li      $v0, 0x8103D046  # Load Immediate
.text:00403618                 xor     $a0, $v0         # Exclusive OR
.text:0040361C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403620                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403624                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403628                 sw      $a0, 8($v0)      # Store Word
; Found the 98th break (@0040362c) ; new pc will be 00403580
; ========================= BLOCK 98 =========================
.text:00403580                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403584                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403588                 sll     $v0, 2           # Shift Left Logical
.text:0040358C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403590                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403594                 lw      $v0, 8($v0)      # Load Word
.text:00403598                 sll     $v1, $v0, 28     # Shift Left Logical
.text:0040359C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004035A0                 sll     $v0, 2           # Shift Left Logical
.text:004035A4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035A8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004035AC                 lw      $v0, 8($v0)      # Load Word
.text:004035B0                 srl     $v0, 4           # Shift Right Logical
.text:004035B4                 or      $v1, $v0         # OR
.text:004035B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004035BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004035C4                 sw      $v1, 8($v0)      # Store Word
; Found the 99th break (@004035c8) ; new pc will be 0040397c
; ========================= BLOCK 99 =========================
.text:0040397C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403980                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403984                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403988                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040398C                 lw      $a0, 8($v0)      # Load Word
.text:00403990                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403994                 xor     $a0, $v0         # Exclusive OR
.text:00403998                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040399C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004039A4                 sw      $a0, 8($v0)      # Store Word
; Found the 100th break (@004039a8) ; new pc will be 004039dc
; ========================= BLOCK 100 =========================
.text:004039DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004039E0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004039E4                 sw      $v0, 0x48+i($fp)  # Store Word
; Found the 0th break (@0040228c) ; new pc will be 004033dc
; ========================= BLOCK 0 =========================
.text:004033DC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004033E0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033E4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033E8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004033EC                 lw      $a0, 8($v0)      # Load Word
.text:004033F0                 li      $v0, 0xD0358C15  # Load Immediate
.text:004033F8                 addu    $a0, $v0         # Add Unsigned
.text:004033FC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403400                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403404                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403408                 sw      $a0, 8($v0)      # Store Word
; Found the 1th break (@0040340c) ; new pc will be 00403778
; ========================= BLOCK 1 =========================
.text:00403778                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040377C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403780                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403784                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403788                 lw      $a0, 8($v0)      # Load Word
.text:0040378C                 li      $v0, 0x6EDC032   # Load Immediate
.text:00403794                 addu    $a0, $v0         # Add Unsigned
.text:00403798                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040379C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004037A4                 sw      $a0, 8($v0)      # Store Word
; Found the 2th break (@004037a8) ; new pc will be 00402290
; ========================= BLOCK 2 =========================
.text:00402290                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402294                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402298                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040229C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004022A0                 lw      $a0, 8($v0)      # Load Word
.text:004022A4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022A8                 subu    $a0, $v0         # Subtract Unsigned
.text:004022AC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004022B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004022B8                 sw      $a0, 8($v0)      # Store Word
; Found the 3th break (@004022bc) ; new pc will be 00403694
; ========================= BLOCK 3 =========================
.text:00403694                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403698                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040369C                 sll     $v0, 2           # Shift Left Logical
.text:004036A0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036A4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004036A8                 lw      $v0, 8($v0)      # Load Word
.text:004036AC                 sll     $v1, $v0, 6      # Shift Left Logical
.text:004036B0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004036B4                 sll     $v0, 2           # Shift Left Logical
.text:004036B8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036BC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004036C0                 lw      $v0, 8($v0)      # Load Word
.text:004036C4                 srl     $v0, 26          # Shift Right Logical
.text:004036C8                 or      $v1, $v0         # OR
.text:004036CC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004036D0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036D4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004036D8                 sw      $v1, 8($v0)      # Store Word
; Found the 4th break (@004036dc) ; new pc will be 00402b08
; ========================= BLOCK 4 =========================
.text:00402B08                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402B0C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402B10                 sll     $v0, 2           # Shift Left Logical
.text:00402B14                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B18                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402B1C                 lw      $v0, 8($v0)      # Load Word
.text:00402B20                 srl     $v1, $v0, 26     # Shift Right Logical
.text:00402B24                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402B28                 sll     $v0, 2           # Shift Left Logical
.text:00402B2C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B30                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402B34                 lw      $v0, 8($v0)      # Load Word
.text:00402B38                 sll     $v0, 6           # Shift Left Logical
.text:00402B3C                 or      $v1, $v0         # OR
.text:00402B40                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402B44                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B48                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B4C                 sw      $v1, 8($v0)      # Store Word
; Found the 5th break (@00402b50) ; new pc will be 00403520
; ========================= BLOCK 5 =========================
.text:00403520                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403524                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403528                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040352C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403530                 lw      $a0, 8($v0)      # Load Word
.text:00403534                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403538                 xor     $a0, $v0         # Exclusive OR
.text:0040353C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403540                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403544                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403548                 sw      $a0, 8($v0)      # Store Word
; Found the 6th break (@0040354c) ; new pc will be 004031d4
; ========================= BLOCK 6 =========================
.text:004031D4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004031D8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004031DC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031E0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004031E4                 lw      $a0, 8($v0)      # Load Word
.text:004031E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004031EC                 xor     $a0, $v0         # Exclusive OR
.text:004031F0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004031F4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031F8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004031FC                 sw      $a0, 8($v0)      # Store Word
; Found the 7th break (@00403200) ; new pc will be 00403378
; ========================= BLOCK 7 =========================
.text:00403378                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040337C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403380                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403384                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403388                 lw      $a0, 8($v0)      # Load Word
.text:0040338C                 li      $v0, 0xBFD991A0  # Load Immediate
.text:00403394                 xor     $a0, $v0         # Exclusive OR
.text:00403398                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040339C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004033A4                 sw      $a0, 8($v0)      # Store Word
; Found the 8th break (@004033a8) ; new pc will be 004027d8
; ========================= BLOCK 8 =========================
.text:004027D8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004027DC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004027E8                 lw      $a0, 8($v0)      # Load Word
.text:004027EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004027F0                 subu    $a0, $v0         # Subtract Unsigned
.text:004027F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027F8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027FC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402800                 sw      $a0, 8($v0)      # Store Word
; Found the 9th break (@00402804) ; new pc will be 0040397c
; ========================= BLOCK 9 =========================
.text:0040397C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403980                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403984                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403988                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040398C                 lw      $a0, 8($v0)      # Load Word
.text:00403990                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403994                 xor     $a0, $v0         # Exclusive OR
.text:00403998                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040399C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039A0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004039A4                 sw      $a0, 8($v0)      # Store Word
; Found the 10th break (@004039a8) ; new pc will be 00402608
; ========================= BLOCK 10 =========================
.text:00402608                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040260C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402610                 sll     $v0, 2           # Shift Left Logical
.text:00402614                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402618                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040261C                 lw      $v0, 8($v0)      # Load Word
.text:00402620                 srl     $v1, $v0, 23     # Shift Right Logical
.text:00402624                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402628                 sll     $v0, 2           # Shift Left Logical
.text:0040262C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402630                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402634                 lw      $v0, 8($v0)      # Load Word
.text:00402638                 sll     $v0, 9           # Shift Left Logical
.text:0040263C                 or      $v1, $v0         # OR
.text:00402640                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402644                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402648                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040264C                 sw      $v1, 8($v0)      # Store Word
; Found the 11th break (@00402650) ; new pc will be 00403068
; ========================= BLOCK 11 =========================
.text:00403068                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040306C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403070                 sll     $v0, 2           # Shift Left Logical
.text:00403074                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403078                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040307C                 lw      $v0, 8($v0)      # Load Word
.text:00403080                 nor     $v1, $zero, $v0  # NOR
.text:00403084                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403088                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040308C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403090                 sw      $v1, 8($v0)      # Store Word
; Found the 12th break (@00403094) ; new pc will be 00402c04
; ========================= BLOCK 12 =========================
.text:00402C04                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402C08                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C0C                 sll     $v0, 2           # Shift Left Logical
.text:00402C10                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C14                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402C18                 lw      $v0, 8($v0)      # Load Word
.text:00402C1C                 srl     $v1, $v0, 4      # Shift Right Logical
.text:00402C20                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C24                 sll     $v0, 2           # Shift Left Logical
.text:00402C28                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C2C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402C30                 lw      $v0, 8($v0)      # Load Word
.text:00402C34                 sll     $v0, 28          # Shift Left Logical
.text:00402C38                 or      $v1, $v0         # OR
.text:00402C3C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402C40                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C44                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402C48                 sw      $v1, 8($v0)      # Store Word
; Found the 13th break (@00402c4c) ; new pc will be 00402548
; ========================= BLOCK 13 =========================
.text:00402548                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040254C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402550                 sll     $v0, 2           # Shift Left Logical
.text:00402554                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402558                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040255C                 lw      $v0, 8($v0)      # Load Word
.text:00402560                 nor     $v1, $zero, $v0  # NOR
.text:00402564                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402568                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040256C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402570                 sw      $v1, 8($v0)      # Store Word
; Found the 14th break (@00402574) ; new pc will be 004034f0
; ========================= BLOCK 14 =========================
.text:004034F0                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004034F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004034F8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034FC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403500                 lw      $a0, 8($v0)      # Load Word
.text:00403504                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403508                 addu    $a0, $v0         # Add Unsigned
.text:0040350C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403510                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403514                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403518                 sw      $a0, 8($v0)      # Store Word
; Found the 15th break (@0040351c) ; new pc will be 004035cc
; ========================= BLOCK 15 =========================
.text:004035CC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004035D0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004035D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004035DC                 lw      $a0, 8($v0)      # Load Word
.text:004035E0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004035E4                 addu    $a0, $v0         # Add Unsigned
.text:004035E8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004035EC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035F0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004035F4                 sw      $a0, 8($v0)      # Store Word
; Found the 16th break (@004035f8) ; new pc will be 004032fc
; ========================= BLOCK 16 =========================
.text:004032FC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403300                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403304                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403308                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040330C                 lw      $a0, 8($v0)      # Load Word
.text:00403310                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403314                 xor     $a0, $v0         # Exclusive OR
.text:00403318                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040331C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403320                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403324                 sw      $a0, 8($v0)      # Store Word
; Found the 17th break (@00403328) ; new pc will be 00403098
; ========================= BLOCK 17 =========================
.text:00403098                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040309C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030A0                 sll     $v0, 2           # Shift Left Logical
.text:004030A4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030A8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004030AC                 lw      $v0, 8($v0)      # Load Word
.text:004030B0                 srl     $v1, $v0, 3      # Shift Right Logical
.text:004030B4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030B8                 sll     $v0, 2           # Shift Left Logical
.text:004030BC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030C0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004030C4                 lw      $v0, 8($v0)      # Load Word
.text:004030C8                 sll     $v0, 29          # Shift Left Logical
.text:004030CC                 or      $v1, $v0         # OR
.text:004030D0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004030D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004030DC                 sw      $v1, 8($v0)      # Store Word
; Found the 18th break (@004030e0) ; new pc will be 0040372c
; ========================= BLOCK 18 =========================
.text:0040372C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403730                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403734                 sll     $v0, 2           # Shift Left Logical
.text:00403738                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040373C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403740                 lw      $v0, 8($v0)      # Load Word
.text:00403744                 sll     $v1, $v0, 5      # Shift Left Logical
.text:00403748                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040374C                 sll     $v0, 2           # Shift Left Logical
.text:00403750                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403754                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403758                 lw      $v0, 8($v0)      # Load Word
.text:0040375C                 srl     $v0, 27          # Shift Right Logical
.text:00403760                 or      $v1, $v0         # OR
.text:00403764                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403768                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040376C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403770                 sw      $v1, 8($v0)      # Store Word
; Found the 19th break (@00403774) ; new pc will be 00402d44
; ========================= BLOCK 19 =========================
.text:00402D44                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D48                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D4C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D50                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D54                 lw      $a0, 8($v0)      # Load Word
.text:00402D58                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402D5C                 addu    $a0, $v0         # Add Unsigned
.text:00402D60                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D64                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D68                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402D6C                 sw      $a0, 8($v0)      # Store Word
; Found the 20th break (@00402d70) ; new pc will be 0040286c
; ========================= BLOCK 20 =========================
.text:0040286C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402870                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402874                 sll     $v0, 2           # Shift Left Logical
.text:00402878                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040287C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402880                 lw      $v1, 8($v0)      # Load Word
.text:00402884                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402888                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040288C                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00402890                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402894                 sll     $v0, 2           # Shift Left Logical
.text:00402898                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040289C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004028A0                 lw      $a1, 8($v0)      # Load Word
.text:004028A4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004028A8                 nor     $v0, $zero, $v0  # NOR
.text:004028AC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004028B0                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004028B4                 or      $v1, $v0         # OR
.text:004028B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004028BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004028C4                 sw      $v1, 8($v0)      # Store Word
; Found the 21th break (@004028c8) ; new pc will be 00403144
; ========================= BLOCK 21 =========================
.text:00403144                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403148                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040314C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403150                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403154                 lw      $a0, 8($v0)      # Load Word
.text:00403158                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040315C                 addu    $a0, $v0         # Add Unsigned
.text:00403160                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403164                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403168                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040316C                 sw      $a0, 8($v0)      # Store Word
; Found the 22th break (@00403170) ; new pc will be 00403550
; ========================= BLOCK 22 =========================
.text:00403550                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403554                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403558                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040355C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403560                 lw      $a0, 8($v0)      # Load Word
.text:00403564                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403568                 xor     $a0, $v0         # Exclusive OR
.text:0040356C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403570                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403574                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403578                 sw      $a0, 8($v0)      # Store Word
; Found the 23th break (@0040357c) ; new pc will be 00402f38
; ========================= BLOCK 23 =========================
.text:00402F38                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402F3C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F40                 sll     $v0, 2           # Shift Left Logical
.text:00402F44                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F48                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F4C                 lw      $v0, 8($v0)      # Load Word
.text:00402F50                 nor     $v1, $zero, $v0  # NOR
.text:00402F54                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402F58                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F5C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402F60                 sw      $v1, 8($v0)      # Store Word
; Found the 24th break (@00402f64) ; new pc will be 00402eb8
; ========================= BLOCK 24 =========================
.text:00402EB8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402EBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402EC0                 sll     $v0, 2           # Shift Left Logical
.text:00402EC4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402ECC                 lw      $v0, 8($v0)      # Load Word
.text:00402ED0                 sll     $v1, $v0, 18     # Shift Left Logical
.text:00402ED4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402ED8                 sll     $v0, 2           # Shift Left Logical
.text:00402EDC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EE0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402EE4                 lw      $v0, 8($v0)      # Load Word
.text:00402EE8                 srl     $v0, 14          # Shift Right Logical
.text:00402EEC                 or      $v1, $v0         # OR
.text:00402EF0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402EF4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EF8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402EFC                 sw      $v1, 8($v0)      # Store Word
; Found the 25th break (@00402f00) ; new pc will be 00402f04
; ========================= BLOCK 25 =========================
.text:00402F04                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402F08                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402F0C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F10                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402F14                 lw      $a0, 8($v0)      # Load Word
.text:00402F18                 li      $v0, 0x3ECA6F23  # Load Immediate
.text:00402F20                 addu    $a0, $v0         # Add Unsigned
.text:00402F24                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402F28                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F2C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F30                 sw      $a0, 8($v0)      # Store Word
; Found the 26th break (@00402f34) ; new pc will be 004035fc
; ========================= BLOCK 26 =========================
.text:004035FC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403600                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403604                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403608                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040360C                 lw      $a0, 8($v0)      # Load Word
.text:00403610                 li      $v0, 0x8103D046  # Load Immediate
.text:00403618                 xor     $a0, $v0         # Exclusive OR
.text:0040361C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403620                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403624                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403628                 sw      $a0, 8($v0)      # Store Word
; Found the 27th break (@0040362c) ; new pc will be 00402aa8
; ========================= BLOCK 27 =========================
.text:00402AA8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402AAC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402AB0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AB4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402AB8                 lw      $a0, 8($v0)      # Load Word
.text:00402ABC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402AC0                 xor     $a0, $v0         # Exclusive OR
.text:00402AC4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402AC8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402ACC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402AD0                 sw      $a0, 8($v0)      # Store Word
; Found the 28th break (@00402ad4) ; new pc will be 00402b88
; ========================= BLOCK 28 =========================
.text:00402B88                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402B8C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B90                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B94                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B98                 lw      $a0, 8($v0)      # Load Word
.text:00402B9C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BA0                 subu    $a0, $v0         # Subtract Unsigned
.text:00402BA4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402BA8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402BB0                 sw      $a0, 8($v0)      # Store Word
; Found the 29th break (@00402bb4) ; new pc will be 00402cb0
; ========================= BLOCK 29 =========================
.text:00402CB0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402CB4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402CB8                 sll     $v0, 2           # Shift Left Logical
.text:00402CBC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CC0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402CC4                 lw      $v0, 8($v0)      # Load Word
.text:00402CC8                 nor     $v1, $zero, $v0  # NOR
.text:00402CCC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402CD0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CD4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402CD8                 sw      $v1, 8($v0)      # Store Word
; Found the 30th break (@00402cdc) ; new pc will be 004033ac
; ========================= BLOCK 30 =========================
.text:004033AC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004033B0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033B4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033B8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004033BC                 lw      $a0, 8($v0)      # Load Word
.text:004033C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004033C4                 addu    $a0, $v0         # Add Unsigned
.text:004033C8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004033CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004033D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004033D4                 sw      $a0, 8($v0)      # Store Word
; Found the 31th break (@004033d8) ; new pc will be 00402c50
; ========================= BLOCK 31 =========================
.text:00402C50                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402C54                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C58                 sll     $v0, 2           # Shift Left Logical
.text:00402C5C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C60                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402C64                 lw      $v1, 8($v0)      # Load Word
.text:00402C68                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C6C                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00402C70                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:00402C74                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C78                 sll     $v0, 2           # Shift Left Logical
.text:00402C7C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402C80                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402C84                 lw      $a1, 8($v0)      # Load Word
.text:00402C88                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402C8C                 nor     $v0, $zero, $v0  # NOR
.text:00402C90                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00402C94                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:00402C98                 or      $v1, $v0         # OR
.text:00402C9C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402CA0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CA4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402CA8                 sw      $v1, 8($v0)      # Store Word
; Found the 32th break (@00402cac) ; new pc will be 00402dd8
; ========================= BLOCK 32 =========================
.text:00402DD8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402DDC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DE0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DE4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402DE8                 lw      $a0, 8($v0)      # Load Word
.text:00402DEC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402DF0                 subu    $a0, $v0         # Subtract Unsigned
.text:00402DF4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DF8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DFC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E00                 sw      $a0, 8($v0)      # Store Word
; Found the 33th break (@00402e04) ; new pc will be 00402420
; ========================= BLOCK 33 =========================
.text:00402420                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402424                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402428                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040242C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402430                 lw      $a0, 8($v0)      # Load Word
.text:00402434                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402438                 xor     $a0, $v0         # Exclusive OR
.text:0040243C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402440                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402444                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402448                 sw      $a0, 8($v0)      # Store Word
; Found the 34th break (@0040244c) ; new pc will be 004023f0
; ========================= BLOCK 34 =========================
.text:004023F0                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004023F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004023F8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023FC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402400                 lw      $a0, 8($v0)      # Load Word
.text:00402404                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402408                 addu    $a0, $v0         # Add Unsigned
.text:0040240C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402410                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402414                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402418                 sw      $a0, 8($v0)      # Store Word
; Found the 35th break (@0040241c) ; new pc will be 004037ac
; ========================= BLOCK 35 =========================
.text:004037AC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004037B0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037B4                 sll     $v0, 2           # Shift Left Logical
.text:004037B8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037BC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004037C0                 lw      $v1, 8($v0)      # Load Word
.text:004037C4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037C8                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004037CC                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004037D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037D4                 sll     $v0, 2           # Shift Left Logical
.text:004037D8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004037DC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004037E0                 lw      $a1, 8($v0)      # Load Word
.text:004037E4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004037E8                 nor     $v0, $zero, $v0  # NOR
.text:004037EC                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004037F0                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004037F4                 or      $v1, $v0         # OR
.text:004037F8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004037FC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403800                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403804                 sw      $v1, 8($v0)      # Store Word
; Found the 36th break (@00403808) ; new pc will be 00403444
; ========================= BLOCK 36 =========================
.text:00403444                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403448                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040344C                 sll     $v0, 2           # Shift Left Logical
.text:00403450                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403454                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403458                 lw      $v1, 8($v0)      # Load Word
.text:0040345C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403460                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403464                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403468                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040346C                 sll     $v0, 2           # Shift Left Logical
.text:00403470                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403474                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403478                 lw      $a1, 8($v0)      # Load Word
.text:0040347C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403480                 nor     $v0, $zero, $v0  # NOR
.text:00403484                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403488                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040348C                 or      $v1, $v0         # OR
.text:00403490                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403494                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403498                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040349C                 sw      $v1, 8($v0)      # Store Word
; Found the 37th break (@004034a0) ; new pc will be 00403174
; ========================= BLOCK 37 =========================
.text:00403174                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403178                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040317C                 sll     $v0, 2           # Shift Left Logical
.text:00403180                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403184                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403188                 lw      $v1, 8($v0)      # Load Word
.text:0040318C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403190                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403194                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403198                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040319C                 sll     $v0, 2           # Shift Left Logical
.text:004031A0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031A4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004031A8                 lw      $a1, 8($v0)      # Load Word
.text:004031AC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004031B0                 nor     $v0, $zero, $v0  # NOR
.text:004031B4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004031B8                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:004031BC                 or      $v1, $v0         # OR
.text:004031C0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004031C4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004031C8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004031CC                 sw      $v1, 8($v0)      # Store Word
; Found the 38th break (@004031d0) ; new pc will be 00402ad8
; ========================= BLOCK 38 =========================
.text:00402AD8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402ADC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402AE0                 sll     $v0, 2           # Shift Left Logical
.text:00402AE4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AE8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402AEC                 lw      $v0, 8($v0)      # Load Word
.text:00402AF0                 nor     $v1, $zero, $v0  # NOR
.text:00402AF4                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402AF8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402AFC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B00                 sw      $v1, 8($v0)      # Store Word
; Found the 39th break (@00402b04) ; new pc will be 004032cc
; ========================= BLOCK 39 =========================
.text:004032CC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004032D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004032D4                 sll     $v0, 2           # Shift Left Logical
.text:004032D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004032E0                 lw      $v0, 8($v0)      # Load Word
.text:004032E4                 nor     $v1, $zero, $v0  # NOR
.text:004032E8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004032EC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032F0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004032F4                 sw      $v1, 8($v0)      # Store Word
; Found the 40th break (@004032f8) ; new pc will be 00402774
; ========================= BLOCK 40 =========================
.text:00402774                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402778                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040277C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402780                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402784                 lw      $a0, 8($v0)      # Load Word
.text:00402788                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040278C                 xor     $a0, $v0         # Exclusive OR
.text:00402790                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402794                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402798                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040279C                 sw      $a0, 8($v0)      # Store Word
; Found the 41th break (@004027a0) ; new pc will be 00402a2c
; ========================= BLOCK 41 =========================
.text:00402A2C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402A30                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A34                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A38                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402A3C                 lw      $a0, 8($v0)      # Load Word
.text:00402A40                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A44                 subu    $a0, $v0         # Subtract Unsigned
.text:00402A48                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A4C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A50                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A54                 sw      $a0, 8($v0)      # Store Word
; Found the 42th break (@00402a58) ; new pc will be 00402964
; ========================= BLOCK 42 =========================
.text:00402964                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402968                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040296C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402970                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402974                 lw      $a0, 8($v0)      # Load Word
.text:00402978                 li      $v0, 0x737F298   # Load Immediate
.text:00402980                 addu    $a0, $v0         # Add Unsigned
.text:00402984                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402988                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040298C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402990                 sw      $a0, 8($v0)      # Store Word
; Found the 43th break (@00402994) ; new pc will be 004024cc
; ========================= BLOCK 43 =========================
.text:004024CC                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004024D0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024D4                 sll     $v0, 2           # Shift Left Logical
.text:004024D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004024E0                 lw      $v0, 8($v0)      # Load Word
.text:004024E4                 sll     $v1, $v0, 30     # Shift Left Logical
.text:004024E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024EC                 sll     $v0, 2           # Shift Left Logical
.text:004024F0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024F4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004024F8                 lw      $v0, 8($v0)      # Load Word
.text:004024FC                 srl     $v0, 2           # Shift Right Logical
.text:00402500                 or      $v1, $v0         # OR
.text:00402504                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402508                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040250C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402510                 sw      $v1, 8($v0)      # Store Word
; Found the 44th break (@00402514) ; new pc will be 00402808
; ========================= BLOCK 44 =========================
.text:00402808                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040280C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402810                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402814                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402818                 lw      $a0, 8($v0)      # Load Word
.text:0040281C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402820                 subu    $a0, $v0         # Subtract Unsigned
.text:00402824                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402828                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040282C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402830                 sw      $a0, 8($v0)      # Store Word
; Found the 45th break (@00402834) ; new pc will be 004022c0
; ========================= BLOCK 45 =========================
.text:004022C0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004022C4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022C8                 sll     $v0, 2           # Shift Left Logical
.text:004022CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004022D4                 lw      $v0, 8($v0)      # Load Word
.text:004022D8                 srl     $v1, $v0, 1      # Shift Right Logical
.text:004022DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004022E0                 sll     $v0, 2           # Shift Left Logical
.text:004022E4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004022E8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004022EC                 lw      $v0, 8($v0)      # Load Word
.text:004022F0                 sll     $v0, 31          # Shift Left Logical
.text:004022F4                 or      $v1, $v0         # OR
.text:004022F8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004022FC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402300                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402304                 sw      $v1, 8($v0)      # Store Word
; Found the 46th break (@00402308) ; new pc will be 004027a4
; ========================= BLOCK 46 =========================
.text:004027A4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004027A8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027AC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027B0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004027B4                 lw      $a0, 8($v0)      # Load Word
.text:004027B8                 li      $v0, 0xD0970C74  # Load Immediate
.text:004027C0                 addu    $a0, $v0         # Add Unsigned
.text:004027C4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004027C8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004027CC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004027D0                 sw      $a0, 8($v0)      # Store Word
; Found the 47th break (@004027d4) ; new pc will be 00402998
; ========================= BLOCK 47 =========================
.text:00402998                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040299C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029A0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029A4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004029A8                 lw      $a0, 8($v0)      # Load Word
.text:004029AC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004029B0                 subu    $a0, $v0         # Subtract Unsigned
.text:004029B4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029B8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029BC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004029C0                 sw      $a0, 8($v0)      # Store Word
; Found the 48th break (@004029c4) ; new pc will be 0040380c
; ========================= BLOCK 48 =========================
.text:0040380C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403810                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403814                 sll     $v0, 2           # Shift Left Logical
.text:00403818                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040381C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403820                 lw      $v0, 8($v0)      # Load Word
.text:00403824                 sll     $v1, $v0, 16     # Shift Left Logical
.text:00403828                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040382C                 sll     $v0, 2           # Shift Left Logical
.text:00403830                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403834                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403838                 lw      $v0, 8($v0)      # Load Word
.text:0040383C                 srl     $v0, 16          # Shift Right Logical
.text:00403840                 or      $v1, $v0         # OR
.text:00403844                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403848                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040384C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403850                 sw      $v1, 8($v0)      # Store Word
; Found the 49th break (@00403854) ; new pc will be 00402fb4
; ========================= BLOCK 49 =========================
.text:00402FB4                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402FB8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FBC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FC0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FC4                 lw      $a0, 8($v0)      # Load Word
.text:00402FC8                 li      $v0, 0xCC4E5D94  # Load Immediate
.text:00402FD0                 xor     $a0, $v0         # Exclusive OR
.text:00402FD4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FD8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FDC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402FE0                 sw      $a0, 8($v0)      # Store Word
; Found the 50th break (@00402fe4) ; new pc will be 00402e08
; ========================= BLOCK 50 =========================
.text:00402E08                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402E0C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E10                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E14                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E18                 lw      $a0, 8($v0)      # Load Word
.text:00402E1C                 li      $v0, 0x73C69F47  # Load Immediate
.text:00402E24                 addu    $a0, $v0         # Add Unsigned
.text:00402E28                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E2C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E30                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E34                 sw      $a0, 8($v0)      # Store Word
; Found the 51th break (@00402e38) ; new pc will be 00402930
; ========================= BLOCK 51 =========================
.text:00402930                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402934                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402938                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040293C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402940                 lw      $a0, 8($v0)      # Load Word
.text:00402944                 li      $v0, 0x4CC0DC26  # Load Immediate
.text:0040294C                 xor     $a0, $v0         # Exclusive OR
.text:00402950                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402954                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402958                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040295C                 sw      $a0, 8($v0)      # Store Word
; Found the 52th break (@00402960) ; new pc will be 004039ac
; ========================= BLOCK 52 =========================
.text:004039AC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004039B0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004039B4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039B8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004039BC                 lw      $a0, 8($v0)      # Load Word
.text:004039C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004039C4                 addu    $a0, $v0         # Add Unsigned
.text:004039C8                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004039CC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004039D0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004039D4                 sw      $a0, 8($v0)      # Store Word
; Found the 53th break (@004039d8) ; new pc will be 004025d8
; ========================= BLOCK 53 =========================
.text:004025D8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004025DC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025E8                 lw      $a0, 8($v0)      # Load Word
.text:004025EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004025F0                 addu    $a0, $v0         # Add Unsigned
.text:004025F4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025F8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025FC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402600                 sw      $a0, 8($v0)      # Store Word
; Found the 54th break (@00402604) ; new pc will be 0040233c
; ========================= BLOCK 54 =========================
.text:0040233C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402340                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402344                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402348                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040234C                 lw      $a0, 8($v0)      # Load Word
.text:00402350                 li      $v0, 0x7B4DE789  # Load Immediate
.text:00402358                 xor     $a0, $v0         # Exclusive OR
.text:0040235C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402360                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402364                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402368                 sw      $a0, 8($v0)      # Store Word
; Found the 55th break (@0040236c) ; new pc will be 00403204
; ========================= BLOCK 55 =========================
.text:00403204                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403208                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040320C                 sll     $v0, 2           # Shift Left Logical
.text:00403210                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403214                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403218                 lw      $v0, 8($v0)      # Load Word
.text:0040321C                 nor     $v1, $zero, $v0  # NOR
.text:00403220                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403224                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403228                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040322C                 sw      $v1, 8($v0)      # Store Word
; Found the 56th break (@00403230) ; new pc will be 00402714
; ========================= BLOCK 56 =========================
.text:00402714                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402718                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040271C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402720                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402724                 lw      $a0, 8($v0)      # Load Word
.text:00402728                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040272C                 addu    $a0, $v0         # Add Unsigned
.text:00402730                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402734                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402738                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040273C                 sw      $a0, 8($v0)      # Store Word
; Found the 57th break (@00402740) ; new pc will be 00403888
; ========================= BLOCK 57 =========================
.text:00403888                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040388C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403890                 sll     $v0, 2           # Shift Left Logical
.text:00403894                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403898                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040389C                 lw      $v0, 8($v0)      # Load Word
.text:004038A0                 nor     $v1, $zero, $v0  # NOR
.text:004038A4                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004038A8                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038AC                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038B0                 sw      $v1, 8($v0)      # Store Word
; Found the 58th break (@004038b4) ; new pc will be 00402d74
; ========================= BLOCK 58 =========================
.text:00402D74                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D78                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D7C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D80                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D84                 lw      $a0, 8($v0)      # Load Word
.text:00402D88                 li      $v0, 0xD45CEF0A  # Load Immediate
.text:00402D90                 addu    $a0, $v0         # Add Unsigned
.text:00402D94                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D98                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D9C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402DA0                 sw      $a0, 8($v0)      # Store Word
; Found the 59th break (@00402da4) ; new pc will be 00402b54
; ========================= BLOCK 59 =========================
.text:00402B54                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402B58                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B5C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B60                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402B64                 lw      $a0, 8($v0)      # Load Word
.text:00402B68                 li      $v0, 0x79662B5D  # Load Immediate
.text:00402B70                 addu    $a0, $v0         # Add Unsigned
.text:00402B74                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402B78                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402B7C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402B80                 sw      $a0, 8($v0)      # Store Word
; Found the 60th break (@00402b84) ; new pc will be 004029f8
; ========================= BLOCK 60 =========================
.text:004029F8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004029FC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A00                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A04                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402A08                 lw      $a0, 8($v0)      # Load Word
.text:00402A0C                 li      $v0, 0x81674F2B  # Load Immediate
.text:00402A14                 addu    $a0, $v0         # Add Unsigned
.text:00402A18                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402A1C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A20                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A24                 sw      $a0, 8($v0)      # Store Word
; Found the 61th break (@00402a28) ; new pc will be 00402fe8
; ========================= BLOCK 61 =========================
.text:00402FE8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402FEC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402FF0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FF4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FF8                 lw      $a0, 8($v0)      # Load Word
.text:00402FFC                 li      $v0, 0x38C1FEB8  # Load Immediate
.text:00403004                 xor     $a0, $v0         # Exclusive OR
.text:00403008                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040300C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403010                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403014                 sw      $a0, 8($v0)      # Store Word
; Found the 62th break (@00403018) ; new pc will be 00402518
; ========================= BLOCK 62 =========================
.text:00402518                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040251C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402520                 sll     $v0, 2           # Shift Left Logical
.text:00402524                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402528                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040252C                 lw      $v0, 8($v0)      # Load Word
.text:00402530                 nor     $v1, $zero, $v0  # NOR
.text:00402534                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402538                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040253C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402540                 sw      $v1, 8($v0)      # Store Word
; Found the 63th break (@00402544) ; new pc will be 00403234
; ========================= BLOCK 63 =========================
.text:00403234                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403238                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040323C                 sll     $v0, 2           # Shift Left Logical
.text:00403240                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403244                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403248                 lw      $v0, 8($v0)      # Load Word
.text:0040324C                 sll     $v1, $v0, 29     # Shift Left Logical
.text:00403250                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403254                 sll     $v0, 2           # Shift Left Logical
.text:00403258                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040325C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403260                 lw      $v0, 8($v0)      # Load Word
.text:00403264                 srl     $v0, 3           # Shift Right Logical
.text:00403268                 or      $v1, $v0         # OR
.text:0040326C                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403270                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403274                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403278                 sw      $v1, 8($v0)      # Store Word
; Found the 64th break (@0040327c) ; new pc will be 00402370
; ========================= BLOCK 64 =========================
.text:00402370                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402374                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402378                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040237C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402380                 lw      $a0, 8($v0)      # Load Word
.text:00402384                 li      $v0, 0x87DD2BC5  # Load Immediate
.text:0040238C                 addu    $a0, $v0         # Add Unsigned
.text:00402390                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402394                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402398                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040239C                 sw      $a0, 8($v0)      # Store Word
; Found the 65th break (@004023a0) ; new pc will be 00402bb8
; ========================= BLOCK 65 =========================
.text:00402BB8                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402BBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BC0                 sll     $v0, 2           # Shift Left Logical
.text:00402BC4                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BC8                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402BCC                 lw      $v0, 8($v0)      # Load Word
.text:00402BD0                 srl     $v1, $v0, 21     # Shift Right Logical
.text:00402BD4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402BD8                 sll     $v0, 2           # Shift Left Logical
.text:00402BDC                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BE0                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402BE4                 lw      $v0, 8($v0)      # Load Word
.text:00402BE8                 sll     $v0, 11          # Shift Left Logical
.text:00402BEC                 or      $v1, $v0         # OR
.text:00402BF0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402BF4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402BF8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402BFC                 sw      $v1, 8($v0)      # Store Word
; Found the 66th break (@00402c00) ; new pc will be 004029c8
; ========================= BLOCK 66 =========================
.text:004029C8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004029CC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029D0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029D4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004029D8                 lw      $a0, 8($v0)      # Load Word
.text:004029DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004029E0                 xor     $a0, $v0         # Exclusive OR
.text:004029E4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004029E8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004029EC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004029F0                 sw      $a0, 8($v0)      # Store Word
; Found the 67th break (@004029f4) ; new pc will be 00402f68
; ========================= BLOCK 67 =========================
.text:00402F68                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402F6C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F70                 sll     $v0, 2           # Shift Left Logical
.text:00402F74                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F78                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402F7C                 lw      $v0, 8($v0)      # Load Word
.text:00402F80                 sll     $v1, $v0, 23     # Shift Left Logical
.text:00402F84                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402F88                 sll     $v0, 2           # Shift Left Logical
.text:00402F8C                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402F90                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402F94                 lw      $v0, 8($v0)      # Load Word
.text:00402F98                 srl     $v0, 9           # Shift Right Logical
.text:00402F9C                 or      $v1, $v0         # OR
.text:00402FA0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402FA4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402FA8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402FAC                 sw      $v1, 8($v0)      # Store Word
; Found the 68th break (@00402fb0) ; new pc will be 00402ce0
; ========================= BLOCK 68 =========================
.text:00402CE0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402CE4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402CE8                 sll     $v0, 2           # Shift Left Logical
.text:00402CEC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402CF0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402CF4                 lw      $v0, 8($v0)      # Load Word
.text:00402CF8                 nor     $v1, $zero, $v0  # NOR
.text:00402CFC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402D00                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D04                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D08                 sw      $v1, 8($v0)      # Store Word
; Found the 69th break (@00402d0c) ; new pc will be 00403858
; ========================= BLOCK 69 =========================
.text:00403858                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040385C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403860                 sll     $v0, 2           # Shift Left Logical
.text:00403864                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403868                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040386C                 lw      $v0, 8($v0)      # Load Word
.text:00403870                 nor     $v1, $zero, $v0  # NOR
.text:00403874                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403878                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040387C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403880                 sw      $v1, 8($v0)      # Store Word
; Found the 70th break (@00403884) ; new pc will be 00402900
; ========================= BLOCK 70 =========================
.text:00402900                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402904                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402908                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040290C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402910                 lw      $a0, 8($v0)      # Load Word
.text:00402914                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402918                 xor     $a0, $v0         # Exclusive OR
.text:0040291C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402920                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402924                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402928                 sw      $a0, 8($v0)      # Store Word
; Found the 71th break (@0040292c) ; new pc will be 004038b8
; ========================= BLOCK 71 =========================
.text:004038B8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004038BC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038C0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038C4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038C8                 lw      $a0, 8($v0)      # Load Word
.text:004038CC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004038D0                 subu    $a0, $v0         # Subtract Unsigned
.text:004038D4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038D8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038DC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004038E0                 sw      $a0, 8($v0)      # Store Word
; Found the 72th break (@004038e4) ; new pc will be 0040230c
; ========================= BLOCK 72 =========================
.text:0040230C                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402310                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402314                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402318                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040231C                 lw      $a0, 8($v0)      # Load Word
.text:00402320                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402324                 subu    $a0, $v0         # Subtract Unsigned
.text:00402328                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040232C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402330                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402334                 sw      $a0, 8($v0)      # Store Word
; Found the 73th break (@00402338) ; new pc will be 00403664
; ========================= BLOCK 73 =========================
.text:00403664                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403668                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040366C                 sll     $v0, 2           # Shift Left Logical
.text:00403670                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403674                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403678                 lw      $v0, 8($v0)      # Load Word
.text:0040367C                 nor     $v1, $zero, $v0  # NOR
.text:00403680                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403684                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403688                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040368C                 sw      $v1, 8($v0)      # Store Word
; Found the 74th break (@00403690) ; new pc will be 004036e0
; ========================= BLOCK 74 =========================
.text:004036E0                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004036E4                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004036E8                 sll     $v0, 2           # Shift Left Logical
.text:004036EC                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004036F0                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004036F4                 lw      $v0, 8($v0)      # Load Word
.text:004036F8                 sll     $v1, $v0, 5      # Shift Left Logical
.text:004036FC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403700                 sll     $v0, 2           # Shift Left Logical
.text:00403704                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403708                 addu    $v0, $a1, $v0    # Add Unsigned
.text:0040370C                 lw      $v0, 8($v0)      # Load Word
.text:00403710                 srl     $v0, 27          # Shift Right Logical
.text:00403714                 or      $v1, $v0         # OR
.text:00403718                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040371C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403720                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403724                 sw      $v1, 8($v0)      # Store Word
; Found the 75th break (@00403728) ; new pc will be 00403580
; ========================= BLOCK 75 =========================
.text:00403580                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403584                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403588                 sll     $v0, 2           # Shift Left Logical
.text:0040358C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403590                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403594                 lw      $v0, 8($v0)      # Load Word
.text:00403598                 sll     $v1, $v0, 28     # Shift Left Logical
.text:0040359C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004035A0                 sll     $v0, 2           # Shift Left Logical
.text:004035A4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035A8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004035AC                 lw      $v0, 8($v0)      # Load Word
.text:004035B0                 srl     $v0, 4           # Shift Right Logical
.text:004035B4                 or      $v1, $v0         # OR
.text:004035B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004035BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004035C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004035C4                 sw      $v1, 8($v0)      # Store Word
; Found the 76th break (@004035c8) ; new pc will be 00402578
; ========================= BLOCK 76 =========================
.text:00402578                 lw      $a0, 0x48+i($fp)  # Load Word
.text:0040257C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402580                 sll     $v0, 2           # Shift Left Logical
.text:00402584                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402588                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040258C                 lw      $v0, 8($v0)      # Load Word
.text:00402590                 nor     $v1, $zero, $v0  # NOR
.text:00402594                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402598                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040259C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025A0                 sw      $v1, 8($v0)      # Store Word
; Found the 77th break (@004025a4) ; new pc will be 004025a8
; ========================= BLOCK 77 =========================
.text:004025A8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004025AC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025B0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025B4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004025B8                 lw      $a0, 8($v0)      # Load Word
.text:004025BC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004025C0                 addu    $a0, $v0         # Add Unsigned
.text:004025C4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004025C8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004025CC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004025D0                 sw      $a0, 8($v0)      # Store Word
; Found the 78th break (@004025d4) ; new pc will be 004038e8
; ========================= BLOCK 78 =========================
.text:004038E8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004038EC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004038F0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004038F4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004038F8                 lw      $a0, 8($v0)      # Load Word
.text:004038FC                 li      $v0, 0xDBFA3745  # Load Immediate
.text:00403904                 addu    $a0, $v0         # Add Unsigned
.text:00403908                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040390C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403910                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403914                 sw      $a0, 8($v0)      # Store Word
; Found the 79th break (@00403918) ; new pc will be 004028cc
; ========================= BLOCK 79 =========================
.text:004028CC                 lw      $v1, 0x48+i($fp)  # Load Word
.text:004028D0                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004028D4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028D8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004028DC                 lw      $a0, 8($v0)      # Load Word
.text:004028E0                 li      $v0, 0x3A2EE307  # Load Immediate
.text:004028E8                 addu    $a0, $v0         # Add Unsigned
.text:004028EC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:004028F0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004028F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004028F8                 sw      $a0, 8($v0)      # Store Word
; Found the 80th break (@004028fc) ; new pc will be 00402da8
; ========================= BLOCK 80 =========================
.text:00402DA8                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402DAC                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DB0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DB4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402DB8                 lw      $a0, 8($v0)      # Load Word
.text:00402DBC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402DC0                 xor     $a0, $v0         # Exclusive OR
.text:00402DC4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402DC8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402DCC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402DD0                 sw      $a0, 8($v0)      # Store Word
; Found the 81th break (@00402dd4) ; new pc will be 00403630
; ========================= BLOCK 81 =========================
.text:00403630                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403634                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403638                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040363C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403640                 lw      $a0, 8($v0)      # Load Word
.text:00403644                 li      $v0, 0x3D68A35C  # Load Immediate
.text:0040364C                 xor     $a0, $v0         # Exclusive OR
.text:00403650                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403654                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403658                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040365C                 sw      $a0, 8($v0)      # Store Word
; Found the 82th break (@00403660) ; new pc will be 00403280
; ========================= BLOCK 82 =========================
.text:00403280                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403284                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403288                 sll     $v0, 2           # Shift Left Logical
.text:0040328C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403290                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403294                 lw      $v0, 8($v0)      # Load Word
.text:00403298                 sll     $v1, $v0, 29     # Shift Left Logical
.text:0040329C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004032A0                 sll     $v0, 2           # Shift Left Logical
.text:004032A4                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032A8                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004032AC                 lw      $v0, 8($v0)      # Load Word
.text:004032B0                 srl     $v0, 3           # Shift Right Logical
.text:004032B4                 or      $v1, $v0         # OR
.text:004032B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004032BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004032C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004032C4                 sw      $v1, 8($v0)      # Store Word
; Found the 83th break (@004032c8) ; new pc will be 00403410
; ========================= BLOCK 83 =========================
.text:00403410                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00403414                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403418                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040341C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403420                 lw      $a0, 8($v0)      # Load Word
.text:00403424                 li      $v0, 0x192B37D2  # Load Immediate
.text:0040342C                 addu    $a0, $v0         # Add Unsigned
.text:00403430                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00403434                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403438                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040343C                 sw      $a0, 8($v0)      # Store Word
; Found the 84th break (@00403440) ; new pc will be 004034a4
; ========================= BLOCK 84 =========================
.text:004034A4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004034A8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004034AC                 sll     $v0, 2           # Shift Left Logical
.text:004034B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004034B8                 lw      $v0, 8($v0)      # Load Word
.text:004034BC                 srl     $v1, $v0, 17     # Shift Right Logical
.text:004034C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004034C4                 sll     $v0, 2           # Shift Left Logical
.text:004034C8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034CC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004034D0                 lw      $v0, 8($v0)      # Load Word
.text:004034D4                 sll     $v0, 15          # Shift Left Logical
.text:004034D8                 or      $v1, $v0         # OR
.text:004034DC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004034E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004034E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004034E8                 sw      $v1, 8($v0)      # Store Word
; Found the 85th break (@004034ec) ; new pc will be 00402744
; ========================= BLOCK 85 =========================
.text:00402744                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402748                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040274C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402750                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402754                 lw      $a0, 8($v0)      # Load Word
.text:00402758                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040275C                 subu    $a0, $v0         # Subtract Unsigned
.text:00402760                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402764                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402768                 addu    $v0, $v1, $v0    # Add Unsigned
.text:0040276C                 sw      $a0, 8($v0)      # Store Word
; Found the 86th break (@00402770) ; new pc will be 00402838
; ========================= BLOCK 86 =========================
.text:00402838                 lw      $v1, 0x48+i($fp)  # Load Word
.text:0040283C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402840                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402844                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402848                 lw      $a0, 8($v0)      # Load Word
.text:0040284C                 li      $v0, 0xB65E867F  # Load Immediate
.text:00402854                 addu    $a0, $v0         # Add Unsigned
.text:00402858                 sll     $v0, $v1, 2      # Shift Left Logical
.text:0040285C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402860                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402864                 sw      $a0, 8($v0)      # Store Word
; Found the 87th break (@00402868) ; new pc will be 00402450
; ========================= BLOCK 87 =========================
.text:00402450                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402454                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402458                 sll     $v0, 2           # Shift Left Logical
.text:0040245C                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402460                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402464                 lw      $v0, 8($v0)      # Load Word
.text:00402468                 sll     $v1, $v0, 13     # Shift Left Logical
.text:0040246C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402470                 sll     $v0, 2           # Shift Left Logical
.text:00402474                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402478                 addu    $v0, $a1, $v0    # Add Unsigned
.text:0040247C                 lw      $v0, 8($v0)      # Load Word
.text:00402480                 srl     $v0, 19          # Shift Right Logical
.text:00402484                 or      $v1, $v0         # OR
.text:00402488                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040248C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402490                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402494                 sw      $v1, 8($v0)      # Store Word
; Found the 88th break (@00402498) ; new pc will be 0040301c
; ========================= BLOCK 88 =========================
.text:0040301C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403020                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403024                 sll     $v0, 2           # Shift Left Logical
.text:00403028                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040302C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403030                 lw      $v0, 8($v0)      # Load Word
.text:00403034                 srl     $v1, $v0, 8      # Shift Right Logical
.text:00403038                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040303C                 sll     $v0, 2           # Shift Left Logical
.text:00403040                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403044                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403048                 lw      $v0, 8($v0)      # Load Word
.text:0040304C                 sll     $v0, 24          # Shift Left Logical
.text:00403050                 or      $v1, $v0         # OR
.text:00403054                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403058                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040305C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403060                 sw      $v1, 8($v0)      # Store Word
; Found the 89th break (@00403064) ; new pc will be 00402d10
; ========================= BLOCK 89 =========================
.text:00402D10                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402D14                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D18                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D1C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402D20                 lw      $a0, 8($v0)      # Load Word
.text:00402D24                 li      $v0, 0xA9BE160D  # Load Immediate
.text:00402D2C                 xor     $a0, $v0         # Exclusive OR
.text:00402D30                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402D34                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402D38                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402D3C                 sw      $a0, 8($v0)      # Store Word
; Found the 90th break (@00402d40) ; new pc will be 00402e88
; ========================= BLOCK 90 =========================
.text:00402E88                 lw      $v1, 0x48+i($fp)  # Load Word
.text:00402E8C                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402E90                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E94                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E98                 lw      $a0, 8($v0)      # Load Word
.text:00402E9C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402EA0                 xor     $a0, $v0         # Exclusive OR
.text:00402EA4                 sll     $v0, $v1, 2      # Shift Left Logical
.text:00402EA8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402EAC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402EB0                 sw      $a0, 8($v0)      # Store Word
; Found the 91th break (@00402eb4) ; new pc will be 0040249c
; ========================= BLOCK 91 =========================
.text:0040249C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004024A0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004024A4                 sll     $v0, 2           # Shift Left Logical
.text:004024A8                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024AC                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004024B0                 lw      $v0, 8($v0)      # Load Word
.text:004024B4                 nor     $v1, $zero, $v0  # NOR
.text:004024B8                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004024BC                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004024C0                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004024C4                 sw      $v1, 8($v0)      # Store Word
; Found the 92th break (@004024c8) ; new pc will be 0040391c
; ========================= BLOCK 92 =========================
.text:0040391C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403920                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403924                 sll     $v0, 2           # Shift Left Logical
.text:00403928                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040392C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403930                 lw      $v1, 8($v0)      # Load Word
.text:00403934                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403938                 addiu   $v0, 1           # Add Immediate Unsigned
.text:0040393C                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403940                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403944                 sll     $v0, 2           # Shift Left Logical
.text:00403948                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040394C                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403950                 lw      $a1, 8($v0)      # Load Word
.text:00403954                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403958                 nor     $v0, $zero, $v0  # NOR
.text:0040395C                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403960                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:00403964                 or      $v1, $v0         # OR
.text:00403968                 sll     $v0, $a0, 2      # Shift Left Logical
.text:0040396C                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403970                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403974                 sw      $v1, 8($v0)      # Store Word
; Found the 93th break (@00403978) ; new pc will be 00402654
; ========================= BLOCK 93 =========================
.text:00402654                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402658                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040265C                 sll     $v0, 2           # Shift Left Logical
.text:00402660                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402664                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402668                 lw      $v1, 8($v0)      # Load Word
.text:0040266C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402670                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00402674                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00402678                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040267C                 sll     $v0, 2           # Shift Left Logical
.text:00402680                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402684                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402688                 lw      $a1, 8($v0)      # Load Word
.text:0040268C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402690                 nor     $v0, $zero, $v0  # NOR
.text:00402694                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00402698                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040269C                 or      $v1, $v0         # OR
.text:004026A0                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004026A4                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026A8                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004026AC                 sw      $v1, 8($v0)      # Store Word
; Found the 94th break (@004026b0) ; new pc will be 0040332c
; ========================= BLOCK 94 =========================
.text:0040332C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00403330                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403334                 sll     $v0, 2           # Shift Left Logical
.text:00403338                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040333C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00403340                 lw      $v0, 8($v0)      # Load Word
.text:00403344                 sll     $v1, $v0, 31     # Shift Left Logical
.text:00403348                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040334C                 sll     $v0, 2           # Shift Left Logical
.text:00403350                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403354                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403358                 lw      $v0, 8($v0)      # Load Word
.text:0040335C                 srl     $v0, 1           # Shift Right Logical
.text:00403360                 or      $v1, $v0         # OR
.text:00403364                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403368                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:0040336C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00403370                 sw      $v1, 8($v0)      # Store Word
; Found the 95th break (@00403374) ; new pc will be 00402a5c
; ========================= BLOCK 95 =========================
.text:00402A5C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402A60                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A64                 sll     $v0, 2           # Shift Left Logical
.text:00402A68                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A6C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402A70                 lw      $v0, 8($v0)      # Load Word
.text:00402A74                 srl     $v1, $v0, 13     # Shift Right Logical
.text:00402A78                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402A7C                 sll     $v0, 2           # Shift Left Logical
.text:00402A80                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A84                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402A88                 lw      $v0, 8($v0)      # Load Word
.text:00402A8C                 sll     $v0, 19          # Shift Left Logical
.text:00402A90                 or      $v1, $v0         # OR
.text:00402A94                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402A98                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402A9C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402AA0                 sw      $v1, 8($v0)      # Store Word
; Found the 96th break (@00402aa4) ; new pc will be 004026b4
; ========================= BLOCK 96 =========================
.text:004026B4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004026B8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026BC                 sll     $v0, 2           # Shift Left Logical
.text:004026C0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026C4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004026C8                 lw      $v1, 8($v0)      # Load Word
.text:004026CC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026D0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004026D4                 srlv    $v1, $v0         # Shift Right Logical Variable
.text:004026D8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026DC                 sll     $v0, 2           # Shift Left Logical
.text:004026E0                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004026E4                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004026E8                 lw      $a1, 8($v0)      # Load Word
.text:004026EC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004026F0                 nor     $v0, $zero, $v0  # NOR
.text:004026F4                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:004026F8                 sllv    $v0, $a1, $v0    # Shift Left Logical Variable
.text:004026FC                 or      $v1, $v0         # OR
.text:00402700                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402704                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402708                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040270C                 sw      $v1, 8($v0)      # Store Word
; Found the 97th break (@00402710) ; new pc will be 00402e3c
; ========================= BLOCK 97 =========================
.text:00402E3C                 lw      $a0, 0x48+i($fp)  # Load Word
.text:00402E40                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402E44                 sll     $v0, 2           # Shift Left Logical
.text:00402E48                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E4C                 addu    $v0, $v1, $v0    # Add Unsigned
.text:00402E50                 lw      $v0, 8($v0)      # Load Word
.text:00402E54                 srl     $v1, $v0, 20     # Shift Right Logical
.text:00402E58                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00402E5C                 sll     $v0, 2           # Shift Left Logical
.text:00402E60                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E64                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00402E68                 lw      $v0, 8($v0)      # Load Word
.text:00402E6C                 sll     $v0, 12          # Shift Left Logical
.text:00402E70                 or      $v1, $v0         # OR
.text:00402E74                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00402E78                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00402E7C                 addu    $v0, $a0, $v0    # Add Unsigned
.text:00402E80                 sw      $v1, 8($v0)      # Store Word
; Found the 98th break (@00402e84) ; new pc will be 004023a4
; ========================= BLOCK 98 =========================
.text:004023A4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004023A8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004023AC                 sll     $v0, 2           # Shift Left Logical
.text:004023B0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023B4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004023B8                 lw      $v0, 8($v0)      # Load Word
.text:004023BC                 srl     $v1, $v0, 12     # Shift Right Logical
.text:004023C0                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004023C4                 sll     $v0, 2           # Shift Left Logical
.text:004023C8                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023CC                 addu    $v0, $a1, $v0    # Add Unsigned
.text:004023D0                 lw      $v0, 8($v0)      # Load Word
.text:004023D4                 sll     $v0, 20          # Shift Left Logical
.text:004023D8                 or      $v1, $v0         # OR
.text:004023DC                 sll     $v0, $a0, 2      # Shift Left Logical
.text:004023E0                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004023E4                 addu    $v0, $a0, $v0    # Add Unsigned
.text:004023E8                 sw      $v1, 8($v0)      # Store Word
; Found the 99th break (@004023ec) ; new pc will be 004030e4
; ========================= BLOCK 99 =========================
.text:004030E4                 lw      $a0, 0x48+i($fp)  # Load Word
.text:004030E8                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004030EC                 sll     $v0, 2           # Shift Left Logical
.text:004030F0                 addiu   $v1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:004030F4                 addu    $v0, $v1, $v0    # Add Unsigned
.text:004030F8                 lw      $v1, 8($v0)      # Load Word
.text:004030FC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403100                 addiu   $v0, 1           # Add Immediate Unsigned
.text:00403104                 sllv    $v1, $v0         # Shift Left Logical Variable
.text:00403108                 lw      $v0, 0x48+i($fp)  # Load Word
.text:0040310C                 sll     $v0, 2           # Shift Left Logical
.text:00403110                 addiu   $a1, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403114                 addu    $v0, $a1, $v0    # Add Unsigned
.text:00403118                 lw      $a1, 8($v0)      # Load Word
.text:0040311C                 lw      $v0, 0x48+i($fp)  # Load Word
.text:00403120                 nor     $v0, $zero, $v0  # NOR
.text:00403124                 addiu   $v0, 0x20        # Add Immediate Unsigned
.text:00403128                 srlv    $v0, $a1, $v0    # Shift Right Logical Variable
.text:0040312C                 or      $v1, $v0         # OR
.text:00403130                 sll     $v0, $a0, 2      # Shift Left Logical
.text:00403134                 addiu   $a0, $fp, 0x48+var_30  # Add Immediate Unsigned
.text:00403138                 addu    $v0, $a0, $v0    # Add Unsigned
.text:0040313C                 sw      $v1, 8($v0)      # Store Word
; Found the 100th break (@00403140) ; new pc will be 004039dc
; ========================= BLOCK 100 =========================
.text:004039DC                 lw      $v0, 0x48+i($fp)  # Load Word
.text:004039E0                 addiu   $v0, 1           # Add Immediate Unsigned
.text:004039E4                 sw      $v0, 0x48+i($fp)  # Store Word'''.split('\n')