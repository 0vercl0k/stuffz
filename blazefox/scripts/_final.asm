push rax ; 50
push rbx ; 53
push rcx ; 51
push rdx ; 52
push rbp ; 55
push rsi ; 56
push rdi ; 57
push r8 ; 4150
push r9 ; 4151
push r10 ; 4152
push r11 ; 4153
push r12 ; 4154
push r13 ; 4155
push r14 ; 4156
push r15 ; 4157
mov r11, rsp ; 4989e3
sub rsp, 0x10 ; 4883ec10
sub rsp, 0x70 ; 4883ec70
sub rsp, 0x70 ; 4883ec70
and sp, 0xfff0 ; 6683e4f0
mov eax, 0x636c6163 ; b863616c63
mov dword ptr [rsp], eax ; 890424
mov byte ptr [rsp + 4], 0 ; c644240400
xor eax, eax ; 31c0
mov qword ptr [r11 + 8], rbx ; 49895b08
lea rdi, qword ptr [r11 - 0x78] ; 498d7b88
mov qword ptr [r11 + 0x10], rsi ; 49897310
mov ecx, 0x68 ; b968000000
xor ebp, ebp ; 31ed
rep stosb byte ptr [rdi], al ; f3aa
mov byte ptr [rsp + 0x70], 0x68 ; c644247068
mov eax, 0x60 ; b860000000
mov rax, dword ptr gs:[eax] ; 6567488b00
mov rcx, qword ptr [rax + 0x18] ; 488b4818
mov r8, qword ptr [rcx + 0x10] ; 4c8b4110
mov rdi, qword ptr [r8 + 0x60] ; 498b7860
mov r9, rdi ; 4989f9
test rdi, rdi ; 4885ff
je 0x3a5 ; 0f841e010000
movzx ecx, word ptr [rdi] ; 0fb70f
mov eax, 0x1505 ; b805150000
mov edx, ebp ; 89ea
test cx, cx ; 6685c9
je 0x3a5 ; 0f84c9000000
nop dword ptr [rax + rax] ; 0f182400
movzx ecx, cx ; 0fb7c9
inc edx ; ffc2
imul eax, eax, 0x21 ; 6bc021
add eax, ecx ; 01c8
mov ecx, edx ; 89d1
movzx ecx, word ptr [rdi + rdx*2] ; 0fb70c57
test cx, cx ; 6685c9
jne 0x2fb ; 7586
cmp eax, 0x6ddb9555 ; 3d5595db6d
je 0x52b ; 0f8494010000
mov r8, qword ptr [r8] ; 4d8b00
mov rdi, qword ptr [r8 + 0x60] ; 498b7860
cmp rdi, r9 ; 4c39cf
jne 0x273 ; 0f8598feffff
mov eax, 1 ; b801000000
lea rsp, qword ptr [rsp + 0x70] ; 488d642470
add rsp, 0x70 ; 4883c470
add rsp, 0x18 ; 4883c418
pop r15 ; 415f
pop r14 ; 415e
pop r13 ; 415d
pop r12 ; 415c
pop r11 ; 415b
pop r9 ; 4159
pop r8 ; 4158
pop rdi ; 5f
pop rsi ; 5e
pop rbp ; 5d
pop rdx ; 5a
pop rcx ; 59
pop rbx ; 5b
pop rax ; 58
ret  ; c3
mov r10, qword ptr [r8 + 0x30] ; 4d8b5030
test r10, r10 ; 4d85d2
je 0x3e7 ; 0f8496feffff
movsxd rax, dword ptr [r10 + 0x3c] ; 4963423c
lea rcx, qword ptr [rax + r10] ; 4a8d0c10
add rcx, 0x70 ; 4883c170
add rcx, 0x18 ; 4883c118
mov ecx, dword ptr [rcx] ; 8b09
test ecx, ecx ; 85c9
je 0x3e7 ; 0f841ffeffff
mov r9d, dword ptr [r10 + rcx + 0x20] ; 458b4c0a20
lea rax, qword ptr [r10 + rcx] ; 498d040a
mov ebx, dword ptr [rax + 0x24] ; 8b5824
add r9, r10 ; 4d01d1
mov esi, dword ptr [rax + 0x1c] ; 8b701c
add rbx, r10 ; 4c01d3
mov r11d, dword ptr [rax + 0x18] ; 448b5818
add rsi, r10 ; 4c01d6
mov r8d, ebp ; 4189e8
test r11d, r11d ; 4585db
je 0x3e7 ; 0f8464fdffff
nop dword ptr [rax + rax] ; 0f182400
mov edi, dword ptr [r9] ; 418b39
mov ecx, 0x1505 ; b905150000
add rdi, r10 ; 4c01d7
mov edx, ebp ; 89ea
movzx eax, byte ptr [rdi] ; 0fb607
test al, al ; 84c0
je 0x7f6 ; 0f84eb000000
movsx eax, al ; 0fbec0
inc edx ; ffc2
imul ecx, ecx, 0x21 ; 6bc921
add ecx, eax ; 01c1
mov eax, edx ; 89d0
movzx eax, byte ptr [rdx + rdi] ; 0fb6043a
test al, al ; 84c0
jne 0x719 ; 7586
push rax ; 50
mov rax, rcx ; 4889c8
cmp eax, 0xaeb52e19 ; 3d192eb5ae
pop rax ; 58
je 0x84b ; 7463
inc r8d ; 41ffc0
add r9, 4 ; 4983c104
cmp r8d, r11d ; 4539d8
jb 0x6a2 ; 0f8276feffff
jmp 0x3e7 ; e9aafbffff
mov eax, r8d ; 4489c0
movzx ecx, word ptr [rbx + rax*2] ; 0fb70c43
mov eax, dword ptr [rsi + rcx*4] ; 8b048e
add rax, r10 ; 4c01d0
je 0x3e7 ; 0f8455fbffff
lea rcx, qword ptr [rsp + 0x10] ; 488d4c2410
xor r9d, r9d ; 4531c9
mov qword ptr [rsp + 0x48], rcx ; 48894c2448
lea rdx, qword ptr [rsp] ; 488d1424
lea rcx, qword ptr [rsp + 0x70] ; 488d4c2470
add rcx, 0x10 ; 4883c110
xor r8d, r8d ; 4531c0
mov qword ptr [rsp + 0x40], rcx ; 48894c2440
xor ecx, ecx ; 31c9
mov qword ptr [rsp + 0x38], rbp ; 48896c2438
mov qword ptr [rsp + 0x30], rbp ; 48896c2430
mov dword ptr [rsp + 0x28], ebp ; 896c2428
mov dword ptr [rsp + 0x20], ebp ; 896c2420
call rax ; ffd0
xor eax, eax ; 31c0
jmp 0x3f8 ; e956faffff
