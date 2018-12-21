bits 32

;
; ebx <- hash
; ebp <- base
;
; perl -Ilib -MPex::Utils -e "printf \"%.8x\", Pex::Utils::Ror(Pex::Utils::RorHash("ExAllocatePool"), 13);"
;

resolve_sym_call:
	pushad
	xor  ecx, ecx
	mov  edi, [ebp + 0x3c]
	mov  edi, [ebp + edi + 0x78]
	add  edi, ebp

find_sym:
	mov  edx, [edi + 0x20]
	add  edx, ebp
	mov  esi, [edx + ecx * 4]
	add  esi, ebp
	xor  eax, eax
	cdq
hash_sym:
	lodsb
	ror  edx, 13
	add  edx, eax
	test al, al
	jnz  hash_sym
check_hash:
	inc  ecx
	cmp  dx, bx
	jnz  find_sym

get_sym_address:
	dec  ecx
	mov  ebx, [edi + 0x24]
	add  ebx, ebp
	mov  cx,  [ebx + ecx * 2]
	mov  ebx, [edi + 0x1c]
	add  ebx, ebp
	mov  eax, [ebx + ecx * 4]
	add  eax, ebp

found_sym:
	mov  [esp + 0x1c], eax
	popad
	jmp  eax
