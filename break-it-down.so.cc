/*
   american fuzzy lop - LLVM-mode instrumentation pass
   ---------------------------------------------------

   Written by Laszlo Szekeres <lszekeres@google.com> and
              Michal Zalewski <lcamtuf@google.com>

   LLVM integration design comes from Laszlo Szekeres. C bits copied-and-pasted
   from afl-as.c are Michal's fault.

   Copyright 2015, 2016 Google Inc. All rights reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:

     http://www.apache.org/licenses/LICENSE-2.0

   This library is plugged into LLVM when invoking clang through afl-clang-fast.
   It tells the compiler to add code roughly equivalent to the bits discussed
   in ../afl-as.h.

 */

#include "../config.h"
#include "../debug.h"

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <string>
#include <set>
#include <algorithm>

#include "llvm/ADT/Statistic.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/Support/Debug.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"

using namespace llvm;

static cl::opt<bool> EnableBreakitDown(
    "break-it-down",
    cl::init(false),
    cl::desc("Enable the Break-it Down feature")
);

static cl::opt<uint32_t> SplitGranularity(
    "split-granularity",
    cl::init(8),
    cl::desc("Choose the bit granularity of the splits")
);

namespace {

  class AFLCoverage : public ModulePass {

    public:

      static char ID;
      AFLCoverage() : ModulePass(ID) { }

      bool runOnModule(Module &M) override;

      const char *getPassName() const override {
        return "American Fuzzy Lop Instrumentation";
      }

  };

  class AFLBreakItDown : public FunctionPass {

    public:

      static char ID;
      AFLBreakItDown() : FunctionPass(ID) { }

      void findCmpToInstrument(Function &F, SmallVector<ICmpInst*, 16> &toInstrument);
      void instrumentCmp(ICmpInst *I, Value *op0, Value *op1);

      bool runOnFunction(Function &F) override;
      bool runOnFunctionCommonNumberBits(Function &F);
      bool runOnFunctionBetterButBBL(Function &F);
      bool runOnFunctionOverkill(Function &F);

      Instruction* getNextInst(Value *cmp);

      const char *getPassName() const override {
        return "American Fuzzy Lop BreakItDown bby";
      }

    private:
      LLVMContext *C;
      Module *M;
  };

  class AFLTokenCap : public BasicBlockPass {

    public:

      static char ID;
      AFLTokenCap()
      : BasicBlockPass(ID), m_TokenFile{ nullptr } {
        char *TokenFilePath = getenv("AFL_TOKEN_FILE");

        if(TokenFilePath == nullptr)
          return;

        m_TokenFile = fopen(TokenFilePath, "a");
      }

      ~AFLTokenCap() {

        if(m_TokenFile != nullptr) {

          for(const std::string &Token : m_Tokens) {

            fwrite(Token.c_str(), 1, Token.size(), m_TokenFile);
            fwrite("\n", 1, 1, m_TokenFile);
          }
          fclose(m_TokenFile);
        }
      }

      bool runOnBasicBlock(BasicBlock &B) override;

      const char *getPassName() const override {
        return "American Fuzzy Lop LibTokenCap";
      }

    private:
      FILE *m_TokenFile;
      std::set<std::string> m_Tokens;
  };
}


char AFLCoverage::ID = 0;
char AFLBreakItDown::ID = 0;
char AFLTokenCap::ID = 0;

