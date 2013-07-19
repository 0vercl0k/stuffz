/*
    llvm-c-frontend-playing-with-ir.c - Trying out the LLVM-C API to emit IR code.
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
    clang++ -x c llvm-c-frontend-playing-with-ir.c `llvm-config --cxxflags --ldflags --libs` -o ./llvm-c-frontend-playing-with-ir
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include <llvm-c/Core.h>

LLVMValueRef create_strlen_function(LLVMModuleRef *Module)
{
    LLVMValueRef Zero8 = LLVMConstInt(LLVMInt8Type(), 0, false);
    LLVMValueRef Zero32 = LLVMConstInt(LLVMInt32Type(), 0, false);
    LLVMValueRef One32 = LLVMConstInt(LLVMInt32Type(), 1, false);

    LLVMBuilderRef Builder = LLVMCreateBuilder();

    /// 1. int strlen(char *);
    LLVMTypeRef StrlenArgsTyList[] = { LLVMPointerType(LLVMInt8Type(), 0) };
    LLVMTypeRef StrlenTy = LLVMFunctionType(
        LLVMInt32Type(),
        StrlenArgsTyList,
        1,
        false
    );

    LLVMValueRef StrlenFunction = LLVMAddFunction(*Module, "strlen", StrlenTy);
    LLVMValueRef s = LLVMGetParam(StrlenFunction, 0);
    LLVMSetValueName(s, "s");

    LLVMBasicBlockRef InitBasicBlock = LLVMAppendBasicBlock(StrlenFunction, "init");
    LLVMBasicBlockRef CheckBasicBlock = LLVMAppendBasicBlock(StrlenFunction, "check");
    LLVMBasicBlockRef BodyBasicBlock = LLVMAppendBasicBlock(StrlenFunction, "body");
    LLVMBasicBlockRef EndBasicBlock = LLVMAppendBasicBlock(StrlenFunction, "end");

    LLVMPositionBuilderAtEnd(Builder, InitBasicBlock);
    /// 2. int i = 0;
    LLVMValueRef i = LLVMBuildAlloca(Builder, LLVMInt32Type(), "i");
    LLVMBuildStore(Builder, Zero32, i);

    LLVMBuildBr(Builder, CheckBasicBlock);

    /// 3. check:
    LLVMPositionBuilderAtEnd(Builder, CheckBasicBlock);
    /// 4. if(s[i] == 0)
    LLVMValueRef id_if[] = { LLVMBuildLoad(Builder, i, "") };
    LLVMValueRef If = LLVMBuildICmp(
        Builder,
        LLVMIntNE,
        Zero8,
        LLVMBuildLoad(
            Builder,
            LLVMBuildGEP(Builder, s, id_if, 1, ""),
            ""
        ),
        ""
    );

    /// 5.     goto end;
    LLVMBuildCondBr(Builder, If, BodyBasicBlock, EndBasicBlock);

    /// 6. body:
    LLVMPositionBuilderAtEnd(Builder, BodyBasicBlock);
    /// 7. i += 1;
    LLVMValueRef id_i[] = { Zero32 };
    LLVMBuildStore(
        Builder,
        LLVMBuildAdd(
            Builder,
            LLVMBuildLoad(
                Builder,
                i,
                ""
            ),
            One32,
            ""
        ),
        i
    );

    /// 8. goto check;
    LLVMBuildBr(Builder, CheckBasicBlock);

    /// 9. end:
    LLVMPositionBuilderAtEnd(Builder, EndBasicBlock);
    /// 10. return i;
    LLVMBuildRet(Builder, LLVMBuildLoad(Builder, i, ""));

    return StrlenFunction;
}

void generate_ir_function()
{
    LLVMValueRef Zero = LLVMConstInt(LLVMInt32Type(), 0, false);

    // An instruction builder represents a point within a basic block and is
    // the exclusive means of building instructions using the C interface.
    LLVMBuilderRef Builder = LLVMCreateBuilder();

    // Modules represent the top-level structure in a LLVM program. An LLVM
    // module is effectively a translation unit or a collection of
    // translation units merged together.
    LLVMModuleRef Module = LLVMModuleCreateWithName("module-c");

    /// Define strlen_llvm
    LLVMValueRef StrlenFunction = create_strlen_function(&Module);

    /// extern int printf(char*, ...)
    LLVMTypeRef PrintfArgsTyList[] = { LLVMPointerType(LLVMInt8Type(), 0) };
    LLVMTypeRef PrintfTy = LLVMFunctionType(
        LLVMInt32Type(),
        PrintfArgsTyList,
        0,
        true // IsVarArg
    );

    LLVMValueRef PrintfFunction = LLVMAddFunction(Module, "printf", PrintfTy);

    /// 1. void main(void)
    LLVMTypeRef MainFunctionTy = LLVMFunctionType(
        LLVMVoidType(),
        NULL,
        0,
        false
    );

    LLVMValueRef MainFunction = LLVMAddFunction(Module, "main", MainFunctionTy);
    // A basic block represents a single entry single exit section of code.
    // Basic blocks contain a list of instructions which form the body of
    // the block.
    // Basic blocks belong to functions. They have the type of label.
    LLVMBasicBlockRef BasicBlock = LLVMAppendBasicBlock(MainFunction, "entrypoint");
    LLVMPositionBuilderAtEnd(Builder, BasicBlock);

    /// 2. char *format = "Hello, %s.\n", *world = "World", *format2 = "len(World) = %d\n";
    LLVMValueRef Format = LLVMBuildGlobalStringPtr(
        Builder,
        "Hello, %s.\n",
        "format"
    ), World = LLVMBuildGlobalStringPtr(
        Builder,
        "World",
        "world"
    ), Format2 = LLVMBuildGlobalStringPtr(
        Builder,
        "len(World) = %d\n",
        "format2"
    );

    /// 3. printf("Hello, %s!", world);
    LLVMValueRef PrintfArgs[] = { Format, World };

    LLVMBuildCall(
        Builder,
        PrintfFunction,
        PrintfArgs,
        2,
        "printf"
    );

    /// 4. printf("len(World) = %d\n", strlen_llvm(hello));
    LLVMValueRef StrlenArgs[] = { World };

    PrintfArgs[0] = Format2;
    PrintfArgs[1] = LLVMBuildCall(
        Builder,
        StrlenFunction,
        StrlenArgs,
        1,
        ""
    );

    LLVMBuildCall(
        Builder,
        PrintfFunction,
        PrintfArgs,
        2,
        ""
    );

    /// 5. return;
    LLVMBuildRetVoid(Builder);

    /// Dump the IR we emited :)
    LLVMDumpModule(Module);

    /// Be clean!
    LLVMDisposeModule(Module);
}

int main()
{
    generate_ir_function();
    return 0;
}

/*
overclok@theokoles:~/dev$ ./llvm-c-playing-with-ir
    ; ModuleID = 'module-c'

    @format = private unnamed_addr constant [12 x i8] c"Hello, %s.\0A\00"
    @world = private unnamed_addr constant [6 x i8] c"World\00"
    @format2 = private unnamed_addr constant [17 x i8] c"len(World) = %d\0A\00"

    define i32 @strlen(i8* %s) {
    init:
      %i = alloca i32
      store i32 0, i32* %i
      br label %check

    check:                                            ; preds = %body, %init
      %0 = load i32* %i
      %1 = getelementptr i8* %s, i32 %0
      %2 = load i8* %1
      %3 = icmp ne i8 0, %2
      br i1 %3, label %body, label %end

    body:                                             ; preds = %check
      %4 = load i32* %i
      %5 = add i32 %4, 1
      store i32 %5, i32* %i
      br label %check

    end:                                              ; preds = %check
      %6 = load i32* %i
      ret i32 %6
    }

    declare i32 @printf(...)

    define void @main() {
    entrypoint:
      %printf = call i32 (...)* @printf(i8* getelementptr inbounds ([12 x i8]* @format, i32 0, i32 0), i8* getelementptr inbounds ([6 x i8]* @world, i32 0, i32 0))
      %0 = call i32 @strlen(i8* getelementptr inbounds ([6 x i8]* @world, i32 0, i32 0))
      %1 = call i32 (...)* @printf(i8* getelementptr inbounds ([17 x i8]* @format2, i32 0, i32 0), i32 %0)
      ret void
    }

overclok@theokoles:~/dev$ ./llvm-c-playing-with-ir 2>&1 | lli
    Hello, World.
    len(World) = 5

*/