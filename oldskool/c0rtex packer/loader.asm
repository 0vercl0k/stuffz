.386
.model flat,stdcall
option casemap:none

.data
.code
	start:
		
		mov eax,00000000h ;entry point
		mov esi,00000000h ;esi = offset 
		mov edi,00000000h ;edi = imageBase		

		.while(esi)
			xor byte ptr [esi+edi],13h
			dec esi;
		.endw
		jmp eax
		
	end start
	
;00401000 > $ BE 37133713    MOV ESI,13371337
;00401005   . BF 37130000    MOV EDI,1337
;0040100A   . 56             PUSH ESI
;0040100B   . EB 05          JMP SHORT loader.00401012
;0040100D   > 803437 13      XOR BYTE PTR DS:[EDI+ESI],13
;00401011   . 4E             DEC ESI
;00401012   > 0BF6           OR ESI,ESI
;00401014   .^75 F7          JNZ SHORT loader.0040100D
;00401016   . 58             POP EAX
;00401017   . 03C7           ADD EAX,EDI
;00401019   . FFE0           JMP EAX