bool AFLCoverage::runOnModule(Module &M) {

  LLVMContext &C = M.getContext();

  IntegerType *Int8Ty  = IntegerType::getInt8Ty(C);
  IntegerType *Int32Ty = IntegerType::getInt32Ty(C);

  /* Show a banner */

  char be_quiet = 0;

  if (isatty(2) && !getenv("AFL_QUIET")) {

    SAYF(cCYA "afl-llvm-pass " cBRI VERSION cRST " by <lszekeres@google.com>\n");

  } else be_quiet = 1;

  /* Decide instrumentation ratio */

  char* inst_ratio_str = getenv("AFL_INST_RATIO");
  unsigned int inst_ratio = 100;

  if (inst_ratio_str) {

    if (sscanf(inst_ratio_str, "%u", &inst_ratio) != 1 || !inst_ratio ||
        inst_ratio > 100)
      FATAL("Bad value of AFL_INST_RATIO (must be between 1 and 100)");

  }

  /* Get globals for the SHM region and the previous location. Note that
     __afl_prev_loc is thread-local. */

  GlobalVariable *AFLPrevLoc = 
      new GlobalVariable(M, Int32Ty, false, GlobalValue::ExternalLinkage, 0, "__afl_prev_loc",
                         0, GlobalVariable::GeneralDynamicTLSModel, 0, false);

  GlobalVariable *AFLMapPtr = 
      new GlobalVariable(M, PointerType::get(Int8Ty, 0), false,
                         GlobalValue::ExternalLinkage, 0, "__afl_area_ptr");

  /* Instrument all the things! */

  int inst_blocks = 0;

  for (auto &F : M)
    for (auto &BB : F) {

      BasicBlock::iterator IP = BB.getFirstInsertionPt();
      IRBuilder<> IRB(&(*IP));

      if (R(100) >= inst_ratio) continue;

      /* Make up cur_loc */

      unsigned int cur_loc = R(MAP_SIZE);

      ConstantInt *CurLoc = ConstantInt::get(Int32Ty, cur_loc);

      /* Load prev_loc */

      LoadInst *PrevLoc = IRB.CreateLoad(AFLPrevLoc);
      PrevLoc->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
      Value *PrevLocCasted = IRB.CreateZExt(PrevLoc, IRB.getInt32Ty());

      /* Load SHM pointer */

      LoadInst *MapPtr = IRB.CreateLoad(AFLMapPtr);
      MapPtr->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
      Value *MapPtrIdx =
          IRB.CreateGEP(MapPtr, IRB.CreateXor(PrevLocCasted, CurLoc));

      /* Update bitmap */

      LoadInst *Counter = IRB.CreateLoad(MapPtrIdx);
      Counter->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));
      Value *Incr = IRB.CreateAdd(Counter, ConstantInt::get(Int8Ty, 1));
      IRB.CreateStore(Incr, MapPtrIdx)
          ->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));

      /* Set prev_loc to cur_loc >> 1 */

      StoreInst *Store =
          IRB.CreateStore(ConstantInt::get(Int32Ty, cur_loc >> 1), AFLPrevLoc);
      Store->setMetadata(M.getMDKindID("nosanitize"), MDNode::get(C, None));

      inst_blocks++;

    }

  /* Say something nice. */

  if (!be_quiet) {

    if (!inst_blocks) WARNF("No instrumentation targets found.");
    else OKF("Instrumented %u locations (%s mode, ratio %u%%).",
             inst_blocks,
             getenv("AFL_HARDEN") ? "hardened" : "non-hardened",
             inst_ratio);

  }

  return true;

}

static Function *checkInterfaceFunction(Constant *FuncOrBitcast) {
  if (Function *F = dyn_cast<Function>(FuncOrBitcast))
     return F;
  FuncOrBitcast->dump();
  FATAL("Interface function redefined");
}

// Will find the `br` instruction associated with the cmp
Instruction* AFLBreakItDown::getNextInst(Value *cmp_)
{
  if(Instruction *cmp = dyn_cast<Instruction>(cmp_)) {

    BasicBlock::iterator I(cmp);
    if (++I == cmp->getParent()->end())
      return nullptr;
    return &*I;
  }

  return nullptr;
}

void AFLBreakItDown::findCmpToInstrument(Function &F, SmallVector<ICmpInst*, 16> &toInstrument)
{
  // Find instructions to instrument
  // XXX: EH?
  for(auto &B : F) {

    for(auto &I_ : B) {

      if(ICmpInst *I = dyn_cast<ICmpInst>(&I_)) {

        ConstantInt *cInt_ = nullptr;

        // Is the predicate eq? Haven't think about the other ones yet :|
        if(I->isEquality() == false)
          continue;

        // ICmpInst means 2 operands
        Value *firstOp = I->getOperand(0);
        Value *secondOp = I->getOperand(1);

        // Try to identify constant integer immediates
        if(isa<ConstantInt>(firstOp))
          cInt_ = cast<ConstantInt>(firstOp);

        if(cInt_ != nullptr && isa<ConstantInt>(secondOp))
          FATAL("fuckit - two csts?!");

        if(cInt_ == nullptr && isa<ConstantInt>(secondOp))
          cInt_ = cast<ConstantInt>(secondOp);
        
        // Have we find any icmp with a constant value?
        if(cInt_ == nullptr)
          continue;

        // Do we care about 0's & 1's ?
        uint64_t CstValue = cInt_->getZExtValue();
        if(CstValue == 0 || CstValue == 1)
          continue;

        toInstrument.push_back(I);
      }
    }
  }
}

void AFLBreakItDown::instrumentCmp(ICmpInst *I, Value *op0, Value *op1)
{
  IRBuilder<> IRB(I);

  IntegerType *Int64Ty = IRB.getInt64Ty();
  IntegerType *Int32Ty = IRB.getInt32Ty();

  Function *F = checkInterfaceFunction(M->getOrInsertFunction(
    "__afl_compare",
    Int32Ty,
    Int64Ty,
    Int64Ty,
    NULL
  ));

  Instruction *NumberOfCommonBits = IRB.CreateCall(
    F,
    { IRB.CreateZExt(op0, Int64Ty), IRB.CreateZExt(op1, Int64Ty) },
    "NumberOfCommonBits"
  );

  for(Instruction *Inst : { NumberOfCommonBits }) {

    // Avoid any instrumentation added on those instruction by potential other sanitizers
    Inst->setMetadata(
      M->getMDKindID("nosanitize"),
      MDNode::get(*C, None)
    );
  }
}

