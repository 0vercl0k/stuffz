/*
gcc -shared leak_result.c -o leak_result.so -fPIC
LD_PRELOAD=./leak_result.so /home/user/crackmips 111111111111111111111111111111111111111111111111
LD_PRELOAD=./leak_result.so /home/user/oneround 111111111111111111111111111111111111111111111111
LD_PRELOAD=./leak_result.so /home/user/tworound 111111111111111111111111111111111111111111111111
LD_PRELOAD=./leak_result.so /home/user/threeround 111111111111111111111111111111111111111111111111
*/
#include <string.h>
#include <stdio.h>

int memcmp(const void *str1, const void *str2, size_t n)
{
    size_t i = 0;
    printf("S1: ");
    for(i = 0; i < n; ++i)
        printf("0x%.2x ", ((unsigned char*)str1)[i]);

    printf("\nS2: ");
    for(i = 0; i < n; ++i)
        printf("0x%.2x ", ((unsigned char*)str2)[i]);

    return 1;
}