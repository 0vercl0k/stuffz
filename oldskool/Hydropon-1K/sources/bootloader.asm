[BITS 16]
[ORG 0x7c00]                    ;Chargement du bootloader en 0x00007c00

%define NbSecteur 40                                 ;Nombre de secteur du kernel (1secteur = 512o)
%define AdresseBase 0x100                           ;Adresse mémoire où notre kernel sera chargé

start:
	xor ax, ax
	xor sp, sp
	xor si, si
	xor bp, bp
	
	mov ds, ax
	
	mov ax, 0x8000
	mov ss, ax
		
	;Pointeur du haut de la stack
	mov sp, 0xf000
	
	;Pointeur du bas de la stack
	mov bp, 0xf000
	
	mov si, chargementBootloaderMsg
	call printf
		
;-----------------[F-o-n-c-t-i-o-n-s]-----------------------------
	;La fonction affiche une chaine de caractère null-terminated
	;Il faut que DS:SI pointe sur la chaine que l'on veut afficher, aucun retour
printf:
	push ax
	
	debut_printf:
	lodsb                      ;ds:(e)si dans al
	cmp al, 0
	je fin_printf
	
	mov ah, 0xE                ;Appel du service n° 0xE, intéruption n°16 du bios
	int 0x10                   ;#  INT 0x10, AH = 0xE -- display char 
	jmp debut_printf
	
	fin_printf:
	pop ax
	ret
	
times (510-($-start)) db 0 ;Notre binaire doit faire 512 octet, on bourre en consequence
dw 0xAA55                  ;Boot signature (55AA)
