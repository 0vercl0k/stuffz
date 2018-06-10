// clang++ -shared -o lib.so -fPIC lib.cc
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

uint32_t number_of_rows = 16;
uint32_t private_key_length = 32;
// In [99]: ', '.join(c for c in list(bin(0xbaadc0de)[2:]))
// Out[99]: '1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0'
uint8_t private_key[32] = { 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0 };

const uint64_t k = 0xba0bab;

uint64_t decrypt(uint64_t x) {
    printf("decrypt(%" PRIx64 ") = %" PRIx64 "\n", x, x ^ k);
    return x ^ k;
}

uint64_t encrypt(uint64_t y) {
    printf("encrypt(%" PRIx64 ") = %" PRIx64 "\n", y, y ^ k);
    return y ^ k;
}