bool AFLBreakItDown::runOnFunction(Function &F) {
  C = &(F.getContext());
  M = F.getParent();

  bool enabled = EnableBreakitDown;

  if(enabled == false)
    return false;

  const char *fname {
    F.hasName() ? F.getName().data() : "unknown"
  };


  SmallVector<ICmpInst*, 16> toInstrument;
  findCmpToInstrument(F, toInstrument);

  if(toInstrument.size() == 0)
    return false;

  OKF("Whadup in AFLBreakItDown::runOnFunction('%s')", fname);

  // Instrumentation time
  for(ICmpInst *I : toInstrument) {

    IRBuilder<> IRB(I);

    OKF("Instrumenting:");
    I->dump();

    ConstantInt *Cst = nullptr;
    Value *FirstOp = I->getOperand(0);
    Value *SecondOp = I->getOperand(1);

    // Find a constant integer operand
    if(isa<ConstantInt>(FirstOp))
      Cst = dyn_cast<ConstantInt>(FirstOp);

    if(Cst == nullptr && isa<ConstantInt>(SecondOp))
      Cst = dyn_cast<ConstantInt>(SecondOp);

    Value *Other = (Cst == FirstOp) ? SecondOp : FirstOp;
    instrumentCmp(I, Cst, Other);
  }

  OKF("Found %zu instructions to instrument", toInstrument.size());
  // F.dump();

  return true;
}

bool AFLBreakItDown::runOnFunctionCommonNumberBits(Function &F) {
  // mongo is teh best!
  bool enabled = EnableBreakitDown;

  if(enabled == false)
    return false;

  Module *M = F.getParent();

  LLVMContext &C = F.getContext();

  const char *fname {
    F.hasName() ? F.getName().data() : "unknown"
  };

  OKF("Whadup in AFLBreakItDown::runOnFunction('%s')", fname);

  SmallVector<ICmpInst*, 16> toInstrument;
  findCmpToInstrument(F, toInstrument);

  if(toInstrument.size() == 0)
    return false;

  // Instrumentation time
  for(ICmpInst *I : toInstrument) {

    OKF("Instrumenting:");
    I->dump();

    Value *Cst = nullptr;
    Value *FirstOp = I->getOperand(0);
    Value *SecondOp = I->getOperand(1);

    // Find a constant integer operand
    if(isa<ConstantInt>(FirstOp))
      Cst = FirstOp;

    if(Cst == nullptr && isa<ConstantInt>(SecondOp))
      Cst = SecondOp;

    Value *Other = (Cst == FirstOp) ? SecondOp : FirstOp;
    IRBuilder<> IRB(I);

    // Compute popcount(~(arg0^arg1)) to know the number of bits in common

    // XXX: We don't need to know the number of bits in common, the number of uncommon bits works too?
    // XXX: Evaluate both
    Value *ArgsXoredNot = IRB.CreateNot(
      IRB.CreateXor(
        Cst,
        Other,
        "ArgsXored"
      ),
      "ArgsXoredNot"
    );

    Instruction *NumberOfCommonBits = IRB.CreateCall(
      Intrinsic::getDeclaration(
        M, Intrinsic::ctpop,
        { ArgsXoredNot->getType() }
      ),
      { ArgsXoredNot },
      "NumberOfCommonBits"
    );

    // Artificially update __afl_prev_loc for faking coverage differences
    // according to the value of the Counter
    IntegerType *AFLPrevLocType = IntegerType::getInt32Ty(C);
    IntegerType *AFLMapPtrType  = IntegerType::getInt8Ty(C);

    GlobalVariable *AFLPrevLoc = dyn_cast<GlobalVariable>(
      M->getNamedValue("__afl_prev_loc")
    );

    GlobalVariable *AFLMapPtr = dyn_cast<GlobalVariable>(
      M->getNamedValue("__afl_area_ptr")
    );

    Instruction *AFLPrevLocLoad = IRB.CreateLoad(AFLPrevLoc);
    Value *CounterLoadAdjusted = 
      // If NumberOfCommonBits is > 32 bits long, we need to trunc it..
      (NumberOfCommonBits->getType()->getIntegerBitWidth() > AFLPrevLocType->getIntegerBitWidth()) ?
      IRB.CreateTrunc(NumberOfCommonBits, AFLPrevLocType) :
      // ..else it's smaller and we need to zero extend it to match
      IRB.CreateZExt(NumberOfCommonBits, AFLPrevLocType);

    Value *AFLPrevLocCounterXor = IRB.CreateXor(AFLPrevLocLoad, CounterLoadAdjusted);
    // XXX: Study with phi node / if(if(if()))

    Instruction *MapPtr = IRB.CreateLoad(AFLMapPtr);
    Value *MapPtrIdx =
        IRB.CreateGEP(MapPtr, AFLPrevLocCounterXor);

    // Force update bitmap
    Instruction *Counter = IRB.CreateLoad(MapPtrIdx);
    Instruction *Store = IRB.CreateStore(
      IRB.CreateAdd(
        Counter,
        ConstantInt::get(AFLMapPtrType, 1)
      ),
      MapPtrIdx
    );

    for(Instruction *Inst : { NumberOfCommonBits, AFLPrevLocLoad, /*AFLPrevLocStore,*/ MapPtr,
      Counter, Store }) {

      // Avoid any instrumentation added on those instruction by potential other sanitizers
      Inst->setMetadata(
        M->getMDKindID("nosanitize"),
        MDNode::get(C, None)
      );
    }
  }

  OKF("Here is function fully instrumented");
  F.dump();

  return true;
}

