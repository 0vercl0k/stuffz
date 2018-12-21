#include <stdio.h>
#include <string.h>

// The LFSR that will serve as the loop counter
#define LFSR_I 0

// The LFSR that will serve as decryption key
#define LFSR_K 1

#define MAGIC_ADDRESS_ENCRYPTED 0xfeb133a3

unsigned int dummy()
{
    printf("Woot?!\n");
    return 1;
}

unsigned int magic()
{
    printf("magic: Hi dudies, what's up? Not too hard to deal with those opaque predicates?\n");
    return 1;
}

unsigned int states_lfsr[] = {
    0, 0
};

unsigned int addresses[] = {
    (unsigned int)magic
};

unsigned int lfsr_init(unsigned int idx_lfsr, unsigned int IV = 0)
{
    states_lfsr[idx_lfsr] = IV;
}

unsigned int lfsr_next(unsigned int idx_lfsr)
{
    // http://en.wikipedia.org/wiki/Linear_feedback_shift_register
    // taps: 32 31 29 1; feedback polynomial: x^32 + x^31 + x^29 + x + 1
    states_lfsr[idx_lfsr] = (states_lfsr[idx_lfsr] >> 1) ^ (-(states_lfsr[idx_lfsr] & 1u) & 0xD0000001u);
    return states_lfsr[idx_lfsr];
}

unsigned int get_lfsr_state(unsigned int idx_lfsr_i, unsigned int IV_i, unsigned int period, unsigned int idx_lfsr_a, unsigned int IV_a)
{
    lfsr_init(idx_lfsr_i, IV_i);
    lfsr_init(idx_lfsr_a, IV_a);

    for(unsigned int j = 0; j < period; ++j)
    {
        lfsr_next(idx_lfsr_i);
        addresses[0] ^= lfsr_next(idx_lfsr_a);
    }

    return lfsr_next(idx_lfsr_i);
}

unsigned int body_loop()
{
    printf(".\n");
    return 0;
}

// For this time, I've removed both the true/false branches. That way, somehow, you have to check the loop at each time.
// Some of you would tell me that we can put a software-conditionnal breakpoint on the "goto" statement to watch which "funcs" it will call ;
// But this software-conditionnal breakpoint will be triggered at each time in the loop (even if it will be kind of transparent for you).
void opaque_predicate_lfsr_lvl2()
{
    unsigned int i = 0, key = 0;
    typedef unsigned int (*p_func)();
    unsigned int funcs[] = { (unsigned int)body_loop, MAGIC_ADDRESS_ENCRYPTED };
    void* labels[] = { &&loopcontinue, &&loopend };

    lfsr_init(LFSR_I, 0xdeadbeef);
    lfsr_init(LFSR_K, 0xbaadc0de);

    loopstart:
    i = lfsr_next(LFSR_I);
    // Usually, the function would not return at loopend ; I just wanted to keep the PoC in a single function
    // without having to do asm inlining trickery.
    goto *labels[((unsigned int (*)())(funcs[i == 0xf87fd5b6]))()];

    loopcontinue:
    funcs[1] ^= lfsr_next(LFSR_K);
    goto loopstart;

    loopend:
    printf("end\n");
    return;
}


// This time, the purpose is to hide where the loop will go when it is done.
// To do so we use another LFSR that will serve as a decryption key ; the address will be in clear only when the loop will be done.
// But the thing is if you want to pass the loop quickly, you just have to put a software-breakpoint in the TRUE branch of the "i == 0xf87fd5b6" test.
void opaque_predicate_lfsr_lvl1()
{
    unsigned int i = 0, key = 0;

    lfsr_init(LFSR_I, 0xdeadbeef);
    lfsr_init(LFSR_K, 0xbaadc0de);

    addresses[0] = MAGIC_ADDRESS_ENCRYPTED;

    loopstart:
    i = lfsr_next(LFSR_I);
    if(i == 0xf87fd5b6)
    {
        ((unsigned int (*)())addresses[0])();
        goto loopend;
    }

    addresses[0] ^= lfsr_next(LFSR_K);

    printf("Addresses[0]: %#.8x\n", addresses[0]);
    goto loopstart;

    loopend:
    return;
}

// This is the easiest piece of code to understand.
// The LFSR is used in order to obfuscate the counter of the loop ; you can't know by looking at it the number of times the
// loop will be executed. You have to iterate through the LFSR until you find the hardcoded value.
// But of course, if you want to pass the loop, you just have to put a software-breakpoint at the 'printf("\n")' level.
void opaque_predicate_lfsr_lvl0()
{
    lfsr_init(LFSR_I, 0xdeadbeef);
    for(unsigned int i = lfsr_next(LFSR_I), j = 0; i != 0xf87fd5b6; i = lfsr_next(LFSR_I), ++j)
        printf("%d", j);
    printf("\n");
}

int main()
{
    printf("Magic@%#.8x, %#.8x\n", magic, secret_msg);
    unsigned int i = get_lfsr_state(
        LFSR_I, 0xdeadbeef, 10,
        LFSR_K, 0xbaadc0de
    );

    printf("get_lfsr_state(10): %#.8x, %#.8x\n", i, addresses[0]);
    getchar();
    printf("Lvl0:\n");
    opaque_predicate_lfsr_lvl0();

    printf("Lvl1:\n");
    opaque_predicate_lfsr_lvl1();

    printf("Lvl2:\n");
    opaque_predicate_lfsr_lvl2();
    return 0;
}
