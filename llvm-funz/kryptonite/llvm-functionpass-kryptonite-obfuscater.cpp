/*
    llvm-functionpass-kryptonite-obfuscater.cpp - FunctionPass that obfuscates the LLVM IR.
    (successfuly tested with LLVM and clang 3.3)
    Copyright (C) 2013 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Compile with:
        clang++ llvm-functionpass-kryptonite-obfuscater.cpp `llvm-config --cxxflags --ldflags --libs core` -shared -o llvm-functionpass-kryptonite-obfuscater.so
    Use it with:
        clang -S -emit-llvm hello.c -o hello.ll # Generate LLVM IR (readable) file
        opt -S -load ~/dev/llvm-functionpass-kryptonite-obfuscater.so -kryptonite -enable-anti-dbg -heavy-add-obfu hello.ll -o hello.obfu.ll
        llc -march=archdesired -filetype=obj -O0 hello.obfu.ll -o hello.obfu.o
        clang hello.obfu.o -o hello

    My usage:
        cp kryptonite-crackme.original.ll kryptonite-crackme.ll ; \
        opt -S -load ~/dev/llvm-functionpass-kryptonite-obfuscater.so -kryptonite kryptonite-crackme.ll -o kryptonite-crackme.opti.ll && \
        mv kryptonite-crackme.opti.ll kryptonite-crackme.ll ; \
        opt -S -load ~/dev/llvm-functionpass-kryptonite-obfuscater.so -kryptonite -heavy-add-obfu -enable-anti-dbg 66 kryptonite-crackme.ll -o kryptonite-crackme.opti.ll && \
        mv kryptonite-crackme.opti.ll kryptonite-crackme.ll ; \
        llc -O0 -filetype=obj -march=x86 kryptonite-crackme.ll -o kryptonite-crackme.o && \
        clang -static kryptonite-crackme.o -o kryptonite-crackme && \
        strip --strip-all ./kryptonite-crackme

    Check samples for Linux x86 (tested on a debian 6.0 x86), Linux x64 (tested on a debian 6.0 x64) and Windows x64 (tested on a Win 7 x64) here:
        -> http://0vercl0k.tuxfamily.org/bl0g/Articles/Obfuscation%20of%20steel:%20meet%20my%20Kryptonite/binaries/

*/
#include <cstdio>
#include <ctime>

#include <list>
#include <vector>

#include <llvm/IR/Instruction.h>
#include <llvm/IR/InstrTypes.h>
#include <llvm/IR/IRBuilder.h>
#include <llvm/IR/BasicBlock.h>
#include <llvm/IR/Constants.h>
#include <llvm/IR/InlineAsm.h>

#include <llvm/Support/CommandLine.h>
#include <llvm/Pass.h>
#include <llvm/Transforms/Utils/BasicBlockUtils.h>

static llvm::cl::opt<bool> EnableHeavyAddObfu(
    "heavy-add-obfu",
    llvm::cl::init(false),
    llvm::cl::desc("Enable the heavy ADD obfuscation for kryptonite")
);

static llvm::cl::opt<unsigned int> EnableAntiDbg(
    "enable-anti-dbg",
    llvm::cl::init(0),
    llvm::cl::desc("Enable the ptrace Linux x86 anti-dbg")
);

// Rands in [a, b[
unsigned int rand_a_b(unsigned int a, unsigned int b)
{
    return (rand() % (b - a)) + a;
}

void mutate_add_inst_1(llvm::BinaryOperator *inst)
{
    llvm::Value *A = inst->getOperand(0);
    llvm::Value *B = inst->getOperand(1);
    llvm::Instruction *prev1 = NULL, *prev2 = NULL;
    llvm::Type *Int32Ty = llvm::IntegerType::getInt32Ty(inst->getContext());
    unsigned int n = rand_a_b(50, 120), c = 0, randed = 0;

    for(unsigned int i = 0; i < n; ++i)
    {
        randed = rand();
        c += randed;
        if(prev1 == NULL)
            prev1 = llvm::BinaryOperator::CreateAdd(A, llvm::ConstantInt::get(Int32Ty, randed));
        else
            prev1 = llvm::BinaryOperator::CreateAdd(prev1, llvm::ConstantInt::get(Int32Ty, randed));

        prev1->insertBefore(inst);
    }

    llvm::Instruction *tmp1 = llvm::BinaryOperator::CreateAdd(prev1, llvm::ConstantInt::get(Int32Ty, 0x100000000 - c));
    tmp1->insertBefore(inst);

    c = 0;
    n = rand_a_b(60, 200);

    for(unsigned int i = 0; i < n; ++i)
    {
        randed = rand();
        c += randed;
        if(prev2 == NULL)
            prev2 = llvm::BinaryOperator::CreateAdd(B, llvm::ConstantInt::get(Int32Ty, randed));
        else
            prev2 = llvm::BinaryOperator::CreateAdd(prev2, llvm::ConstantInt::get(Int32Ty, randed));

        prev2->insertBefore(inst);
    }

    llvm::Instruction *tmp2 = llvm::BinaryOperator::CreateAdd(prev2, llvm::ConstantInt::get(Int32Ty, 0x100000000 - c));
    tmp2->insertBefore(inst);

    llvm::Instruction *FinalResult = llvm::BinaryOperator::CreateAdd(tmp1, tmp2);
    llvm::ReplaceInstWithInst(inst, FinalResult);
}