bool AFLBreakItDown::runOnFunctionBetterButBBL(Function &F) {
  // mongo is teh best!
  uint32_t Granularity = SplitGranularity;
  bool enabled = EnableBreakitDown;

  if(enabled == false)
    return false;

  LLVMContext &C = F.getContext();

  const char *fname {
    F.hasName() ? F.getName().data() : "unknown"
  };

  OKF("Whadup in AFLBreakItDown::runOnFunction('%s')", fname);

  SmallVector<ICmpInst*, 16> toInstrument;
  findCmpToInstrument(F, toInstrument);
  
  if(toInstrument.size() == 0)
    return false;

  OKF("Here is the function before instrumentation");
  F.dump();

  // Instrumentation time
  for(ICmpInst *I : toInstrument) {

    BasicBlock *ParentBBL = I->getParent();
    Function *ParentFunction = ParentBBL->getParent();

    OKF("Instrumenting:");
    I->dump();

    Value *Cst = nullptr;
    Value *FirstOp = I->getOperand(0);
    Value *SecondOp = I->getOperand(1);

    // Find a constant integer operand
    if(isa<ConstantInt>(FirstOp))
      Cst = FirstOp;

    if(Cst == nullptr && isa<ConstantInt>(SecondOp))
      Cst = SecondOp;

    Value *Other = (Cst == FirstOp) ? SecondOp : FirstOp;

    ConstantInt *CstInt = reinterpret_cast<ConstantInt*>(Cst);
    size_t BitLength = CstInt->getBitWidth();

    // Retrieve the conditional branch instruction to extract
    // the two bbls: true/bad that we are going to reuse
    if(isa<BranchInst>(getNextInst(I)) == false)
      FATAL("hmm weird @ condBR");

    BranchInst *OriginalCondBr = dyn_cast<BranchInst>(getNextInst(I));

    BasicBlock *TrueBBL = OriginalCondBr->getSuccessor(0);
    BasicBlock *FalseBBL = OriginalCondBr->getSuccessor(1);

    size_t NumberComparaisons = BitLength / Granularity;
    OKF("Breaking it up in %zu comparaisons (%lx)", NumberComparaisons, CstInt->getZExtValue());

    IRBuilder<> IRB(I);

    // Introducing a variable that will keep track of the comparaisons that worked
    Type *CstIntType = CstInt->getType();

    // Type Counter;
    Value *Counter = IRB.CreateAlloca(
      CstIntType,
      nullptr,
      "Counter"
    );
    // Counter = 0;
    IRB.CreateStore(
      ConstantInt::get(
        CstIntType,
        0
      ),
      Counter
    );

    uint64_t CurrentMask = (1ULL << Granularity) - 1;

    // Compute all the broken down constant values
    // Compute all the broken down other values
    for(size_t i = 0; i < NumberComparaisons; ++i) {

        Value *Mask = ConstantInt::get(
          CstIntType,
          CurrentMask
        );

        Value *Shift = ConstantInt::get(
          CstIntType,
          uint64_t(i * Granularity)
        );

        // (CstInt & mask) >> X
        Value *CstIntAndedShifted = IRB.CreateLShr(
            IRB.CreateAnd(
              CstInt,
              Mask
          ),
          Shift,
          "CstIntAndedShifted"
        );

        // (Other & mask) >> X
        Value *OtherAndedShifted = IRB.CreateLShr(
          IRB.CreateAnd(
            Other,
            Mask
          ),
          Shift,
          "OtherAndedShifted"
        );

        Value *Cmp = IRB.CreateICmpEQ(
            CstIntAndedShifted,
            OtherAndedShifted,
            "cmpCstIntOther"
          );

        // We always introduce a new bbl where we will increment the counter
        BasicBlock *IncCounter = BasicBlock::Create(
          C,
          "IncCounter",
          ParentFunction
        );

        // We always introduce another bbl to keep going
        BasicBlock *NextBBL = BasicBlock::Create(
          C,
          ((i + 1) == NumberComparaisons) ? "FinalComparaisonBBL" : "NextBBL",
          ParentFunction
        );

        // if(((CstInt & mask) >> X) == ((Other & mask) >> X))
        //   goto IncCounter;
        // else
        //   goto NextBBL;
        IRB.CreateCondBr(
          Cmp,
          IncCounter,
          NextBBL
        );

        // Populate the BBL with the counter incrementation
        IRB.SetInsertPoint(IncCounter);

        // InCounter:
        // Counter = Counter + 1;
        IRB.CreateStore(
          IRB.CreateAdd(
            IRB.CreateLoad(Counter),
            ConstantInt::get(
              CstIntType,
              1 << i
            )
          ),
          Counter
        );

        // goto NextBBL;
        IRB.CreateBr(NextBBL);

        // Prepare to insert instruction in the NextBBL here for next time
        IRB.SetInsertPoint(NextBBL);

        CurrentMask <<= Granularity;
    }

    // Artificially update __afl_prev_loc for faking coverage differences
    // according to the value of the Counter
    IntegerType *Int32Ty = IntegerType::getInt32Ty(C);
    Module *ParentModule = ParentFunction->getParent();
    GlobalVariable *AFLPrevLoc = dyn_cast_or_null<GlobalVariable>(
      ParentModule->getNamedValue("__afl_prev_loc")
    );

    if(!AFLPrevLoc) {

      OKF("Creating an __afl_prev_loc instance");
      AFLPrevLoc = new GlobalVariable(
          *ParentModule, Int32Ty, false, GlobalValue::ExternalLinkage, 0, "__afl_prev_loc",
          0, GlobalVariable::GeneralDynamicTLSModel, 0, false
      );
      AFLPrevLoc->dump();
    }

    Instruction *AFLPrevLocLoad = IRB.CreateLoad(AFLPrevLoc);
    Instruction *CounterLoad = IRB.CreateLoad(Counter);
    Instruction *CounterLoadTrunc = reinterpret_cast<Instruction*>(IRB.CreateTrunc(CounterLoad, Int32Ty));
    Instruction *AFLPrevLocCounterXor = reinterpret_cast<Instruction*>(IRB.CreateXor(AFLPrevLocLoad, CounterLoadTrunc));
    Instruction *AFLPrevLocStore = IRB.CreateStore(AFLPrevLocCounterXor, AFLPrevLoc);

    for(Instruction *Inst : { AFLPrevLocLoad, CounterLoad, CounterLoadTrunc, AFLPrevLocCounterXor, AFLPrevLocStore }) {

      // Avoid any instrumentation added on those instruction by a potential other sanitizer
      Inst->setMetadata(
        ParentModule->getMDKindID("nosanitize"),
        MDNode::get(C, None)
      );
    }

    // FinalComparaison:
    // if(Counter == NumberComparaisons)
    //   goto TrueBBL;
    // else
    //   goto FalseBBL;
    IRB.CreateCondBr(
      IRB.CreateICmpEQ(
        IRB.CreateLoad(Counter),
        ConstantInt::get(
          CstIntType,
          (1 << NumberComparaisons) - 1
        )
      ),
      TrueBBL,
      FalseBBL
    );

    OKF("Remove the icmp/condbr insts");

    // Remove the original compare instruction
    I->eraseFromParent();
    // Remove the original conditional branching instruction
    OriginalCondBr->eraseFromParent();
  }

  // OKF("Here is function fully instrumented");
  F.dump();

  return true;
}

