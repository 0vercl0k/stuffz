/*
   american fuzzy lop - LLVM tokencap pass
   ---------------------------------------------------

   Written by Axel '0vercl0k' Souchet <0vercl0k@tuxfamily.org>

   This attempts to find important "tokens" in a library - as
   libtokencap would do, but at compile-time thanks to LLVM.

*/

#include "../config.h"
#include "../debug.h"

#include <cstdio>
#include <cstdlib>
#include <unistd.h>

#include <string>
#include <set>
#include <array>

#include "llvm/ADT/Statistic.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"

using namespace llvm;

namespace {

class AFLTokenCap : public BasicBlockPass {

    public:

      static char ID;
      struct FunctionOfInterest_t {
        const char *Name;
        bool IsText;
      };

      static const std::array<FunctionOfInterest_t, 5> FunctionsOfInterest;

      AFLTokenCap()
      : BasicBlockPass{ ID }, m_TokenFile{ nullptr },
      m_quiet { false }, m_FunctionName{ nullptr },
      m_ModuleName { nullptr } {

        char *TokenFilePath = getenv("AFL_TOKEN_FILE");

        if(TokenFilePath == nullptr)
          return;

        m_TokenFile = fopen(TokenFilePath, "a");
        if(m_TokenFile == nullptr) {

          FATAL("Cannot open the AFL_TOKEN_FILE file.");
        }

        if (isatty(2) && !getenv("AFL_QUIET")) {

          SAYF(cCYA "afl-llvm-tokencap-pass " cBRI VERSION cRST " by <0vercl0k@tuxfamily.org>\n");
        } else m_quiet = true;

      }

      ~AFLTokenCap() {

        if(m_TokenFile != nullptr) {

          for(const std::string &Token : m_Tokens)
            fprintf(m_TokenFile, "\"%s\"\n", Token.c_str());

          fclose(m_TokenFile);
        }
      }

      bool runOnBasicBlock(BasicBlock &B) override;

      const char *getPassName() const override {

        return "American Fuzzy Lop TokenCapture";
      }

      static bool is_valid_token_size(size_t TokenSize) {

        return TokenSize >= MIN_AUTO_EXTRA && TokenSize <= MAX_AUTO_EXTRA;
      }

      static bool filter_ascii(uint8_t *Data, size_t DataSize) {

        if(is_valid_token_size(DataSize) == false)
          return false;

        for(size_t i = 0; i < DataSize; ++i)
          if(isprint(Data[i]) == false)
            return false;
        return true;
      }

      static bool filter_likely_size(int64_t Data, size_t DataSize) {

        /* Get rid of "usual" error codes, and sizes */
        return (Data <= -0x100 || Data >= 0x1000) && DataSize > 1;
      }

      static std::string stringify(const uint8_t *Data, size_t DataSize, int Step, bool Text = false) {

        std::string TokenStr;
        for(size_t i = 0; i < DataSize; ++i) {

          uint8_t c = Data[i * Step];
          switch (c) {
            case 0 ... 31:
            case 127 ... 255:
            case '\"':
            case '\\': {

              if (c == 0 && Text == true)
                break;

              char buf[5] { };
              sprintf(buf, "\\x%02x", c);
              TokenStr.append(buf);
              break;
            }

            default: {

              TokenStr.push_back(c);
              break;
            }
          }
        }

        return TokenStr;
      }

    private:

      /* nullptr if no AFL_TOKEN_FILE has been provided */
      FILE *m_TokenFile;
      /* Set of tokens */
      std::set<std::string> m_Tokens;
      /* No output if AFL_QUIET defined */
      bool m_quiet;
      /* Current function name */
      const char *m_FunctionName;
      /* Current module name */
      const char *m_ModuleName;