void mutate_add_inst_heavy(llvm::BinaryOperator *inst, llvm::Value *A = NULL, llvm::Value *B = NULL)
{
    if(A == NULL)
        A = inst->getOperand(0);

    if(B == NULL)
        B = inst->getOperand(1);

    llvm::Type *Int32Ty = llvm::IntegerType::getInt32Ty(inst->getContext());

    llvm::Instruction *LO_RShifted0 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 0), "", inst);
    llvm::Instruction *LO_RShiftedAnded0 = llvm::BinaryOperator::CreateAnd(LO_RShifted0, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted0 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded0, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted0 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 0), "", inst);
    llvm::Instruction *RO_RShiftedAnded0 = llvm::BinaryOperator::CreateAnd(RO_RShifted0, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted0 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded0, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And010 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted0, RO_RShiftedAnded0, "", inst);
    llvm::Instruction *R_And020 = llvm::BinaryOperator::CreateAnd(R_And010, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And110 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded0, RO_RShiftedAndedNoted0, "", inst);
    llvm::Instruction *R_And120 = llvm::BinaryOperator::CreateAnd(R_And110, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And210 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted0, RO_RShiftedAndedNoted0, "", inst);
    llvm::Instruction *R_And220 = llvm::BinaryOperator::CreateAnd(R_And210, llvm::ConstantInt::get(Int32Ty, 0), "", inst);
    llvm::Instruction *R_And310 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded0, RO_RShiftedAnded0, "", inst);
    llvm::Instruction *R_And320 = llvm::BinaryOperator::CreateAnd(R_And310, llvm::ConstantInt::get(Int32Ty, 0), "", inst);
    llvm::Instruction *R_Or00 = llvm::BinaryOperator::CreateOr(R_And020, R_And120, "", inst);
    llvm::Instruction *R_Or10 = llvm::BinaryOperator::CreateOr(R_And220, R_And320, "", inst);
    llvm::Instruction *R0 = llvm::BinaryOperator::CreateOr(R_Or00, R_Or10, "", inst);
    llvm::Instruction *Cout_And010 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted0, RO_RShiftedAnded0, "", inst);
    llvm::Instruction *Cout_And020 = llvm::BinaryOperator::CreateAnd(Cout_And010, llvm::ConstantInt::get(Int32Ty, 0), "", inst);
    llvm::Instruction *Cout_And110 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded0, RO_RShiftedAndedNoted0, "", inst);
    llvm::Instruction *Cout_And120 = llvm::BinaryOperator::CreateAnd(Cout_And110, llvm::ConstantInt::get(Int32Ty, 0), "", inst);
    llvm::Instruction *Cout_And210 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded0, RO_RShiftedAnded0, "", inst);
    llvm::Instruction *Cout_And220 = llvm::BinaryOperator::CreateAnd(Cout_And210, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *Cout_And310 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded0, RO_RShiftedAnded0, "", inst);
    llvm::Instruction *Cout_And320 = llvm::BinaryOperator::CreateAnd(Cout_And310, llvm::ConstantInt::get(Int32Ty, 0), "", inst);
    llvm::Instruction *Cout_Or00 = llvm::BinaryOperator::CreateOr(Cout_And020, Cout_And120, "", inst);
    llvm::Instruction *Cout_Or10 = llvm::BinaryOperator::CreateOr(Cout_And220, Cout_And320, "", inst);
    llvm::Instruction *Cout0 = llvm::BinaryOperator::CreateOr(Cout_Or00, Cout_Or10, "", inst);
    llvm::Instruction *NotCout0 = llvm::BinaryOperator::CreateXor(Cout0, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted1 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAnded1 = llvm::BinaryOperator::CreateAnd(LO_RShifted1, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted1 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded1, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted1 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAnded1 = llvm::BinaryOperator::CreateAnd(RO_RShifted1, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted1 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded1, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And011 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted1, RO_RShiftedAnded1, "", inst);
    llvm::Instruction *R_And021 = llvm::BinaryOperator::CreateAnd(R_And011, NotCout0, "", inst);
    llvm::Instruction *R_And111 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded1, RO_RShiftedAndedNoted1, "", inst);
    llvm::Instruction *R_And121 = llvm::BinaryOperator::CreateAnd(R_And111, NotCout0, "", inst);
    llvm::Instruction *R_And211 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted1, RO_RShiftedAndedNoted1, "", inst);
    llvm::Instruction *R_And221 = llvm::BinaryOperator::CreateAnd(R_And211, Cout0, "", inst);
    llvm::Instruction *R_And311 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded1, RO_RShiftedAnded1, "", inst);
    llvm::Instruction *R_And321 = llvm::BinaryOperator::CreateAnd(R_And311, Cout0, "", inst);
    llvm::Instruction *R_Or01 = llvm::BinaryOperator::CreateOr(R_And021, R_And121, "", inst);
    llvm::Instruction *R_Or11 = llvm::BinaryOperator::CreateOr(R_And221, R_And321, "", inst);
    llvm::Instruction *R1 = llvm::BinaryOperator::CreateOr(R_Or01, R_Or11, "", inst);
    llvm::Instruction *Cout_And011 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted1, RO_RShiftedAnded1, "", inst);
    llvm::Instruction *Cout_And021 = llvm::BinaryOperator::CreateAnd(Cout_And011, Cout0, "", inst);
    llvm::Instruction *Cout_And111 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded1, RO_RShiftedAndedNoted1, "", inst);
    llvm::Instruction *Cout_And121 = llvm::BinaryOperator::CreateAnd(Cout_And111, Cout0, "", inst);
    llvm::Instruction *Cout_And211 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded1, RO_RShiftedAnded1, "", inst);
    llvm::Instruction *Cout_And221 = llvm::BinaryOperator::CreateAnd(Cout_And211, NotCout0, "", inst);
    llvm::Instruction *Cout_And311 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded1, RO_RShiftedAnded1, "", inst);
    llvm::Instruction *Cout_And321 = llvm::BinaryOperator::CreateAnd(Cout_And311, Cout0, "", inst);
    llvm::Instruction *Cout_Or01 = llvm::BinaryOperator::CreateOr(Cout_And021, Cout_And121, "", inst);
    llvm::Instruction *Cout_Or11 = llvm::BinaryOperator::CreateOr(Cout_And221, Cout_And321, "", inst);
    llvm::Instruction *Cout1 = llvm::BinaryOperator::CreateOr(Cout_Or01, Cout_Or11, "", inst);
    llvm::Instruction *NotCout1 = llvm::BinaryOperator::CreateXor(Cout1, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted2 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 2), "", inst);
    llvm::Instruction *LO_RShiftedAnded2 = llvm::BinaryOperator::CreateAnd(LO_RShifted2, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted2 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded2, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted2 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 2), "", inst);
    llvm::Instruction *RO_RShiftedAnded2 = llvm::BinaryOperator::CreateAnd(RO_RShifted2, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted2 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded2, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And012 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted2, RO_RShiftedAnded2, "", inst);
    llvm::Instruction *R_And022 = llvm::BinaryOperator::CreateAnd(R_And012, NotCout1, "", inst);
    llvm::Instruction *R_And112 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded2, RO_RShiftedAndedNoted2, "", inst);
    llvm::Instruction *R_And122 = llvm::BinaryOperator::CreateAnd(R_And112, NotCout1, "", inst);
    llvm::Instruction *R_And212 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted2, RO_RShiftedAndedNoted2, "", inst);
    llvm::Instruction *R_And222 = llvm::BinaryOperator::CreateAnd(R_And212, Cout1, "", inst);
    llvm::Instruction *R_And312 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded2, RO_RShiftedAnded2, "", inst);
    llvm::Instruction *R_And322 = llvm::BinaryOperator::CreateAnd(R_And312, Cout1, "", inst);
    llvm::Instruction *R_Or02 = llvm::BinaryOperator::CreateOr(R_And022, R_And122, "", inst);
    llvm::Instruction *R_Or12 = llvm::BinaryOperator::CreateOr(R_And222, R_And322, "", inst);
    llvm::Instruction *R2 = llvm::BinaryOperator::CreateOr(R_Or02, R_Or12, "", inst);
    llvm::Instruction *Cout_And012 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted2, RO_RShiftedAnded2, "", inst);
    llvm::Instruction *Cout_And022 = llvm::BinaryOperator::CreateAnd(Cout_And012, Cout1, "", inst);
    llvm::Instruction *Cout_And112 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded2, RO_RShiftedAndedNoted2, "", inst);
    llvm::Instruction *Cout_And122 = llvm::BinaryOperator::CreateAnd(Cout_And112, Cout1, "", inst);
    llvm::Instruction *Cout_And212 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded2, RO_RShiftedAnded2, "", inst);
    llvm::Instruction *Cout_And222 = llvm::BinaryOperator::CreateAnd(Cout_And212, NotCout1, "", inst);
    llvm::Instruction *Cout_And312 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded2, RO_RShiftedAnded2, "", inst);
    llvm::Instruction *Cout_And322 = llvm::BinaryOperator::CreateAnd(Cout_And312, Cout1, "", inst);
    llvm::Instruction *Cout_Or02 = llvm::BinaryOperator::CreateOr(Cout_And022, Cout_And122, "", inst);
    llvm::Instruction *Cout_Or12 = llvm::BinaryOperator::CreateOr(Cout_And222, Cout_And322, "", inst);
    llvm::Instruction *Cout2 = llvm::BinaryOperator::CreateOr(Cout_Or02, Cout_Or12, "", inst);
    llvm::Instruction *NotCout2 = llvm::BinaryOperator::CreateXor(Cout2, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted3 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 3), "", inst);
    llvm::Instruction *LO_RShiftedAnded3 = llvm::BinaryOperator::CreateAnd(LO_RShifted3, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted3 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded3, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted3 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 3), "", inst);
    llvm::Instruction *RO_RShiftedAnded3 = llvm::BinaryOperator::CreateAnd(RO_RShifted3, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted3 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded3, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And013 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted3, RO_RShiftedAnded3, "", inst);
    llvm::Instruction *R_And023 = llvm::BinaryOperator::CreateAnd(R_And013, NotCout2, "", inst);
    llvm::Instruction *R_And113 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded3, RO_RShiftedAndedNoted3, "", inst);
    llvm::Instruction *R_And123 = llvm::BinaryOperator::CreateAnd(R_And113, NotCout2, "", inst);
    llvm::Instruction *R_And213 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted3, RO_RShiftedAndedNoted3, "", inst);
    llvm::Instruction *R_And223 = llvm::BinaryOperator::CreateAnd(R_And213, Cout2, "", inst);
    llvm::Instruction *R_And313 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded3, RO_RShiftedAnded3, "", inst);
    llvm::Instruction *R_And323 = llvm::BinaryOperator::CreateAnd(R_And313, Cout2, "", inst);
    llvm::Instruction *R_Or03 = llvm::BinaryOperator::CreateOr(R_And023, R_And123, "", inst);
    llvm::Instruction *R_Or13 = llvm::BinaryOperator::CreateOr(R_And223, R_And323, "", inst);
    llvm::Instruction *R3 = llvm::BinaryOperator::CreateOr(R_Or03, R_Or13, "", inst);
    llvm::Instruction *Cout_And013 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted3, RO_RShiftedAnded3, "", inst);
    llvm::Instruction *Cout_And023 = llvm::BinaryOperator::CreateAnd(Cout_And013, Cout2, "", inst);
    llvm::Instruction *Cout_And113 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded3, RO_RShiftedAndedNoted3, "", inst);
    llvm::Instruction *Cout_And123 = llvm::BinaryOperator::CreateAnd(Cout_And113, Cout2, "", inst);
    llvm::Instruction *Cout_And213 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded3, RO_RShiftedAnded3, "", inst);
    llvm::Instruction *Cout_And223 = llvm::BinaryOperator::CreateAnd(Cout_And213, NotCout2, "", inst);
    llvm::Instruction *Cout_And313 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded3, RO_RShiftedAnded3, "", inst);
    llvm::Instruction *Cout_And323 = llvm::BinaryOperator::CreateAnd(Cout_And313, Cout2, "", inst);
    llvm::Instruction *Cout_Or03 = llvm::BinaryOperator::CreateOr(Cout_And023, Cout_And123, "", inst);
    llvm::Instruction *Cout_Or13 = llvm::BinaryOperator::CreateOr(Cout_And223, Cout_And323, "", inst);
    llvm::Instruction *Cout3 = llvm::BinaryOperator::CreateOr(Cout_Or03, Cout_Or13, "", inst);
    llvm::Instruction *NotCout3 = llvm::BinaryOperator::CreateXor(Cout3, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted4 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 4), "", inst);
    llvm::Instruction *LO_RShiftedAnded4 = llvm::BinaryOperator::CreateAnd(LO_RShifted4, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted4 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded4, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted4 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 4), "", inst);
    llvm::Instruction *RO_RShiftedAnded4 = llvm::BinaryOperator::CreateAnd(RO_RShifted4, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted4 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded4, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And014 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted4, RO_RShiftedAnded4, "", inst);
    llvm::Instruction *R_And024 = llvm::BinaryOperator::CreateAnd(R_And014, NotCout3, "", inst);
    llvm::Instruction *R_And114 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded4, RO_RShiftedAndedNoted4, "", inst);
    llvm::Instruction *R_And124 = llvm::BinaryOperator::CreateAnd(R_And114, NotCout3, "", inst);
    llvm::Instruction *R_And214 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted4, RO_RShiftedAndedNoted4, "", inst);
    llvm::Instruction *R_And224 = llvm::BinaryOperator::CreateAnd(R_And214, Cout3, "", inst);
    llvm::Instruction *R_And314 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded4, RO_RShiftedAnded4, "", inst);
    llvm::Instruction *R_And324 = llvm::BinaryOperator::CreateAnd(R_And314, Cout3, "", inst);
    llvm::Instruction *R_Or04 = llvm::BinaryOperator::CreateOr(R_And024, R_And124, "", inst);
    llvm::Instruction *R_Or14 = llvm::BinaryOperator::CreateOr(R_And224, R_And324, "", inst);
    llvm::Instruction *R4 = llvm::BinaryOperator::CreateOr(R_Or04, R_Or14, "", inst);
    llvm::Instruction *Cout_And014 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted4, RO_RShiftedAnded4, "", inst);
    llvm::Instruction *Cout_And024 = llvm::BinaryOperator::CreateAnd(Cout_And014, Cout3, "", inst);
    llvm::Instruction *Cout_And114 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded4, RO_RShiftedAndedNoted4, "", inst);
    llvm::Instruction *Cout_And124 = llvm::BinaryOperator::CreateAnd(Cout_And114, Cout3, "", inst);
    llvm::Instruction *Cout_And214 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded4, RO_RShiftedAnded4, "", inst);
    llvm::Instruction *Cout_And224 = llvm::BinaryOperator::CreateAnd(Cout_And214, NotCout3, "", inst);
    llvm::Instruction *Cout_And314 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded4, RO_RShiftedAnded4, "", inst);
    llvm::Instruction *Cout_And324 = llvm::BinaryOperator::CreateAnd(Cout_And314, Cout3, "", inst);
    llvm::Instruction *Cout_Or04 = llvm::BinaryOperator::CreateOr(Cout_And024, Cout_And124, "", inst);
    llvm::Instruction *Cout_Or14 = llvm::BinaryOperator::CreateOr(Cout_And224, Cout_And324, "", inst);
    llvm::Instruction *Cout4 = llvm::BinaryOperator::CreateOr(Cout_Or04, Cout_Or14, "", inst);
    llvm::Instruction *NotCout4 = llvm::BinaryOperator::CreateXor(Cout4, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted5 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 5), "", inst);
    llvm::Instruction *LO_RShiftedAnded5 = llvm::BinaryOperator::CreateAnd(LO_RShifted5, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted5 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded5, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted5 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 5), "", inst);
    llvm::Instruction *RO_RShiftedAnded5 = llvm::BinaryOperator::CreateAnd(RO_RShifted5, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted5 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded5, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And015 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted5, RO_RShiftedAnded5, "", inst);
    llvm::Instruction *R_And025 = llvm::BinaryOperator::CreateAnd(R_And015, NotCout4, "", inst);
    llvm::Instruction *R_And115 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded5, RO_RShiftedAndedNoted5, "", inst);
    llvm::Instruction *R_And125 = llvm::BinaryOperator::CreateAnd(R_And115, NotCout4, "", inst);
    llvm::Instruction *R_And215 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted5, RO_RShiftedAndedNoted5, "", inst);
    llvm::Instruction *R_And225 = llvm::BinaryOperator::CreateAnd(R_And215, Cout4, "", inst);
    llvm::Instruction *R_And315 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded5, RO_RShiftedAnded5, "", inst);
    llvm::Instruction *R_And325 = llvm::BinaryOperator::CreateAnd(R_And315, Cout4, "", inst);
    llvm::Instruction *R_Or05 = llvm::BinaryOperator::CreateOr(R_And025, R_And125, "", inst);
    llvm::Instruction *R_Or15 = llvm::BinaryOperator::CreateOr(R_And225, R_And325, "", inst);
    llvm::Instruction *R5 = llvm::BinaryOperator::CreateOr(R_Or05, R_Or15, "", inst);
    llvm::Instruction *Cout_And015 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted5, RO_RShiftedAnded5, "", inst);
    llvm::Instruction *Cout_And025 = llvm::BinaryOperator::CreateAnd(Cout_And015, Cout4, "", inst);
    llvm::Instruction *Cout_And115 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded5, RO_RShiftedAndedNoted5, "", inst);
    llvm::Instruction *Cout_And125 = llvm::BinaryOperator::CreateAnd(Cout_And115, Cout4, "", inst);
    llvm::Instruction *Cout_And215 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded5, RO_RShiftedAnded5, "", inst);
    llvm::Instruction *Cout_And225 = llvm::BinaryOperator::CreateAnd(Cout_And215, NotCout4, "", inst);
    llvm::Instruction *Cout_And315 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded5, RO_RShiftedAnded5, "", inst);
    llvm::Instruction *Cout_And325 = llvm::BinaryOperator::CreateAnd(Cout_And315, Cout4, "", inst);
    llvm::Instruction *Cout_Or05 = llvm::BinaryOperator::CreateOr(Cout_And025, Cout_And125, "", inst);
    llvm::Instruction *Cout_Or15 = llvm::BinaryOperator::CreateOr(Cout_And225, Cout_And325, "", inst);
    llvm::Instruction *Cout5 = llvm::BinaryOperator::CreateOr(Cout_Or05, Cout_Or15, "", inst);
    llvm::Instruction *NotCout5 = llvm::BinaryOperator::CreateXor(Cout5, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted6 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 6), "", inst);
    llvm::Instruction *LO_RShiftedAnded6 = llvm::BinaryOperator::CreateAnd(LO_RShifted6, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted6 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded6, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted6 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 6), "", inst);
    llvm::Instruction *RO_RShiftedAnded6 = llvm::BinaryOperator::CreateAnd(RO_RShifted6, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted6 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded6, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And016 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted6, RO_RShiftedAnded6, "", inst);
    llvm::Instruction *R_And026 = llvm::BinaryOperator::CreateAnd(R_And016, NotCout5, "", inst);
    llvm::Instruction *R_And116 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded6, RO_RShiftedAndedNoted6, "", inst);
    llvm::Instruction *R_And126 = llvm::BinaryOperator::CreateAnd(R_And116, NotCout5, "", inst);
    llvm::Instruction *R_And216 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted6, RO_RShiftedAndedNoted6, "", inst);
    llvm::Instruction *R_And226 = llvm::BinaryOperator::CreateAnd(R_And216, Cout5, "", inst);
    llvm::Instruction *R_And316 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded6, RO_RShiftedAnded6, "", inst);
    llvm::Instruction *R_And326 = llvm::BinaryOperator::CreateAnd(R_And316, Cout5, "", inst);
    llvm::Instruction *R_Or06 = llvm::BinaryOperator::CreateOr(R_And026, R_And126, "", inst);
    llvm::Instruction *R_Or16 = llvm::BinaryOperator::CreateOr(R_And226, R_And326, "", inst);
    llvm::Instruction *R6 = llvm::BinaryOperator::CreateOr(R_Or06, R_Or16, "", inst);
    llvm::Instruction *Cout_And016 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted6, RO_RShiftedAnded6, "", inst);
    llvm::Instruction *Cout_And026 = llvm::BinaryOperator::CreateAnd(Cout_And016, Cout5, "", inst);
    llvm::Instruction *Cout_And116 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded6, RO_RShiftedAndedNoted6, "", inst);
    llvm::Instruction *Cout_And126 = llvm::BinaryOperator::CreateAnd(Cout_And116, Cout5, "", inst);
    llvm::Instruction *Cout_And216 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded6, RO_RShiftedAnded6, "", inst);
    llvm::Instruction *Cout_And226 = llvm::BinaryOperator::CreateAnd(Cout_And216, NotCout5, "", inst);
    llvm::Instruction *Cout_And316 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded6, RO_RShiftedAnded6, "", inst);
    llvm::Instruction *Cout_And326 = llvm::BinaryOperator::CreateAnd(Cout_And316, Cout5, "", inst);
    llvm::Instruction *Cout_Or06 = llvm::BinaryOperator::CreateOr(Cout_And026, Cout_And126, "", inst);
    llvm::Instruction *Cout_Or16 = llvm::BinaryOperator::CreateOr(Cout_And226, Cout_And326, "", inst);
    llvm::Instruction *Cout6 = llvm::BinaryOperator::CreateOr(Cout_Or06, Cout_Or16, "", inst);
    llvm::Instruction *NotCout6 = llvm::BinaryOperator::CreateXor(Cout6, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted7 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 7), "", inst);
    llvm::Instruction *LO_RShiftedAnded7 = llvm::BinaryOperator::CreateAnd(LO_RShifted7, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted7 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded7, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted7 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 7), "", inst);
    llvm::Instruction *RO_RShiftedAnded7 = llvm::BinaryOperator::CreateAnd(RO_RShifted7, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted7 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded7, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And017 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted7, RO_RShiftedAnded7, "", inst);
    llvm::Instruction *R_And027 = llvm::BinaryOperator::CreateAnd(R_And017, NotCout6, "", inst);
    llvm::Instruction *R_And117 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded7, RO_RShiftedAndedNoted7, "", inst);
    llvm::Instruction *R_And127 = llvm::BinaryOperator::CreateAnd(R_And117, NotCout6, "", inst);
    llvm::Instruction *R_And217 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted7, RO_RShiftedAndedNoted7, "", inst);
    llvm::Instruction *R_And227 = llvm::BinaryOperator::CreateAnd(R_And217, Cout6, "", inst);
    llvm::Instruction *R_And317 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded7, RO_RShiftedAnded7, "", inst);
    llvm::Instruction *R_And327 = llvm::BinaryOperator::CreateAnd(R_And317, Cout6, "", inst);
    llvm::Instruction *R_Or07 = llvm::BinaryOperator::CreateOr(R_And027, R_And127, "", inst);
    llvm::Instruction *R_Or17 = llvm::BinaryOperator::CreateOr(R_And227, R_And327, "", inst);
    llvm::Instruction *R7 = llvm::BinaryOperator::CreateOr(R_Or07, R_Or17, "", inst);
    llvm::Instruction *Cout_And017 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted7, RO_RShiftedAnded7, "", inst);
    llvm::Instruction *Cout_And027 = llvm::BinaryOperator::CreateAnd(Cout_And017, Cout6, "", inst);
    llvm::Instruction *Cout_And117 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded7, RO_RShiftedAndedNoted7, "", inst);
    llvm::Instruction *Cout_And127 = llvm::BinaryOperator::CreateAnd(Cout_And117, Cout6, "", inst);
    llvm::Instruction *Cout_And217 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded7, RO_RShiftedAnded7, "", inst);
    llvm::Instruction *Cout_And227 = llvm::BinaryOperator::CreateAnd(Cout_And217, NotCout6, "", inst);
    llvm::Instruction *Cout_And317 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded7, RO_RShiftedAnded7, "", inst);
    llvm::Instruction *Cout_And327 = llvm::BinaryOperator::CreateAnd(Cout_And317, Cout6, "", inst);
    llvm::Instruction *Cout_Or07 = llvm::BinaryOperator::CreateOr(Cout_And027, Cout_And127, "", inst);
    llvm::Instruction *Cout_Or17 = llvm::BinaryOperator::CreateOr(Cout_And227, Cout_And327, "", inst);
    llvm::Instruction *Cout7 = llvm::BinaryOperator::CreateOr(Cout_Or07, Cout_Or17, "", inst);
    llvm::Instruction *NotCout7 = llvm::BinaryOperator::CreateXor(Cout7, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted8 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 8), "", inst);
    llvm::Instruction *LO_RShiftedAnded8 = llvm::BinaryOperator::CreateAnd(LO_RShifted8, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted8 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded8, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted8 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 8), "", inst);
    llvm::Instruction *RO_RShiftedAnded8 = llvm::BinaryOperator::CreateAnd(RO_RShifted8, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted8 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded8, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And018 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted8, RO_RShiftedAnded8, "", inst);
    llvm::Instruction *R_And028 = llvm::BinaryOperator::CreateAnd(R_And018, NotCout7, "", inst);
    llvm::Instruction *R_And118 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded8, RO_RShiftedAndedNoted8, "", inst);
    llvm::Instruction *R_And128 = llvm::BinaryOperator::CreateAnd(R_And118, NotCout7, "", inst);
    llvm::Instruction *R_And218 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted8, RO_RShiftedAndedNoted8, "", inst);
    llvm::Instruction *R_And228 = llvm::BinaryOperator::CreateAnd(R_And218, Cout7, "", inst);
    llvm::Instruction *R_And318 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded8, RO_RShiftedAnded8, "", inst);
    llvm::Instruction *R_And328 = llvm::BinaryOperator::CreateAnd(R_And318, Cout7, "", inst);
    llvm::Instruction *R_Or08 = llvm::BinaryOperator::CreateOr(R_And028, R_And128, "", inst);
    llvm::Instruction *R_Or18 = llvm::BinaryOperator::CreateOr(R_And228, R_And328, "", inst);
    llvm::Instruction *R8 = llvm::BinaryOperator::CreateOr(R_Or08, R_Or18, "", inst);
    llvm::Instruction *Cout_And018 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted8, RO_RShiftedAnded8, "", inst);
    llvm::Instruction *Cout_And028 = llvm::BinaryOperator::CreateAnd(Cout_And018, Cout7, "", inst);
    llvm::Instruction *Cout_And118 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded8, RO_RShiftedAndedNoted8, "", inst);
    llvm::Instruction *Cout_And128 = llvm::BinaryOperator::CreateAnd(Cout_And118, Cout7, "", inst);
    llvm::Instruction *Cout_And218 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded8, RO_RShiftedAnded8, "", inst);
    llvm::Instruction *Cout_And228 = llvm::BinaryOperator::CreateAnd(Cout_And218, NotCout7, "", inst);
    llvm::Instruction *Cout_And318 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded8, RO_RShiftedAnded8, "", inst);
    llvm::Instruction *Cout_And328 = llvm::BinaryOperator::CreateAnd(Cout_And318, Cout7, "", inst);
    llvm::Instruction *Cout_Or08 = llvm::BinaryOperator::CreateOr(Cout_And028, Cout_And128, "", inst);
    llvm::Instruction *Cout_Or18 = llvm::BinaryOperator::CreateOr(Cout_And228, Cout_And328, "", inst);
    llvm::Instruction *Cout8 = llvm::BinaryOperator::CreateOr(Cout_Or08, Cout_Or18, "", inst);
    llvm::Instruction *NotCout8 = llvm::BinaryOperator::CreateXor(Cout8, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted9 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 9), "", inst);
    llvm::Instruction *LO_RShiftedAnded9 = llvm::BinaryOperator::CreateAnd(LO_RShifted9, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted9 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded9, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted9 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 9), "", inst);
    llvm::Instruction *RO_RShiftedAnded9 = llvm::BinaryOperator::CreateAnd(RO_RShifted9, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted9 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded9, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And019 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted9, RO_RShiftedAnded9, "", inst);
    llvm::Instruction *R_And029 = llvm::BinaryOperator::CreateAnd(R_And019, NotCout8, "", inst);
    llvm::Instruction *R_And119 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded9, RO_RShiftedAndedNoted9, "", inst);
    llvm::Instruction *R_And129 = llvm::BinaryOperator::CreateAnd(R_And119, NotCout8, "", inst);
    llvm::Instruction *R_And219 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted9, RO_RShiftedAndedNoted9, "", inst);
    llvm::Instruction *R_And229 = llvm::BinaryOperator::CreateAnd(R_And219, Cout8, "", inst);
    llvm::Instruction *R_And319 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded9, RO_RShiftedAnded9, "", inst);
    llvm::Instruction *R_And329 = llvm::BinaryOperator::CreateAnd(R_And319, Cout8, "", inst);
    llvm::Instruction *R_Or09 = llvm::BinaryOperator::CreateOr(R_And029, R_And129, "", inst);
    llvm::Instruction *R_Or19 = llvm::BinaryOperator::CreateOr(R_And229, R_And329, "", inst);
    llvm::Instruction *R9 = llvm::BinaryOperator::CreateOr(R_Or09, R_Or19, "", inst);
    llvm::Instruction *Cout_And019 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted9, RO_RShiftedAnded9, "", inst);
    llvm::Instruction *Cout_And029 = llvm::BinaryOperator::CreateAnd(Cout_And019, Cout8, "", inst);
    llvm::Instruction *Cout_And119 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded9, RO_RShiftedAndedNoted9, "", inst);
    llvm::Instruction *Cout_And129 = llvm::BinaryOperator::CreateAnd(Cout_And119, Cout8, "", inst);
    llvm::Instruction *Cout_And219 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded9, RO_RShiftedAnded9, "", inst);
    llvm::Instruction *Cout_And229 = llvm::BinaryOperator::CreateAnd(Cout_And219, NotCout8, "", inst);
    llvm::Instruction *Cout_And319 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded9, RO_RShiftedAnded9, "", inst);
    llvm::Instruction *Cout_And329 = llvm::BinaryOperator::CreateAnd(Cout_And319, Cout8, "", inst);
    llvm::Instruction *Cout_Or09 = llvm::BinaryOperator::CreateOr(Cout_And029, Cout_And129, "", inst);
    llvm::Instruction *Cout_Or19 = llvm::BinaryOperator::CreateOr(Cout_And229, Cout_And329, "", inst);
    llvm::Instruction *Cout9 = llvm::BinaryOperator::CreateOr(Cout_Or09, Cout_Or19, "", inst);
    llvm::Instruction *NotCout9 = llvm::BinaryOperator::CreateXor(Cout9, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted10 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 10), "", inst);
    llvm::Instruction *LO_RShiftedAnded10 = llvm::BinaryOperator::CreateAnd(LO_RShifted10, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted10 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded10, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted10 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 10), "", inst);
    llvm::Instruction *RO_RShiftedAnded10 = llvm::BinaryOperator::CreateAnd(RO_RShifted10, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted10 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded10, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0110 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted10, RO_RShiftedAnded10, "", inst);
    llvm::Instruction *R_And0210 = llvm::BinaryOperator::CreateAnd(R_And0110, NotCout9, "", inst);
    llvm::Instruction *R_And1110 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded10, RO_RShiftedAndedNoted10, "", inst);
    llvm::Instruction *R_And1210 = llvm::BinaryOperator::CreateAnd(R_And1110, NotCout9, "", inst);
    llvm::Instruction *R_And2110 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted10, RO_RShiftedAndedNoted10, "", inst);
    llvm::Instruction *R_And2210 = llvm::BinaryOperator::CreateAnd(R_And2110, Cout9, "", inst);
    llvm::Instruction *R_And3110 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded10, RO_RShiftedAnded10, "", inst);
    llvm::Instruction *R_And3210 = llvm::BinaryOperator::CreateAnd(R_And3110, Cout9, "", inst);
    llvm::Instruction *R_Or010 = llvm::BinaryOperator::CreateOr(R_And0210, R_And1210, "", inst);
    llvm::Instruction *R_Or110 = llvm::BinaryOperator::CreateOr(R_And2210, R_And3210, "", inst);
    llvm::Instruction *R10 = llvm::BinaryOperator::CreateOr(R_Or010, R_Or110, "", inst);
    llvm::Instruction *Cout_And0110 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted10, RO_RShiftedAnded10, "", inst);
    llvm::Instruction *Cout_And0210 = llvm::BinaryOperator::CreateAnd(Cout_And0110, Cout9, "", inst);
    llvm::Instruction *Cout_And1110 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded10, RO_RShiftedAndedNoted10, "", inst);
    llvm::Instruction *Cout_And1210 = llvm::BinaryOperator::CreateAnd(Cout_And1110, Cout9, "", inst);
    llvm::Instruction *Cout_And2110 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded10, RO_RShiftedAnded10, "", inst);
    llvm::Instruction *Cout_And2210 = llvm::BinaryOperator::CreateAnd(Cout_And2110, NotCout9, "", inst);
    llvm::Instruction *Cout_And3110 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded10, RO_RShiftedAnded10, "", inst);
    llvm::Instruction *Cout_And3210 = llvm::BinaryOperator::CreateAnd(Cout_And3110, Cout9, "", inst);
    llvm::Instruction *Cout_Or010 = llvm::BinaryOperator::CreateOr(Cout_And0210, Cout_And1210, "", inst);
    llvm::Instruction *Cout_Or110 = llvm::BinaryOperator::CreateOr(Cout_And2210, Cout_And3210, "", inst);
    llvm::Instruction *Cout10 = llvm::BinaryOperator::CreateOr(Cout_Or010, Cout_Or110, "", inst);
    llvm::Instruction *NotCout10 = llvm::BinaryOperator::CreateXor(Cout10, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted11 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 11), "", inst);
    llvm::Instruction *LO_RShiftedAnded11 = llvm::BinaryOperator::CreateAnd(LO_RShifted11, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted11 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded11, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted11 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 11), "", inst);
    llvm::Instruction *RO_RShiftedAnded11 = llvm::BinaryOperator::CreateAnd(RO_RShifted11, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted11 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded11, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0111 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted11, RO_RShiftedAnded11, "", inst);
    llvm::Instruction *R_And0211 = llvm::BinaryOperator::CreateAnd(R_And0111, NotCout10, "", inst);
    llvm::Instruction *R_And1111 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded11, RO_RShiftedAndedNoted11, "", inst);
    llvm::Instruction *R_And1211 = llvm::BinaryOperator::CreateAnd(R_And1111, NotCout10, "", inst);
    llvm::Instruction *R_And2111 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted11, RO_RShiftedAndedNoted11, "", inst);
    llvm::Instruction *R_And2211 = llvm::BinaryOperator::CreateAnd(R_And2111, Cout10, "", inst);
    llvm::Instruction *R_And3111 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded11, RO_RShiftedAnded11, "", inst);
    llvm::Instruction *R_And3211 = llvm::BinaryOperator::CreateAnd(R_And3111, Cout10, "", inst);
    llvm::Instruction *R_Or011 = llvm::BinaryOperator::CreateOr(R_And0211, R_And1211, "", inst);
    llvm::Instruction *R_Or111 = llvm::BinaryOperator::CreateOr(R_And2211, R_And3211, "", inst);
    llvm::Instruction *R11 = llvm::BinaryOperator::CreateOr(R_Or011, R_Or111, "", inst);
    llvm::Instruction *Cout_And0111 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted11, RO_RShiftedAnded11, "", inst);
    llvm::Instruction *Cout_And0211 = llvm::BinaryOperator::CreateAnd(Cout_And0111, Cout10, "", inst);
    llvm::Instruction *Cout_And1111 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded11, RO_RShiftedAndedNoted11, "", inst);
    llvm::Instruction *Cout_And1211 = llvm::BinaryOperator::CreateAnd(Cout_And1111, Cout10, "", inst);
    llvm::Instruction *Cout_And2111 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded11, RO_RShiftedAnded11, "", inst);
    llvm::Instruction *Cout_And2211 = llvm::BinaryOperator::CreateAnd(Cout_And2111, NotCout10, "", inst);
    llvm::Instruction *Cout_And3111 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded11, RO_RShiftedAnded11, "", inst);
    llvm::Instruction *Cout_And3211 = llvm::BinaryOperator::CreateAnd(Cout_And3111, Cout10, "", inst);
    llvm::Instruction *Cout_Or011 = llvm::BinaryOperator::CreateOr(Cout_And0211, Cout_And1211, "", inst);
    llvm::Instruction *Cout_Or111 = llvm::BinaryOperator::CreateOr(Cout_And2211, Cout_And3211, "", inst);
    llvm::Instruction *Cout11 = llvm::BinaryOperator::CreateOr(Cout_Or011, Cout_Or111, "", inst);
    llvm::Instruction *NotCout11 = llvm::BinaryOperator::CreateXor(Cout11, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted12 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 12), "", inst);
    llvm::Instruction *LO_RShiftedAnded12 = llvm::BinaryOperator::CreateAnd(LO_RShifted12, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted12 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded12, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted12 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 12), "", inst);
    llvm::Instruction *RO_RShiftedAnded12 = llvm::BinaryOperator::CreateAnd(RO_RShifted12, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted12 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded12, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0112 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted12, RO_RShiftedAnded12, "", inst);
    llvm::Instruction *R_And0212 = llvm::BinaryOperator::CreateAnd(R_And0112, NotCout11, "", inst);
    llvm::Instruction *R_And1112 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded12, RO_RShiftedAndedNoted12, "", inst);
    llvm::Instruction *R_And1212 = llvm::BinaryOperator::CreateAnd(R_And1112, NotCout11, "", inst);
    llvm::Instruction *R_And2112 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted12, RO_RShiftedAndedNoted12, "", inst);
    llvm::Instruction *R_And2212 = llvm::BinaryOperator::CreateAnd(R_And2112, Cout11, "", inst);
    llvm::Instruction *R_And3112 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded12, RO_RShiftedAnded12, "", inst);
    llvm::Instruction *R_And3212 = llvm::BinaryOperator::CreateAnd(R_And3112, Cout11, "", inst);
    llvm::Instruction *R_Or012 = llvm::BinaryOperator::CreateOr(R_And0212, R_And1212, "", inst);
    llvm::Instruction *R_Or112 = llvm::BinaryOperator::CreateOr(R_And2212, R_And3212, "", inst);
    llvm::Instruction *R12 = llvm::BinaryOperator::CreateOr(R_Or012, R_Or112, "", inst);
    llvm::Instruction *Cout_And0112 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted12, RO_RShiftedAnded12, "", inst);
    llvm::Instruction *Cout_And0212 = llvm::BinaryOperator::CreateAnd(Cout_And0112, Cout11, "", inst);
    llvm::Instruction *Cout_And1112 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded12, RO_RShiftedAndedNoted12, "", inst);
    llvm::Instruction *Cout_And1212 = llvm::BinaryOperator::CreateAnd(Cout_And1112, Cout11, "", inst);
    llvm::Instruction *Cout_And2112 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded12, RO_RShiftedAnded12, "", inst);
    llvm::Instruction *Cout_And2212 = llvm::BinaryOperator::CreateAnd(Cout_And2112, NotCout11, "", inst);
    llvm::Instruction *Cout_And3112 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded12, RO_RShiftedAnded12, "", inst);
    llvm::Instruction *Cout_And3212 = llvm::BinaryOperator::CreateAnd(Cout_And3112, Cout11, "", inst);
    llvm::Instruction *Cout_Or012 = llvm::BinaryOperator::CreateOr(Cout_And0212, Cout_And1212, "", inst);
    llvm::Instruction *Cout_Or112 = llvm::BinaryOperator::CreateOr(Cout_And2212, Cout_And3212, "", inst);
    llvm::Instruction *Cout12 = llvm::BinaryOperator::CreateOr(Cout_Or012, Cout_Or112, "", inst);
    llvm::Instruction *NotCout12 = llvm::BinaryOperator::CreateXor(Cout12, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted13 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 13), "", inst);
    llvm::Instruction *LO_RShiftedAnded13 = llvm::BinaryOperator::CreateAnd(LO_RShifted13, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted13 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded13, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted13 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 13), "", inst);
    llvm::Instruction *RO_RShiftedAnded13 = llvm::BinaryOperator::CreateAnd(RO_RShifted13, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted13 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded13, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0113 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted13, RO_RShiftedAnded13, "", inst);
    llvm::Instruction *R_And0213 = llvm::BinaryOperator::CreateAnd(R_And0113, NotCout12, "", inst);
    llvm::Instruction *R_And1113 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded13, RO_RShiftedAndedNoted13, "", inst);
    llvm::Instruction *R_And1213 = llvm::BinaryOperator::CreateAnd(R_And1113, NotCout12, "", inst);
    llvm::Instruction *R_And2113 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted13, RO_RShiftedAndedNoted13, "", inst);
    llvm::Instruction *R_And2213 = llvm::BinaryOperator::CreateAnd(R_And2113, Cout12, "", inst);
    llvm::Instruction *R_And3113 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded13, RO_RShiftedAnded13, "", inst);
    llvm::Instruction *R_And3213 = llvm::BinaryOperator::CreateAnd(R_And3113, Cout12, "", inst);
    llvm::Instruction *R_Or013 = llvm::BinaryOperator::CreateOr(R_And0213, R_And1213, "", inst);
    llvm::Instruction *R_Or113 = llvm::BinaryOperator::CreateOr(R_And2213, R_And3213, "", inst);
    llvm::Instruction *R13 = llvm::BinaryOperator::CreateOr(R_Or013, R_Or113, "", inst);
    llvm::Instruction *Cout_And0113 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted13, RO_RShiftedAnded13, "", inst);
    llvm::Instruction *Cout_And0213 = llvm::BinaryOperator::CreateAnd(Cout_And0113, Cout12, "", inst);
    llvm::Instruction *Cout_And1113 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded13, RO_RShiftedAndedNoted13, "", inst);
    llvm::Instruction *Cout_And1213 = llvm::BinaryOperator::CreateAnd(Cout_And1113, Cout12, "", inst);
    llvm::Instruction *Cout_And2113 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded13, RO_RShiftedAnded13, "", inst);
    llvm::Instruction *Cout_And2213 = llvm::BinaryOperator::CreateAnd(Cout_And2113, NotCout12, "", inst);
    llvm::Instruction *Cout_And3113 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded13, RO_RShiftedAnded13, "", inst);
    llvm::Instruction *Cout_And3213 = llvm::BinaryOperator::CreateAnd(Cout_And3113, Cout12, "", inst);
    llvm::Instruction *Cout_Or013 = llvm::BinaryOperator::CreateOr(Cout_And0213, Cout_And1213, "", inst);
    llvm::Instruction *Cout_Or113 = llvm::BinaryOperator::CreateOr(Cout_And2213, Cout_And3213, "", inst);
    llvm::Instruction *Cout13 = llvm::BinaryOperator::CreateOr(Cout_Or013, Cout_Or113, "", inst);
    llvm::Instruction *NotCout13 = llvm::BinaryOperator::CreateXor(Cout13, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted14 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 14), "", inst);
    llvm::Instruction *LO_RShiftedAnded14 = llvm::BinaryOperator::CreateAnd(LO_RShifted14, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted14 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded14, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted14 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 14), "", inst);
    llvm::Instruction *RO_RShiftedAnded14 = llvm::BinaryOperator::CreateAnd(RO_RShifted14, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted14 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded14, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0114 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted14, RO_RShiftedAnded14, "", inst);
    llvm::Instruction *R_And0214 = llvm::BinaryOperator::CreateAnd(R_And0114, NotCout13, "", inst);
    llvm::Instruction *R_And1114 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded14, RO_RShiftedAndedNoted14, "", inst);
    llvm::Instruction *R_And1214 = llvm::BinaryOperator::CreateAnd(R_And1114, NotCout13, "", inst);
    llvm::Instruction *R_And2114 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted14, RO_RShiftedAndedNoted14, "", inst);
    llvm::Instruction *R_And2214 = llvm::BinaryOperator::CreateAnd(R_And2114, Cout13, "", inst);
    llvm::Instruction *R_And3114 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded14, RO_RShiftedAnded14, "", inst);
    llvm::Instruction *R_And3214 = llvm::BinaryOperator::CreateAnd(R_And3114, Cout13, "", inst);
    llvm::Instruction *R_Or014 = llvm::BinaryOperator::CreateOr(R_And0214, R_And1214, "", inst);
    llvm::Instruction *R_Or114 = llvm::BinaryOperator::CreateOr(R_And2214, R_And3214, "", inst);
    llvm::Instruction *R14 = llvm::BinaryOperator::CreateOr(R_Or014, R_Or114, "", inst);
    llvm::Instruction *Cout_And0114 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted14, RO_RShiftedAnded14, "", inst);
    llvm::Instruction *Cout_And0214 = llvm::BinaryOperator::CreateAnd(Cout_And0114, Cout13, "", inst);
    llvm::Instruction *Cout_And1114 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded14, RO_RShiftedAndedNoted14, "", inst);
    llvm::Instruction *Cout_And1214 = llvm::BinaryOperator::CreateAnd(Cout_And1114, Cout13, "", inst);
    llvm::Instruction *Cout_And2114 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded14, RO_RShiftedAnded14, "", inst);
    llvm::Instruction *Cout_And2214 = llvm::BinaryOperator::CreateAnd(Cout_And2114, NotCout13, "", inst);
    llvm::Instruction *Cout_And3114 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded14, RO_RShiftedAnded14, "", inst);
    llvm::Instruction *Cout_And3214 = llvm::BinaryOperator::CreateAnd(Cout_And3114, Cout13, "", inst);
    llvm::Instruction *Cout_Or014 = llvm::BinaryOperator::CreateOr(Cout_And0214, Cout_And1214, "", inst);
    llvm::Instruction *Cout_Or114 = llvm::BinaryOperator::CreateOr(Cout_And2214, Cout_And3214, "", inst);
    llvm::Instruction *Cout14 = llvm::BinaryOperator::CreateOr(Cout_Or014, Cout_Or114, "", inst);
    llvm::Instruction *NotCout14 = llvm::BinaryOperator::CreateXor(Cout14, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted15 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 15), "", inst);
    llvm::Instruction *LO_RShiftedAnded15 = llvm::BinaryOperator::CreateAnd(LO_RShifted15, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted15 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded15, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted15 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 15), "", inst);
    llvm::Instruction *RO_RShiftedAnded15 = llvm::BinaryOperator::CreateAnd(RO_RShifted15, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted15 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded15, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0115 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted15, RO_RShiftedAnded15, "", inst);
    llvm::Instruction *R_And0215 = llvm::BinaryOperator::CreateAnd(R_And0115, NotCout14, "", inst);
    llvm::Instruction *R_And1115 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded15, RO_RShiftedAndedNoted15, "", inst);
    llvm::Instruction *R_And1215 = llvm::BinaryOperator::CreateAnd(R_And1115, NotCout14, "", inst);
    llvm::Instruction *R_And2115 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted15, RO_RShiftedAndedNoted15, "", inst);
    llvm::Instruction *R_And2215 = llvm::BinaryOperator::CreateAnd(R_And2115, Cout14, "", inst);
    llvm::Instruction *R_And3115 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded15, RO_RShiftedAnded15, "", inst);
    llvm::Instruction *R_And3215 = llvm::BinaryOperator::CreateAnd(R_And3115, Cout14, "", inst);
    llvm::Instruction *R_Or015 = llvm::BinaryOperator::CreateOr(R_And0215, R_And1215, "", inst);
    llvm::Instruction *R_Or115 = llvm::BinaryOperator::CreateOr(R_And2215, R_And3215, "", inst);
    llvm::Instruction *R15 = llvm::BinaryOperator::CreateOr(R_Or015, R_Or115, "", inst);
    llvm::Instruction *Cout_And0115 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted15, RO_RShiftedAnded15, "", inst);
    llvm::Instruction *Cout_And0215 = llvm::BinaryOperator::CreateAnd(Cout_And0115, Cout14, "", inst);
    llvm::Instruction *Cout_And1115 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded15, RO_RShiftedAndedNoted15, "", inst);
    llvm::Instruction *Cout_And1215 = llvm::BinaryOperator::CreateAnd(Cout_And1115, Cout14, "", inst);
    llvm::Instruction *Cout_And2115 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded15, RO_RShiftedAnded15, "", inst);
    llvm::Instruction *Cout_And2215 = llvm::BinaryOperator::CreateAnd(Cout_And2115, NotCout14, "", inst);
    llvm::Instruction *Cout_And3115 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded15, RO_RShiftedAnded15, "", inst);
    llvm::Instruction *Cout_And3215 = llvm::BinaryOperator::CreateAnd(Cout_And3115, Cout14, "", inst);
    llvm::Instruction *Cout_Or015 = llvm::BinaryOperator::CreateOr(Cout_And0215, Cout_And1215, "", inst);
    llvm::Instruction *Cout_Or115 = llvm::BinaryOperator::CreateOr(Cout_And2215, Cout_And3215, "", inst);
    llvm::Instruction *Cout15 = llvm::BinaryOperator::CreateOr(Cout_Or015, Cout_Or115, "", inst);
    llvm::Instruction *NotCout15 = llvm::BinaryOperator::CreateXor(Cout15, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted16 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 16), "", inst);
    llvm::Instruction *LO_RShiftedAnded16 = llvm::BinaryOperator::CreateAnd(LO_RShifted16, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted16 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded16, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted16 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 16), "", inst);
    llvm::Instruction *RO_RShiftedAnded16 = llvm::BinaryOperator::CreateAnd(RO_RShifted16, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted16 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded16, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0116 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted16, RO_RShiftedAnded16, "", inst);
    llvm::Instruction *R_And0216 = llvm::BinaryOperator::CreateAnd(R_And0116, NotCout15, "", inst);
    llvm::Instruction *R_And1116 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded16, RO_RShiftedAndedNoted16, "", inst);
    llvm::Instruction *R_And1216 = llvm::BinaryOperator::CreateAnd(R_And1116, NotCout15, "", inst);
    llvm::Instruction *R_And2116 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted16, RO_RShiftedAndedNoted16, "", inst);
    llvm::Instruction *R_And2216 = llvm::BinaryOperator::CreateAnd(R_And2116, Cout15, "", inst);
    llvm::Instruction *R_And3116 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded16, RO_RShiftedAnded16, "", inst);
    llvm::Instruction *R_And3216 = llvm::BinaryOperator::CreateAnd(R_And3116, Cout15, "", inst);
    llvm::Instruction *R_Or016 = llvm::BinaryOperator::CreateOr(R_And0216, R_And1216, "", inst);
    llvm::Instruction *R_Or116 = llvm::BinaryOperator::CreateOr(R_And2216, R_And3216, "", inst);
    llvm::Instruction *R16 = llvm::BinaryOperator::CreateOr(R_Or016, R_Or116, "", inst);
    llvm::Instruction *Cout_And0116 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted16, RO_RShiftedAnded16, "", inst);
    llvm::Instruction *Cout_And0216 = llvm::BinaryOperator::CreateAnd(Cout_And0116, Cout15, "", inst);
    llvm::Instruction *Cout_And1116 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded16, RO_RShiftedAndedNoted16, "", inst);
    llvm::Instruction *Cout_And1216 = llvm::BinaryOperator::CreateAnd(Cout_And1116, Cout15, "", inst);
    llvm::Instruction *Cout_And2116 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded16, RO_RShiftedAnded16, "", inst);
    llvm::Instruction *Cout_And2216 = llvm::BinaryOperator::CreateAnd(Cout_And2116, NotCout15, "", inst);
    llvm::Instruction *Cout_And3116 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded16, RO_RShiftedAnded16, "", inst);
    llvm::Instruction *Cout_And3216 = llvm::BinaryOperator::CreateAnd(Cout_And3116, Cout15, "", inst);
    llvm::Instruction *Cout_Or016 = llvm::BinaryOperator::CreateOr(Cout_And0216, Cout_And1216, "", inst);
    llvm::Instruction *Cout_Or116 = llvm::BinaryOperator::CreateOr(Cout_And2216, Cout_And3216, "", inst);
    llvm::Instruction *Cout16 = llvm::BinaryOperator::CreateOr(Cout_Or016, Cout_Or116, "", inst);
    llvm::Instruction *NotCout16 = llvm::BinaryOperator::CreateXor(Cout16, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted17 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 17), "", inst);
    llvm::Instruction *LO_RShiftedAnded17 = llvm::BinaryOperator::CreateAnd(LO_RShifted17, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted17 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded17, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted17 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 17), "", inst);
    llvm::Instruction *RO_RShiftedAnded17 = llvm::BinaryOperator::CreateAnd(RO_RShifted17, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted17 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded17, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0117 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted17, RO_RShiftedAnded17, "", inst);
    llvm::Instruction *R_And0217 = llvm::BinaryOperator::CreateAnd(R_And0117, NotCout16, "", inst);
    llvm::Instruction *R_And1117 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded17, RO_RShiftedAndedNoted17, "", inst);
    llvm::Instruction *R_And1217 = llvm::BinaryOperator::CreateAnd(R_And1117, NotCout16, "", inst);
    llvm::Instruction *R_And2117 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted17, RO_RShiftedAndedNoted17, "", inst);
    llvm::Instruction *R_And2217 = llvm::BinaryOperator::CreateAnd(R_And2117, Cout16, "", inst);
    llvm::Instruction *R_And3117 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded17, RO_RShiftedAnded17, "", inst);
    llvm::Instruction *R_And3217 = llvm::BinaryOperator::CreateAnd(R_And3117, Cout16, "", inst);
    llvm::Instruction *R_Or017 = llvm::BinaryOperator::CreateOr(R_And0217, R_And1217, "", inst);
    llvm::Instruction *R_Or117 = llvm::BinaryOperator::CreateOr(R_And2217, R_And3217, "", inst);
    llvm::Instruction *R17 = llvm::BinaryOperator::CreateOr(R_Or017, R_Or117, "", inst);
    llvm::Instruction *Cout_And0117 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted17, RO_RShiftedAnded17, "", inst);
    llvm::Instruction *Cout_And0217 = llvm::BinaryOperator::CreateAnd(Cout_And0117, Cout16, "", inst);
    llvm::Instruction *Cout_And1117 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded17, RO_RShiftedAndedNoted17, "", inst);
    llvm::Instruction *Cout_And1217 = llvm::BinaryOperator::CreateAnd(Cout_And1117, Cout16, "", inst);
    llvm::Instruction *Cout_And2117 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded17, RO_RShiftedAnded17, "", inst);
    llvm::Instruction *Cout_And2217 = llvm::BinaryOperator::CreateAnd(Cout_And2117, NotCout16, "", inst);
    llvm::Instruction *Cout_And3117 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded17, RO_RShiftedAnded17, "", inst);
    llvm::Instruction *Cout_And3217 = llvm::BinaryOperator::CreateAnd(Cout_And3117, Cout16, "", inst);
    llvm::Instruction *Cout_Or017 = llvm::BinaryOperator::CreateOr(Cout_And0217, Cout_And1217, "", inst);
    llvm::Instruction *Cout_Or117 = llvm::BinaryOperator::CreateOr(Cout_And2217, Cout_And3217, "", inst);
    llvm::Instruction *Cout17 = llvm::BinaryOperator::CreateOr(Cout_Or017, Cout_Or117, "", inst);
    llvm::Instruction *NotCout17 = llvm::BinaryOperator::CreateXor(Cout17, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted18 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 18), "", inst);
    llvm::Instruction *LO_RShiftedAnded18 = llvm::BinaryOperator::CreateAnd(LO_RShifted18, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted18 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded18, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted18 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 18), "", inst);
    llvm::Instruction *RO_RShiftedAnded18 = llvm::BinaryOperator::CreateAnd(RO_RShifted18, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted18 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded18, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0118 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted18, RO_RShiftedAnded18, "", inst);
    llvm::Instruction *R_And0218 = llvm::BinaryOperator::CreateAnd(R_And0118, NotCout17, "", inst);
    llvm::Instruction *R_And1118 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded18, RO_RShiftedAndedNoted18, "", inst);
    llvm::Instruction *R_And1218 = llvm::BinaryOperator::CreateAnd(R_And1118, NotCout17, "", inst);
    llvm::Instruction *R_And2118 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted18, RO_RShiftedAndedNoted18, "", inst);
    llvm::Instruction *R_And2218 = llvm::BinaryOperator::CreateAnd(R_And2118, Cout17, "", inst);
    llvm::Instruction *R_And3118 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded18, RO_RShiftedAnded18, "", inst);
    llvm::Instruction *R_And3218 = llvm::BinaryOperator::CreateAnd(R_And3118, Cout17, "", inst);
    llvm::Instruction *R_Or018 = llvm::BinaryOperator::CreateOr(R_And0218, R_And1218, "", inst);
    llvm::Instruction *R_Or118 = llvm::BinaryOperator::CreateOr(R_And2218, R_And3218, "", inst);
    llvm::Instruction *R18 = llvm::BinaryOperator::CreateOr(R_Or018, R_Or118, "", inst);
    llvm::Instruction *Cout_And0118 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted18, RO_RShiftedAnded18, "", inst);
    llvm::Instruction *Cout_And0218 = llvm::BinaryOperator::CreateAnd(Cout_And0118, Cout17, "", inst);
    llvm::Instruction *Cout_And1118 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded18, RO_RShiftedAndedNoted18, "", inst);
    llvm::Instruction *Cout_And1218 = llvm::BinaryOperator::CreateAnd(Cout_And1118, Cout17, "", inst);
    llvm::Instruction *Cout_And2118 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded18, RO_RShiftedAnded18, "", inst);
    llvm::Instruction *Cout_And2218 = llvm::BinaryOperator::CreateAnd(Cout_And2118, NotCout17, "", inst);
    llvm::Instruction *Cout_And3118 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded18, RO_RShiftedAnded18, "", inst);
    llvm::Instruction *Cout_And3218 = llvm::BinaryOperator::CreateAnd(Cout_And3118, Cout17, "", inst);
    llvm::Instruction *Cout_Or018 = llvm::BinaryOperator::CreateOr(Cout_And0218, Cout_And1218, "", inst);
    llvm::Instruction *Cout_Or118 = llvm::BinaryOperator::CreateOr(Cout_And2218, Cout_And3218, "", inst);
    llvm::Instruction *Cout18 = llvm::BinaryOperator::CreateOr(Cout_Or018, Cout_Or118, "", inst);
    llvm::Instruction *NotCout18 = llvm::BinaryOperator::CreateXor(Cout18, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted19 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 19), "", inst);
    llvm::Instruction *LO_RShiftedAnded19 = llvm::BinaryOperator::CreateAnd(LO_RShifted19, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted19 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded19, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted19 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 19), "", inst);
    llvm::Instruction *RO_RShiftedAnded19 = llvm::BinaryOperator::CreateAnd(RO_RShifted19, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted19 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded19, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0119 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted19, RO_RShiftedAnded19, "", inst);
    llvm::Instruction *R_And0219 = llvm::BinaryOperator::CreateAnd(R_And0119, NotCout18, "", inst);
    llvm::Instruction *R_And1119 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded19, RO_RShiftedAndedNoted19, "", inst);
    llvm::Instruction *R_And1219 = llvm::BinaryOperator::CreateAnd(R_And1119, NotCout18, "", inst);
    llvm::Instruction *R_And2119 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted19, RO_RShiftedAndedNoted19, "", inst);
    llvm::Instruction *R_And2219 = llvm::BinaryOperator::CreateAnd(R_And2119, Cout18, "", inst);
    llvm::Instruction *R_And3119 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded19, RO_RShiftedAnded19, "", inst);
    llvm::Instruction *R_And3219 = llvm::BinaryOperator::CreateAnd(R_And3119, Cout18, "", inst);
    llvm::Instruction *R_Or019 = llvm::BinaryOperator::CreateOr(R_And0219, R_And1219, "", inst);
    llvm::Instruction *R_Or119 = llvm::BinaryOperator::CreateOr(R_And2219, R_And3219, "", inst);
    llvm::Instruction *R19 = llvm::BinaryOperator::CreateOr(R_Or019, R_Or119, "", inst);
    llvm::Instruction *Cout_And0119 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted19, RO_RShiftedAnded19, "", inst);
    llvm::Instruction *Cout_And0219 = llvm::BinaryOperator::CreateAnd(Cout_And0119, Cout18, "", inst);
    llvm::Instruction *Cout_And1119 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded19, RO_RShiftedAndedNoted19, "", inst);
    llvm::Instruction *Cout_And1219 = llvm::BinaryOperator::CreateAnd(Cout_And1119, Cout18, "", inst);
    llvm::Instruction *Cout_And2119 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded19, RO_RShiftedAnded19, "", inst);
    llvm::Instruction *Cout_And2219 = llvm::BinaryOperator::CreateAnd(Cout_And2119, NotCout18, "", inst);
    llvm::Instruction *Cout_And3119 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded19, RO_RShiftedAnded19, "", inst);
    llvm::Instruction *Cout_And3219 = llvm::BinaryOperator::CreateAnd(Cout_And3119, Cout18, "", inst);
    llvm::Instruction *Cout_Or019 = llvm::BinaryOperator::CreateOr(Cout_And0219, Cout_And1219, "", inst);
    llvm::Instruction *Cout_Or119 = llvm::BinaryOperator::CreateOr(Cout_And2219, Cout_And3219, "", inst);
    llvm::Instruction *Cout19 = llvm::BinaryOperator::CreateOr(Cout_Or019, Cout_Or119, "", inst);
    llvm::Instruction *NotCout19 = llvm::BinaryOperator::CreateXor(Cout19, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted20 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 20), "", inst);
    llvm::Instruction *LO_RShiftedAnded20 = llvm::BinaryOperator::CreateAnd(LO_RShifted20, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted20 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded20, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted20 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 20), "", inst);
    llvm::Instruction *RO_RShiftedAnded20 = llvm::BinaryOperator::CreateAnd(RO_RShifted20, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted20 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded20, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0120 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted20, RO_RShiftedAnded20, "", inst);
    llvm::Instruction *R_And0220 = llvm::BinaryOperator::CreateAnd(R_And0120, NotCout19, "", inst);
    llvm::Instruction *R_And1120 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded20, RO_RShiftedAndedNoted20, "", inst);
    llvm::Instruction *R_And1220 = llvm::BinaryOperator::CreateAnd(R_And1120, NotCout19, "", inst);
    llvm::Instruction *R_And2120 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted20, RO_RShiftedAndedNoted20, "", inst);
    llvm::Instruction *R_And2220 = llvm::BinaryOperator::CreateAnd(R_And2120, Cout19, "", inst);
    llvm::Instruction *R_And3120 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded20, RO_RShiftedAnded20, "", inst);
    llvm::Instruction *R_And3220 = llvm::BinaryOperator::CreateAnd(R_And3120, Cout19, "", inst);
    llvm::Instruction *R_Or020 = llvm::BinaryOperator::CreateOr(R_And0220, R_And1220, "", inst);
    llvm::Instruction *R_Or120 = llvm::BinaryOperator::CreateOr(R_And2220, R_And3220, "", inst);
    llvm::Instruction *R20 = llvm::BinaryOperator::CreateOr(R_Or020, R_Or120, "", inst);
    llvm::Instruction *Cout_And0120 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted20, RO_RShiftedAnded20, "", inst);
    llvm::Instruction *Cout_And0220 = llvm::BinaryOperator::CreateAnd(Cout_And0120, Cout19, "", inst);
    llvm::Instruction *Cout_And1120 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded20, RO_RShiftedAndedNoted20, "", inst);
    llvm::Instruction *Cout_And1220 = llvm::BinaryOperator::CreateAnd(Cout_And1120, Cout19, "", inst);
    llvm::Instruction *Cout_And2120 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded20, RO_RShiftedAnded20, "", inst);
    llvm::Instruction *Cout_And2220 = llvm::BinaryOperator::CreateAnd(Cout_And2120, NotCout19, "", inst);
    llvm::Instruction *Cout_And3120 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded20, RO_RShiftedAnded20, "", inst);
    llvm::Instruction *Cout_And3220 = llvm::BinaryOperator::CreateAnd(Cout_And3120, Cout19, "", inst);
    llvm::Instruction *Cout_Or020 = llvm::BinaryOperator::CreateOr(Cout_And0220, Cout_And1220, "", inst);
    llvm::Instruction *Cout_Or120 = llvm::BinaryOperator::CreateOr(Cout_And2220, Cout_And3220, "", inst);
    llvm::Instruction *Cout20 = llvm::BinaryOperator::CreateOr(Cout_Or020, Cout_Or120, "", inst);
    llvm::Instruction *NotCout20 = llvm::BinaryOperator::CreateXor(Cout20, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted21 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 21), "", inst);
    llvm::Instruction *LO_RShiftedAnded21 = llvm::BinaryOperator::CreateAnd(LO_RShifted21, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted21 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded21, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted21 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 21), "", inst);
    llvm::Instruction *RO_RShiftedAnded21 = llvm::BinaryOperator::CreateAnd(RO_RShifted21, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted21 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded21, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0121 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted21, RO_RShiftedAnded21, "", inst);
    llvm::Instruction *R_And0221 = llvm::BinaryOperator::CreateAnd(R_And0121, NotCout20, "", inst);
    llvm::Instruction *R_And1121 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded21, RO_RShiftedAndedNoted21, "", inst);
    llvm::Instruction *R_And1221 = llvm::BinaryOperator::CreateAnd(R_And1121, NotCout20, "", inst);
    llvm::Instruction *R_And2121 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted21, RO_RShiftedAndedNoted21, "", inst);
    llvm::Instruction *R_And2221 = llvm::BinaryOperator::CreateAnd(R_And2121, Cout20, "", inst);
    llvm::Instruction *R_And3121 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded21, RO_RShiftedAnded21, "", inst);
    llvm::Instruction *R_And3221 = llvm::BinaryOperator::CreateAnd(R_And3121, Cout20, "", inst);
    llvm::Instruction *R_Or021 = llvm::BinaryOperator::CreateOr(R_And0221, R_And1221, "", inst);
    llvm::Instruction *R_Or121 = llvm::BinaryOperator::CreateOr(R_And2221, R_And3221, "", inst);
    llvm::Instruction *R21 = llvm::BinaryOperator::CreateOr(R_Or021, R_Or121, "", inst);
    llvm::Instruction *Cout_And0121 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted21, RO_RShiftedAnded21, "", inst);
    llvm::Instruction *Cout_And0221 = llvm::BinaryOperator::CreateAnd(Cout_And0121, Cout20, "", inst);
    llvm::Instruction *Cout_And1121 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded21, RO_RShiftedAndedNoted21, "", inst);
    llvm::Instruction *Cout_And1221 = llvm::BinaryOperator::CreateAnd(Cout_And1121, Cout20, "", inst);
    llvm::Instruction *Cout_And2121 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded21, RO_RShiftedAnded21, "", inst);
    llvm::Instruction *Cout_And2221 = llvm::BinaryOperator::CreateAnd(Cout_And2121, NotCout20, "", inst);
    llvm::Instruction *Cout_And3121 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded21, RO_RShiftedAnded21, "", inst);
    llvm::Instruction *Cout_And3221 = llvm::BinaryOperator::CreateAnd(Cout_And3121, Cout20, "", inst);
    llvm::Instruction *Cout_Or021 = llvm::BinaryOperator::CreateOr(Cout_And0221, Cout_And1221, "", inst);
    llvm::Instruction *Cout_Or121 = llvm::BinaryOperator::CreateOr(Cout_And2221, Cout_And3221, "", inst);
    llvm::Instruction *Cout21 = llvm::BinaryOperator::CreateOr(Cout_Or021, Cout_Or121, "", inst);
    llvm::Instruction *NotCout21 = llvm::BinaryOperator::CreateXor(Cout21, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted22 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 22), "", inst);
    llvm::Instruction *LO_RShiftedAnded22 = llvm::BinaryOperator::CreateAnd(LO_RShifted22, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted22 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded22, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted22 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 22), "", inst);
    llvm::Instruction *RO_RShiftedAnded22 = llvm::BinaryOperator::CreateAnd(RO_RShifted22, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted22 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded22, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0122 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted22, RO_RShiftedAnded22, "", inst);
    llvm::Instruction *R_And0222 = llvm::BinaryOperator::CreateAnd(R_And0122, NotCout21, "", inst);
    llvm::Instruction *R_And1122 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded22, RO_RShiftedAndedNoted22, "", inst);
    llvm::Instruction *R_And1222 = llvm::BinaryOperator::CreateAnd(R_And1122, NotCout21, "", inst);
    llvm::Instruction *R_And2122 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted22, RO_RShiftedAndedNoted22, "", inst);
    llvm::Instruction *R_And2222 = llvm::BinaryOperator::CreateAnd(R_And2122, Cout21, "", inst);
    llvm::Instruction *R_And3122 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded22, RO_RShiftedAnded22, "", inst);
    llvm::Instruction *R_And3222 = llvm::BinaryOperator::CreateAnd(R_And3122, Cout21, "", inst);
    llvm::Instruction *R_Or022 = llvm::BinaryOperator::CreateOr(R_And0222, R_And1222, "", inst);
    llvm::Instruction *R_Or122 = llvm::BinaryOperator::CreateOr(R_And2222, R_And3222, "", inst);
    llvm::Instruction *R22 = llvm::BinaryOperator::CreateOr(R_Or022, R_Or122, "", inst);
    llvm::Instruction *Cout_And0122 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted22, RO_RShiftedAnded22, "", inst);
    llvm::Instruction *Cout_And0222 = llvm::BinaryOperator::CreateAnd(Cout_And0122, Cout21, "", inst);
    llvm::Instruction *Cout_And1122 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded22, RO_RShiftedAndedNoted22, "", inst);
    llvm::Instruction *Cout_And1222 = llvm::BinaryOperator::CreateAnd(Cout_And1122, Cout21, "", inst);
    llvm::Instruction *Cout_And2122 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded22, RO_RShiftedAnded22, "", inst);
    llvm::Instruction *Cout_And2222 = llvm::BinaryOperator::CreateAnd(Cout_And2122, NotCout21, "", inst);
    llvm::Instruction *Cout_And3122 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded22, RO_RShiftedAnded22, "", inst);
    llvm::Instruction *Cout_And3222 = llvm::BinaryOperator::CreateAnd(Cout_And3122, Cout21, "", inst);
    llvm::Instruction *Cout_Or022 = llvm::BinaryOperator::CreateOr(Cout_And0222, Cout_And1222, "", inst);
    llvm::Instruction *Cout_Or122 = llvm::BinaryOperator::CreateOr(Cout_And2222, Cout_And3222, "", inst);
    llvm::Instruction *Cout22 = llvm::BinaryOperator::CreateOr(Cout_Or022, Cout_Or122, "", inst);
    llvm::Instruction *NotCout22 = llvm::BinaryOperator::CreateXor(Cout22, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted23 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 23), "", inst);
    llvm::Instruction *LO_RShiftedAnded23 = llvm::BinaryOperator::CreateAnd(LO_RShifted23, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted23 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded23, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted23 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 23), "", inst);
    llvm::Instruction *RO_RShiftedAnded23 = llvm::BinaryOperator::CreateAnd(RO_RShifted23, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted23 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded23, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0123 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted23, RO_RShiftedAnded23, "", inst);
    llvm::Instruction *R_And0223 = llvm::BinaryOperator::CreateAnd(R_And0123, NotCout22, "", inst);
    llvm::Instruction *R_And1123 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded23, RO_RShiftedAndedNoted23, "", inst);
    llvm::Instruction *R_And1223 = llvm::BinaryOperator::CreateAnd(R_And1123, NotCout22, "", inst);
    llvm::Instruction *R_And2123 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted23, RO_RShiftedAndedNoted23, "", inst);
    llvm::Instruction *R_And2223 = llvm::BinaryOperator::CreateAnd(R_And2123, Cout22, "", inst);
    llvm::Instruction *R_And3123 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded23, RO_RShiftedAnded23, "", inst);
    llvm::Instruction *R_And3223 = llvm::BinaryOperator::CreateAnd(R_And3123, Cout22, "", inst);
    llvm::Instruction *R_Or023 = llvm::BinaryOperator::CreateOr(R_And0223, R_And1223, "", inst);
    llvm::Instruction *R_Or123 = llvm::BinaryOperator::CreateOr(R_And2223, R_And3223, "", inst);
    llvm::Instruction *R23 = llvm::BinaryOperator::CreateOr(R_Or023, R_Or123, "", inst);
    llvm::Instruction *Cout_And0123 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted23, RO_RShiftedAnded23, "", inst);
    llvm::Instruction *Cout_And0223 = llvm::BinaryOperator::CreateAnd(Cout_And0123, Cout22, "", inst);
    llvm::Instruction *Cout_And1123 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded23, RO_RShiftedAndedNoted23, "", inst);
    llvm::Instruction *Cout_And1223 = llvm::BinaryOperator::CreateAnd(Cout_And1123, Cout22, "", inst);
    llvm::Instruction *Cout_And2123 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded23, RO_RShiftedAnded23, "", inst);
    llvm::Instruction *Cout_And2223 = llvm::BinaryOperator::CreateAnd(Cout_And2123, NotCout22, "", inst);
    llvm::Instruction *Cout_And3123 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded23, RO_RShiftedAnded23, "", inst);
    llvm::Instruction *Cout_And3223 = llvm::BinaryOperator::CreateAnd(Cout_And3123, Cout22, "", inst);
    llvm::Instruction *Cout_Or023 = llvm::BinaryOperator::CreateOr(Cout_And0223, Cout_And1223, "", inst);
    llvm::Instruction *Cout_Or123 = llvm::BinaryOperator::CreateOr(Cout_And2223, Cout_And3223, "", inst);
    llvm::Instruction *Cout23 = llvm::BinaryOperator::CreateOr(Cout_Or023, Cout_Or123, "", inst);
    llvm::Instruction *NotCout23 = llvm::BinaryOperator::CreateXor(Cout23, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted24 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 24), "", inst);
    llvm::Instruction *LO_RShiftedAnded24 = llvm::BinaryOperator::CreateAnd(LO_RShifted24, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted24 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded24, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted24 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 24), "", inst);
    llvm::Instruction *RO_RShiftedAnded24 = llvm::BinaryOperator::CreateAnd(RO_RShifted24, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted24 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded24, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0124 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted24, RO_RShiftedAnded24, "", inst);
    llvm::Instruction *R_And0224 = llvm::BinaryOperator::CreateAnd(R_And0124, NotCout23, "", inst);
    llvm::Instruction *R_And1124 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded24, RO_RShiftedAndedNoted24, "", inst);
    llvm::Instruction *R_And1224 = llvm::BinaryOperator::CreateAnd(R_And1124, NotCout23, "", inst);
    llvm::Instruction *R_And2124 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted24, RO_RShiftedAndedNoted24, "", inst);
    llvm::Instruction *R_And2224 = llvm::BinaryOperator::CreateAnd(R_And2124, Cout23, "", inst);
    llvm::Instruction *R_And3124 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded24, RO_RShiftedAnded24, "", inst);
    llvm::Instruction *R_And3224 = llvm::BinaryOperator::CreateAnd(R_And3124, Cout23, "", inst);
    llvm::Instruction *R_Or024 = llvm::BinaryOperator::CreateOr(R_And0224, R_And1224, "", inst);
    llvm::Instruction *R_Or124 = llvm::BinaryOperator::CreateOr(R_And2224, R_And3224, "", inst);
    llvm::Instruction *R24 = llvm::BinaryOperator::CreateOr(R_Or024, R_Or124, "", inst);
    llvm::Instruction *Cout_And0124 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted24, RO_RShiftedAnded24, "", inst);
    llvm::Instruction *Cout_And0224 = llvm::BinaryOperator::CreateAnd(Cout_And0124, Cout23, "", inst);
    llvm::Instruction *Cout_And1124 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded24, RO_RShiftedAndedNoted24, "", inst);
    llvm::Instruction *Cout_And1224 = llvm::BinaryOperator::CreateAnd(Cout_And1124, Cout23, "", inst);
    llvm::Instruction *Cout_And2124 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded24, RO_RShiftedAnded24, "", inst);
    llvm::Instruction *Cout_And2224 = llvm::BinaryOperator::CreateAnd(Cout_And2124, NotCout23, "", inst);
    llvm::Instruction *Cout_And3124 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded24, RO_RShiftedAnded24, "", inst);
    llvm::Instruction *Cout_And3224 = llvm::BinaryOperator::CreateAnd(Cout_And3124, Cout23, "", inst);
    llvm::Instruction *Cout_Or024 = llvm::BinaryOperator::CreateOr(Cout_And0224, Cout_And1224, "", inst);
    llvm::Instruction *Cout_Or124 = llvm::BinaryOperator::CreateOr(Cout_And2224, Cout_And3224, "", inst);
    llvm::Instruction *Cout24 = llvm::BinaryOperator::CreateOr(Cout_Or024, Cout_Or124, "", inst);
    llvm::Instruction *NotCout24 = llvm::BinaryOperator::CreateXor(Cout24, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted25 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 25), "", inst);
    llvm::Instruction *LO_RShiftedAnded25 = llvm::BinaryOperator::CreateAnd(LO_RShifted25, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted25 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded25, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted25 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 25), "", inst);
    llvm::Instruction *RO_RShiftedAnded25 = llvm::BinaryOperator::CreateAnd(RO_RShifted25, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted25 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded25, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0125 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted25, RO_RShiftedAnded25, "", inst);
    llvm::Instruction *R_And0225 = llvm::BinaryOperator::CreateAnd(R_And0125, NotCout24, "", inst);
    llvm::Instruction *R_And1125 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded25, RO_RShiftedAndedNoted25, "", inst);
    llvm::Instruction *R_And1225 = llvm::BinaryOperator::CreateAnd(R_And1125, NotCout24, "", inst);
    llvm::Instruction *R_And2125 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted25, RO_RShiftedAndedNoted25, "", inst);
    llvm::Instruction *R_And2225 = llvm::BinaryOperator::CreateAnd(R_And2125, Cout24, "", inst);
    llvm::Instruction *R_And3125 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded25, RO_RShiftedAnded25, "", inst);
    llvm::Instruction *R_And3225 = llvm::BinaryOperator::CreateAnd(R_And3125, Cout24, "", inst);
    llvm::Instruction *R_Or025 = llvm::BinaryOperator::CreateOr(R_And0225, R_And1225, "", inst);
    llvm::Instruction *R_Or125 = llvm::BinaryOperator::CreateOr(R_And2225, R_And3225, "", inst);
    llvm::Instruction *R25 = llvm::BinaryOperator::CreateOr(R_Or025, R_Or125, "", inst);
    llvm::Instruction *Cout_And0125 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted25, RO_RShiftedAnded25, "", inst);
    llvm::Instruction *Cout_And0225 = llvm::BinaryOperator::CreateAnd(Cout_And0125, Cout24, "", inst);
    llvm::Instruction *Cout_And1125 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded25, RO_RShiftedAndedNoted25, "", inst);
    llvm::Instruction *Cout_And1225 = llvm::BinaryOperator::CreateAnd(Cout_And1125, Cout24, "", inst);
    llvm::Instruction *Cout_And2125 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded25, RO_RShiftedAnded25, "", inst);
    llvm::Instruction *Cout_And2225 = llvm::BinaryOperator::CreateAnd(Cout_And2125, NotCout24, "", inst);
    llvm::Instruction *Cout_And3125 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded25, RO_RShiftedAnded25, "", inst);
    llvm::Instruction *Cout_And3225 = llvm::BinaryOperator::CreateAnd(Cout_And3125, Cout24, "", inst);
    llvm::Instruction *Cout_Or025 = llvm::BinaryOperator::CreateOr(Cout_And0225, Cout_And1225, "", inst);
    llvm::Instruction *Cout_Or125 = llvm::BinaryOperator::CreateOr(Cout_And2225, Cout_And3225, "", inst);
    llvm::Instruction *Cout25 = llvm::BinaryOperator::CreateOr(Cout_Or025, Cout_Or125, "", inst);
    llvm::Instruction *NotCout25 = llvm::BinaryOperator::CreateXor(Cout25, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted26 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 26), "", inst);
    llvm::Instruction *LO_RShiftedAnded26 = llvm::BinaryOperator::CreateAnd(LO_RShifted26, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted26 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded26, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted26 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 26), "", inst);
    llvm::Instruction *RO_RShiftedAnded26 = llvm::BinaryOperator::CreateAnd(RO_RShifted26, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted26 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded26, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0126 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted26, RO_RShiftedAnded26, "", inst);
    llvm::Instruction *R_And0226 = llvm::BinaryOperator::CreateAnd(R_And0126, NotCout25, "", inst);
    llvm::Instruction *R_And1126 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded26, RO_RShiftedAndedNoted26, "", inst);
    llvm::Instruction *R_And1226 = llvm::BinaryOperator::CreateAnd(R_And1126, NotCout25, "", inst);
    llvm::Instruction *R_And2126 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted26, RO_RShiftedAndedNoted26, "", inst);
    llvm::Instruction *R_And2226 = llvm::BinaryOperator::CreateAnd(R_And2126, Cout25, "", inst);
    llvm::Instruction *R_And3126 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded26, RO_RShiftedAnded26, "", inst);
    llvm::Instruction *R_And3226 = llvm::BinaryOperator::CreateAnd(R_And3126, Cout25, "", inst);
    llvm::Instruction *R_Or026 = llvm::BinaryOperator::CreateOr(R_And0226, R_And1226, "", inst);
    llvm::Instruction *R_Or126 = llvm::BinaryOperator::CreateOr(R_And2226, R_And3226, "", inst);
    llvm::Instruction *R26 = llvm::BinaryOperator::CreateOr(R_Or026, R_Or126, "", inst);
    llvm::Instruction *Cout_And0126 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted26, RO_RShiftedAnded26, "", inst);
    llvm::Instruction *Cout_And0226 = llvm::BinaryOperator::CreateAnd(Cout_And0126, Cout25, "", inst);
    llvm::Instruction *Cout_And1126 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded26, RO_RShiftedAndedNoted26, "", inst);
    llvm::Instruction *Cout_And1226 = llvm::BinaryOperator::CreateAnd(Cout_And1126, Cout25, "", inst);
    llvm::Instruction *Cout_And2126 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded26, RO_RShiftedAnded26, "", inst);
    llvm::Instruction *Cout_And2226 = llvm::BinaryOperator::CreateAnd(Cout_And2126, NotCout25, "", inst);
    llvm::Instruction *Cout_And3126 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded26, RO_RShiftedAnded26, "", inst);
    llvm::Instruction *Cout_And3226 = llvm::BinaryOperator::CreateAnd(Cout_And3126, Cout25, "", inst);
    llvm::Instruction *Cout_Or026 = llvm::BinaryOperator::CreateOr(Cout_And0226, Cout_And1226, "", inst);
    llvm::Instruction *Cout_Or126 = llvm::BinaryOperator::CreateOr(Cout_And2226, Cout_And3226, "", inst);
    llvm::Instruction *Cout26 = llvm::BinaryOperator::CreateOr(Cout_Or026, Cout_Or126, "", inst);
    llvm::Instruction *NotCout26 = llvm::BinaryOperator::CreateXor(Cout26, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted27 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 27), "", inst);
    llvm::Instruction *LO_RShiftedAnded27 = llvm::BinaryOperator::CreateAnd(LO_RShifted27, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted27 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded27, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted27 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 27), "", inst);
    llvm::Instruction *RO_RShiftedAnded27 = llvm::BinaryOperator::CreateAnd(RO_RShifted27, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted27 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded27, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0127 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted27, RO_RShiftedAnded27, "", inst);
    llvm::Instruction *R_And0227 = llvm::BinaryOperator::CreateAnd(R_And0127, NotCout26, "", inst);
    llvm::Instruction *R_And1127 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded27, RO_RShiftedAndedNoted27, "", inst);
    llvm::Instruction *R_And1227 = llvm::BinaryOperator::CreateAnd(R_And1127, NotCout26, "", inst);
    llvm::Instruction *R_And2127 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted27, RO_RShiftedAndedNoted27, "", inst);
    llvm::Instruction *R_And2227 = llvm::BinaryOperator::CreateAnd(R_And2127, Cout26, "", inst);
    llvm::Instruction *R_And3127 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded27, RO_RShiftedAnded27, "", inst);
    llvm::Instruction *R_And3227 = llvm::BinaryOperator::CreateAnd(R_And3127, Cout26, "", inst);
    llvm::Instruction *R_Or027 = llvm::BinaryOperator::CreateOr(R_And0227, R_And1227, "", inst);
    llvm::Instruction *R_Or127 = llvm::BinaryOperator::CreateOr(R_And2227, R_And3227, "", inst);
    llvm::Instruction *R27 = llvm::BinaryOperator::CreateOr(R_Or027, R_Or127, "", inst);
    llvm::Instruction *Cout_And0127 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted27, RO_RShiftedAnded27, "", inst);
    llvm::Instruction *Cout_And0227 = llvm::BinaryOperator::CreateAnd(Cout_And0127, Cout26, "", inst);
    llvm::Instruction *Cout_And1127 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded27, RO_RShiftedAndedNoted27, "", inst);
    llvm::Instruction *Cout_And1227 = llvm::BinaryOperator::CreateAnd(Cout_And1127, Cout26, "", inst);
    llvm::Instruction *Cout_And2127 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded27, RO_RShiftedAnded27, "", inst);
    llvm::Instruction *Cout_And2227 = llvm::BinaryOperator::CreateAnd(Cout_And2127, NotCout26, "", inst);
    llvm::Instruction *Cout_And3127 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded27, RO_RShiftedAnded27, "", inst);
    llvm::Instruction *Cout_And3227 = llvm::BinaryOperator::CreateAnd(Cout_And3127, Cout26, "", inst);
    llvm::Instruction *Cout_Or027 = llvm::BinaryOperator::CreateOr(Cout_And0227, Cout_And1227, "", inst);
    llvm::Instruction *Cout_Or127 = llvm::BinaryOperator::CreateOr(Cout_And2227, Cout_And3227, "", inst);
    llvm::Instruction *Cout27 = llvm::BinaryOperator::CreateOr(Cout_Or027, Cout_Or127, "", inst);
    llvm::Instruction *NotCout27 = llvm::BinaryOperator::CreateXor(Cout27, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted28 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 28), "", inst);
    llvm::Instruction *LO_RShiftedAnded28 = llvm::BinaryOperator::CreateAnd(LO_RShifted28, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted28 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded28, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted28 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 28), "", inst);
    llvm::Instruction *RO_RShiftedAnded28 = llvm::BinaryOperator::CreateAnd(RO_RShifted28, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted28 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded28, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0128 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted28, RO_RShiftedAnded28, "", inst);
    llvm::Instruction *R_And0228 = llvm::BinaryOperator::CreateAnd(R_And0128, NotCout27, "", inst);
    llvm::Instruction *R_And1128 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded28, RO_RShiftedAndedNoted28, "", inst);
    llvm::Instruction *R_And1228 = llvm::BinaryOperator::CreateAnd(R_And1128, NotCout27, "", inst);
    llvm::Instruction *R_And2128 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted28, RO_RShiftedAndedNoted28, "", inst);
    llvm::Instruction *R_And2228 = llvm::BinaryOperator::CreateAnd(R_And2128, Cout27, "", inst);
    llvm::Instruction *R_And3128 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded28, RO_RShiftedAnded28, "", inst);
    llvm::Instruction *R_And3228 = llvm::BinaryOperator::CreateAnd(R_And3128, Cout27, "", inst);
    llvm::Instruction *R_Or028 = llvm::BinaryOperator::CreateOr(R_And0228, R_And1228, "", inst);
    llvm::Instruction *R_Or128 = llvm::BinaryOperator::CreateOr(R_And2228, R_And3228, "", inst);
    llvm::Instruction *R28 = llvm::BinaryOperator::CreateOr(R_Or028, R_Or128, "", inst);
    llvm::Instruction *Cout_And0128 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted28, RO_RShiftedAnded28, "", inst);
    llvm::Instruction *Cout_And0228 = llvm::BinaryOperator::CreateAnd(Cout_And0128, Cout27, "", inst);
    llvm::Instruction *Cout_And1128 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded28, RO_RShiftedAndedNoted28, "", inst);
    llvm::Instruction *Cout_And1228 = llvm::BinaryOperator::CreateAnd(Cout_And1128, Cout27, "", inst);
    llvm::Instruction *Cout_And2128 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded28, RO_RShiftedAnded28, "", inst);
    llvm::Instruction *Cout_And2228 = llvm::BinaryOperator::CreateAnd(Cout_And2128, NotCout27, "", inst);
    llvm::Instruction *Cout_And3128 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded28, RO_RShiftedAnded28, "", inst);
    llvm::Instruction *Cout_And3228 = llvm::BinaryOperator::CreateAnd(Cout_And3128, Cout27, "", inst);
    llvm::Instruction *Cout_Or028 = llvm::BinaryOperator::CreateOr(Cout_And0228, Cout_And1228, "", inst);
    llvm::Instruction *Cout_Or128 = llvm::BinaryOperator::CreateOr(Cout_And2228, Cout_And3228, "", inst);
    llvm::Instruction *Cout28 = llvm::BinaryOperator::CreateOr(Cout_Or028, Cout_Or128, "", inst);
    llvm::Instruction *NotCout28 = llvm::BinaryOperator::CreateXor(Cout28, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted29 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 29), "", inst);
    llvm::Instruction *LO_RShiftedAnded29 = llvm::BinaryOperator::CreateAnd(LO_RShifted29, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted29 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded29, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted29 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 29), "", inst);
    llvm::Instruction *RO_RShiftedAnded29 = llvm::BinaryOperator::CreateAnd(RO_RShifted29, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted29 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded29, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0129 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted29, RO_RShiftedAnded29, "", inst);
    llvm::Instruction *R_And0229 = llvm::BinaryOperator::CreateAnd(R_And0129, NotCout28, "", inst);
    llvm::Instruction *R_And1129 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded29, RO_RShiftedAndedNoted29, "", inst);
    llvm::Instruction *R_And1229 = llvm::BinaryOperator::CreateAnd(R_And1129, NotCout28, "", inst);
    llvm::Instruction *R_And2129 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted29, RO_RShiftedAndedNoted29, "", inst);
    llvm::Instruction *R_And2229 = llvm::BinaryOperator::CreateAnd(R_And2129, Cout28, "", inst);
    llvm::Instruction *R_And3129 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded29, RO_RShiftedAnded29, "", inst);
    llvm::Instruction *R_And3229 = llvm::BinaryOperator::CreateAnd(R_And3129, Cout28, "", inst);
    llvm::Instruction *R_Or029 = llvm::BinaryOperator::CreateOr(R_And0229, R_And1229, "", inst);
    llvm::Instruction *R_Or129 = llvm::BinaryOperator::CreateOr(R_And2229, R_And3229, "", inst);
    llvm::Instruction *R29 = llvm::BinaryOperator::CreateOr(R_Or029, R_Or129, "", inst);
    llvm::Instruction *Cout_And0129 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted29, RO_RShiftedAnded29, "", inst);
    llvm::Instruction *Cout_And0229 = llvm::BinaryOperator::CreateAnd(Cout_And0129, Cout28, "", inst);
    llvm::Instruction *Cout_And1129 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded29, RO_RShiftedAndedNoted29, "", inst);
    llvm::Instruction *Cout_And1229 = llvm::BinaryOperator::CreateAnd(Cout_And1129, Cout28, "", inst);
    llvm::Instruction *Cout_And2129 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded29, RO_RShiftedAnded29, "", inst);
    llvm::Instruction *Cout_And2229 = llvm::BinaryOperator::CreateAnd(Cout_And2129, NotCout28, "", inst);
    llvm::Instruction *Cout_And3129 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded29, RO_RShiftedAnded29, "", inst);
    llvm::Instruction *Cout_And3229 = llvm::BinaryOperator::CreateAnd(Cout_And3129, Cout28, "", inst);
    llvm::Instruction *Cout_Or029 = llvm::BinaryOperator::CreateOr(Cout_And0229, Cout_And1229, "", inst);
    llvm::Instruction *Cout_Or129 = llvm::BinaryOperator::CreateOr(Cout_And2229, Cout_And3229, "", inst);
    llvm::Instruction *Cout29 = llvm::BinaryOperator::CreateOr(Cout_Or029, Cout_Or129, "", inst);
    llvm::Instruction *NotCout29 = llvm::BinaryOperator::CreateXor(Cout29, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted30 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 30), "", inst);
    llvm::Instruction *LO_RShiftedAnded30 = llvm::BinaryOperator::CreateAnd(LO_RShifted30, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted30 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded30, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted30 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 30), "", inst);
    llvm::Instruction *RO_RShiftedAnded30 = llvm::BinaryOperator::CreateAnd(RO_RShifted30, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted30 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded30, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0130 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted30, RO_RShiftedAnded30, "", inst);
    llvm::Instruction *R_And0230 = llvm::BinaryOperator::CreateAnd(R_And0130, NotCout29, "", inst);
    llvm::Instruction *R_And1130 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded30, RO_RShiftedAndedNoted30, "", inst);
    llvm::Instruction *R_And1230 = llvm::BinaryOperator::CreateAnd(R_And1130, NotCout29, "", inst);
    llvm::Instruction *R_And2130 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted30, RO_RShiftedAndedNoted30, "", inst);
    llvm::Instruction *R_And2230 = llvm::BinaryOperator::CreateAnd(R_And2130, Cout29, "", inst);
    llvm::Instruction *R_And3130 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded30, RO_RShiftedAnded30, "", inst);
    llvm::Instruction *R_And3230 = llvm::BinaryOperator::CreateAnd(R_And3130, Cout29, "", inst);
    llvm::Instruction *R_Or030 = llvm::BinaryOperator::CreateOr(R_And0230, R_And1230, "", inst);
    llvm::Instruction *R_Or130 = llvm::BinaryOperator::CreateOr(R_And2230, R_And3230, "", inst);
    llvm::Instruction *R30 = llvm::BinaryOperator::CreateOr(R_Or030, R_Or130, "", inst);
    llvm::Instruction *Cout_And0130 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted30, RO_RShiftedAnded30, "", inst);
    llvm::Instruction *Cout_And0230 = llvm::BinaryOperator::CreateAnd(Cout_And0130, Cout29, "", inst);
    llvm::Instruction *Cout_And1130 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded30, RO_RShiftedAndedNoted30, "", inst);
    llvm::Instruction *Cout_And1230 = llvm::BinaryOperator::CreateAnd(Cout_And1130, Cout29, "", inst);
    llvm::Instruction *Cout_And2130 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded30, RO_RShiftedAnded30, "", inst);
    llvm::Instruction *Cout_And2230 = llvm::BinaryOperator::CreateAnd(Cout_And2130, NotCout29, "", inst);
    llvm::Instruction *Cout_And3130 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded30, RO_RShiftedAnded30, "", inst);
    llvm::Instruction *Cout_And3230 = llvm::BinaryOperator::CreateAnd(Cout_And3130, Cout29, "", inst);
    llvm::Instruction *Cout_Or030 = llvm::BinaryOperator::CreateOr(Cout_And0230, Cout_And1230, "", inst);
    llvm::Instruction *Cout_Or130 = llvm::BinaryOperator::CreateOr(Cout_And2230, Cout_And3230, "", inst);
    llvm::Instruction *Cout30 = llvm::BinaryOperator::CreateOr(Cout_Or030, Cout_Or130, "", inst);
    llvm::Instruction *NotCout30 = llvm::BinaryOperator::CreateXor(Cout30, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShifted31 = llvm::BinaryOperator::CreateLShr(A, llvm::ConstantInt::get(Int32Ty, 31), "", inst);
    llvm::Instruction *LO_RShiftedAnded31 = llvm::BinaryOperator::CreateAnd(LO_RShifted31, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *LO_RShiftedAndedNoted31 = llvm::BinaryOperator::CreateXor(LO_RShiftedAnded31, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShifted31 = llvm::BinaryOperator::CreateLShr(B, llvm::ConstantInt::get(Int32Ty, 31), "", inst);
    llvm::Instruction *RO_RShiftedAnded31 = llvm::BinaryOperator::CreateAnd(RO_RShifted31, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *RO_RShiftedAndedNoted31 = llvm::BinaryOperator::CreateXor(RO_RShiftedAnded31, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R_And0131 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted31, RO_RShiftedAnded31, "", inst);
    llvm::Instruction *R_And0231 = llvm::BinaryOperator::CreateAnd(R_And0131, NotCout30, "", inst);
    llvm::Instruction *R_And1131 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded31, RO_RShiftedAndedNoted31, "", inst);
    llvm::Instruction *R_And1231 = llvm::BinaryOperator::CreateAnd(R_And1131, NotCout30, "", inst);
    llvm::Instruction *R_And2131 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted31, RO_RShiftedAndedNoted31, "", inst);
    llvm::Instruction *R_And2231 = llvm::BinaryOperator::CreateAnd(R_And2131, Cout30, "", inst);
    llvm::Instruction *R_And3131 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded31, RO_RShiftedAnded31, "", inst);
    llvm::Instruction *R_And3231 = llvm::BinaryOperator::CreateAnd(R_And3131, Cout30, "", inst);
    llvm::Instruction *R_Or031 = llvm::BinaryOperator::CreateOr(R_And0231, R_And1231, "", inst);
    llvm::Instruction *R_Or131 = llvm::BinaryOperator::CreateOr(R_And2231, R_And3231, "", inst);
    llvm::Instruction *R31 = llvm::BinaryOperator::CreateOr(R_Or031, R_Or131, "", inst);
    llvm::Instruction *Cout_And0131 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAndedNoted31, RO_RShiftedAnded31, "", inst);
    llvm::Instruction *Cout_And0231 = llvm::BinaryOperator::CreateAnd(Cout_And0131, Cout30, "", inst);
    llvm::Instruction *Cout_And1131 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded31, RO_RShiftedAndedNoted31, "", inst);
    llvm::Instruction *Cout_And1231 = llvm::BinaryOperator::CreateAnd(Cout_And1131, Cout30, "", inst);
    llvm::Instruction *Cout_And2131 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded31, RO_RShiftedAnded31, "", inst);
    llvm::Instruction *Cout_And2231 = llvm::BinaryOperator::CreateAnd(Cout_And2131, NotCout30, "", inst);
    llvm::Instruction *Cout_And3131 = llvm::BinaryOperator::CreateAnd(LO_RShiftedAnded31, RO_RShiftedAnded31, "", inst);
    llvm::Instruction *Cout_And3231 = llvm::BinaryOperator::CreateAnd(Cout_And3131, Cout30, "", inst);
    llvm::Instruction *Cout_Or031 = llvm::BinaryOperator::CreateOr(Cout_And0231, Cout_And1231, "", inst);
    llvm::Instruction *Cout_Or131 = llvm::BinaryOperator::CreateOr(Cout_And2231, Cout_And3231, "", inst);
    llvm::Instruction *Cout31 = llvm::BinaryOperator::CreateOr(Cout_Or031, Cout_Or131, "", inst);
    llvm::Instruction *NotCout31 = llvm::BinaryOperator::CreateXor(Cout31, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R0_LShifted = llvm::BinaryOperator::CreateShl(R0, llvm::ConstantInt::get(Int32Ty, 0), "", inst);
    llvm::Instruction *R1_LShifted = llvm::BinaryOperator::CreateShl(R1, llvm::ConstantInt::get(Int32Ty, 1), "", inst);
    llvm::Instruction *R2_LShifted = llvm::BinaryOperator::CreateShl(R2, llvm::ConstantInt::get(Int32Ty, 2), "", inst);
    llvm::Instruction *R3_LShifted = llvm::BinaryOperator::CreateShl(R3, llvm::ConstantInt::get(Int32Ty, 3), "", inst);
    llvm::Instruction *R4_LShifted = llvm::BinaryOperator::CreateShl(R4, llvm::ConstantInt::get(Int32Ty, 4), "", inst);
    llvm::Instruction *R5_LShifted = llvm::BinaryOperator::CreateShl(R5, llvm::ConstantInt::get(Int32Ty, 5), "", inst);
    llvm::Instruction *R6_LShifted = llvm::BinaryOperator::CreateShl(R6, llvm::ConstantInt::get(Int32Ty, 6), "", inst);
    llvm::Instruction *R7_LShifted = llvm::BinaryOperator::CreateShl(R7, llvm::ConstantInt::get(Int32Ty, 7), "", inst);
    llvm::Instruction *R8_LShifted = llvm::BinaryOperator::CreateShl(R8, llvm::ConstantInt::get(Int32Ty, 8), "", inst);
    llvm::Instruction *R9_LShifted = llvm::BinaryOperator::CreateShl(R9, llvm::ConstantInt::get(Int32Ty, 9), "", inst);
    llvm::Instruction *R10_LShifted = llvm::BinaryOperator::CreateShl(R10, llvm::ConstantInt::get(Int32Ty, 10), "", inst);
    llvm::Instruction *R11_LShifted = llvm::BinaryOperator::CreateShl(R11, llvm::ConstantInt::get(Int32Ty, 11), "", inst);
    llvm::Instruction *R12_LShifted = llvm::BinaryOperator::CreateShl(R12, llvm::ConstantInt::get(Int32Ty, 12), "", inst);
    llvm::Instruction *R13_LShifted = llvm::BinaryOperator::CreateShl(R13, llvm::ConstantInt::get(Int32Ty, 13), "", inst);
    llvm::Instruction *R14_LShifted = llvm::BinaryOperator::CreateShl(R14, llvm::ConstantInt::get(Int32Ty, 14), "", inst);
    llvm::Instruction *R15_LShifted = llvm::BinaryOperator::CreateShl(R15, llvm::ConstantInt::get(Int32Ty, 15), "", inst);
    llvm::Instruction *R16_LShifted = llvm::BinaryOperator::CreateShl(R16, llvm::ConstantInt::get(Int32Ty, 16), "", inst);
    llvm::Instruction *R17_LShifted = llvm::BinaryOperator::CreateShl(R17, llvm::ConstantInt::get(Int32Ty, 17), "", inst);
    llvm::Instruction *R18_LShifted = llvm::BinaryOperator::CreateShl(R18, llvm::ConstantInt::get(Int32Ty, 18), "", inst);
    llvm::Instruction *R19_LShifted = llvm::BinaryOperator::CreateShl(R19, llvm::ConstantInt::get(Int32Ty, 19), "", inst);
    llvm::Instruction *R20_LShifted = llvm::BinaryOperator::CreateShl(R20, llvm::ConstantInt::get(Int32Ty, 20), "", inst);
    llvm::Instruction *R21_LShifted = llvm::BinaryOperator::CreateShl(R21, llvm::ConstantInt::get(Int32Ty, 21), "", inst);
    llvm::Instruction *R22_LShifted = llvm::BinaryOperator::CreateShl(R22, llvm::ConstantInt::get(Int32Ty, 22), "", inst);
    llvm::Instruction *R23_LShifted = llvm::BinaryOperator::CreateShl(R23, llvm::ConstantInt::get(Int32Ty, 23), "", inst);
    llvm::Instruction *R24_LShifted = llvm::BinaryOperator::CreateShl(R24, llvm::ConstantInt::get(Int32Ty, 24), "", inst);
    llvm::Instruction *R25_LShifted = llvm::BinaryOperator::CreateShl(R25, llvm::ConstantInt::get(Int32Ty, 25), "", inst);
    llvm::Instruction *R26_LShifted = llvm::BinaryOperator::CreateShl(R26, llvm::ConstantInt::get(Int32Ty, 26), "", inst);
    llvm::Instruction *R27_LShifted = llvm::BinaryOperator::CreateShl(R27, llvm::ConstantInt::get(Int32Ty, 27), "", inst);
    llvm::Instruction *R28_LShifted = llvm::BinaryOperator::CreateShl(R28, llvm::ConstantInt::get(Int32Ty, 28), "", inst);
    llvm::Instruction *R29_LShifted = llvm::BinaryOperator::CreateShl(R29, llvm::ConstantInt::get(Int32Ty, 29), "", inst);
    llvm::Instruction *R30_LShifted = llvm::BinaryOperator::CreateShl(R30, llvm::ConstantInt::get(Int32Ty, 30), "", inst);
    llvm::Instruction *R31_LShifted = llvm::BinaryOperator::CreateShl(R31, llvm::ConstantInt::get(Int32Ty, 31), "", inst);
    llvm::Instruction *R_Tmp0 = llvm::BinaryOperator::CreateAdd(R0_LShifted, R1_LShifted, "", inst);
    llvm::Instruction *R_Tmp1 = llvm::BinaryOperator::CreateAdd(R_Tmp0, R2_LShifted, "", inst);
    llvm::Instruction *R_Tmp2 = llvm::BinaryOperator::CreateAdd(R_Tmp1, R3_LShifted, "", inst);
    llvm::Instruction *R_Tmp3 = llvm::BinaryOperator::CreateAdd(R_Tmp2, R4_LShifted, "", inst);
    llvm::Instruction *R_Tmp4 = llvm::BinaryOperator::CreateAdd(R_Tmp3, R5_LShifted, "", inst);
    llvm::Instruction *R_Tmp5 = llvm::BinaryOperator::CreateAdd(R_Tmp4, R6_LShifted, "", inst);
    llvm::Instruction *R_Tmp6 = llvm::BinaryOperator::CreateAdd(R_Tmp5, R7_LShifted, "", inst);
    llvm::Instruction *R_Tmp7 = llvm::BinaryOperator::CreateAdd(R_Tmp6, R8_LShifted, "", inst);
    llvm::Instruction *R_Tmp8 = llvm::BinaryOperator::CreateAdd(R_Tmp7, R9_LShifted, "", inst);
    llvm::Instruction *R_Tmp9 = llvm::BinaryOperator::CreateAdd(R_Tmp8, R10_LShifted, "", inst);
    llvm::Instruction *R_Tmp10 = llvm::BinaryOperator::CreateAdd(R_Tmp9, R11_LShifted, "", inst);
    llvm::Instruction *R_Tmp11 = llvm::BinaryOperator::CreateAdd(R_Tmp10, R12_LShifted, "", inst);
    llvm::Instruction *R_Tmp12 = llvm::BinaryOperator::CreateAdd(R_Tmp11, R13_LShifted, "", inst);
    llvm::Instruction *R_Tmp13 = llvm::BinaryOperator::CreateAdd(R_Tmp12, R14_LShifted, "", inst);
    llvm::Instruction *R_Tmp14 = llvm::BinaryOperator::CreateAdd(R_Tmp13, R15_LShifted, "", inst);
    llvm::Instruction *R_Tmp15 = llvm::BinaryOperator::CreateAdd(R_Tmp14, R16_LShifted, "", inst);
    llvm::Instruction *R_Tmp16 = llvm::BinaryOperator::CreateAdd(R_Tmp15, R17_LShifted, "", inst);
    llvm::Instruction *R_Tmp17 = llvm::BinaryOperator::CreateAdd(R_Tmp16, R18_LShifted, "", inst);
    llvm::Instruction *R_Tmp18 = llvm::BinaryOperator::CreateAdd(R_Tmp17, R19_LShifted, "", inst);
    llvm::Instruction *R_Tmp19 = llvm::BinaryOperator::CreateAdd(R_Tmp18, R20_LShifted, "", inst);
    llvm::Instruction *R_Tmp20 = llvm::BinaryOperator::CreateAdd(R_Tmp19, R21_LShifted, "", inst);
    llvm::Instruction *R_Tmp21 = llvm::BinaryOperator::CreateAdd(R_Tmp20, R22_LShifted, "", inst);
    llvm::Instruction *R_Tmp22 = llvm::BinaryOperator::CreateAdd(R_Tmp21, R23_LShifted, "", inst);
    llvm::Instruction *R_Tmp23 = llvm::BinaryOperator::CreateAdd(R_Tmp22, R24_LShifted, "", inst);
    llvm::Instruction *R_Tmp24 = llvm::BinaryOperator::CreateAdd(R_Tmp23, R25_LShifted, "", inst);
    llvm::Instruction *R_Tmp25 = llvm::BinaryOperator::CreateAdd(R_Tmp24, R26_LShifted, "", inst);
    llvm::Instruction *R_Tmp26 = llvm::BinaryOperator::CreateAdd(R_Tmp25, R27_LShifted, "", inst);
    llvm::Instruction *R_Tmp27 = llvm::BinaryOperator::CreateAdd(R_Tmp26, R28_LShifted, "", inst);
    llvm::Instruction *R_Tmp28 = llvm::BinaryOperator::CreateAdd(R_Tmp27, R29_LShifted, "", inst);
    llvm::Instruction *R_Tmp29 = llvm::BinaryOperator::CreateAdd(R_Tmp28, R30_LShifted, "", inst);
    
    llvm::Instruction *FinalResult = llvm::BinaryOperator::CreateAdd(R_Tmp29, R31_LShifted, "", inst);
    llvm::ReplaceInstWithInst(inst, FinalResult);
}

