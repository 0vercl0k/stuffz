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