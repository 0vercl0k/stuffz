00007ff6`6ede1021 push    rax
00007ff6`6ede1022 push    rbx
00007ff6`6ede1023 push    rcx
00007ff6`6ede1024 push    rdx
00007ff6`6ede1025 push    rbp
00007ff6`6ede1026 push    rsi
00007ff6`6ede1027 push    rdi
00007ff6`6ede1028 push    r8
00007ff6`6ede102a push    r9
00007ff6`6ede102c push    r10
00007ff6`6ede102e push    r11
00007ff6`6ede1030 push    r12
00007ff6`6ede1032 push    r13
00007ff6`6ede1034 push    r14
00007ff6`6ede1036 push    r15
00007ff6`6ede1038 mov     r11,rsp
00007ff6`6ede103b sub     rsp,10h
00007ff6`6ede103f sub     rsp,70h
00007ff6`6ede1043 sub     rsp,70h
00007ff6`6ede1047 and     sp,0FFF0h
00007ff6`6ede104b mov     eax,636C6163h
00007ff6`6ede1050 mov     dword ptr [rsp],eax
00007ff6`6ede1053 mov     byte ptr [rsp+4],0
00007ff6`6ede1058 xor     eax,eax
00007ff6`6ede105a mov     qword ptr [r11+8],rbx
00007ff6`6ede105e lea     rdi,[r11-78h]
00007ff6`6ede1062 mov     qword ptr [r11+10h],rsi
00007ff6`6ede1066 mov     ecx,68h
00007ff6`6ede106b xor     ebp,ebp
00007ff6`6ede106d rep stos byte ptr [rdi]
00007ff6`6ede106f mov     byte ptr [rsp+70h],68h
00007ff6`6ede1074 mov     eax,60h
00007ff6`6ede1079 mov     rax,qword ptr gs:[eax]
00007ff6`6ede107e mov     rcx,qword ptr [rax+18h]
00007ff6`6ede1082 mov     r8,qword ptr [rcx+10h]
00007ff6`6ede1086 mov     rdi,qword ptr [r8+60h]
00007ff6`6ede108a mov     r9,rdi
00007ff6`6ede108d test    rdi,rdi
00007ff6`6ede1090 je      00007ff6`6ede10c1
00007ff6`6ede1092 movzx   ecx,word ptr [rdi]
00007ff6`6ede1095 mov     eax,1505h
00007ff6`6ede109a mov     edx,ebp
00007ff6`6ede109c test    cx,cx
00007ff6`6ede109f je      00007ff6`6ede10c1
00007ff6`6ede10a1 nop     dword ptr [rax+rax]
00007ff6`6ede10a5 movzx   ecx,cx
00007ff6`6ede10a8 inc     edx
00007ff6`6ede10aa imul    eax,eax,21h
00007ff6`6ede10ad add     eax,ecx
00007ff6`6ede10af mov     ecx,edx
00007ff6`6ede10b1 movzx   ecx,word ptr [rdi+rdx*2]
00007ff6`6ede10b5 test    cx,cx
00007ff6`6ede10b8 jne     00007ff6`6ede10a5
00007ff6`6ede10ba cmp     eax,6DDB9555h
00007ff6`6ede10bf je      00007ff6`6ede10f5
00007ff6`6ede10c1 mov     r8,qword ptr [r8]
00007ff6`6ede10c4 mov     rdi,qword ptr [r8+60h]
00007ff6`6ede10c8 cmp     rdi,r9
00007ff6`6ede10cb jne     00007ff6`6ede108d
00007ff6`6ede10cd mov     eax,1
00007ff6`6ede10d2 lea     rsp,[rsp+70h]
00007ff6`6ede10d7 add     rsp,70h
00007ff6`6ede10db add     rsp,18h
00007ff6`6ede10df pop     r15
00007ff6`6ede10e1 pop     r14
00007ff6`6ede10e3 pop     r13
00007ff6`6ede10e5 pop     r12
00007ff6`6ede10e7 pop     r11
00007ff6`6ede10e9 pop     r9
00007ff6`6ede10eb pop     r8
00007ff6`6ede10ed pop     rdi
00007ff6`6ede10ee pop     rsi
00007ff6`6ede10ef pop     rbp
00007ff6`6ede10f0 pop     rdx
00007ff6`6ede10f1 pop     rcx
00007ff6`6ede10f2 pop     rbx
00007ff6`6ede10f3 pop     rax
00007ff6`6ede10f4 ret
00007ff6`6ede10f5 mov     r10,qword ptr [r8+30h]
00007ff6`6ede10f9 test    r10,r10
00007ff6`6ede10fc je      00007ff6`6ede10cd
00007ff6`6ede10fe movsxd  rax,dword ptr [r10+3Ch]
00007ff6`6ede1102 lea     rcx,[rax+r10]
00007ff6`6ede1106 add     rcx,70h
00007ff6`6ede110a add     rcx,18h
00007ff6`6ede110e mov     ecx,dword ptr [rcx]
00007ff6`6ede1110 test    ecx,ecx
00007ff6`6ede1112 je      00007ff6`6ede10cd
00007ff6`6ede1114 mov     r9d,dword ptr [r10+rcx+20h]
00007ff6`6ede1119 lea     rax,[r10+rcx]
00007ff6`6ede111d mov     ebx,dword ptr [rax+24h]
00007ff6`6ede1120 add     r9,r10
00007ff6`6ede1123 mov     esi,dword ptr [rax+1Ch]
00007ff6`6ede1126 add     rbx,r10
00007ff6`6ede1129 mov     r11d,dword ptr [rax+18h]
00007ff6`6ede112d add     rsi,r10
00007ff6`6ede1130 mov     r8d,ebp
00007ff6`6ede1133 test    r11d,r11d
00007ff6`6ede1136 je      00007ff6`6ede10cd
00007ff6`6ede1138 nop     dword ptr [rax+rax]
00007ff6`6ede113c mov     edi,dword ptr [r9]
00007ff6`6ede113f mov     ecx,1505h
00007ff6`6ede1144 add     rdi,r10
00007ff6`6ede1147 mov     edx,ebp
00007ff6`6ede1149 movzx   eax,byte ptr [rdi]
00007ff6`6ede114c test    al,al
00007ff6`6ede114e je      00007ff6`6ede1170
00007ff6`6ede1150 movsx   eax,al
00007ff6`6ede1153 inc     edx
00007ff6`6ede1155 imul    ecx,ecx,21h
00007ff6`6ede1158 add     ecx,eax
00007ff6`6ede115a mov     eax,edx
00007ff6`6ede115c movzx   eax,byte ptr [rdx+rdi]
00007ff6`6ede1160 test    al,al
00007ff6`6ede1162 jne     00007ff6`6ede1150
00007ff6`6ede1164 push    rax
00007ff6`6ede1165 mov     rax,rcx
00007ff6`6ede1168 cmp     eax,0AEB52E19h
00007ff6`6ede116d pop     rax
00007ff6`6ede116e je      00007ff6`6ede1181
00007ff6`6ede1170 inc     r8d
00007ff6`6ede1173 add     r9,4
00007ff6`6ede1177 cmp     r8d,r11d
00007ff6`6ede117a jb      00007ff6`6ede113c
00007ff6`6ede117c jmp     00007ff6`6ede10cd
00007ff6`6ede1181 mov     eax,r8d
00007ff6`6ede1184 movzx   ecx,word ptr [rbx+rax*2]
00007ff6`6ede1188 mov     eax,dword ptr [rsi+rcx*4]
00007ff6`6ede118b add     rax,r10
00007ff6`6ede118e je      00007ff6`6ede10cd
00007ff6`6ede1194 lea     rcx,[rsp+10h]
00007ff6`6ede1199 xor     r9d,r9d
00007ff6`6ede119c mov     qword ptr [rsp+48h],rcx
00007ff6`6ede11a1 lea     rdx,[rsp]
00007ff6`6ede11a5 lea     rcx,[rsp+70h]
00007ff6`6ede11aa add     rcx,10h
00007ff6`6ede11ae xor     r8d,r8d
00007ff6`6ede11b1 mov     qword ptr [rsp+40h],rcx
00007ff6`6ede11b6 xor     ecx,ecx
00007ff6`6ede11b8 mov     qword ptr [rsp+38h],rbp
00007ff6`6ede11bd mov     qword ptr [rsp+30h],rbp
00007ff6`6ede11c2 mov     dword ptr [rsp+28h],ebp
00007ff6`6ede11c6 mov     dword ptr [rsp+20h],ebp
00007ff6`6ede11ca call    rax
00007ff6`6ede11cc xor     eax,eax
00007ff6`6ede11ce jmp     00007ff6`6ede10d2