// if(x == y)
//    counter += 1

// if(x2 == y2)
//    counter += 1
bool AFLBreakItDown::runOnFunctionOverkill(Function &F) {
  // mongo is teh best!
  uint32_t Granularity = SplitGranularity;
  bool enabled = EnableBreakitDown;

  if(enabled == false)
    return false;

  LLVMContext &C = F.getContext();

  const char *fname {
    F.hasName() ? F.getName().data() : "unknown"
  };

  OKF("Whadup in AFLBreakItDown::runOnFunction('%s')", fname);

  SmallVector<ICmpInst*, 16> toInstrument;
  findCmpToInstrument(F, toInstrument);

  if(toInstrument.size() == 0)
    return false;

  OKF("Here is the function before instrumentation");
  F.dump();

  // Instrumentation time
  for(ICmpInst *I : toInstrument) {

    BasicBlock *ParentBBL = I->getParent();
    Function *ParentFunction = ParentBBL->getParent();

    OKF("Instrumenting:");
    I->dump();

    Value *Cst = nullptr;
    Value *FirstOp = I->getOperand(0);
    Value *SecondOp = I->getOperand(1);

    // Find a constant integer operand
    if(isa<ConstantInt>(FirstOp))
      Cst = FirstOp;

    if(Cst == nullptr && isa<ConstantInt>(SecondOp))
      Cst = SecondOp;

    Value *Other = (Cst == FirstOp) ? SecondOp : FirstOp;

    ConstantInt *CstInt = reinterpret_cast<ConstantInt*>(Cst);
    size_t BitLength = CstInt->getBitWidth();

    // Retrieve the conditional branch instruction to extract
    // the two bbls: true/bad that we are going to reuse
    if(isa<BranchInst>(getNextInst(I)) == false)
      FATAL("hmm weird @ condBR");

    BranchInst *OriginalCondBr = dyn_cast<BranchInst>(getNextInst(I));

    BasicBlock *TrueBBL = OriginalCondBr->getSuccessor(0);
    BasicBlock *FalseBBL = OriginalCondBr->getSuccessor(1);

    size_t NumberComparaisons = BitLength / Granularity;
    OKF("Breaking it up in %zu comparaisons (%lx)", NumberComparaisons, CstInt->getZExtValue());

    IRBuilder<> IRB(I);

    // Introducing a variable that will keep track of the comparaisons that worked
    Type *CstIntType = CstInt->getType();

    // Type Counter;
    Value *Counter = IRB.CreateAlloca(
      CstIntType,
      nullptr,
      "Counter"
    );
    // Counter = 0;
    IRB.CreateStore(
      ConstantInt::get(
        CstIntType,
        0
      ),
      Counter
    );

    uint64_t CurrentMask = (1ULL << Granularity) - 1;
    std::vector<Value*> ConstantValues { };
    std::vector<Value*> OtherValues { };
    size_t WinCounterValue = 0;

    // Compute all the broken down constant values
    // Compute all the broken down other values
    for(size_t i = 0; i < NumberComparaisons; ++i) {

        Value *Mask = ConstantInt::get(
          CstIntType,
          CurrentMask
        );

        Value *Shift = ConstantInt::get(
          CstIntType,
          uint64_t(i * Granularity)
        );

        // (CstInt & mask) >> X
        Value *CstIntAndedShifted = IRB.CreateLShr(
            IRB.CreateAnd(
              CstInt,
              Mask
          ),
          Shift,
          "CstIntAndedShifted"
        );

        // (Other & mask) >> X
        Value *OtherAndedShifted = IRB.CreateLShr(
          IRB.CreateAnd(
            Other,
            Mask
          ),
          Shift,
          "OtherAndedShifted"
        );

        ConstantValues.emplace_back(CstIntAndedShifted);
        OtherValues.emplace_back(OtherAndedShifted);
        CurrentMask <<= Granularity;
    }

    // Now prepare the instrumentation
    for(size_t i = 0; i < (NumberComparaisons - 1); ++i) {

        // Lord forgive me:
        // http://stackoverflow.com/questions/9430568/generating-combinations-in-c
        {
          int n = NumberComparaisons;
          int r = i + 1;
          OKF("n=%d, r=%d", n, r);
          std::vector<bool> v(n);

          for (int j = 0; j < n; ++j) {
              v[j] = (j >= (n - r));
          }

          do {
              std::vector<size_t> seq;
              for (size_t j = 0; j < size_t(n); ++j) {
                  if (v[j]) {
                      seq.push_back(j);
                  }
              }

              WinCounterValue++;

              // Generate the accumulated comparaison
              OKF("Size SEQ: %zu", seq.size());
              Value *CmpAccumulated = nullptr;
              for(size_t idx : seq) {

                Value *CstChunk = ConstantValues.at(idx);
                Value *OtherChunk = OtherValues.at(idx);

                Value *Cmp = IRB.CreateICmpEQ(
                    CstChunk,
                    OtherChunk,
                    "cmpCstIntOther"
                  );

                Value *CmpZExt = IRB.CreateZExt(Cmp, CstIntType);

                if(CmpAccumulated == nullptr) {

                    CmpAccumulated = CmpZExt;
                } else {

                  CmpAccumulated = IRB.CreateAdd(CmpZExt, CmpAccumulated);
                }

              }

              CmpAccumulated = IRB.CreateICmpEQ(
                CmpAccumulated,
                ConstantInt::get(
                    CmpAccumulated->getType(),
                    seq.size()
                  )
              );

              OKF("%zu - CmpAccumulated dump:\n", i);
              CmpAccumulated->dump();

              // We always introduce a new bbl where we will increment the counter
              BasicBlock *IncCounter = BasicBlock::Create(
                C,
                "IncCounter",
                ParentFunction
              );

              // We always introduce another bbl to keep going
              BasicBlock *NextBBL = BasicBlock::Create(
                C,
                ((i + 1) == NumberComparaisons) ? "FinalComparaisonBBL" : "NextBBL",
                ParentFunction
              );

              // if(((CstInt & mask) >> X) == ((Other & mask) >> X))
              //   goto IncCounter;
              // else
              //   goto NextBBL;
              IRB.CreateCondBr(
                CmpAccumulated,
                IncCounter,
                NextBBL
              );

              // Populate the BBL with the counter incrementation
              IRB.SetInsertPoint(IncCounter);

              // InCounter:
              // Counter = Counter + 1;
              IRB.CreateStore(
                IRB.CreateAdd(
                  IRB.CreateLoad(Counter),
                  ConstantInt::get(
                    CstIntType,
                    1
                  )
                ),
                Counter
              );

              // goto NextBBL;
              IRB.CreateBr(NextBBL);

              // Prepare to insert instruction in the NextBBL here for next time
              IRB.SetInsertPoint(NextBBL);


          } while (std::next_permutation(v.begin(), v.end()));
        }

      }

    // FinalComparaison:
    // if(Counter == NumberComparaisons)
    //   goto TrueBBL;
    // else
    //   goto FalseBBL;
    IRB.CreateCondBr(
      IRB.CreateICmpEQ(
        IRB.CreateLoad(Counter),
        ConstantInt::get(
          CstIntType,
          WinCounterValue
        )
      ),
      TrueBBL,
      FalseBBL
    );

    OKF("Remove the icmp/condbr insts (%zu)", WinCounterValue);

    // Remove the original compare instruction
    I->eraseFromParent();
    // Remove the original conditional branching instruction
    OriginalCondBr->eraseFromParent();
  }

  OKF("Here is function fully instrumented");
  F.dump();

  return true;
}