struct Kryptonite : public llvm::FunctionPass
{
    static char ID;

    Kryptonite()
    : FunctionPass(ID)
    {
        srand(time(NULL));
    }

    bool runOnFunction(llvm::Function &F)
    {
        unsigned long long total_instruction_before_obf = 0, total_instruction_after_obf = 0;
        bool HeavyMode = EnableHeavyAddObfu;
        unsigned int AntiDebug = EnableAntiDbg;
        unsigned int i = 0;

        printf("Function being handled: %s (heavy mode: %s, anti debug: %u)\n", F.getName().data(), (HeavyMode) ? "yes":"no", AntiDebug);

        printf("0. Let's find instructions to obfuscate..");
        std::list<llvm::Instruction*> to_mutate;
        for(llvm::Function::iterator FI = F.begin(); FI != F.end(); FI++)
        {
            llvm::BasicBlock &BB = *FI;
            for(llvm::BasicBlock::iterator DI = BB.begin(); DI != BB.end(); DI++, total_instruction_before_obf++)
            {
                llvm::Instruction &Inst = *DI;

                if(
                    llvm::isa<llvm::BinaryOperator>(Inst) && 
                    (
                        Inst.getOpcode() == llvm::Instruction::Add || Inst.getOpcode() == llvm::Instruction::Sub ||
                        Inst.getOpcode() == llvm::Instruction::Mul || Inst.getOpcode() == llvm::Instruction::Xor
                    )
                )
                {
                    to_mutate.push_back(&Inst);
                }
            }
        }

        printf(" -- Found %u instructions to obfuscate (total instructions: %lld)\n", to_mutate.size(), total_instruction_before_obf);
        total_instruction_after_obf = 0;
        printf("1. Time to obfuscate them now..\n");
        for(std::list<llvm::Instruction*>::iterator it = to_mutate.begin(); it != to_mutate.end(); ++it)
        {
            llvm::LLVMContext &context = (*it)->getContext();
            llvm::Type *Int32Ty = llvm::IntegerType::getInt32Ty(context);

            llvm::Value *A = (*it)->getOperand(0);
            llvm::Value *B = (*it)->getOperand(1);
            if(rand_a_b(0, 19) == 3)
                continue;
            
            switch((*it)->getOpcode())
            {
                case llvm::Instruction::Add:
                {
                    if(EnableHeavyAddObfu)
                    {
                        if(rand_a_b(0, 2) == 1)
                            mutate_add_inst_heavy((llvm::BinaryOperator*)(*it));
                        else
                            mutate_add_inst_1((llvm::BinaryOperator*)(*it));
                    }
                    else
                        mutate_add_inst_1((llvm::BinaryOperator*)(*it));

                    break;
                }

                case llvm::Instruction::Sub:
                {
                    llvm::Instruction *BNot = llvm::BinaryOperator::CreateXor(B, llvm::ConstantInt::get(Int32Ty, -1), "", *it);
                    llvm::Instruction *BNeg = llvm::BinaryOperator::CreateAdd(BNot, llvm::ConstantInt::get(Int32Ty, 1), "", *it);

                    llvm::Instruction *NewAdd = llvm::BinaryOperator::CreateAdd(A, BNeg);
                    llvm::ReplaceInstWithInst(*it, NewAdd);
                    break;
                }

                case llvm::Instruction::Mul:
                {
                    llvm::BasicBlock *Body = llvm::BasicBlock::Create(context, "", &F);
                    llvm::BasicBlock *Check = llvm::BasicBlock::Create(context, "", &F);
                    llvm::BasicBlock *Origin = (*it)->getParent();

                    // counter = 0
                    // res = 0
                    llvm::Instruction *PtrCounter = new llvm::AllocaInst(Int32Ty, "", *it);
                    llvm::Instruction *InitCounter = new llvm::StoreInst(llvm::ConstantInt::get(Int32Ty, 0), PtrCounter, *it);
                    llvm::Instruction *PtrRes = new llvm::AllocaInst(Int32Ty, "", *it);
                    llvm::Instruction *InitRes = new llvm::StoreInst(llvm::ConstantInt::get(Int32Ty, 0), PtrRes, *it);

                    llvm::BasicBlock::iterator it_inst(*it);
                    llvm::BasicBlock *Next = Origin->splitBasicBlock(it_inst);
                    Origin->getTerminator()->eraseFromParent();
                    llvm::Instruction *BrCheck = llvm::BranchInst::Create(Check, Origin);

                    // if(counter < A) { Body: stuff } else { Next: the normal flow }
                    llvm::Value *Counter = new llvm::LoadInst(PtrCounter, "", Check);
                    llvm::Instruction *Cmp = new llvm::ICmpInst(*Check, llvm::CmpInst::ICMP_ULT, Counter, A);
                    llvm::Instruction *Branch = llvm::BranchInst::Create(Body, Next, Cmp, Check);

                    // add res, B
                    // counter += 1
                    // goto Check
                    llvm::Instruction *Res = new llvm::LoadInst(PtrRes, "", Body);
                    llvm::Instruction *AddB = llvm::BinaryOperator::CreateAdd(Res, B, "", Body);
                    llvm::Instruction *StoreRes = new llvm::StoreInst(AddB, PtrRes, Body);
                    llvm::Instruction *Counter_ = new llvm::LoadInst(PtrCounter, "", Body);
                    llvm::Instruction *CounterOne = llvm::BinaryOperator::CreateAdd(Counter_, llvm::ConstantInt::get(Int32Ty, 1), "", Body);
                    llvm::Instruction *StoreCounterOne = new llvm::StoreInst(CounterOne, PtrCounter, Body);
                    llvm::Instruction *BranchCheck = llvm::BranchInst::Create(Check, Body);

                    llvm::Instruction *ResFinalValue = new llvm::LoadInst(PtrRes);
                    llvm::ReplaceInstWithInst(*it, ResFinalValue);
                    break;
                }

                case llvm::Instruction::Xor:
                {
                    llvm::Instruction *NotB  = llvm::BinaryOperator::CreateXor(B, llvm::ConstantInt::get(Int32Ty, -1), "", *it);
                    llvm::Instruction *AAndNotB = llvm::BinaryOperator::CreateAnd(NotB, A, "", *it);
                    llvm::Instruction *NotA = llvm::BinaryOperator::CreateXor(A, llvm::ConstantInt::get(Int32Ty, -1), "", *it);
                    llvm::Instruction *NotAAndB = llvm::BinaryOperator::CreateAnd(NotA, B, "", *it);
                    
                    llvm::Instruction *FinalValue = llvm::BinaryOperator::CreateOr(AAndNotB, NotAAndB);
                    llvm::ReplaceInstWithInst(*it, FinalValue);
                    break;
                }
                // Add more!
            }
        }

        if(AntiDebug > 0)
        {
            unsigned long long total_instruction_after_obf = 0;
            unsigned int total_antidbg = 0;
            printf("2. Now adding some little anti-debug..");
            // 3. Looking for places where insert the Anti-Debug
            std::list<llvm::Instruction*> where_insert_antidbg;
            for(llvm::Function::iterator FI = F.begin(); FI != F.end(); FI++)
            {
                llvm::BasicBlock &BB = *FI;
                for(llvm::BasicBlock::iterator DI = BB.begin(); DI != BB.end(); DI++, total_instruction_after_obf++)
                {
                    llvm::Instruction &Inst = *DI;
                    if(rand_a_b(0, 20) == 3 && total_antidbg < AntiDebug)
                    {
                        where_insert_antidbg.push_back(&Inst);
                        total_antidbg++;
                    }
                }
            }

            printf(" -- %u anti-debugs will be placed (among %lld instructions)\n", where_insert_antidbg.size(), total_instruction_after_obf);
            i = 0;
            for(std::list<llvm::Instruction*>::iterator it = where_insert_antidbg.begin(); it != where_insert_antidbg.end(); ++it, ++i)
            {
                // Two follow fork mode
                // 1/ if follow-fork-mode == child
                //    -> Fork
                //    -> The father tries to attach to the son (because gdb will follow the child)
                //    -> If it doesn't work, debugger spotted, else we continue
                // 2/ if follow-fork-mode == parent
                //    -> Fork
                //    -> The son tries to attach to the parent (because gdb will be debugging the parent)
                //    -> If it doesn't work, debugger spotted, else we continue
                char stubX86Ptrace_child_attach_to_parent[4096] = {0}, stubX86Ptrace_parent_attach_to_son[4096] = {0};
                sprintf(stubX86Ptrace_child_attach_to_parent,
                    ".intel_syntax           \n"
                    "pushad                  \n"

                    // fork()
                    "mov eax, 0x2            \n"
                    "mov ebx, 0x0            \n"
                    "int 0x80                \n"
                    "cmp eax, 0x0            \n"
                    "jne father_%1$d         \n"

                    // if(son){
                    // getppid()
                    "mov eax, 0x40           \n"
                    "int 0x80                \n"
                    "mov ebp, eax            \n"
                    // ptrace(PTRACE_ATTACH, father, 0, 0)
                    "mov ecx, eax            \n"
                    "mov eax, 0x1a           \n"
                    "mov ebx, 0x10           \n"
                    "mov edx, 0x0            \n"
                    "mov esi, 0x0            \n"
                    "int 0x80                \n"
                    "cmp eax, 0x0            \n"
                    "jl father_debugged_%1$d \n"

                    // if(father_debugged == false){
                    // waitpid(ppid, NULL, 0) ; wait for the target to stop
                    "mov eax, 0x7            \n"
                    "mov ebx, ebp            \n"
                    "mov ecx, 0x0            \n"
                    "mov edx, 0x0            \n"
                    "int 0x80                \n"
                    // ptrace(PTRACE_DETACH, father, 0, 0)
                    "mov ecx, ebp            \n"
                    "mov eax, 0x1a           \n"
                    "mov ebx, 0x11           \n"
                    "int 0x80                \n"
                    // kill(ppid, SIGKILL)
                    // }
                    "mov eax, 0x25           \n"
                    "mov ebx, ebp            \n"
                    "mov ecx, 0x9            \n"
                    "int 0x80                \n"
                    "jmp end_%1$d            \n"

                    // if(father_debugged == true){
                    "father_debugged_%1$d:   \n"
                    //kill(father, SIGKILL)
                    "mov eax, 0x25           \n"
                    "mov ebx, ebp            \n"
                    "mov ecx, 0x9            \n"
                    "int 0x80                \n"
                    // exit()
                    // }
                    "mov eax, 1              \n"
                    "int 0x80                \n"

                    // }
                    // if(father){
                    "father_%1$d:            \n"
                    // waitpid(pid_son, NULL, NULL) ; waiting for the son is finished
                    "mov ebx, eax            \n"
                    "mov eax, 0x7            \n"
                    "mov ecx, 0x0            \n"
                    "mov edx, 0x0            \n"
                    "int 0x80                \n"
                    // }

                    "end_%1$d:               \n"
                    "popad                   \n"
                    ".att_syntax             \n", i);

                sprintf(stubX86Ptrace_parent_attach_to_son,
                    ".intel_syntax           \n"
                    "pushad                  \n"

                    // fork()
                    "mov eax, 0x2            \n"
                    "mov ebx, 0x0            \n"
                    "int 0x80                \n"
                    "cmp eax, 0x0            \n"
                    "je son_%1$d             \n"

                    // if(father){
                    "mov ebp, eax            \n"
                    // ptrace(PTRACE_ATTACH, son, 0, 0)
                    "mov ecx, eax            \n"
                    "mov eax, 0x1a           \n"
                    "mov ebx, 0x10           \n"
                    "mov edx, 0x0            \n"
                    "mov esi, 0x0            \n"
                    "int 0x80                \n"
                    "cmp eax, 0x0            \n"
                    "jl son_debugged_%1$d \n"

                    // if(son_debugged == false){
                    // waitpid(pid, NULL, 0)
                    "mov eax, 0x7            \n"
                    "mov ebx, ebp            \n"
                    "mov ecx, 0x0            \n"
                    "mov edx, 0x0            \n"
                    "int 0x80                \n"
                    // ptrace(PTRACE_DETACH, son, 0, 0)
                    "mov ecx, ebp            \n"
                    "mov eax, 0x1a           \n"
                    "mov ebx, 0x11           \n"
                    "int 0x80                \n"
                    // kill(son, SIGKILL)
                    // }
                    "mov eax, 0x25           \n"
                    "mov ebx, ebp            \n"
                    "mov ecx, 0x9            \n"
                    "int 0x80                \n"
                    "jmp end__%1$d            \n"

                    // if(son_debugged == true){
                    "son_debugged_%1$d:   \n"
                    //kill(son, SIGKILL)
                    "mov eax, 0x25           \n"
                    "mov ebx, ebp            \n"
                    "mov ecx, 0x9            \n"
                    "int 0x80                \n"
                    // kill(son, SIGKILL)
                    "mov eax, 0x25           \n"
                    "mov ebx, ebp            \n"
                    "mov ecx, 0x9            \n"
                    "int 0x80                \n"
                    // exit()
                    // }
                    "mov eax, 1              \n"
                    "int 0x80                \n"

                    // }
                    // if(son){
                    "son_%1$d:            \n"
                    // getppid()
                    "mov eax, 0x40           \n"
                    "int 0x80                \n"
                    // waitpid(ppid, NULL, NULL)
                    "mov ebx, eax            \n"
                    "mov eax, 0x7            \n"
                    "mov ecx, 0x0            \n"
                    "mov edx, 0x0            \n"
                    "int 0x80                \n"
                    // }

                    "end__%1$d:               \n"
                    "popad                   \n"
                    ".att_syntax             \n", i);

                llvm::LLVMContext &context = (*it)->getContext();
                llvm::Type *VoidTy = llvm::IntegerType::getVoidTy(context);

                llvm::FunctionType *AsmTy = llvm::FunctionType::get(VoidTy, false);
                llvm::InlineAsm *AsmParent = llvm::InlineAsm::get(AsmTy, stubX86Ptrace_parent_attach_to_son, "", true, false, llvm::InlineAsm::AD_Intel);
                llvm::CallInst::Create(AsmParent, "", *it);

                llvm::InlineAsm *AsmChild = llvm::InlineAsm::get(AsmTy, stubX86Ptrace_child_attach_to_parent, "", true, false, llvm::InlineAsm::AD_Intel);
                llvm::CallInst::Create(AsmChild, "", *it);
            }
        }

        printf("Done!\n");
        return true;
    }
};

char Kryptonite::ID = 0;
static llvm::RegisterPass<Kryptonite> X("kryptonite", "Obfuscate your code with Kryptonite!", false, false);