      /* Dump a ConstantInt inside the token set if the
      integer is valid and properly formed */
      void dump_integer_token(ConstantInt *CI) {

        size_t DataSize = CI->getBitWidth() / 8;
        uint64_t CstValue = CI->getZExtValue();
        uint8_t *Data = (uint8_t*)&CstValue;

        /* First, filter out too small or too big tokens */
        if(is_valid_token_size(DataSize) == false)
          return;

        if(filter_ascii(Data, DataSize) == 0)
          return;

        /* Be wary of the endianess */
        int step = 1;
        if(sys::IsLittleEndianHost == true) {

          Data += DataSize - 1;
          step = -1;
        }

        /* Dump the token stringify-ed into the set*/
        auto Result = m_Tokens.insert(
          stringify(
            Data,
            DataSize,
            step
          )
        );

        /* Display if it's a new token and we are allowed to write out */
        if(m_quiet == false && Result.second == true)
          OKF("Found alphanum constant \"%s\" in %s/%s", Result.first->c_str(), m_ModuleName, m_FunctionName);
      }

};

char AFLTokenCap::ID = 0;
const std::array<AFLTokenCap::FunctionOfInterest_t, 5> AFLTokenCap::FunctionsOfInterest { {
  { "strcmp", true }, { "strncmp", true },
  { "strcasecmp", true }, { "strncasecmp", true },
  { "memcmp", false }
} };

bool AFLTokenCap::runOnBasicBlock(BasicBlock &B) {

  if(m_TokenFile == nullptr)
    return false;

  Function *F = B.getParent();
  m_FunctionName = F->hasName() ? F->getName().data() : "unknown";

  /* Avoid main to not have the option parsing, etc that
     will generate not meaningful tokens */
  if(strcmp(m_FunctionName, "main") == 0)
    return false;

  Module *M = F->getParent();
  m_ModuleName = M->getName().data();

  for(auto &I_ : B) {

    /* Handle comparaison against an integer immediate */
    if(ICmpInst *I = dyn_cast<ICmpInst>(&I_)) {

      ConstantInt *CI = nullptr;

      /* Predicate has to be an equality predicate for us to be interested */
      if(I->isEquality() == false)
        continue;

      {
        /* Find an immediate constant integer operand if there is one */
        Value *FirstOperand = I->getOperand(0);
        Value *SecondOperand = I->getOperand(1);

        if(isa<ConstantInt>(FirstOperand))
          CI = cast<ConstantInt>(FirstOperand);

        /* Haven't been able to have two constants passed, the compiler
        will get of those before kicking off the passes */

        if(CI == nullptr && isa<ConstantInt>(SecondOperand))
          CI = cast<ConstantInt>(SecondOperand);

        if(CI == nullptr)
          continue;
      }

      dump_integer_token(CI);
    }
    /* Handle switch/case with integer immediates */
    else if(SwitchInst *SI = dyn_cast<SwitchInst>(&I_)) {
      for(auto &CIT : SI->cases()) {

        ConstantInt *CI = CIT.getCaseValue();
        dump_integer_token(CI);
      }
    }
    /* Handle calls to functions of interest */
    else if(CallInst *I = dyn_cast<CallInst>(&I_)) {

      /* Retrieve the name of the call target */
      const char *FunctionCalledName = nullptr;
      if(I->getCalledFunction() != nullptr && I->getCalledFunction()->hasName())
        FunctionCalledName = I->getCalledFunction()->getName().data();

      if(FunctionCalledName == nullptr)
        continue;

      /* Walk the functions of interest */
      for(auto &FunctionOfInterest : FunctionsOfInterest) {

        const char *FunctionOfInterestName = FunctionOfInterest.Name;
        if(strcmp(FunctionCalledName, FunctionOfInterestName) != 0)
          continue;

        /* If we find an interesting call, we walk the arguments to
           find a potential constant string */
        for(size_t j = 0; j < I->getNumArgOperands(); ++j) {

          Value *ArgValue = I->getArgOperand(j);
          ConstantExpr *ConstantArg = dyn_cast<ConstantExpr>(ArgValue);
          if(ConstantArg == nullptr)
            continue;

          GlobalVariable *GV = dyn_cast<GlobalVariable>(ConstantArg->getOperand(0));
          if(GV == nullptr)
            continue;

          ConstantDataArray *AR = dyn_cast<ConstantDataArray>(GV->getInitializer());
          if(AR == nullptr)
            continue;

          StringRef StringData = AR->getRawDataValues();
          size_t TotalSize = StringData.size();
          if(TotalSize <= 1)
            continue;

          /* We are not interested in the final null-byte.
          Keep in mind that there is an extra-byte counted for the null terminator */
          TotalSize -= 1;

          /* Compare the token length to the auto-detected length dictionary tokens. */
          if(is_valid_token_size(TotalSize) == false)
            continue;

          auto Result = m_Tokens.insert(
            stringify(
              (uint8_t*)StringData.data(),
              TotalSize,
              1,
              FunctionOfInterest.IsText
            )
          );

          if(m_quiet == false && Result.second == true) {

            OKF("Call to %s with constant \"%s\" found in %s/%s", FunctionCalledName, Result.first->c_str(), m_ModuleName, m_FunctionName);
          }
        }
      }
    }
  }

  return false;
}
}

static void registerAFLTokenCapPass(const PassManagerBuilder &,
                            legacy::PassManagerBase &PM) {

  PM.add(new AFLTokenCap());
}

static RegisterStandardPasses RegisterAFLTokenCapPassLast(
    PassManagerBuilder::EP_OptimizerLast, registerAFLTokenCapPass);