bool filter_ascii(uint8_t *p, size_t size) {
  for(size_t i = 0; i < size; ++i)
    if(isalnum(p[i]) == false)
      return false;
  return true;
}

bool AFLTokenCap::runOnBasicBlock(BasicBlock &B) {

  static const struct {
    const char *Name;
    bool IsText;
  } functions[] = {
    { "strcmp", true }, { "strncmp", true },
    { "strcasecmp", true }, { "strncasecmp", true },
    { "memcmp", false },
  };

  if(m_TokenFile == nullptr)
    return false;

  Function *F = B.getParent();
  const char *FunctionName {
    F->hasName() ? F->getName().data() : "unknown"
  };

  for(auto &I_ : B) {

    if(ICmpInst *I = dyn_cast<ICmpInst>(&I_)) {

        ConstantInt *cInt = nullptr;
        if(I->isEquality() == false)
          continue;

        Value *firstOp = I->getOperand(0);
        Value *secondOp = I->getOperand(1);

        // Try to identify constant integer immediates
        if(isa<ConstantInt>(firstOp))
          cInt = cast<ConstantInt>(firstOp);

        if(cInt != nullptr && isa<ConstantInt>(secondOp))
          FATAL("fuckit - two csts?!");

        if(cInt == nullptr && isa<ConstantInt>(secondOp))
          cInt = cast<ConstantInt>(secondOp);
        
        // Have we find any icmp with a constant value?
        if(cInt == nullptr)
          continue;

        // Do we care about 0's & 1's ?
        uint64_t CstValue = cInt->getZExtValue();
        if(CstValue == 0 || CstValue == 1)
          continue;

        std::string cst("\"");
        uint8_t *PointerData = (uint8_t*)&CstValue;
        size_t TotalSize = cInt->getBitWidth() / 8;

        if(filter_ascii(PointerData, TotalSize) == false)
          continue;

        for(size_t i = TotalSize; i >= 1; --i)
          cst += PointerData[i - 1];

        cst += '"';
        if(m_Tokens.find(cst) != m_Tokens.end())
          continue;

        OKF("Found an ascii constant %s in %s (TotalSize=%zu)", cst.c_str(), FunctionName, TotalSize);
        m_Tokens.insert(cst);
    }
    else if(CallInst *I = dyn_cast<CallInst>(&I_)) {

        const char *fname = nullptr;

        if(I->getCalledFunction() != nullptr && I->getCalledFunction()->hasName())
          fname = I->getCalledFunction()->getName().data();

        if(fname == nullptr)
          continue;

        // Walk the functions
        for(size_t i = 0; i < sizeof(functions) / sizeof(functions[0]); ++i) {

          if(strstr(fname, functions[i].Name) == 0)
            continue;

          // Walk the operands
          for(size_t j = 0; j < I->getNumArgOperands(); ++j) {

            Value *ArgValue = I->getArgOperand(j);
            if(isa<ConstantExpr>(ArgValue) == false)
              continue;

            ConstantExpr *Arg = reinterpret_cast<ConstantExpr*>(ArgValue);
            Value *FirstOp = Arg->getOperand(0);
            if(isa<GlobalVariable>(FirstOp) == false)
              continue;

            GlobalVariable *GV = reinterpret_cast<GlobalVariable*>(FirstOp);
            Constant *Initializer = GV->getInitializer();
            if(isa<ConstantDataArray>(Initializer) == false)
              continue;

            ConstantDataArray *AR = reinterpret_cast<ConstantDataArray*>(Initializer);
            size_t SizeOneValue = AR->getElementByteSize();
            size_t NumberElements = AR->getNumElements();
            uint64_t TotalSize = SizeOneValue * NumberElements;
            // XXX: Get the size parameter instead
            StringRef ArgData = AR->getRawDataValues();
            std::string cst("\"");
            for(uint8_t c : ArgData) {

              switch (c) {
                case 0 ... 31:
                case 127 ... 255:
                case '\"':
                case '\\': {

                  if (c == 0 && functions[i].IsText)
                    break;

                  char buf[5] { };
                  sprintf(buf, "\\x%02x", c);
                  cst.append(buf);
                  break;
                }

                default:

                  cst += c;
              }
            }

            cst += '"';
            OKF("Call to %s with constant %s found in %s (TotalSize=%zu)", fname, cst.c_str(), FunctionName, TotalSize);
            m_Tokens.insert(cst);
          }
        }
    }
  }
  return false;
}

