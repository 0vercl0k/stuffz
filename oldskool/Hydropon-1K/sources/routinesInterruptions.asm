%macro  _PrologueDeSauvegarde_ 0
        pushad ;Sauvegarde des registres generaux
		push ds
        push es
        push fs
        push gs
        push ebx
        mov bx,0x10
        mov ds,bx
        pop ebx
%endmacro

%macro  _EpilogueDeSauvegarde_ 0
        pop gs
        pop fs
        pop es
        pop ds
        popad
%endmacro

extern _isrIntClavier
extern _isrPageFault
extern _isrIntAppelSysteme
extern _isrGP

segment .text
global _traiteInterruptionHardwareParDefautCtrlM
global _traiteInterruptionHardwareParDefautCtrlE
global _traiteInterruptionClavier

global _traiteInterruptionParDefaut
global _traitePageFault
global _traiteAppelSysteme
global _traiteGP

;-------------HW----------------

;IRQ1 -> controleur maitre
_traiteInterruptionClavier:
	_PrologueDeSauvegarde_
	call _isrIntClavier
	_EpilogueDeSauvegarde_

	jmp _traiteInterruptionHardwareParDefautCtrlM


_traiteInterruptionHardwareParDefautCtrlM:

	push eax
	mov al, 0x20
	out 0x20, al
	pop eax

	iret
	
	
_traiteInterruptionHardwareParDefautCtrlE:

	push eax
	mov al, 0x20
	out 0xA0, al
	pop eax
	
	iret
	
;---------------Exception / int logiciel----------------

_traiteAppelSysteme
	_PrologueDeSauvegarde_
	call _isrIntAppelSysteme
	
	jmp	_traiteInterruptionParDefaut	
	

_traitePageFault:
	_PrologueDeSauvegarde_
	call _isrPageFault
	_EpilogueDeSauvegarde_

	add esp, 4
	iret
	
_traiteGP:
	_PrologueDeSauvegarde_
	call _isrGP
	_EpilogueDeSauvegarde_

	add esp, 4
	iret
	
_traiteInterruptionParDefaut:
	_EpilogueDeSauvegarde_

	;Retour d'interruption
	iret
