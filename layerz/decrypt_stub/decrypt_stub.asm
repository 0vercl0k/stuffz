CODE SECTION .text
start:
call get_eip
get_eip:
pop eax
push 0
mov ebx, esp
invoke VirtualProtect, eax, 0xfffff, 0x40, ebx