static void registerAFLPass(const PassManagerBuilder &,
                            legacy::PassManagerBase &PM) {

  PM.add(new AFLCoverage());

}

static void registerAFLBreakItDownPass(const PassManagerBuilder &,
                            legacy::PassManagerBase &PM) {

  PM.add(new AFLBreakItDown());

}

static void registerAFLTokenCapPass(const PassManagerBuilder &,
                            legacy::PassManagerBase &PM) {

  PM.add(new AFLTokenCap());

}

static RegisterStandardPasses RegisterAFLPass(
    PassManagerBuilder::EP_OptimizerLast, registerAFLPass);

static RegisterStandardPasses RegisterAFLTokenCapPass(
    PassManagerBuilder::EP_EarlyAsPossible, registerAFLTokenCapPass);

static RegisterStandardPasses RegisterAFLPass0(
    PassManagerBuilder::EP_EnabledOnOptLevel0, registerAFLPass);

static RegisterStandardPasses RegisterAFLPassBreakItDown(
    PassManagerBuilder::EP_OptimizerLast, registerAFLBreakItDownPass);

/*
overclok@wildout:~/workz/afl-2.31b/llvm_mode$ cat test.cc
#include <stdio.h>
#include <stdint.h>
int main()
{
        unsigned char buffer[12] = {0};
        if(fread(buffer, 1, 12, stdin) == 12) {
                if(*(uint32_t*)(buffer) == 'zlol' && *(uint64_t*)(buffer + 4) == 0x4e616d3464756f79ULL) {
                        printf("win!\n");
                        *(uint32_t*)0xDEAD = 0xDEAD;
                }else {
                        printf("bad!\n");
                }
        }
        return 0;
}
overclok@wildout:~/workz/afl-2.31b/llvm_mode$ cat compile.sh
make
AFL_TOKEN_FILE=/tmp/foo.txt ../afl-clang-fast++ test.cc -o test.instru.normal
../afl-clang-fast++ test.cc -o test.instru.normal
../afl-clang-fast++ -mllvm -break-it-down test.cc -march=native -o test.instru.optimized
#../afl-clang-fast++ -mllvm -break-it-down -mllvm -split-granularity=16 test.cc -o test.instru.para.16
#../afl-clang-fast++ -mllvm -break-it-down -mllvm -split-granularity=8 test.cc -o test.instru.para.8
#../afl-clang-fast++ -mllvm -break-it-down -mllvm -split-granularity=4 test.cc -o test.instru.para.4
#../afl-clang-fast++ -mllvm -break-it-down -mllvm -split-granularity=1 test.cc -o test.instru.para.1

CC=~/workz/afl-2.31b/afl-clang-fast CXX=~/workz/afl-2.31b/afl-clang-fast++ ./configure
AFL_TOKEN_FILE=/tmp/test.txt make -j2
*/