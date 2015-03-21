#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Windows.h>

#include "..\common\tboxes.h"
#include "..\common\ty.h"
#include "..\common\txor.h"
#include "..\common\tyboxes.h"

const unsigned char S_box[] = { 0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76, 0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0, 0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15, 0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75, 0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84, 0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF, 0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8, 0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2, 0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73, 0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB, 0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79, 0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08, 0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A, 0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E, 0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF, 0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16 };

#define DW(t) (*(unsigned int*)(t))
#define ROR(a, n) ((a >> n) | ((a) << (32 - n)))
#define ROT(a) (ROR((a), 8))

#define DUMP_CURR_STATE() {          \
    printf("State dumped:\n");       \
    for (size_t i = 0; i < 16; ++i)  \
    {                                \
        if (i % 16 == 0)             \
            printf("\n");            \
        printf("%02X ", out[i]);     \
    }                                \
}

void AddRoundKey(unsigned char roundkey[16], unsigned char out[16])
{
    for (size_t i = 0; i < 16; ++i)
        out[i] ^= roundkey[i];
}

void SubBytes(unsigned char out[16])
{
    for (size_t i = 0; i < 16; ++i)
        out[i] = S_box[out[i]];
}

__forceinline void ShiftRows(unsigned char out[16])
{
    // +----+----+----+----+
    // | 00 | 04 | 08 | 12 |
    // +----+----+----+----+
    // | 01 | 05 | 09 | 13 |
    // +----+----+----+----+
    // | 02 | 06 | 10 | 14 |
    // +----+----+----+----+
    // | 03 | 07 | 11 | 15 |
    // +----+----+----+----+
    unsigned char tmp1, tmp2;

    // 8-bits left rotation of the second line
    tmp1 = out[1];
    out[1] = out[5];
    out[5] = out[9];
    out[9] = out[13];
    out[13] = tmp1;

    // 16-bits left rotation of the third line
    tmp1 = out[2];
    tmp2 = out[6];
    out[2] = out[10];
    out[6] = out[14];
    out[10] = tmp1;
    out[14] = tmp2;

    // 24-bits left rotation of the last line
    tmp1 = out[3];
    out[3] = out[15];
    out[15] = out[11];
    out[11] = out[7];
    out[7] = tmp1;
}

void MixColumns(unsigned char out[16])
{
    const unsigned char matrix[16] = {
        1, 2, 0, 0,
        0, 1, 2, 0,
        0, 0, 1, 2,
        2, 0, 0, 1
    },
    
    /// In[19]: reduce(operator.xor, [gmul[1][0xd4], gmul[2][0xbf], gmul[0][0x5d], gmul[0][0x30]])
    /// Out[19] : 4
    /// In [20]: reduce(operator.xor, [gmul[0][0xd4], gmul[1][0xbf], gmul[2][0x5d], gmul[0][0x30]])
    /// Out[20]: 102
    
    gmul[3][0x100] = {
        { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E, 0x7F, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F, 0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0x9B, 0x9C, 0x9D, 0x9E, 0x9F, 0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xAB, 0xAC, 0xAD, 0xAE, 0xAF, 0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF, 0xC0, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9, 0xCA, 0xCB, 0xCC, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xDB, 0xDC, 0xDD, 0xDE, 0xDF, 0xE0, 0xE1, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xEB, 0xEC, 0xED, 0xEE, 0xEF, 0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF },
        { 0x00, 0x02, 0x04, 0x06, 0x08, 0x0A, 0x0C, 0x0E, 0x10, 0x12, 0x14, 0x16, 0x18, 0x1A, 0x1C, 0x1E, 0x20, 0x22, 0x24, 0x26, 0x28, 0x2A, 0x2C, 0x2E, 0x30, 0x32, 0x34, 0x36, 0x38, 0x3A, 0x3C, 0x3E, 0x40, 0x42, 0x44, 0x46, 0x48, 0x4A, 0x4C, 0x4E, 0x50, 0x52, 0x54, 0x56, 0x58, 0x5A, 0x5C, 0x5E, 0x60, 0x62, 0x64, 0x66, 0x68, 0x6A, 0x6C, 0x6E, 0x70, 0x72, 0x74, 0x76, 0x78, 0x7A, 0x7C, 0x7E, 0x80, 0x82, 0x84, 0x86, 0x88, 0x8A, 0x8C, 0x8E, 0x90, 0x92, 0x94, 0x96, 0x98, 0x9A, 0x9C, 0x9E, 0xA0, 0xA2, 0xA4, 0xA6, 0xA8, 0xAA, 0xAC, 0xAE, 0xB0, 0xB2, 0xB4, 0xB6, 0xB8, 0xBA, 0xBC, 0xBE, 0xC0, 0xC2, 0xC4, 0xC6, 0xC8, 0xCA, 0xCC, 0xCE, 0xD0, 0xD2, 0xD4, 0xD6, 0xD8, 0xDA, 0xDC, 0xDE, 0xE0, 0xE2, 0xE4, 0xE6, 0xE8, 0xEA, 0xEC, 0xEE, 0xF0, 0xF2, 0xF4, 0xF6, 0xF8, 0xFA, 0xFC, 0xFE, 0x1B, 0x19, 0x1F, 0x1D, 0x13, 0x11, 0x17, 0x15, 0x0B, 0x09, 0x0F, 0x0D, 0x03, 0x01, 0x07, 0x05, 0x3B, 0x39, 0x3F, 0x3D, 0x33, 0x31, 0x37, 0x35, 0x2B, 0x29, 0x2F, 0x2D, 0x23, 0x21, 0x27, 0x25, 0x5B, 0x59, 0x5F, 0x5D, 0x53, 0x51, 0x57, 0x55, 0x4B, 0x49, 0x4F, 0x4D, 0x43, 0x41, 0x47, 0x45, 0x7B, 0x79, 0x7F, 0x7D, 0x73, 0x71, 0x77, 0x75, 0x6B, 0x69, 0x6F, 0x6D, 0x63, 0x61, 0x67, 0x65, 0x9B, 0x99, 0x9F, 0x9D, 0x93, 0x91, 0x97, 0x95, 0x8B, 0x89, 0x8F, 0x8D, 0x83, 0x81, 0x87, 0x85, 0xBB, 0xB9, 0xBF, 0xBD, 0xB3, 0xB1, 0xB7, 0xB5, 0xAB, 0xA9, 0xAF, 0xAD, 0xA3, 0xA1, 0xA7, 0xA5, 0xDB, 0xD9, 0xDF, 0xDD, 0xD3, 0xD1, 0xD7, 0xD5, 0xCB, 0xC9, 0xCF, 0xCD, 0xC3, 0xC1, 0xC7, 0xC5, 0xFB, 0xF9, 0xFF, 0xFD, 0xF3, 0xF1, 0xF7, 0xF5, 0xEB, 0xE9, 0xEF, 0xED, 0xE3, 0xE1, 0xE7, 0xE5 },
        { 0x00, 0x03, 0x06, 0x05, 0x0C, 0x0F, 0x0A, 0x09, 0x18, 0x1B, 0x1E, 0x1D, 0x14, 0x17, 0x12, 0x11, 0x30, 0x33, 0x36, 0x35, 0x3C, 0x3F, 0x3A, 0x39, 0x28, 0x2B, 0x2E, 0x2D, 0x24, 0x27, 0x22, 0x21, 0x60, 0x63, 0x66, 0x65, 0x6C, 0x6F, 0x6A, 0x69, 0x78, 0x7B, 0x7E, 0x7D, 0x74, 0x77, 0x72, 0x71, 0x50, 0x53, 0x56, 0x55, 0x5C, 0x5F, 0x5A, 0x59, 0x48, 0x4B, 0x4E, 0x4D, 0x44, 0x47, 0x42, 0x41, 0xC0, 0xC3, 0xC6, 0xC5, 0xCC, 0xCF, 0xCA, 0xC9, 0xD8, 0xDB, 0xDE, 0xDD, 0xD4, 0xD7, 0xD2, 0xD1, 0xF0, 0xF3, 0xF6, 0xF5, 0xFC, 0xFF, 0xFA, 0xF9, 0xE8, 0xEB, 0xEE, 0xED, 0xE4, 0xE7, 0xE2, 0xE1, 0xA0, 0xA3, 0xA6, 0xA5, 0xAC, 0xAF, 0xAA, 0xA9, 0xB8, 0xBB, 0xBE, 0xBD, 0xB4, 0xB7, 0xB2, 0xB1, 0x90, 0x93, 0x96, 0x95, 0x9C, 0x9F, 0x9A, 0x99, 0x88, 0x8B, 0x8E, 0x8D, 0x84, 0x87, 0x82, 0x81, 0x9B, 0x98, 0x9D, 0x9E, 0x97, 0x94, 0x91, 0x92, 0x83, 0x80, 0x85, 0x86, 0x8F, 0x8C, 0x89, 0x8A, 0xAB, 0xA8, 0xAD, 0xAE, 0xA7, 0xA4, 0xA1, 0xA2, 0xB3, 0xB0, 0xB5, 0xB6, 0xBF, 0xBC, 0xB9, 0xBA, 0xFB, 0xF8, 0xFD, 0xFE, 0xF7, 0xF4, 0xF1, 0xF2, 0xE3, 0xE0, 0xE5, 0xE6, 0xEF, 0xEC, 0xE9, 0xEA, 0xCB, 0xC8, 0xCD, 0xCE, 0xC7, 0xC4, 0xC1, 0xC2, 0xD3, 0xD0, 0xD5, 0xD6, 0xDF, 0xDC, 0xD9, 0xDA, 0x5B, 0x58, 0x5D, 0x5E, 0x57, 0x54, 0x51, 0x52, 0x43, 0x40, 0x45, 0x46, 0x4F, 0x4C, 0x49, 0x4A, 0x6B, 0x68, 0x6D, 0x6E, 0x67, 0x64, 0x61, 0x62, 0x73, 0x70, 0x75, 0x76, 0x7F, 0x7C, 0x79, 0x7A, 0x3B, 0x38, 0x3D, 0x3E, 0x37, 0x34, 0x31, 0x32, 0x23, 0x20, 0x25, 0x26, 0x2F, 0x2C, 0x29, 0x2A, 0x0B, 0x08, 0x0D, 0x0E, 0x07, 0x04, 0x01, 0x02, 0x13, 0x10, 0x15, 0x16, 0x1F, 0x1C, 0x19, 0x1A }
    };

    for (size_t i = 0; i < 4; ++i)
    {
        unsigned char a = out[i * 4 + 0];
        unsigned char b = out[i * 4 + 1];
        unsigned char c = out[i * 4 + 2];
        unsigned char d = out[i * 4 + 3];

        out[i * 4 + 0] = gmul[matrix[0]][a] ^ gmul[matrix[1]][b] ^ gmul[matrix[2]][c] ^ gmul[matrix[3]][d];
        out[i * 4 + 1] = gmul[matrix[4]][a] ^ gmul[matrix[5]][b] ^ gmul[matrix[6]][c] ^ gmul[matrix[7]][d];
        out[i * 4 + 2] = gmul[matrix[8]][a] ^ gmul[matrix[9]][b] ^ gmul[matrix[10]][c] ^ gmul[matrix[11]][d];
        out[i * 4 + 3] = gmul[matrix[12]][a] ^ gmul[matrix[13]][b] ^ gmul[matrix[14]][c] ^ gmul[matrix[15]][d];
    }
}

void aes128_enc_base(unsigned char in[16], unsigned char out[16], unsigned char key[16])
{
    unsigned int d;
    unsigned char round_keys[11][16] = { 0 };
    const unsigned char rcon[] = { 0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D };

    /// Key schedule -- Generate one subkey for each round
    /// http://www.formaestudio.com/rijndaelinspector/archivos/Rijndael_Animation_v4_eng.swf

    // First round-key is the actual key
    memcpy(&round_keys[0][0], key, 16);
    d = DW(&round_keys[0][12]);
    for (size_t i = 1; i < 11; ++i)
    {
        // Rotate `d` 8 bits to the right
        d = ROT(d);

        // Takes every bytes of `d` & substitute them using `S_box`
        unsigned char a1, a2, a3, a4;
        // Do not forget to xor this byte with `rcon[i]`
        a1 = S_box[(d >> 0) & 0xff] ^ rcon[i]; // a1 is the LSB
        a2 = S_box[(d >> 8) & 0xff];
        a3 = S_box[(d >> 16) & 0xff];
        a4 = S_box[(d >> 24) & 0xff];

        d = (a1 << 0) | (a2 << 8) | (a3 << 16) | (a4 << 24);

        // Now we can generate the current roundkey using the previous one
        for (size_t j = 0; j < 4; j++)
        {
            d ^= DW(&(round_keys[i - 1][j * 4]));
            *(unsigned int*)(&(round_keys[i][j * 4])) = d;
        }
    }

    //printf("Key schedule output:");
    //for (i = 0; i < 11 * 16; ++i)
    //{
    //    if (i % 16 == 0)
    //        printf("\nRounKey%02d: ", i / 16);
    //    printf("%02X ", round_keys[i / 16][i % 16]);
    //}
    //printf("\n");

    /// Dig in now
    /// The initial round is just AddRoundKey with the first one (being the encryption key)
    memcpy(out, in, 16);
    AddRoundKey(round_keys[0], out);

    //DUMP_CURR_STATE();

    /// Let's start the encryption process now
    for (size_t i = 1; i < 10; ++i)
    {
        SubBytes(out);
        ShiftRows(out);
        MixColumns(out);
        AddRoundKey(round_keys[i], out);
    }

    /// Last round which is a bit different
    SubBytes(out);
    ShiftRows(out);
    AddRoundKey(round_keys[10], out);
}

void aes128_enc_reorg_step1(unsigned char in[16], unsigned char out[16], unsigned char key[16])
{
    unsigned int d;
    unsigned char round_keys[11][16] = { 0 };
    const unsigned char rcon[] = { 0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D };

    /// Key schedule -- Generate one subkey for each round
    /// http://www.formaestudio.com/rijndaelinspector/archivos/Rijndael_Animation_v4_eng.swf

    // First round-key is the actual key
    memcpy(&round_keys[0][0], key, 16);
    d = DW(&round_keys[0][12]);
    for (size_t i = 1; i < 11; ++i)
    {
        // Rotate `d` 8 bits to the right
        d = ROT(d);

        // Takes every bytes of `d` & substitute them using `S_box`
        unsigned char a1, a2, a3, a4;
        // Do not forget to xor this byte with `rcon[i]`
        a1 = S_box[(d >> 0) & 0xff] ^ rcon[i]; // a1 is the LSB
        a2 = S_box[(d >> 8) & 0xff];
        a3 = S_box[(d >> 16) & 0xff];
        a4 = S_box[(d >> 24) & 0xff];

        d = (a1 << 0) | (a2 << 8) | (a3 << 16) | (a4 << 24);

        // Now we can generate the current roundkey using the previous one
        for (size_t j = 0; j < 4; j++)
        {
            d ^= DW(&(round_keys[i - 1][j * 4]));
            *(unsigned int*)(&(round_keys[i][j * 4])) = d;
        }
    }

    /// Dig in now

    /// The conventional way to describe AES - 128 encryption is as follows :
    /// state <- plaintext
    /// AddRoundKey(state, k0)
    /// for r = 1 ... 9
    ///     SubBytes(state)
    ///     ShiftRows(state)
    ///     MixColumns(state)
    ///     AddRoundKey(state, kr)
    /// SubBytes(state)
    /// ShiftRows(state)
    /// AddRoundKey(state, k10)
    /// ciphertext <- state
    /// BUT
    /// 1. The for - loop can be redefined to bring the transformation AddRoundKey(state, k0)
    ///    inside it while pushing AddRoundKey(state, k9) out.

    memcpy(out, in, 16);

    /// Let's start the encryption process now
    for (size_t i = 0; i < 9; ++i)
    {
        AddRoundKey(round_keys[i], out);
        SubBytes(out);
        ShiftRows(out);
        MixColumns(out);
    }

    /// Last round which is a bit different
    AddRoundKey(round_keys[9], out);
    SubBytes(out);
    ShiftRows(out);
    AddRoundKey(round_keys[10], out);
}

void aes128_enc_reorg_step2(unsigned char in[16], unsigned char out[16], unsigned char key[16])
{
    unsigned int d;
    unsigned char round_keys[11][16] = { 0 };
    const unsigned char rcon[] = { 0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D };

    /// Key schedule -- Generate one subkey for each round
    /// http://www.formaestudio.com/rijndaelinspector/archivos/Rijndael_Animation_v4_eng.swf

    // First round-key is the actual key
    memcpy(&round_keys[0][0], key, 16);
    d = DW(&round_keys[0][12]);
    for (size_t i = 1; i < 11; ++i)
    {
        // Rotate `d` 8 bits to the right
        d = ROT(d);

        // Takes every bytes of `d` & substitute them using `S_box`
        unsigned char a1, a2, a3, a4;
        // Do not forget to xor this byte with `rcon[i]`
        a1 = S_box[(d >> 0) & 0xff] ^ rcon[i]; // a1 is the LSB
        a2 = S_box[(d >> 8) & 0xff];
        a3 = S_box[(d >> 16) & 0xff];
        a4 = S_box[(d >> 24) & 0xff];

        d = (a1 << 0) | (a2 << 8) | (a3 << 16) | (a4 << 24);

        // Now we can generate the current roundkey using the previous one
        for (size_t j = 0; j < 4; j++)
        {
            d ^= DW(&(round_keys[i - 1][j * 4]));
            *(unsigned int*)(&(round_keys[i][j * 4])) = d;
        }
    }

    /// Dig in now

    /// The conventional way to describe AES - 128 encryption is as follows :
    /// state <- plaintext
    /// AddRoundKey(state, k0)
    /// for r = 1 ... 9
    ///     SubBytes(state)
    ///     ShiftRows(state)
    ///     MixColumns(state)
    ///     AddRoundKey(state, kr)
    /// SubBytes(state)
    /// ShiftRows(state)
    /// AddRoundKey(state, k10)
    /// ciphertext <- state

    /// BUT
    /// 1. The for - loop can be redefined to bring the transformation AddRoundKey(state, k0)
    ///    inside it while pushing AddRoundKey(state, k9) out.
    /// 2. Since SubBytes applies the same S - box to each byte of the state, SubBytes
    ///    followed by ShiftRows gives the same result as ShiftRows followed by
    ///    SubBytes.
    /// From these observations, we can generate the following description :
    /// state <- plaintext
    /// for r = 1 ... 9
    ///     AddRoundKey(state, kr-1)
    ///     ShiftRows(state)
    ///     SubBytes(state)
    ///     MixColumns(state)
    /// AddRoundKey(state, k9)
    /// ShiftRows(state)
    /// SubBytes(state)
    /// AddRoundKey(state, k10)
    /// ciphertext <- state
    memcpy(out, in, 16);

    /// Let's start the encryption process now
    for (size_t i = 0; i < 9; ++i)
    {
        AddRoundKey(round_keys[i], out);
        ShiftRows(out);
        SubBytes(out);
        MixColumns(out);
    }

    /// Last round which is a bit different
    AddRoundKey(round_keys[9], out);
    ShiftRows(out);
    SubBytes(out);
    AddRoundKey(round_keys[10], out);
}

void aes128_enc_reorg_step3(unsigned char in[16], unsigned char out[16], unsigned char key[16])
{
    unsigned int d;
    unsigned char round_keys[11][16] = { 0 };
    const unsigned char rcon[] = { 0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39, 0x72, 0xE4, 0xD3, 0xBD, 0x61, 0xC2, 0x9F, 0x25, 0x4A, 0x94, 0x33, 0x66, 0xCC, 0x83, 0x1D, 0x3A, 0x74, 0xE8, 0xCB, 0x8D };

    /// Key schedule -- Generate one subkey for each round
    /// http://www.formaestudio.com/rijndaelinspector/archivos/Rijndael_Animation_v4_eng.swf

    // First round-key is the actual key
    memcpy(&round_keys[0][0], key, 16);
    d = DW(&round_keys[0][12]);
    for (size_t i = 1; i < 11; ++i)
    {
        // Rotate `d` 8 bits to the right
        d = ROT(d);

        // Takes every bytes of `d` & substitute them using `S_box`
        unsigned char a1, a2, a3, a4;
        // Do not forget to xor this byte with `rcon[i]`
        a1 = S_box[(d >> 0) & 0xff] ^ rcon[i]; // a1 is the LSB
        a2 = S_box[(d >> 8) & 0xff];
        a3 = S_box[(d >> 16) & 0xff];
        a4 = S_box[(d >> 24) & 0xff];

        d = (a1 << 0) | (a2 << 8) | (a3 << 16) | (a4 << 24);

        // Now we can generate the current roundkey using the previous one
        for (size_t j = 0; j < 4; j++)
        {
            d ^= DW(&(round_keys[i - 1][j * 4]));
            *(unsigned int*)(&(round_keys[i][j * 4])) = d;
        }
    }

    /// Dig in now

    /// The conventional way to describe AES - 128 encryption is as follows :
    /// state <- plaintext
    /// AddRoundKey(state, k0)
    /// for r = 1 ... 9
    ///     SubBytes(state)
    ///     ShiftRows(state)
    ///     MixColumns(state)
    ///     AddRoundKey(state, kr)
    /// SubBytes(state)
    /// ShiftRows(state)
    /// AddRoundKey(state, k10)
    /// ciphertext <- state

    /// BUT
    /// 1. The for - loop can be redefined to bring the transformation AddRoundKey(state, k0)
    ///    inside it while pushing AddRoundKey(state, k9) out.
    /// 2. Since SubBytes applies the same S - box to each byte of the state, SubBytes
    ///    followed by ShiftRows gives the same result as ShiftRows followed by
    ///    SubBytes.
    /// From these observations, we can generate the following description :
    /// state <- plaintext
    /// for r = 1 ... 9
    ///     AddRoundKey(state, kr-1)
    ///     ShiftRows(state)
    ///     SubBytes(state)
    ///     MixColumns(state)
    /// AddRoundKey(state, k9)
    /// ShiftRows(state)
    /// SubBytes(state)
    /// AddRoundKey(state, k10)
    /// ciphertext <- state

    /// Here is another observation:
    /// 3. Since ShiftRows is a linear transformation (recall that it is a permutation),
    ///    AddRoundKey(state, kr-1) followed by ShiftRows(state) gives the same result
    ///    as ShiftRows(state) followed by AddRoundKey(state, ShiftRows(bkr-1));

    /// This gives us:
    /// state <- plaintext
    /// for r = 1 ... 9
    ///     ShiftRows(state)
    ///     AddRoundKey(state, ShiftRows(bkr-1))
    ///     SubBytes(state)
    ///     MixColumns(state)
    /// ShiftRows(state)
    /// AddRoundKey(state, ShiftRows(bk9))
    /// SubBytes(state)
    /// AddRoundKey(state, k10)
    /// ciphertext <- state
    memcpy(out, in, 16);

    /// Let's start the encryption process now
    for (size_t i = 0; i < 9; ++i)
    {
        ShiftRows(out);
        ShiftRows(round_keys[i]);
        AddRoundKey(round_keys[i], out);
        SubBytes(out);
        MixColumns(out);
    }

    /// Last round which is a bit different
    ShiftRows(out);
    ShiftRows(round_keys[9]);
    AddRoundKey(round_keys[9], out);
    SubBytes(out);
    AddRoundKey(round_keys[10], out);
}

void aes128_enc_wb_step1(unsigned char in[16], unsigned char out[16])
{
    memcpy(out, in, 16);

    /// Let's start the encryption process now
    for (size_t i = 0; i < 9; ++i)
    {
        ShiftRows(out);

        for (size_t j = 0; j < 16; ++j)
        {
            unsigned char x = Tboxes[i][j][out[j]];
            out[j] = x;
        }

        MixColumns(out);
    }

    /// Last round which is a bit different
    ShiftRows(out);

    for (size_t j = 0; j < 16; ++j)
    {
        unsigned char x = Tboxes[9][j][out[j]];
        out[j] = x;
    }
}

void aes128_enc_wb_step2(unsigned char in[16], unsigned char out[16])
{
    memcpy(out, in, 16);

    /// Let's start the encryption process now
    for (size_t i = 0; i < 9; ++i)
    {
        ShiftRows(out);

        for (size_t j = 0; j < 16; ++j)
        {
            unsigned char x = Tboxes[i][j][out[j]];
            out[j] = x;
        }
        
        for (size_t j = 0; j < 4; ++j)
        {
            unsigned char a = out[j * 4 + 0];
            unsigned char b = out[j * 4 + 1];
            unsigned char c = out[j * 4 + 2];
            unsigned char d = out[j * 4 + 3];

            DW(&out[j * 4]) = Ty[0][a] ^ Ty[1][b] ^ Ty[2][c] ^ Ty[3][d];
        }
    }

    /// Last round which is a bit different
    ShiftRows(out);

    for (size_t j = 0; j < 16; ++j)
    {
        unsigned char x = Tboxes[9][j][out[j]];
        out[j] = x;
    }
}

void aes128_enc_wb_step3(unsigned char in[16], unsigned char out[16])
{
    memcpy(out, in, 16);

    /// Let's start the encryption process now
    for (size_t i = 0; i < 9; ++i)
    {
        ShiftRows(out);

        for (size_t j = 0; j < 4; ++j)
        {
            unsigned char a = out[j * 4 + 0];
            unsigned char b = out[j * 4 + 1];
            unsigned char c = out[j * 4 + 2];
            unsigned char d = out[j * 4 + 3];

            a = out[j * 4 + 0] = Tboxes[i][j * 4 + 0][a];
            b = out[j * 4 + 1] = Tboxes[i][j * 4 + 1][b];
            c = out[j * 4 + 2] = Tboxes[i][j * 4 + 2][c];
            d = out[j * 4 + 3] = Tboxes[i][j * 4 + 3][d];

            DW(&out[j * 4]) = Ty[0][a] ^ Ty[1][b] ^ Ty[2][c] ^ Ty[3][d];
        }
    }

    /// Last round which is a bit different
    ShiftRows(out);

    for (size_t j = 0; j < 16; ++j)
    {
        unsigned char x = Tboxes[9][j][out[j]];
        out[j] = x;
    }
}

void aes128_enc_wb_step4(unsigned char in[16], unsigned char out[16])
{
    memcpy(out, in, 16);

    /// Let's start the encryption process now
    for (size_t i = 0; i < 9; ++i)
    {
        ShiftRows(out);

        for (size_t j = 0; j < 4; ++j)
        {
            unsigned char a = out[j * 4 + 0];
            unsigned char b = out[j * 4 + 1];
            unsigned char c = out[j * 4 + 2];
            unsigned char d = out[j * 4 + 3];

            a = out[j * 4 + 0] = Tboxes[i][j * 4 + 0][a];
            b = out[j * 4 + 1] = Tboxes[i][j * 4 + 1][b];
            c = out[j * 4 + 2] = Tboxes[i][j * 4 + 2][c];
            d = out[j * 4 + 3] = Tboxes[i][j * 4 + 3][d];

            unsigned int aa = Ty[0][a];
            unsigned int bb = Ty[1][b];
            unsigned int cc = Ty[2][c];
            unsigned int dd = Ty[3][d];

            out[j * 4 + 0] = (Txor[Txor[(aa >>  0) & 0xf][(bb >>  0) & 0xf]][Txor[(cc >>  0) & 0xf][(dd >>  0) & 0xf]])  | ((Txor[Txor[(aa >>  4) & 0xf][(bb >>  4) & 0xf]][Txor[(cc >>  4) & 0xf][(dd >>  4) & 0xf]]) << 4);
            out[j * 4 + 1] = (Txor[Txor[(aa >>  8) & 0xf][(bb >>  8) & 0xf]][Txor[(cc >>  8) & 0xf][(dd >>  8) & 0xf]])  | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
            out[j * 4 + 2] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]])  | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
            out[j * 4 + 3] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]])  | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);
        }
    }

    /// Last round which is a bit different
    ShiftRows(out);

    for (size_t j = 0; j < 16; ++j)
    {
        unsigned char x = Tboxes[9][j][out[j]];
        out[j] = x;
    }
}

void aes128_enc_wb_step5(unsigned char in[16], unsigned char out[16])
{
    memcpy(out, in, 16);

    /// Let's start the encryption process now
    for (size_t i = 0; i < 9; ++i)
    {
        ShiftRows(out);

        for (size_t j = 0; j < 4; ++j)
        {
            unsigned char a = out[j * 4 + 0];
            unsigned char b = out[j * 4 + 1];
            unsigned char c = out[j * 4 + 2];
            unsigned char d = out[j * 4 + 3];

            unsigned int aa = Tyboxes[i][j * 4 + 0][a];
            unsigned int bb = Tyboxes[i][j * 4 + 1][b];
            unsigned int cc = Tyboxes[i][j * 4 + 2][c];
            unsigned int dd = Tyboxes[i][j * 4 + 3][d];

            out[j * 4 + 0] = (Txor[Txor[(aa >>  0) & 0xf][(bb >>  0) & 0xf]][Txor[(cc >>  0) & 0xf][(dd >>  0) & 0xf]]) | ((Txor[Txor[(aa >>  4) & 0xf][(bb >>  4) & 0xf]][Txor[(cc >>  4) & 0xf][(dd >>  4) & 0xf]]) << 4);
            out[j * 4 + 1] = (Txor[Txor[(aa >>  8) & 0xf][(bb >>  8) & 0xf]][Txor[(cc >>  8) & 0xf][(dd >>  8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
            out[j * 4 + 2] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
            out[j * 4 + 3] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);
        }
    }

    /// Last round which is a bit different
    ShiftRows(out);

    for (size_t j = 0; j < 16; ++j)
    {
        unsigned char x = Tboxes_[j][out[j]];
        out[j] = x;
    }
}

void aes128_enc_wb_final(unsigned char in[16], unsigned char out[16])
{
    memcpy(out, in, 16);

    /// Let's start the encryption process now
    for (size_t i = 0; i < 9; ++i)
    {
        ShiftRows(out);

        for (size_t j = 0; j < 4; ++j)
        {
            unsigned int aa = Tyboxes[i][j * 4 + 0][out[j * 4 + 0]];
            unsigned int bb = Tyboxes[i][j * 4 + 1][out[j * 4 + 1]];
            unsigned int cc = Tyboxes[i][j * 4 + 2][out[j * 4 + 2]];
            unsigned int dd = Tyboxes[i][j * 4 + 3][out[j * 4 + 3]];

            out[j * 4 + 0] = (Txor[Txor[(aa >>  0) & 0xf][(bb >>  0) & 0xf]][Txor[(cc >>  0) & 0xf][(dd >>  0) & 0xf]]) | ((Txor[Txor[(aa >>  4) & 0xf][(bb >>  4) & 0xf]][Txor[(cc >>  4) & 0xf][(dd >>  4) & 0xf]]) << 4);
            out[j * 4 + 1] = (Txor[Txor[(aa >>  8) & 0xf][(bb >>  8) & 0xf]][Txor[(cc >>  8) & 0xf][(dd >>  8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
            out[j * 4 + 2] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
            out[j * 4 + 3] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);
        }
    }

    /// Last round which is a bit different
    ShiftRows(out);

    for (size_t j = 0; j < 16; ++j)
    {
        unsigned char x = Tboxes_[j][out[j]];
        out[j] = x;
    }
}

void aes128_enc_wb_final_unrolled(unsigned char in[16], unsigned char out[16])
{
    memcpy(out, in, 16);

    /// Let's start the encryption process now
    /// R0
    ShiftRows(out);

    unsigned int aa = Tyboxes[0][0][out[0]];
    unsigned int bb = Tyboxes[0][1][out[1]];
    unsigned int cc = Tyboxes[0][2][out[2]];
    unsigned int dd = Tyboxes[0][3][out[3]];

    out[0] = (Txor[Txor[(aa >>  0) & 0xf][(bb >>  0) & 0xf]][Txor[(cc >>  0) & 0xf][(dd >>  0) & 0xf]]) | ((Txor[Txor[(aa >>  4) & 0xf][(bb >>  4) & 0xf]][Txor[(cc >>  4) & 0xf][(dd >>  4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa >>  8) & 0xf][(bb >>  8) & 0xf]][Txor[(cc >>  8) & 0xf][(dd >>  8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[0][4][out[4]];
    bb = Tyboxes[0][5][out[5]];
    cc = Tyboxes[0][6][out[6]];
    dd = Tyboxes[0][7][out[7]];

    out[4] = (Txor[Txor[(aa >>  0) & 0xf][(bb >>  0) & 0xf]][Txor[(cc >>  0) & 0xf][(dd >>  0) & 0xf]]) | ((Txor[Txor[(aa >>  4) & 0xf][(bb >>  4) & 0xf]][Txor[(cc >>  4) & 0xf][(dd >>  4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa >>  8) & 0xf][(bb >>  8) & 0xf]][Txor[(cc >>  8) & 0xf][(dd >>  8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[0][8][out[8]];
    bb = Tyboxes[0][9][out[9]];
    cc = Tyboxes[0][10][out[10]];
    dd = Tyboxes[0][11][out[11]];

    out[ 8] = (Txor[Txor[(aa >>  0) & 0xf][(bb >>  0) & 0xf]][Txor[(cc >>  0) & 0xf][(dd >>  0) & 0xf]]) | ((Txor[Txor[(aa >>  4) & 0xf][(bb >>  4) & 0xf]][Txor[(cc >>  4) & 0xf][(dd >>  4) & 0xf]]) << 4);
    out[ 9] = (Txor[Txor[(aa >>  8) & 0xf][(bb >>  8) & 0xf]][Txor[(cc >>  8) & 0xf][(dd >>  8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[0][12][out[12]];
    bb = Tyboxes[0][13][out[13]];
    cc = Tyboxes[0][14][out[14]];
    dd = Tyboxes[0][15][out[15]];

    out[12] = (Txor[Txor[(aa >>  0) & 0xf][(bb >>  0) & 0xf]][Txor[(cc >>  0) & 0xf][(dd >>  0) & 0xf]]) | ((Txor[Txor[(aa >>  4) & 0xf][(bb >>  4) & 0xf]][Txor[(cc >>  4) & 0xf][(dd >>  4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa >>  8) & 0xf][(bb >>  8) & 0xf]][Txor[(cc >>  8) & 0xf][(dd >>  8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    ///R1
    ShiftRows(out);

    aa = Tyboxes[1][0][out[0]];
    bb = Tyboxes[1][1][out[1]];
    cc = Tyboxes[1][2][out[2]];
    dd = Tyboxes[1][3][out[3]];

    out[0] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[1][4][out[4]];
    bb = Tyboxes[1][5][out[5]];
    cc = Tyboxes[1][6][out[6]];
    dd = Tyboxes[1][7][out[7]];

    out[4] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[1][8][out[8]];
    bb = Tyboxes[1][9][out[9]];
    cc = Tyboxes[1][10][out[10]];
    dd = Tyboxes[1][11][out[11]];

    out[8] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[1][12][out[12]];
    bb = Tyboxes[1][13][out[13]];
    cc = Tyboxes[1][14][out[14]];
    dd = Tyboxes[1][15][out[15]];

    out[12] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    ///R2
    ShiftRows(out);

    aa = Tyboxes[2][0][out[0]];
    bb = Tyboxes[2][1][out[1]];
    cc = Tyboxes[2][2][out[2]];
    dd = Tyboxes[2][3][out[3]];

    out[0] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[2][4][out[4]];
    bb = Tyboxes[2][5][out[5]];
    cc = Tyboxes[2][6][out[6]];
    dd = Tyboxes[2][7][out[7]];

    out[4] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[2][8][out[8]];
    bb = Tyboxes[2][9][out[9]];
    cc = Tyboxes[2][10][out[10]];
    dd = Tyboxes[2][11][out[11]];

    out[8] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[2][12][out[12]];
    bb = Tyboxes[2][13][out[13]];
    cc = Tyboxes[2][14][out[14]];
    dd = Tyboxes[2][15][out[15]];

    out[12] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    ///R3
    ShiftRows(out);

    aa = Tyboxes[3][0][out[0]];
    bb = Tyboxes[3][1][out[1]];
    cc = Tyboxes[3][2][out[2]];
    dd = Tyboxes[3][3][out[3]];

    out[0] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[3][4][out[4]];
    bb = Tyboxes[3][5][out[5]];
    cc = Tyboxes[3][6][out[6]];
    dd = Tyboxes[3][7][out[7]];

    out[4] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[3][8][out[8]];
    bb = Tyboxes[3][9][out[9]];
    cc = Tyboxes[3][10][out[10]];
    dd = Tyboxes[3][11][out[11]];

    out[8] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[3][12][out[12]];
    bb = Tyboxes[3][13][out[13]];
    cc = Tyboxes[3][14][out[14]];
    dd = Tyboxes[3][15][out[15]];

    out[12] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    ///R4
    ShiftRows(out);

    aa = Tyboxes[4][0][out[0]];
    bb = Tyboxes[4][1][out[1]];
    cc = Tyboxes[4][2][out[2]];
    dd = Tyboxes[4][3][out[3]];

    out[0] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[4][4][out[4]];
    bb = Tyboxes[4][5][out[5]];
    cc = Tyboxes[4][6][out[6]];
    dd = Tyboxes[4][7][out[7]];

    out[4] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[4][8][out[8]];
    bb = Tyboxes[4][9][out[9]];
    cc = Tyboxes[4][10][out[10]];
    dd = Tyboxes[4][11][out[11]];

    out[8] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[4][12][out[12]];
    bb = Tyboxes[4][13][out[13]];
    cc = Tyboxes[4][14][out[14]];
    dd = Tyboxes[4][15][out[15]];

    out[12] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    ///R5
    ShiftRows(out);

    aa = Tyboxes[5][0][out[0]];
    bb = Tyboxes[5][1][out[1]];
    cc = Tyboxes[5][2][out[2]];
    dd = Tyboxes[5][3][out[3]];

    out[0] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[5][4][out[4]];
    bb = Tyboxes[5][5][out[5]];
    cc = Tyboxes[5][6][out[6]];
    dd = Tyboxes[5][7][out[7]];

    out[4] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[5][8][out[8]];
    bb = Tyboxes[5][9][out[9]];
    cc = Tyboxes[5][10][out[10]];
    dd = Tyboxes[5][11][out[11]];

    out[8] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[5][12][out[12]];
    bb = Tyboxes[5][13][out[13]];
    cc = Tyboxes[5][14][out[14]];
    dd = Tyboxes[5][15][out[15]];

    out[12] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    ///R6
    ShiftRows(out);

    aa = Tyboxes[6][0][out[0]];
    bb = Tyboxes[6][1][out[1]];
    cc = Tyboxes[6][2][out[2]];
    dd = Tyboxes[6][3][out[3]];

    out[0] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[6][4][out[4]];
    bb = Tyboxes[6][5][out[5]];
    cc = Tyboxes[6][6][out[6]];
    dd = Tyboxes[6][7][out[7]];

    out[4] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[6][8][out[8]];
    bb = Tyboxes[6][9][out[9]];
    cc = Tyboxes[6][10][out[10]];
    dd = Tyboxes[6][11][out[11]];

    out[8] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[6][12][out[12]];
    bb = Tyboxes[6][13][out[13]];
    cc = Tyboxes[6][14][out[14]];
    dd = Tyboxes[6][15][out[15]];

    out[12] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    ///R7
    ShiftRows(out);

    aa = Tyboxes[7][0][out[0]];
    bb = Tyboxes[7][1][out[1]];
    cc = Tyboxes[7][2][out[2]];
    dd = Tyboxes[7][3][out[3]];

    out[0] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[7][4][out[4]];
    bb = Tyboxes[7][5][out[5]];
    cc = Tyboxes[7][6][out[6]];
    dd = Tyboxes[7][7][out[7]];

    out[4] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[7][8][out[8]];
    bb = Tyboxes[7][9][out[9]];
    cc = Tyboxes[7][10][out[10]];
    dd = Tyboxes[7][11][out[11]];

    out[8] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[7][12][out[12]];
    bb = Tyboxes[7][13][out[13]];
    cc = Tyboxes[7][14][out[14]];
    dd = Tyboxes[7][15][out[15]];

    out[12] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    ///R8
    ShiftRows(out);

    aa = Tyboxes[8][0][out[0]];
    bb = Tyboxes[8][1][out[1]];
    cc = Tyboxes[8][2][out[2]];
    dd = Tyboxes[8][3][out[3]];

    out[0] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[8][4][out[4]];
    bb = Tyboxes[8][5][out[5]];
    cc = Tyboxes[8][6][out[6]];
    dd = Tyboxes[8][7][out[7]];

    out[4] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[8][8][out[8]];
    bb = Tyboxes[8][9][out[9]];
    cc = Tyboxes[8][10][out[10]];
    dd = Tyboxes[8][11][out[11]];

    out[8] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[8][12][out[12]];
    bb = Tyboxes[8][13][out[13]];
    cc = Tyboxes[8][14][out[14]];
    dd = Tyboxes[8][15][out[15]];

    out[12] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    /// R9 - Last round which is a bit different
    ShiftRows(out);

    out[ 0] = Tboxes_[ 0][out[ 0]];
    out[ 1] = Tboxes_[ 1][out[ 1]];
    out[ 2] = Tboxes_[ 2][out[ 2]];
    out[ 3] = Tboxes_[ 3][out[ 3]];
    out[ 4] = Tboxes_[ 4][out[ 4]];
    out[ 5] = Tboxes_[ 5][out[ 5]];
    out[ 6] = Tboxes_[ 6][out[ 6]];
    out[ 7] = Tboxes_[ 7][out[ 7]];
    out[ 8] = Tboxes_[ 8][out[ 8]];
    out[ 9] = Tboxes_[ 9][out[ 9]];
    out[10] = Tboxes_[10][out[ 10]];
    out[11] = Tboxes_[11][out[11]];
    out[12] = Tboxes_[12][out[12]];
    out[13] = Tboxes_[13][out[13]];
    out[14] = Tboxes_[14][out[14]];
    out[15] = Tboxes_[15][out[15]];
}

void aes128_enc_wb_final_unrolled_unique(unsigned char in[16], unsigned char out[16])
{
    memcpy(out, in, 16);
    ShiftRows(out);
    unsigned int aa_0 = Tyboxes[0][0][out[0]];
    unsigned int bb_0 = Tyboxes[0][1][out[1]];
    unsigned int cc_0 = Tyboxes[0][2][out[2]];
    unsigned int dd_0 = Tyboxes[0][3][out[3]];
    out[0] = (Txor[Txor[(aa_0 >> 0) & 0xf][(bb_0 >> 0) & 0xf]][Txor[(cc_0 >> 0) & 0xf][(dd_0 >> 0) & 0xf]]) | ((Txor[Txor[(aa_0 >> 4) & 0xf][(bb_0 >> 4) & 0xf]][Txor[(cc_0 >> 4) & 0xf][(dd_0 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_0 >> 8) & 0xf][(bb_0 >> 8) & 0xf]][Txor[(cc_0 >> 8) & 0xf][(dd_0 >> 8) & 0xf]]) | ((Txor[Txor[(aa_0 >> 12) & 0xf][(bb_0 >> 12) & 0xf]][Txor[(cc_0 >> 12) & 0xf][(dd_0 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_0 >> 16) & 0xf][(bb_0 >> 16) & 0xf]][Txor[(cc_0 >> 16) & 0xf][(dd_0 >> 16) & 0xf]]) | ((Txor[Txor[(aa_0 >> 20) & 0xf][(bb_0 >> 20) & 0xf]][Txor[(cc_0 >> 20) & 0xf][(dd_0 >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_0 >> 24) & 0xf][(bb_0 >> 24) & 0xf]][Txor[(cc_0 >> 24) & 0xf][(dd_0 >> 24) & 0xf]]) | ((Txor[Txor[(aa_0 >> 28) & 0xf][(bb_0 >> 28) & 0xf]][Txor[(cc_0 >> 28) & 0xf][(dd_0 >> 28) & 0xf]]) << 4);
    unsigned int aa_1 = Tyboxes[0][4][out[4]];
    unsigned int bb_1 = Tyboxes[0][5][out[5]];
    unsigned int cc_1 = Tyboxes[0][6][out[6]];
    unsigned int dd_1 = Tyboxes[0][7][out[7]];
    out[4] = (Txor[Txor[(aa_1 >> 0) & 0xf][(bb_1 >> 0) & 0xf]][Txor[(cc_1 >> 0) & 0xf][(dd_1 >> 0) & 0xf]]) | ((Txor[Txor[(aa_1 >> 4) & 0xf][(bb_1 >> 4) & 0xf]][Txor[(cc_1 >> 4) & 0xf][(dd_1 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_1 >> 8) & 0xf][(bb_1 >> 8) & 0xf]][Txor[(cc_1 >> 8) & 0xf][(dd_1 >> 8) & 0xf]]) | ((Txor[Txor[(aa_1 >> 12) & 0xf][(bb_1 >> 12) & 0xf]][Txor[(cc_1 >> 12) & 0xf][(dd_1 >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_1 >> 16) & 0xf][(bb_1 >> 16) & 0xf]][Txor[(cc_1 >> 16) & 0xf][(dd_1 >> 16) & 0xf]]) | ((Txor[Txor[(aa_1 >> 20) & 0xf][(bb_1 >> 20) & 0xf]][Txor[(cc_1 >> 20) & 0xf][(dd_1 >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_1 >> 24) & 0xf][(bb_1 >> 24) & 0xf]][Txor[(cc_1 >> 24) & 0xf][(dd_1 >> 24) & 0xf]]) | ((Txor[Txor[(aa_1 >> 28) & 0xf][(bb_1 >> 28) & 0xf]][Txor[(cc_1 >> 28) & 0xf][(dd_1 >> 28) & 0xf]]) << 4);
    unsigned int aa_2 = Tyboxes[0][8][out[8]];
    unsigned int bb_2 = Tyboxes[0][9][out[9]];
    unsigned int cc_2 = Tyboxes[0][10][out[10]];
    unsigned int dd_2 = Tyboxes[0][11][out[11]];
    out[8] = (Txor[Txor[(aa_2 >> 0) & 0xf][(bb_2 >> 0) & 0xf]][Txor[(cc_2 >> 0) & 0xf][(dd_2 >> 0) & 0xf]]) | ((Txor[Txor[(aa_2 >> 4) & 0xf][(bb_2 >> 4) & 0xf]][Txor[(cc_2 >> 4) & 0xf][(dd_2 >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_2 >> 8) & 0xf][(bb_2 >> 8) & 0xf]][Txor[(cc_2 >> 8) & 0xf][(dd_2 >> 8) & 0xf]]) | ((Txor[Txor[(aa_2 >> 12) & 0xf][(bb_2 >> 12) & 0xf]][Txor[(cc_2 >> 12) & 0xf][(dd_2 >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_2 >> 16) & 0xf][(bb_2 >> 16) & 0xf]][Txor[(cc_2 >> 16) & 0xf][(dd_2 >> 16) & 0xf]]) | ((Txor[Txor[(aa_2 >> 20) & 0xf][(bb_2 >> 20) & 0xf]][Txor[(cc_2 >> 20) & 0xf][(dd_2 >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_2 >> 24) & 0xf][(bb_2 >> 24) & 0xf]][Txor[(cc_2 >> 24) & 0xf][(dd_2 >> 24) & 0xf]]) | ((Txor[Txor[(aa_2 >> 28) & 0xf][(bb_2 >> 28) & 0xf]][Txor[(cc_2 >> 28) & 0xf][(dd_2 >> 28) & 0xf]]) << 4);
    unsigned int aa_3 = Tyboxes[0][12][out[12]];
    unsigned int bb_3 = Tyboxes[0][13][out[13]];
    unsigned int cc_3 = Tyboxes[0][14][out[14]];
    unsigned int dd_3 = Tyboxes[0][15][out[15]];
    out[12] = (Txor[Txor[(aa_3 >> 0) & 0xf][(bb_3 >> 0) & 0xf]][Txor[(cc_3 >> 0) & 0xf][(dd_3 >> 0) & 0xf]]) | ((Txor[Txor[(aa_3 >> 4) & 0xf][(bb_3 >> 4) & 0xf]][Txor[(cc_3 >> 4) & 0xf][(dd_3 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_3 >> 8) & 0xf][(bb_3 >> 8) & 0xf]][Txor[(cc_3 >> 8) & 0xf][(dd_3 >> 8) & 0xf]]) | ((Txor[Txor[(aa_3 >> 12) & 0xf][(bb_3 >> 12) & 0xf]][Txor[(cc_3 >> 12) & 0xf][(dd_3 >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_3 >> 16) & 0xf][(bb_3 >> 16) & 0xf]][Txor[(cc_3 >> 16) & 0xf][(dd_3 >> 16) & 0xf]]) | ((Txor[Txor[(aa_3 >> 20) & 0xf][(bb_3 >> 20) & 0xf]][Txor[(cc_3 >> 20) & 0xf][(dd_3 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_3 >> 24) & 0xf][(bb_3 >> 24) & 0xf]][Txor[(cc_3 >> 24) & 0xf][(dd_3 >> 24) & 0xf]]) | ((Txor[Txor[(aa_3 >> 28) & 0xf][(bb_3 >> 28) & 0xf]][Txor[(cc_3 >> 28) & 0xf][(dd_3 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int aa_4 = Tyboxes[1][0][out[0]];
    unsigned int bb_4 = Tyboxes[1][1][out[1]];
    unsigned int cc_4 = Tyboxes[1][2][out[2]];
    unsigned int dd_4 = Tyboxes[1][3][out[3]];
    out[0] = (Txor[Txor[(aa_4 >> 0) & 0xf][(bb_4 >> 0) & 0xf]][Txor[(cc_4 >> 0) & 0xf][(dd_4 >> 0) & 0xf]]) | ((Txor[Txor[(aa_4 >> 4) & 0xf][(bb_4 >> 4) & 0xf]][Txor[(cc_4 >> 4) & 0xf][(dd_4 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_4 >> 8) & 0xf][(bb_4 >> 8) & 0xf]][Txor[(cc_4 >> 8) & 0xf][(dd_4 >> 8) & 0xf]]) | ((Txor[Txor[(aa_4 >> 12) & 0xf][(bb_4 >> 12) & 0xf]][Txor[(cc_4 >> 12) & 0xf][(dd_4 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_4 >> 16) & 0xf][(bb_4 >> 16) & 0xf]][Txor[(cc_4 >> 16) & 0xf][(dd_4 >> 16) & 0xf]]) | ((Txor[Txor[(aa_4 >> 20) & 0xf][(bb_4 >> 20) & 0xf]][Txor[(cc_4 >> 20) & 0xf][(dd_4 >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_4 >> 24) & 0xf][(bb_4 >> 24) & 0xf]][Txor[(cc_4 >> 24) & 0xf][(dd_4 >> 24) & 0xf]]) | ((Txor[Txor[(aa_4 >> 28) & 0xf][(bb_4 >> 28) & 0xf]][Txor[(cc_4 >> 28) & 0xf][(dd_4 >> 28) & 0xf]]) << 4);
    unsigned int aa_5 = Tyboxes[1][4][out[4]];
    unsigned int bb_5 = Tyboxes[1][5][out[5]];
    unsigned int cc_5 = Tyboxes[1][6][out[6]];
    unsigned int dd_5 = Tyboxes[1][7][out[7]];
    out[4] = (Txor[Txor[(aa_5 >> 0) & 0xf][(bb_5 >> 0) & 0xf]][Txor[(cc_5 >> 0) & 0xf][(dd_5 >> 0) & 0xf]]) | ((Txor[Txor[(aa_5 >> 4) & 0xf][(bb_5 >> 4) & 0xf]][Txor[(cc_5 >> 4) & 0xf][(dd_5 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_5 >> 8) & 0xf][(bb_5 >> 8) & 0xf]][Txor[(cc_5 >> 8) & 0xf][(dd_5 >> 8) & 0xf]]) | ((Txor[Txor[(aa_5 >> 12) & 0xf][(bb_5 >> 12) & 0xf]][Txor[(cc_5 >> 12) & 0xf][(dd_5 >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_5 >> 16) & 0xf][(bb_5 >> 16) & 0xf]][Txor[(cc_5 >> 16) & 0xf][(dd_5 >> 16) & 0xf]]) | ((Txor[Txor[(aa_5 >> 20) & 0xf][(bb_5 >> 20) & 0xf]][Txor[(cc_5 >> 20) & 0xf][(dd_5 >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_5 >> 24) & 0xf][(bb_5 >> 24) & 0xf]][Txor[(cc_5 >> 24) & 0xf][(dd_5 >> 24) & 0xf]]) | ((Txor[Txor[(aa_5 >> 28) & 0xf][(bb_5 >> 28) & 0xf]][Txor[(cc_5 >> 28) & 0xf][(dd_5 >> 28) & 0xf]]) << 4);
    unsigned int aa_6 = Tyboxes[1][8][out[8]];
    unsigned int bb_6 = Tyboxes[1][9][out[9]];
    unsigned int cc_6 = Tyboxes[1][10][out[10]];
    unsigned int dd_6 = Tyboxes[1][11][out[11]];
    out[8] = (Txor[Txor[(aa_6 >> 0) & 0xf][(bb_6 >> 0) & 0xf]][Txor[(cc_6 >> 0) & 0xf][(dd_6 >> 0) & 0xf]]) | ((Txor[Txor[(aa_6 >> 4) & 0xf][(bb_6 >> 4) & 0xf]][Txor[(cc_6 >> 4) & 0xf][(dd_6 >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_6 >> 8) & 0xf][(bb_6 >> 8) & 0xf]][Txor[(cc_6 >> 8) & 0xf][(dd_6 >> 8) & 0xf]]) | ((Txor[Txor[(aa_6 >> 12) & 0xf][(bb_6 >> 12) & 0xf]][Txor[(cc_6 >> 12) & 0xf][(dd_6 >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_6 >> 16) & 0xf][(bb_6 >> 16) & 0xf]][Txor[(cc_6 >> 16) & 0xf][(dd_6 >> 16) & 0xf]]) | ((Txor[Txor[(aa_6 >> 20) & 0xf][(bb_6 >> 20) & 0xf]][Txor[(cc_6 >> 20) & 0xf][(dd_6 >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_6 >> 24) & 0xf][(bb_6 >> 24) & 0xf]][Txor[(cc_6 >> 24) & 0xf][(dd_6 >> 24) & 0xf]]) | ((Txor[Txor[(aa_6 >> 28) & 0xf][(bb_6 >> 28) & 0xf]][Txor[(cc_6 >> 28) & 0xf][(dd_6 >> 28) & 0xf]]) << 4);
    unsigned int aa_7 = Tyboxes[1][12][out[12]];
    unsigned int bb_7 = Tyboxes[1][13][out[13]];
    unsigned int cc_7 = Tyboxes[1][14][out[14]];
    unsigned int dd_7 = Tyboxes[1][15][out[15]];
    out[12] = (Txor[Txor[(aa_7 >> 0) & 0xf][(bb_7 >> 0) & 0xf]][Txor[(cc_7 >> 0) & 0xf][(dd_7 >> 0) & 0xf]]) | ((Txor[Txor[(aa_7 >> 4) & 0xf][(bb_7 >> 4) & 0xf]][Txor[(cc_7 >> 4) & 0xf][(dd_7 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_7 >> 8) & 0xf][(bb_7 >> 8) & 0xf]][Txor[(cc_7 >> 8) & 0xf][(dd_7 >> 8) & 0xf]]) | ((Txor[Txor[(aa_7 >> 12) & 0xf][(bb_7 >> 12) & 0xf]][Txor[(cc_7 >> 12) & 0xf][(dd_7 >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_7 >> 16) & 0xf][(bb_7 >> 16) & 0xf]][Txor[(cc_7 >> 16) & 0xf][(dd_7 >> 16) & 0xf]]) | ((Txor[Txor[(aa_7 >> 20) & 0xf][(bb_7 >> 20) & 0xf]][Txor[(cc_7 >> 20) & 0xf][(dd_7 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_7 >> 24) & 0xf][(bb_7 >> 24) & 0xf]][Txor[(cc_7 >> 24) & 0xf][(dd_7 >> 24) & 0xf]]) | ((Txor[Txor[(aa_7 >> 28) & 0xf][(bb_7 >> 28) & 0xf]][Txor[(cc_7 >> 28) & 0xf][(dd_7 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int aa_8 = Tyboxes[2][0][out[0]];
    unsigned int bb_8 = Tyboxes[2][1][out[1]];
    unsigned int cc_8 = Tyboxes[2][2][out[2]];
    unsigned int dd_8 = Tyboxes[2][3][out[3]];
    out[0] = (Txor[Txor[(aa_8 >> 0) & 0xf][(bb_8 >> 0) & 0xf]][Txor[(cc_8 >> 0) & 0xf][(dd_8 >> 0) & 0xf]]) | ((Txor[Txor[(aa_8 >> 4) & 0xf][(bb_8 >> 4) & 0xf]][Txor[(cc_8 >> 4) & 0xf][(dd_8 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_8 >> 8) & 0xf][(bb_8 >> 8) & 0xf]][Txor[(cc_8 >> 8) & 0xf][(dd_8 >> 8) & 0xf]]) | ((Txor[Txor[(aa_8 >> 12) & 0xf][(bb_8 >> 12) & 0xf]][Txor[(cc_8 >> 12) & 0xf][(dd_8 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_8 >> 16) & 0xf][(bb_8 >> 16) & 0xf]][Txor[(cc_8 >> 16) & 0xf][(dd_8 >> 16) & 0xf]]) | ((Txor[Txor[(aa_8 >> 20) & 0xf][(bb_8 >> 20) & 0xf]][Txor[(cc_8 >> 20) & 0xf][(dd_8 >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_8 >> 24) & 0xf][(bb_8 >> 24) & 0xf]][Txor[(cc_8 >> 24) & 0xf][(dd_8 >> 24) & 0xf]]) | ((Txor[Txor[(aa_8 >> 28) & 0xf][(bb_8 >> 28) & 0xf]][Txor[(cc_8 >> 28) & 0xf][(dd_8 >> 28) & 0xf]]) << 4);
    unsigned int aa_9 = Tyboxes[2][4][out[4]];
    unsigned int bb_9 = Tyboxes[2][5][out[5]];
    unsigned int cc_9 = Tyboxes[2][6][out[6]];
    unsigned int dd_9 = Tyboxes[2][7][out[7]];
    out[4] = (Txor[Txor[(aa_9 >> 0) & 0xf][(bb_9 >> 0) & 0xf]][Txor[(cc_9 >> 0) & 0xf][(dd_9 >> 0) & 0xf]]) | ((Txor[Txor[(aa_9 >> 4) & 0xf][(bb_9 >> 4) & 0xf]][Txor[(cc_9 >> 4) & 0xf][(dd_9 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_9 >> 8) & 0xf][(bb_9 >> 8) & 0xf]][Txor[(cc_9 >> 8) & 0xf][(dd_9 >> 8) & 0xf]]) | ((Txor[Txor[(aa_9 >> 12) & 0xf][(bb_9 >> 12) & 0xf]][Txor[(cc_9 >> 12) & 0xf][(dd_9 >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_9 >> 16) & 0xf][(bb_9 >> 16) & 0xf]][Txor[(cc_9 >> 16) & 0xf][(dd_9 >> 16) & 0xf]]) | ((Txor[Txor[(aa_9 >> 20) & 0xf][(bb_9 >> 20) & 0xf]][Txor[(cc_9 >> 20) & 0xf][(dd_9 >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_9 >> 24) & 0xf][(bb_9 >> 24) & 0xf]][Txor[(cc_9 >> 24) & 0xf][(dd_9 >> 24) & 0xf]]) | ((Txor[Txor[(aa_9 >> 28) & 0xf][(bb_9 >> 28) & 0xf]][Txor[(cc_9 >> 28) & 0xf][(dd_9 >> 28) & 0xf]]) << 4);
    unsigned int aa_10 = Tyboxes[2][8][out[8]];
    unsigned int bb_10 = Tyboxes[2][9][out[9]];
    unsigned int cc_10 = Tyboxes[2][10][out[10]];
    unsigned int dd_10 = Tyboxes[2][11][out[11]];
    out[8] = (Txor[Txor[(aa_10 >> 0) & 0xf][(bb_10 >> 0) & 0xf]][Txor[(cc_10 >> 0) & 0xf][(dd_10 >> 0) & 0xf]]) | ((Txor[Txor[(aa_10 >> 4) & 0xf][(bb_10 >> 4) & 0xf]][Txor[(cc_10 >> 4) & 0xf][(dd_10 >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_10 >> 8) & 0xf][(bb_10 >> 8) & 0xf]][Txor[(cc_10 >> 8) & 0xf][(dd_10 >> 8) & 0xf]]) | ((Txor[Txor[(aa_10 >> 12) & 0xf][(bb_10 >> 12) & 0xf]][Txor[(cc_10 >> 12) & 0xf][(dd_10 >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_10 >> 16) & 0xf][(bb_10 >> 16) & 0xf]][Txor[(cc_10 >> 16) & 0xf][(dd_10 >> 16) & 0xf]]) | ((Txor[Txor[(aa_10 >> 20) & 0xf][(bb_10 >> 20) & 0xf]][Txor[(cc_10 >> 20) & 0xf][(dd_10 >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_10 >> 24) & 0xf][(bb_10 >> 24) & 0xf]][Txor[(cc_10 >> 24) & 0xf][(dd_10 >> 24) & 0xf]]) | ((Txor[Txor[(aa_10 >> 28) & 0xf][(bb_10 >> 28) & 0xf]][Txor[(cc_10 >> 28) & 0xf][(dd_10 >> 28) & 0xf]]) << 4);
    unsigned int aa_11 = Tyboxes[2][12][out[12]];
    unsigned int bb_11 = Tyboxes[2][13][out[13]];
    unsigned int cc_11 = Tyboxes[2][14][out[14]];
    unsigned int dd_11 = Tyboxes[2][15][out[15]];
    out[12] = (Txor[Txor[(aa_11 >> 0) & 0xf][(bb_11 >> 0) & 0xf]][Txor[(cc_11 >> 0) & 0xf][(dd_11 >> 0) & 0xf]]) | ((Txor[Txor[(aa_11 >> 4) & 0xf][(bb_11 >> 4) & 0xf]][Txor[(cc_11 >> 4) & 0xf][(dd_11 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_11 >> 8) & 0xf][(bb_11 >> 8) & 0xf]][Txor[(cc_11 >> 8) & 0xf][(dd_11 >> 8) & 0xf]]) | ((Txor[Txor[(aa_11 >> 12) & 0xf][(bb_11 >> 12) & 0xf]][Txor[(cc_11 >> 12) & 0xf][(dd_11 >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_11 >> 16) & 0xf][(bb_11 >> 16) & 0xf]][Txor[(cc_11 >> 16) & 0xf][(dd_11 >> 16) & 0xf]]) | ((Txor[Txor[(aa_11 >> 20) & 0xf][(bb_11 >> 20) & 0xf]][Txor[(cc_11 >> 20) & 0xf][(dd_11 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_11 >> 24) & 0xf][(bb_11 >> 24) & 0xf]][Txor[(cc_11 >> 24) & 0xf][(dd_11 >> 24) & 0xf]]) | ((Txor[Txor[(aa_11 >> 28) & 0xf][(bb_11 >> 28) & 0xf]][Txor[(cc_11 >> 28) & 0xf][(dd_11 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int aa_12 = Tyboxes[3][0][out[0]];
    unsigned int bb_12 = Tyboxes[3][1][out[1]];
    unsigned int cc_12 = Tyboxes[3][2][out[2]];
    unsigned int dd_12 = Tyboxes[3][3][out[3]];
    out[0] = (Txor[Txor[(aa_12 >> 0) & 0xf][(bb_12 >> 0) & 0xf]][Txor[(cc_12 >> 0) & 0xf][(dd_12 >> 0) & 0xf]]) | ((Txor[Txor[(aa_12 >> 4) & 0xf][(bb_12 >> 4) & 0xf]][Txor[(cc_12 >> 4) & 0xf][(dd_12 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_12 >> 8) & 0xf][(bb_12 >> 8) & 0xf]][Txor[(cc_12 >> 8) & 0xf][(dd_12 >> 8) & 0xf]]) | ((Txor[Txor[(aa_12 >> 12) & 0xf][(bb_12 >> 12) & 0xf]][Txor[(cc_12 >> 12) & 0xf][(dd_12 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_12 >> 16) & 0xf][(bb_12 >> 16) & 0xf]][Txor[(cc_12 >> 16) & 0xf][(dd_12 >> 16) & 0xf]]) | ((Txor[Txor[(aa_12 >> 20) & 0xf][(bb_12 >> 20) & 0xf]][Txor[(cc_12 >> 20) & 0xf][(dd_12 >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_12 >> 24) & 0xf][(bb_12 >> 24) & 0xf]][Txor[(cc_12 >> 24) & 0xf][(dd_12 >> 24) & 0xf]]) | ((Txor[Txor[(aa_12 >> 28) & 0xf][(bb_12 >> 28) & 0xf]][Txor[(cc_12 >> 28) & 0xf][(dd_12 >> 28) & 0xf]]) << 4);
    unsigned int aa_13 = Tyboxes[3][4][out[4]];
    unsigned int bb_13 = Tyboxes[3][5][out[5]];
    unsigned int cc_13 = Tyboxes[3][6][out[6]];
    unsigned int dd_13 = Tyboxes[3][7][out[7]];
    out[4] = (Txor[Txor[(aa_13 >> 0) & 0xf][(bb_13 >> 0) & 0xf]][Txor[(cc_13 >> 0) & 0xf][(dd_13 >> 0) & 0xf]]) | ((Txor[Txor[(aa_13 >> 4) & 0xf][(bb_13 >> 4) & 0xf]][Txor[(cc_13 >> 4) & 0xf][(dd_13 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_13 >> 8) & 0xf][(bb_13 >> 8) & 0xf]][Txor[(cc_13 >> 8) & 0xf][(dd_13 >> 8) & 0xf]]) | ((Txor[Txor[(aa_13 >> 12) & 0xf][(bb_13 >> 12) & 0xf]][Txor[(cc_13 >> 12) & 0xf][(dd_13 >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_13 >> 16) & 0xf][(bb_13 >> 16) & 0xf]][Txor[(cc_13 >> 16) & 0xf][(dd_13 >> 16) & 0xf]]) | ((Txor[Txor[(aa_13 >> 20) & 0xf][(bb_13 >> 20) & 0xf]][Txor[(cc_13 >> 20) & 0xf][(dd_13 >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_13 >> 24) & 0xf][(bb_13 >> 24) & 0xf]][Txor[(cc_13 >> 24) & 0xf][(dd_13 >> 24) & 0xf]]) | ((Txor[Txor[(aa_13 >> 28) & 0xf][(bb_13 >> 28) & 0xf]][Txor[(cc_13 >> 28) & 0xf][(dd_13 >> 28) & 0xf]]) << 4);
    unsigned int aa_14 = Tyboxes[3][8][out[8]];
    unsigned int bb_14 = Tyboxes[3][9][out[9]];
    unsigned int cc_14 = Tyboxes[3][10][out[10]];
    unsigned int dd_14 = Tyboxes[3][11][out[11]];
    out[8] = (Txor[Txor[(aa_14 >> 0) & 0xf][(bb_14 >> 0) & 0xf]][Txor[(cc_14 >> 0) & 0xf][(dd_14 >> 0) & 0xf]]) | ((Txor[Txor[(aa_14 >> 4) & 0xf][(bb_14 >> 4) & 0xf]][Txor[(cc_14 >> 4) & 0xf][(dd_14 >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_14 >> 8) & 0xf][(bb_14 >> 8) & 0xf]][Txor[(cc_14 >> 8) & 0xf][(dd_14 >> 8) & 0xf]]) | ((Txor[Txor[(aa_14 >> 12) & 0xf][(bb_14 >> 12) & 0xf]][Txor[(cc_14 >> 12) & 0xf][(dd_14 >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_14 >> 16) & 0xf][(bb_14 >> 16) & 0xf]][Txor[(cc_14 >> 16) & 0xf][(dd_14 >> 16) & 0xf]]) | ((Txor[Txor[(aa_14 >> 20) & 0xf][(bb_14 >> 20) & 0xf]][Txor[(cc_14 >> 20) & 0xf][(dd_14 >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_14 >> 24) & 0xf][(bb_14 >> 24) & 0xf]][Txor[(cc_14 >> 24) & 0xf][(dd_14 >> 24) & 0xf]]) | ((Txor[Txor[(aa_14 >> 28) & 0xf][(bb_14 >> 28) & 0xf]][Txor[(cc_14 >> 28) & 0xf][(dd_14 >> 28) & 0xf]]) << 4);
    unsigned int aa_15 = Tyboxes[3][12][out[12]];
    unsigned int bb_15 = Tyboxes[3][13][out[13]];
    unsigned int cc_15 = Tyboxes[3][14][out[14]];
    unsigned int dd_15 = Tyboxes[3][15][out[15]];
    out[12] = (Txor[Txor[(aa_15 >> 0) & 0xf][(bb_15 >> 0) & 0xf]][Txor[(cc_15 >> 0) & 0xf][(dd_15 >> 0) & 0xf]]) | ((Txor[Txor[(aa_15 >> 4) & 0xf][(bb_15 >> 4) & 0xf]][Txor[(cc_15 >> 4) & 0xf][(dd_15 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_15 >> 8) & 0xf][(bb_15 >> 8) & 0xf]][Txor[(cc_15 >> 8) & 0xf][(dd_15 >> 8) & 0xf]]) | ((Txor[Txor[(aa_15 >> 12) & 0xf][(bb_15 >> 12) & 0xf]][Txor[(cc_15 >> 12) & 0xf][(dd_15 >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_15 >> 16) & 0xf][(bb_15 >> 16) & 0xf]][Txor[(cc_15 >> 16) & 0xf][(dd_15 >> 16) & 0xf]]) | ((Txor[Txor[(aa_15 >> 20) & 0xf][(bb_15 >> 20) & 0xf]][Txor[(cc_15 >> 20) & 0xf][(dd_15 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_15 >> 24) & 0xf][(bb_15 >> 24) & 0xf]][Txor[(cc_15 >> 24) & 0xf][(dd_15 >> 24) & 0xf]]) | ((Txor[Txor[(aa_15 >> 28) & 0xf][(bb_15 >> 28) & 0xf]][Txor[(cc_15 >> 28) & 0xf][(dd_15 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int aa_16 = Tyboxes[4][0][out[0]];
    unsigned int bb_16 = Tyboxes[4][1][out[1]];
    unsigned int cc_16 = Tyboxes[4][2][out[2]];
    unsigned int dd_16 = Tyboxes[4][3][out[3]];
    out[0] = (Txor[Txor[(aa_16 >> 0) & 0xf][(bb_16 >> 0) & 0xf]][Txor[(cc_16 >> 0) & 0xf][(dd_16 >> 0) & 0xf]]) | ((Txor[Txor[(aa_16 >> 4) & 0xf][(bb_16 >> 4) & 0xf]][Txor[(cc_16 >> 4) & 0xf][(dd_16 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_16 >> 8) & 0xf][(bb_16 >> 8) & 0xf]][Txor[(cc_16 >> 8) & 0xf][(dd_16 >> 8) & 0xf]]) | ((Txor[Txor[(aa_16 >> 12) & 0xf][(bb_16 >> 12) & 0xf]][Txor[(cc_16 >> 12) & 0xf][(dd_16 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_16 >> 16) & 0xf][(bb_16 >> 16) & 0xf]][Txor[(cc_16 >> 16) & 0xf][(dd_16 >> 16) & 0xf]]) | ((Txor[Txor[(aa_16 >> 20) & 0xf][(bb_16 >> 20) & 0xf]][Txor[(cc_16 >> 20) & 0xf][(dd_16 >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_16 >> 24) & 0xf][(bb_16 >> 24) & 0xf]][Txor[(cc_16 >> 24) & 0xf][(dd_16 >> 24) & 0xf]]) | ((Txor[Txor[(aa_16 >> 28) & 0xf][(bb_16 >> 28) & 0xf]][Txor[(cc_16 >> 28) & 0xf][(dd_16 >> 28) & 0xf]]) << 4);
    unsigned int aa_17 = Tyboxes[4][4][out[4]];
    unsigned int bb_17 = Tyboxes[4][5][out[5]];
    unsigned int cc_17 = Tyboxes[4][6][out[6]];
    unsigned int dd_17 = Tyboxes[4][7][out[7]];
    out[4] = (Txor[Txor[(aa_17 >> 0) & 0xf][(bb_17 >> 0) & 0xf]][Txor[(cc_17 >> 0) & 0xf][(dd_17 >> 0) & 0xf]]) | ((Txor[Txor[(aa_17 >> 4) & 0xf][(bb_17 >> 4) & 0xf]][Txor[(cc_17 >> 4) & 0xf][(dd_17 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_17 >> 8) & 0xf][(bb_17 >> 8) & 0xf]][Txor[(cc_17 >> 8) & 0xf][(dd_17 >> 8) & 0xf]]) | ((Txor[Txor[(aa_17 >> 12) & 0xf][(bb_17 >> 12) & 0xf]][Txor[(cc_17 >> 12) & 0xf][(dd_17 >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_17 >> 16) & 0xf][(bb_17 >> 16) & 0xf]][Txor[(cc_17 >> 16) & 0xf][(dd_17 >> 16) & 0xf]]) | ((Txor[Txor[(aa_17 >> 20) & 0xf][(bb_17 >> 20) & 0xf]][Txor[(cc_17 >> 20) & 0xf][(dd_17 >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_17 >> 24) & 0xf][(bb_17 >> 24) & 0xf]][Txor[(cc_17 >> 24) & 0xf][(dd_17 >> 24) & 0xf]]) | ((Txor[Txor[(aa_17 >> 28) & 0xf][(bb_17 >> 28) & 0xf]][Txor[(cc_17 >> 28) & 0xf][(dd_17 >> 28) & 0xf]]) << 4);
    unsigned int aa_18 = Tyboxes[4][8][out[8]];
    unsigned int bb_18 = Tyboxes[4][9][out[9]];
    unsigned int cc_18 = Tyboxes[4][10][out[10]];
    unsigned int dd_18 = Tyboxes[4][11][out[11]];
    out[8] = (Txor[Txor[(aa_18 >> 0) & 0xf][(bb_18 >> 0) & 0xf]][Txor[(cc_18 >> 0) & 0xf][(dd_18 >> 0) & 0xf]]) | ((Txor[Txor[(aa_18 >> 4) & 0xf][(bb_18 >> 4) & 0xf]][Txor[(cc_18 >> 4) & 0xf][(dd_18 >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_18 >> 8) & 0xf][(bb_18 >> 8) & 0xf]][Txor[(cc_18 >> 8) & 0xf][(dd_18 >> 8) & 0xf]]) | ((Txor[Txor[(aa_18 >> 12) & 0xf][(bb_18 >> 12) & 0xf]][Txor[(cc_18 >> 12) & 0xf][(dd_18 >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_18 >> 16) & 0xf][(bb_18 >> 16) & 0xf]][Txor[(cc_18 >> 16) & 0xf][(dd_18 >> 16) & 0xf]]) | ((Txor[Txor[(aa_18 >> 20) & 0xf][(bb_18 >> 20) & 0xf]][Txor[(cc_18 >> 20) & 0xf][(dd_18 >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_18 >> 24) & 0xf][(bb_18 >> 24) & 0xf]][Txor[(cc_18 >> 24) & 0xf][(dd_18 >> 24) & 0xf]]) | ((Txor[Txor[(aa_18 >> 28) & 0xf][(bb_18 >> 28) & 0xf]][Txor[(cc_18 >> 28) & 0xf][(dd_18 >> 28) & 0xf]]) << 4);
    unsigned int aa_19 = Tyboxes[4][12][out[12]];
    unsigned int bb_19 = Tyboxes[4][13][out[13]];
    unsigned int cc_19 = Tyboxes[4][14][out[14]];
    unsigned int dd_19 = Tyboxes[4][15][out[15]];
    out[12] = (Txor[Txor[(aa_19 >> 0) & 0xf][(bb_19 >> 0) & 0xf]][Txor[(cc_19 >> 0) & 0xf][(dd_19 >> 0) & 0xf]]) | ((Txor[Txor[(aa_19 >> 4) & 0xf][(bb_19 >> 4) & 0xf]][Txor[(cc_19 >> 4) & 0xf][(dd_19 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_19 >> 8) & 0xf][(bb_19 >> 8) & 0xf]][Txor[(cc_19 >> 8) & 0xf][(dd_19 >> 8) & 0xf]]) | ((Txor[Txor[(aa_19 >> 12) & 0xf][(bb_19 >> 12) & 0xf]][Txor[(cc_19 >> 12) & 0xf][(dd_19 >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_19 >> 16) & 0xf][(bb_19 >> 16) & 0xf]][Txor[(cc_19 >> 16) & 0xf][(dd_19 >> 16) & 0xf]]) | ((Txor[Txor[(aa_19 >> 20) & 0xf][(bb_19 >> 20) & 0xf]][Txor[(cc_19 >> 20) & 0xf][(dd_19 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_19 >> 24) & 0xf][(bb_19 >> 24) & 0xf]][Txor[(cc_19 >> 24) & 0xf][(dd_19 >> 24) & 0xf]]) | ((Txor[Txor[(aa_19 >> 28) & 0xf][(bb_19 >> 28) & 0xf]][Txor[(cc_19 >> 28) & 0xf][(dd_19 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int aa_20 = Tyboxes[5][0][out[0]];
    unsigned int bb_20 = Tyboxes[5][1][out[1]];
    unsigned int cc_20 = Tyboxes[5][2][out[2]];
    unsigned int dd_20 = Tyboxes[5][3][out[3]];
    out[0] = (Txor[Txor[(aa_20 >> 0) & 0xf][(bb_20 >> 0) & 0xf]][Txor[(cc_20 >> 0) & 0xf][(dd_20 >> 0) & 0xf]]) | ((Txor[Txor[(aa_20 >> 4) & 0xf][(bb_20 >> 4) & 0xf]][Txor[(cc_20 >> 4) & 0xf][(dd_20 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_20 >> 8) & 0xf][(bb_20 >> 8) & 0xf]][Txor[(cc_20 >> 8) & 0xf][(dd_20 >> 8) & 0xf]]) | ((Txor[Txor[(aa_20 >> 12) & 0xf][(bb_20 >> 12) & 0xf]][Txor[(cc_20 >> 12) & 0xf][(dd_20 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_20 >> 16) & 0xf][(bb_20 >> 16) & 0xf]][Txor[(cc_20 >> 16) & 0xf][(dd_20 >> 16) & 0xf]]) | ((Txor[Txor[(aa_20 >> 20) & 0xf][(bb_20 >> 20) & 0xf]][Txor[(cc_20 >> 20) & 0xf][(dd_20 >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_20 >> 24) & 0xf][(bb_20 >> 24) & 0xf]][Txor[(cc_20 >> 24) & 0xf][(dd_20 >> 24) & 0xf]]) | ((Txor[Txor[(aa_20 >> 28) & 0xf][(bb_20 >> 28) & 0xf]][Txor[(cc_20 >> 28) & 0xf][(dd_20 >> 28) & 0xf]]) << 4);
    unsigned int aa_21 = Tyboxes[5][4][out[4]];
    unsigned int bb_21 = Tyboxes[5][5][out[5]];
    unsigned int cc_21 = Tyboxes[5][6][out[6]];
    unsigned int dd_21 = Tyboxes[5][7][out[7]];
    out[4] = (Txor[Txor[(aa_21 >> 0) & 0xf][(bb_21 >> 0) & 0xf]][Txor[(cc_21 >> 0) & 0xf][(dd_21 >> 0) & 0xf]]) | ((Txor[Txor[(aa_21 >> 4) & 0xf][(bb_21 >> 4) & 0xf]][Txor[(cc_21 >> 4) & 0xf][(dd_21 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_21 >> 8) & 0xf][(bb_21 >> 8) & 0xf]][Txor[(cc_21 >> 8) & 0xf][(dd_21 >> 8) & 0xf]]) | ((Txor[Txor[(aa_21 >> 12) & 0xf][(bb_21 >> 12) & 0xf]][Txor[(cc_21 >> 12) & 0xf][(dd_21 >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_21 >> 16) & 0xf][(bb_21 >> 16) & 0xf]][Txor[(cc_21 >> 16) & 0xf][(dd_21 >> 16) & 0xf]]) | ((Txor[Txor[(aa_21 >> 20) & 0xf][(bb_21 >> 20) & 0xf]][Txor[(cc_21 >> 20) & 0xf][(dd_21 >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_21 >> 24) & 0xf][(bb_21 >> 24) & 0xf]][Txor[(cc_21 >> 24) & 0xf][(dd_21 >> 24) & 0xf]]) | ((Txor[Txor[(aa_21 >> 28) & 0xf][(bb_21 >> 28) & 0xf]][Txor[(cc_21 >> 28) & 0xf][(dd_21 >> 28) & 0xf]]) << 4);
    unsigned int aa_22 = Tyboxes[5][8][out[8]];
    unsigned int bb_22 = Tyboxes[5][9][out[9]];
    unsigned int cc_22 = Tyboxes[5][10][out[10]];
    unsigned int dd_22 = Tyboxes[5][11][out[11]];
    out[8] = (Txor[Txor[(aa_22 >> 0) & 0xf][(bb_22 >> 0) & 0xf]][Txor[(cc_22 >> 0) & 0xf][(dd_22 >> 0) & 0xf]]) | ((Txor[Txor[(aa_22 >> 4) & 0xf][(bb_22 >> 4) & 0xf]][Txor[(cc_22 >> 4) & 0xf][(dd_22 >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_22 >> 8) & 0xf][(bb_22 >> 8) & 0xf]][Txor[(cc_22 >> 8) & 0xf][(dd_22 >> 8) & 0xf]]) | ((Txor[Txor[(aa_22 >> 12) & 0xf][(bb_22 >> 12) & 0xf]][Txor[(cc_22 >> 12) & 0xf][(dd_22 >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_22 >> 16) & 0xf][(bb_22 >> 16) & 0xf]][Txor[(cc_22 >> 16) & 0xf][(dd_22 >> 16) & 0xf]]) | ((Txor[Txor[(aa_22 >> 20) & 0xf][(bb_22 >> 20) & 0xf]][Txor[(cc_22 >> 20) & 0xf][(dd_22 >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_22 >> 24) & 0xf][(bb_22 >> 24) & 0xf]][Txor[(cc_22 >> 24) & 0xf][(dd_22 >> 24) & 0xf]]) | ((Txor[Txor[(aa_22 >> 28) & 0xf][(bb_22 >> 28) & 0xf]][Txor[(cc_22 >> 28) & 0xf][(dd_22 >> 28) & 0xf]]) << 4);
    unsigned int aa_23 = Tyboxes[5][12][out[12]];
    unsigned int bb_23 = Tyboxes[5][13][out[13]];
    unsigned int cc_23 = Tyboxes[5][14][out[14]];
    unsigned int dd_23 = Tyboxes[5][15][out[15]];
    out[12] = (Txor[Txor[(aa_23 >> 0) & 0xf][(bb_23 >> 0) & 0xf]][Txor[(cc_23 >> 0) & 0xf][(dd_23 >> 0) & 0xf]]) | ((Txor[Txor[(aa_23 >> 4) & 0xf][(bb_23 >> 4) & 0xf]][Txor[(cc_23 >> 4) & 0xf][(dd_23 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_23 >> 8) & 0xf][(bb_23 >> 8) & 0xf]][Txor[(cc_23 >> 8) & 0xf][(dd_23 >> 8) & 0xf]]) | ((Txor[Txor[(aa_23 >> 12) & 0xf][(bb_23 >> 12) & 0xf]][Txor[(cc_23 >> 12) & 0xf][(dd_23 >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_23 >> 16) & 0xf][(bb_23 >> 16) & 0xf]][Txor[(cc_23 >> 16) & 0xf][(dd_23 >> 16) & 0xf]]) | ((Txor[Txor[(aa_23 >> 20) & 0xf][(bb_23 >> 20) & 0xf]][Txor[(cc_23 >> 20) & 0xf][(dd_23 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_23 >> 24) & 0xf][(bb_23 >> 24) & 0xf]][Txor[(cc_23 >> 24) & 0xf][(dd_23 >> 24) & 0xf]]) | ((Txor[Txor[(aa_23 >> 28) & 0xf][(bb_23 >> 28) & 0xf]][Txor[(cc_23 >> 28) & 0xf][(dd_23 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int aa_24 = Tyboxes[6][0][out[0]];
    unsigned int bb_24 = Tyboxes[6][1][out[1]];
    unsigned int cc_24 = Tyboxes[6][2][out[2]];
    unsigned int dd_24 = Tyboxes[6][3][out[3]];
    out[0] = (Txor[Txor[(aa_24 >> 0) & 0xf][(bb_24 >> 0) & 0xf]][Txor[(cc_24 >> 0) & 0xf][(dd_24 >> 0) & 0xf]]) | ((Txor[Txor[(aa_24 >> 4) & 0xf][(bb_24 >> 4) & 0xf]][Txor[(cc_24 >> 4) & 0xf][(dd_24 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_24 >> 8) & 0xf][(bb_24 >> 8) & 0xf]][Txor[(cc_24 >> 8) & 0xf][(dd_24 >> 8) & 0xf]]) | ((Txor[Txor[(aa_24 >> 12) & 0xf][(bb_24 >> 12) & 0xf]][Txor[(cc_24 >> 12) & 0xf][(dd_24 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_24 >> 16) & 0xf][(bb_24 >> 16) & 0xf]][Txor[(cc_24 >> 16) & 0xf][(dd_24 >> 16) & 0xf]]) | ((Txor[Txor[(aa_24 >> 20) & 0xf][(bb_24 >> 20) & 0xf]][Txor[(cc_24 >> 20) & 0xf][(dd_24 >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_24 >> 24) & 0xf][(bb_24 >> 24) & 0xf]][Txor[(cc_24 >> 24) & 0xf][(dd_24 >> 24) & 0xf]]) | ((Txor[Txor[(aa_24 >> 28) & 0xf][(bb_24 >> 28) & 0xf]][Txor[(cc_24 >> 28) & 0xf][(dd_24 >> 28) & 0xf]]) << 4);
    unsigned int aa_25 = Tyboxes[6][4][out[4]];
    unsigned int bb_25 = Tyboxes[6][5][out[5]];
    unsigned int cc_25 = Tyboxes[6][6][out[6]];
    unsigned int dd_25 = Tyboxes[6][7][out[7]];
    out[4] = (Txor[Txor[(aa_25 >> 0) & 0xf][(bb_25 >> 0) & 0xf]][Txor[(cc_25 >> 0) & 0xf][(dd_25 >> 0) & 0xf]]) | ((Txor[Txor[(aa_25 >> 4) & 0xf][(bb_25 >> 4) & 0xf]][Txor[(cc_25 >> 4) & 0xf][(dd_25 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_25 >> 8) & 0xf][(bb_25 >> 8) & 0xf]][Txor[(cc_25 >> 8) & 0xf][(dd_25 >> 8) & 0xf]]) | ((Txor[Txor[(aa_25 >> 12) & 0xf][(bb_25 >> 12) & 0xf]][Txor[(cc_25 >> 12) & 0xf][(dd_25 >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_25 >> 16) & 0xf][(bb_25 >> 16) & 0xf]][Txor[(cc_25 >> 16) & 0xf][(dd_25 >> 16) & 0xf]]) | ((Txor[Txor[(aa_25 >> 20) & 0xf][(bb_25 >> 20) & 0xf]][Txor[(cc_25 >> 20) & 0xf][(dd_25 >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_25 >> 24) & 0xf][(bb_25 >> 24) & 0xf]][Txor[(cc_25 >> 24) & 0xf][(dd_25 >> 24) & 0xf]]) | ((Txor[Txor[(aa_25 >> 28) & 0xf][(bb_25 >> 28) & 0xf]][Txor[(cc_25 >> 28) & 0xf][(dd_25 >> 28) & 0xf]]) << 4);
    unsigned int aa_26 = Tyboxes[6][8][out[8]];
    unsigned int bb_26 = Tyboxes[6][9][out[9]];
    unsigned int cc_26 = Tyboxes[6][10][out[10]];
    unsigned int dd_26 = Tyboxes[6][11][out[11]];
    out[8] = (Txor[Txor[(aa_26 >> 0) & 0xf][(bb_26 >> 0) & 0xf]][Txor[(cc_26 >> 0) & 0xf][(dd_26 >> 0) & 0xf]]) | ((Txor[Txor[(aa_26 >> 4) & 0xf][(bb_26 >> 4) & 0xf]][Txor[(cc_26 >> 4) & 0xf][(dd_26 >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_26 >> 8) & 0xf][(bb_26 >> 8) & 0xf]][Txor[(cc_26 >> 8) & 0xf][(dd_26 >> 8) & 0xf]]) | ((Txor[Txor[(aa_26 >> 12) & 0xf][(bb_26 >> 12) & 0xf]][Txor[(cc_26 >> 12) & 0xf][(dd_26 >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_26 >> 16) & 0xf][(bb_26 >> 16) & 0xf]][Txor[(cc_26 >> 16) & 0xf][(dd_26 >> 16) & 0xf]]) | ((Txor[Txor[(aa_26 >> 20) & 0xf][(bb_26 >> 20) & 0xf]][Txor[(cc_26 >> 20) & 0xf][(dd_26 >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_26 >> 24) & 0xf][(bb_26 >> 24) & 0xf]][Txor[(cc_26 >> 24) & 0xf][(dd_26 >> 24) & 0xf]]) | ((Txor[Txor[(aa_26 >> 28) & 0xf][(bb_26 >> 28) & 0xf]][Txor[(cc_26 >> 28) & 0xf][(dd_26 >> 28) & 0xf]]) << 4);
    unsigned int aa_27 = Tyboxes[6][12][out[12]];
    unsigned int bb_27 = Tyboxes[6][13][out[13]];
    unsigned int cc_27 = Tyboxes[6][14][out[14]];
    unsigned int dd_27 = Tyboxes[6][15][out[15]];
    out[12] = (Txor[Txor[(aa_27 >> 0) & 0xf][(bb_27 >> 0) & 0xf]][Txor[(cc_27 >> 0) & 0xf][(dd_27 >> 0) & 0xf]]) | ((Txor[Txor[(aa_27 >> 4) & 0xf][(bb_27 >> 4) & 0xf]][Txor[(cc_27 >> 4) & 0xf][(dd_27 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_27 >> 8) & 0xf][(bb_27 >> 8) & 0xf]][Txor[(cc_27 >> 8) & 0xf][(dd_27 >> 8) & 0xf]]) | ((Txor[Txor[(aa_27 >> 12) & 0xf][(bb_27 >> 12) & 0xf]][Txor[(cc_27 >> 12) & 0xf][(dd_27 >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_27 >> 16) & 0xf][(bb_27 >> 16) & 0xf]][Txor[(cc_27 >> 16) & 0xf][(dd_27 >> 16) & 0xf]]) | ((Txor[Txor[(aa_27 >> 20) & 0xf][(bb_27 >> 20) & 0xf]][Txor[(cc_27 >> 20) & 0xf][(dd_27 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_27 >> 24) & 0xf][(bb_27 >> 24) & 0xf]][Txor[(cc_27 >> 24) & 0xf][(dd_27 >> 24) & 0xf]]) | ((Txor[Txor[(aa_27 >> 28) & 0xf][(bb_27 >> 28) & 0xf]][Txor[(cc_27 >> 28) & 0xf][(dd_27 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int aa_28 = Tyboxes[7][0][out[0]];
    unsigned int bb_28 = Tyboxes[7][1][out[1]];
    unsigned int cc_28 = Tyboxes[7][2][out[2]];
    unsigned int dd_28 = Tyboxes[7][3][out[3]];
    out[0] = (Txor[Txor[(aa_28 >> 0) & 0xf][(bb_28 >> 0) & 0xf]][Txor[(cc_28 >> 0) & 0xf][(dd_28 >> 0) & 0xf]]) | ((Txor[Txor[(aa_28 >> 4) & 0xf][(bb_28 >> 4) & 0xf]][Txor[(cc_28 >> 4) & 0xf][(dd_28 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_28 >> 8) & 0xf][(bb_28 >> 8) & 0xf]][Txor[(cc_28 >> 8) & 0xf][(dd_28 >> 8) & 0xf]]) | ((Txor[Txor[(aa_28 >> 12) & 0xf][(bb_28 >> 12) & 0xf]][Txor[(cc_28 >> 12) & 0xf][(dd_28 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_28 >> 16) & 0xf][(bb_28 >> 16) & 0xf]][Txor[(cc_28 >> 16) & 0xf][(dd_28 >> 16) & 0xf]]) | ((Txor[Txor[(aa_28 >> 20) & 0xf][(bb_28 >> 20) & 0xf]][Txor[(cc_28 >> 20) & 0xf][(dd_28 >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_28 >> 24) & 0xf][(bb_28 >> 24) & 0xf]][Txor[(cc_28 >> 24) & 0xf][(dd_28 >> 24) & 0xf]]) | ((Txor[Txor[(aa_28 >> 28) & 0xf][(bb_28 >> 28) & 0xf]][Txor[(cc_28 >> 28) & 0xf][(dd_28 >> 28) & 0xf]]) << 4);
    unsigned int aa_29 = Tyboxes[7][4][out[4]];
    unsigned int bb_29 = Tyboxes[7][5][out[5]];
    unsigned int cc_29 = Tyboxes[7][6][out[6]];
    unsigned int dd_29 = Tyboxes[7][7][out[7]];
    out[4] = (Txor[Txor[(aa_29 >> 0) & 0xf][(bb_29 >> 0) & 0xf]][Txor[(cc_29 >> 0) & 0xf][(dd_29 >> 0) & 0xf]]) | ((Txor[Txor[(aa_29 >> 4) & 0xf][(bb_29 >> 4) & 0xf]][Txor[(cc_29 >> 4) & 0xf][(dd_29 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_29 >> 8) & 0xf][(bb_29 >> 8) & 0xf]][Txor[(cc_29 >> 8) & 0xf][(dd_29 >> 8) & 0xf]]) | ((Txor[Txor[(aa_29 >> 12) & 0xf][(bb_29 >> 12) & 0xf]][Txor[(cc_29 >> 12) & 0xf][(dd_29 >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_29 >> 16) & 0xf][(bb_29 >> 16) & 0xf]][Txor[(cc_29 >> 16) & 0xf][(dd_29 >> 16) & 0xf]]) | ((Txor[Txor[(aa_29 >> 20) & 0xf][(bb_29 >> 20) & 0xf]][Txor[(cc_29 >> 20) & 0xf][(dd_29 >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_29 >> 24) & 0xf][(bb_29 >> 24) & 0xf]][Txor[(cc_29 >> 24) & 0xf][(dd_29 >> 24) & 0xf]]) | ((Txor[Txor[(aa_29 >> 28) & 0xf][(bb_29 >> 28) & 0xf]][Txor[(cc_29 >> 28) & 0xf][(dd_29 >> 28) & 0xf]]) << 4);
    unsigned int aa_30 = Tyboxes[7][8][out[8]];
    unsigned int bb_30 = Tyboxes[7][9][out[9]];
    unsigned int cc_30 = Tyboxes[7][10][out[10]];
    unsigned int dd_30 = Tyboxes[7][11][out[11]];
    out[8] = (Txor[Txor[(aa_30 >> 0) & 0xf][(bb_30 >> 0) & 0xf]][Txor[(cc_30 >> 0) & 0xf][(dd_30 >> 0) & 0xf]]) | ((Txor[Txor[(aa_30 >> 4) & 0xf][(bb_30 >> 4) & 0xf]][Txor[(cc_30 >> 4) & 0xf][(dd_30 >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_30 >> 8) & 0xf][(bb_30 >> 8) & 0xf]][Txor[(cc_30 >> 8) & 0xf][(dd_30 >> 8) & 0xf]]) | ((Txor[Txor[(aa_30 >> 12) & 0xf][(bb_30 >> 12) & 0xf]][Txor[(cc_30 >> 12) & 0xf][(dd_30 >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_30 >> 16) & 0xf][(bb_30 >> 16) & 0xf]][Txor[(cc_30 >> 16) & 0xf][(dd_30 >> 16) & 0xf]]) | ((Txor[Txor[(aa_30 >> 20) & 0xf][(bb_30 >> 20) & 0xf]][Txor[(cc_30 >> 20) & 0xf][(dd_30 >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_30 >> 24) & 0xf][(bb_30 >> 24) & 0xf]][Txor[(cc_30 >> 24) & 0xf][(dd_30 >> 24) & 0xf]]) | ((Txor[Txor[(aa_30 >> 28) & 0xf][(bb_30 >> 28) & 0xf]][Txor[(cc_30 >> 28) & 0xf][(dd_30 >> 28) & 0xf]]) << 4);
    unsigned int aa_31 = Tyboxes[7][12][out[12]];
    unsigned int bb_31 = Tyboxes[7][13][out[13]];
    unsigned int cc_31 = Tyboxes[7][14][out[14]];
    unsigned int dd_31 = Tyboxes[7][15][out[15]];
    out[12] = (Txor[Txor[(aa_31 >> 0) & 0xf][(bb_31 >> 0) & 0xf]][Txor[(cc_31 >> 0) & 0xf][(dd_31 >> 0) & 0xf]]) | ((Txor[Txor[(aa_31 >> 4) & 0xf][(bb_31 >> 4) & 0xf]][Txor[(cc_31 >> 4) & 0xf][(dd_31 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_31 >> 8) & 0xf][(bb_31 >> 8) & 0xf]][Txor[(cc_31 >> 8) & 0xf][(dd_31 >> 8) & 0xf]]) | ((Txor[Txor[(aa_31 >> 12) & 0xf][(bb_31 >> 12) & 0xf]][Txor[(cc_31 >> 12) & 0xf][(dd_31 >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_31 >> 16) & 0xf][(bb_31 >> 16) & 0xf]][Txor[(cc_31 >> 16) & 0xf][(dd_31 >> 16) & 0xf]]) | ((Txor[Txor[(aa_31 >> 20) & 0xf][(bb_31 >> 20) & 0xf]][Txor[(cc_31 >> 20) & 0xf][(dd_31 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_31 >> 24) & 0xf][(bb_31 >> 24) & 0xf]][Txor[(cc_31 >> 24) & 0xf][(dd_31 >> 24) & 0xf]]) | ((Txor[Txor[(aa_31 >> 28) & 0xf][(bb_31 >> 28) & 0xf]][Txor[(cc_31 >> 28) & 0xf][(dd_31 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int aa_32 = Tyboxes[8][0][out[0]];
    unsigned int bb_32 = Tyboxes[8][1][out[1]];
    unsigned int cc_32 = Tyboxes[8][2][out[2]];
    unsigned int dd_32 = Tyboxes[8][3][out[3]];
    out[0] = (Txor[Txor[(aa_32 >> 0) & 0xf][(bb_32 >> 0) & 0xf]][Txor[(cc_32 >> 0) & 0xf][(dd_32 >> 0) & 0xf]]) | ((Txor[Txor[(aa_32 >> 4) & 0xf][(bb_32 >> 4) & 0xf]][Txor[(cc_32 >> 4) & 0xf][(dd_32 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_32 >> 8) & 0xf][(bb_32 >> 8) & 0xf]][Txor[(cc_32 >> 8) & 0xf][(dd_32 >> 8) & 0xf]]) | ((Txor[Txor[(aa_32 >> 12) & 0xf][(bb_32 >> 12) & 0xf]][Txor[(cc_32 >> 12) & 0xf][(dd_32 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_32 >> 16) & 0xf][(bb_32 >> 16) & 0xf]][Txor[(cc_32 >> 16) & 0xf][(dd_32 >> 16) & 0xf]]) | ((Txor[Txor[(aa_32 >> 20) & 0xf][(bb_32 >> 20) & 0xf]][Txor[(cc_32 >> 20) & 0xf][(dd_32 >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_32 >> 24) & 0xf][(bb_32 >> 24) & 0xf]][Txor[(cc_32 >> 24) & 0xf][(dd_32 >> 24) & 0xf]]) | ((Txor[Txor[(aa_32 >> 28) & 0xf][(bb_32 >> 28) & 0xf]][Txor[(cc_32 >> 28) & 0xf][(dd_32 >> 28) & 0xf]]) << 4);
    unsigned int aa_33 = Tyboxes[8][4][out[4]];
    unsigned int bb_33 = Tyboxes[8][5][out[5]];
    unsigned int cc_33 = Tyboxes[8][6][out[6]];
    unsigned int dd_33 = Tyboxes[8][7][out[7]];
    out[4] = (Txor[Txor[(aa_33 >> 0) & 0xf][(bb_33 >> 0) & 0xf]][Txor[(cc_33 >> 0) & 0xf][(dd_33 >> 0) & 0xf]]) | ((Txor[Txor[(aa_33 >> 4) & 0xf][(bb_33 >> 4) & 0xf]][Txor[(cc_33 >> 4) & 0xf][(dd_33 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_33 >> 8) & 0xf][(bb_33 >> 8) & 0xf]][Txor[(cc_33 >> 8) & 0xf][(dd_33 >> 8) & 0xf]]) | ((Txor[Txor[(aa_33 >> 12) & 0xf][(bb_33 >> 12) & 0xf]][Txor[(cc_33 >> 12) & 0xf][(dd_33 >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_33 >> 16) & 0xf][(bb_33 >> 16) & 0xf]][Txor[(cc_33 >> 16) & 0xf][(dd_33 >> 16) & 0xf]]) | ((Txor[Txor[(aa_33 >> 20) & 0xf][(bb_33 >> 20) & 0xf]][Txor[(cc_33 >> 20) & 0xf][(dd_33 >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_33 >> 24) & 0xf][(bb_33 >> 24) & 0xf]][Txor[(cc_33 >> 24) & 0xf][(dd_33 >> 24) & 0xf]]) | ((Txor[Txor[(aa_33 >> 28) & 0xf][(bb_33 >> 28) & 0xf]][Txor[(cc_33 >> 28) & 0xf][(dd_33 >> 28) & 0xf]]) << 4);
    unsigned int aa_34 = Tyboxes[8][8][out[8]];
    unsigned int bb_34 = Tyboxes[8][9][out[9]];
    unsigned int cc_34 = Tyboxes[8][10][out[10]];
    unsigned int dd_34 = Tyboxes[8][11][out[11]];
    out[8] = (Txor[Txor[(aa_34 >> 0) & 0xf][(bb_34 >> 0) & 0xf]][Txor[(cc_34 >> 0) & 0xf][(dd_34 >> 0) & 0xf]]) | ((Txor[Txor[(aa_34 >> 4) & 0xf][(bb_34 >> 4) & 0xf]][Txor[(cc_34 >> 4) & 0xf][(dd_34 >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_34 >> 8) & 0xf][(bb_34 >> 8) & 0xf]][Txor[(cc_34 >> 8) & 0xf][(dd_34 >> 8) & 0xf]]) | ((Txor[Txor[(aa_34 >> 12) & 0xf][(bb_34 >> 12) & 0xf]][Txor[(cc_34 >> 12) & 0xf][(dd_34 >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_34 >> 16) & 0xf][(bb_34 >> 16) & 0xf]][Txor[(cc_34 >> 16) & 0xf][(dd_34 >> 16) & 0xf]]) | ((Txor[Txor[(aa_34 >> 20) & 0xf][(bb_34 >> 20) & 0xf]][Txor[(cc_34 >> 20) & 0xf][(dd_34 >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_34 >> 24) & 0xf][(bb_34 >> 24) & 0xf]][Txor[(cc_34 >> 24) & 0xf][(dd_34 >> 24) & 0xf]]) | ((Txor[Txor[(aa_34 >> 28) & 0xf][(bb_34 >> 28) & 0xf]][Txor[(cc_34 >> 28) & 0xf][(dd_34 >> 28) & 0xf]]) << 4);
    unsigned int aa_35 = Tyboxes[8][12][out[12]];
    unsigned int bb_35 = Tyboxes[8][13][out[13]];
    unsigned int cc_35 = Tyboxes[8][14][out[14]];
    unsigned int dd_35 = Tyboxes[8][15][out[15]];
    out[12] = (Txor[Txor[(aa_35 >> 0) & 0xf][(bb_35 >> 0) & 0xf]][Txor[(cc_35 >> 0) & 0xf][(dd_35 >> 0) & 0xf]]) | ((Txor[Txor[(aa_35 >> 4) & 0xf][(bb_35 >> 4) & 0xf]][Txor[(cc_35 >> 4) & 0xf][(dd_35 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_35 >> 8) & 0xf][(bb_35 >> 8) & 0xf]][Txor[(cc_35 >> 8) & 0xf][(dd_35 >> 8) & 0xf]]) | ((Txor[Txor[(aa_35 >> 12) & 0xf][(bb_35 >> 12) & 0xf]][Txor[(cc_35 >> 12) & 0xf][(dd_35 >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_35 >> 16) & 0xf][(bb_35 >> 16) & 0xf]][Txor[(cc_35 >> 16) & 0xf][(dd_35 >> 16) & 0xf]]) | ((Txor[Txor[(aa_35 >> 20) & 0xf][(bb_35 >> 20) & 0xf]][Txor[(cc_35 >> 20) & 0xf][(dd_35 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_35 >> 24) & 0xf][(bb_35 >> 24) & 0xf]][Txor[(cc_35 >> 24) & 0xf][(dd_35 >> 24) & 0xf]]) | ((Txor[Txor[(aa_35 >> 28) & 0xf][(bb_35 >> 28) & 0xf]][Txor[(cc_35 >> 28) & 0xf][(dd_35 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    out[0] = Tboxes_[0][out[0]];
    out[1] = Tboxes_[1][out[1]];
    out[2] = Tboxes_[2][out[2]];
    out[3] = Tboxes_[3][out[3]];
    out[4] = Tboxes_[4][out[4]];
    out[5] = Tboxes_[5][out[5]];
    out[6] = Tboxes_[6][out[6]];
    out[7] = Tboxes_[7][out[7]];
    out[8] = Tboxes_[8][out[8]];
    out[9] = Tboxes_[9][out[9]];
    out[10] = Tboxes_[10][out[10]];
    out[11] = Tboxes_[11][out[11]];
    out[12] = Tboxes_[12][out[12]];
    out[13] = Tboxes_[13][out[13]];
    out[14] = Tboxes_[14][out[14]];
    out[15] = Tboxes_[15][out[15]];
}

void aes128_enc_wb_final_unrolled_shuffled_3533280945(unsigned char in[16], unsigned char out[16])
{
    memcpy(out, in, 16);
    ShiftRows(out);
    unsigned int bb_0 = Tyboxes[0][1][out[1]];
    unsigned int aa_1 = Tyboxes[0][4][out[4]];
    unsigned int dd_0 = Tyboxes[0][3][out[3]];
    unsigned int cc_3 = Tyboxes[0][14][out[14]];
    unsigned int cc_0 = Tyboxes[0][2][out[2]];
    unsigned int aa_0 = Tyboxes[0][0][out[0]];
    unsigned int dd_3 = Tyboxes[0][15][out[15]];
    unsigned int bb_2 = Tyboxes[0][9][out[9]];
    unsigned int cc_2 = Tyboxes[0][10][out[10]];
    unsigned int aa_3 = Tyboxes[0][12][out[12]];
    unsigned int aa_2 = Tyboxes[0][8][out[8]];
    unsigned int dd_2 = Tyboxes[0][11][out[11]];
    unsigned int dd_1 = Tyboxes[0][7][out[7]];
    unsigned int bb_3 = Tyboxes[0][13][out[13]];
    unsigned int bb_1 = Tyboxes[0][5][out[5]];
    unsigned int cc_1 = Tyboxes[0][6][out[6]];
    out[8] = (Txor[Txor[(aa_2 >> 0) & 0xf][(bb_2 >> 0) & 0xf]][Txor[(cc_2 >> 0) & 0xf][(dd_2 >> 0) & 0xf]]) | ((Txor[Txor[(aa_2 >> 4) & 0xf][(bb_2 >> 4) & 0xf]][Txor[(cc_2 >> 4) & 0xf][(dd_2 >> 4) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_0 >> 24) & 0xf][(bb_0 >> 24) & 0xf]][Txor[(cc_0 >> 24) & 0xf][(dd_0 >> 24) & 0xf]]) | ((Txor[Txor[(aa_0 >> 28) & 0xf][(bb_0 >> 28) & 0xf]][Txor[(cc_0 >> 28) & 0xf][(dd_0 >> 28) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_0 >> 8) & 0xf][(bb_0 >> 8) & 0xf]][Txor[(cc_0 >> 8) & 0xf][(dd_0 >> 8) & 0xf]]) | ((Txor[Txor[(aa_0 >> 12) & 0xf][(bb_0 >> 12) & 0xf]][Txor[(cc_0 >> 12) & 0xf][(dd_0 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_0 >> 16) & 0xf][(bb_0 >> 16) & 0xf]][Txor[(cc_0 >> 16) & 0xf][(dd_0 >> 16) & 0xf]]) | ((Txor[Txor[(aa_0 >> 20) & 0xf][(bb_0 >> 20) & 0xf]][Txor[(cc_0 >> 20) & 0xf][(dd_0 >> 20) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_0 >> 0) & 0xf][(bb_0 >> 0) & 0xf]][Txor[(cc_0 >> 0) & 0xf][(dd_0 >> 0) & 0xf]]) | ((Txor[Txor[(aa_0 >> 4) & 0xf][(bb_0 >> 4) & 0xf]][Txor[(cc_0 >> 4) & 0xf][(dd_0 >> 4) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_3 >> 0) & 0xf][(bb_3 >> 0) & 0xf]][Txor[(cc_3 >> 0) & 0xf][(dd_3 >> 0) & 0xf]]) | ((Txor[Txor[(aa_3 >> 4) & 0xf][(bb_3 >> 4) & 0xf]][Txor[(cc_3 >> 4) & 0xf][(dd_3 >> 4) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_2 >> 16) & 0xf][(bb_2 >> 16) & 0xf]][Txor[(cc_2 >> 16) & 0xf][(dd_2 >> 16) & 0xf]]) | ((Txor[Txor[(aa_2 >> 20) & 0xf][(bb_2 >> 20) & 0xf]][Txor[(cc_2 >> 20) & 0xf][(dd_2 >> 20) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_3 >> 16) & 0xf][(bb_3 >> 16) & 0xf]][Txor[(cc_3 >> 16) & 0xf][(dd_3 >> 16) & 0xf]]) | ((Txor[Txor[(aa_3 >> 20) & 0xf][(bb_3 >> 20) & 0xf]][Txor[(cc_3 >> 20) & 0xf][(dd_3 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_3 >> 24) & 0xf][(bb_3 >> 24) & 0xf]][Txor[(cc_3 >> 24) & 0xf][(dd_3 >> 24) & 0xf]]) | ((Txor[Txor[(aa_3 >> 28) & 0xf][(bb_3 >> 28) & 0xf]][Txor[(cc_3 >> 28) & 0xf][(dd_3 >> 28) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_1 >> 24) & 0xf][(bb_1 >> 24) & 0xf]][Txor[(cc_1 >> 24) & 0xf][(dd_1 >> 24) & 0xf]]) | ((Txor[Txor[(aa_1 >> 28) & 0xf][(bb_1 >> 28) & 0xf]][Txor[(cc_1 >> 28) & 0xf][(dd_1 >> 28) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_2 >> 8) & 0xf][(bb_2 >> 8) & 0xf]][Txor[(cc_2 >> 8) & 0xf][(dd_2 >> 8) & 0xf]]) | ((Txor[Txor[(aa_2 >> 12) & 0xf][(bb_2 >> 12) & 0xf]][Txor[(cc_2 >> 12) & 0xf][(dd_2 >> 12) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_1 >> 8) & 0xf][(bb_1 >> 8) & 0xf]][Txor[(cc_1 >> 8) & 0xf][(dd_1 >> 8) & 0xf]]) | ((Txor[Txor[(aa_1 >> 12) & 0xf][(bb_1 >> 12) & 0xf]][Txor[(cc_1 >> 12) & 0xf][(dd_1 >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_1 >> 16) & 0xf][(bb_1 >> 16) & 0xf]][Txor[(cc_1 >> 16) & 0xf][(dd_1 >> 16) & 0xf]]) | ((Txor[Txor[(aa_1 >> 20) & 0xf][(bb_1 >> 20) & 0xf]][Txor[(cc_1 >> 20) & 0xf][(dd_1 >> 20) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_3 >> 8) & 0xf][(bb_3 >> 8) & 0xf]][Txor[(cc_3 >> 8) & 0xf][(dd_3 >> 8) & 0xf]]) | ((Txor[Txor[(aa_3 >> 12) & 0xf][(bb_3 >> 12) & 0xf]][Txor[(cc_3 >> 12) & 0xf][(dd_3 >> 12) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_1 >> 0) & 0xf][(bb_1 >> 0) & 0xf]][Txor[(cc_1 >> 0) & 0xf][(dd_1 >> 0) & 0xf]]) | ((Txor[Txor[(aa_1 >> 4) & 0xf][(bb_1 >> 4) & 0xf]][Txor[(cc_1 >> 4) & 0xf][(dd_1 >> 4) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_2 >> 24) & 0xf][(bb_2 >> 24) & 0xf]][Txor[(cc_2 >> 24) & 0xf][(dd_2 >> 24) & 0xf]]) | ((Txor[Txor[(aa_2 >> 28) & 0xf][(bb_2 >> 28) & 0xf]][Txor[(cc_2 >> 28) & 0xf][(dd_2 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int aa_6 = Tyboxes[1][8][out[8]];
    unsigned int aa_4 = Tyboxes[1][0][out[0]];
    unsigned int dd_6 = Tyboxes[1][11][out[11]];
    unsigned int cc_6 = Tyboxes[1][10][out[10]];
    unsigned int dd_7 = Tyboxes[1][15][out[15]];
    unsigned int cc_7 = Tyboxes[1][14][out[14]];
    unsigned int cc_4 = Tyboxes[1][2][out[2]];
    unsigned int bb_4 = Tyboxes[1][1][out[1]];
    unsigned int bb_5 = Tyboxes[1][5][out[5]];
    unsigned int aa_5 = Tyboxes[1][4][out[4]];
    unsigned int dd_5 = Tyboxes[1][7][out[7]];
    unsigned int cc_5 = Tyboxes[1][6][out[6]];
    unsigned int dd_4 = Tyboxes[1][3][out[3]];
    unsigned int aa_7 = Tyboxes[1][12][out[12]];
    unsigned int bb_7 = Tyboxes[1][13][out[13]];
    unsigned int bb_6 = Tyboxes[1][9][out[9]];
    out[8] = (Txor[Txor[(aa_6 >> 0) & 0xf][(bb_6 >> 0) & 0xf]][Txor[(cc_6 >> 0) & 0xf][(dd_6 >> 0) & 0xf]]) | ((Txor[Txor[(aa_6 >> 4) & 0xf][(bb_6 >> 4) & 0xf]][Txor[(cc_6 >> 4) & 0xf][(dd_6 >> 4) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_7 >> 24) & 0xf][(bb_7 >> 24) & 0xf]][Txor[(cc_7 >> 24) & 0xf][(dd_7 >> 24) & 0xf]]) | ((Txor[Txor[(aa_7 >> 28) & 0xf][(bb_7 >> 28) & 0xf]][Txor[(cc_7 >> 28) & 0xf][(dd_7 >> 28) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_7 >> 16) & 0xf][(bb_7 >> 16) & 0xf]][Txor[(cc_7 >> 16) & 0xf][(dd_7 >> 16) & 0xf]]) | ((Txor[Txor[(aa_7 >> 20) & 0xf][(bb_7 >> 20) & 0xf]][Txor[(cc_7 >> 20) & 0xf][(dd_7 >> 20) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_7 >> 8) & 0xf][(bb_7 >> 8) & 0xf]][Txor[(cc_7 >> 8) & 0xf][(dd_7 >> 8) & 0xf]]) | ((Txor[Txor[(aa_7 >> 12) & 0xf][(bb_7 >> 12) & 0xf]][Txor[(cc_7 >> 12) & 0xf][(dd_7 >> 12) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_7 >> 0) & 0xf][(bb_7 >> 0) & 0xf]][Txor[(cc_7 >> 0) & 0xf][(dd_7 >> 0) & 0xf]]) | ((Txor[Txor[(aa_7 >> 4) & 0xf][(bb_7 >> 4) & 0xf]][Txor[(cc_7 >> 4) & 0xf][(dd_7 >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_6 >> 8) & 0xf][(bb_6 >> 8) & 0xf]][Txor[(cc_6 >> 8) & 0xf][(dd_6 >> 8) & 0xf]]) | ((Txor[Txor[(aa_6 >> 12) & 0xf][(bb_6 >> 12) & 0xf]][Txor[(cc_6 >> 12) & 0xf][(dd_6 >> 12) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_4 >> 24) & 0xf][(bb_4 >> 24) & 0xf]][Txor[(cc_4 >> 24) & 0xf][(dd_4 >> 24) & 0xf]]) | ((Txor[Txor[(aa_4 >> 28) & 0xf][(bb_4 >> 28) & 0xf]][Txor[(cc_4 >> 28) & 0xf][(dd_4 >> 28) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_4 >> 16) & 0xf][(bb_4 >> 16) & 0xf]][Txor[(cc_4 >> 16) & 0xf][(dd_4 >> 16) & 0xf]]) | ((Txor[Txor[(aa_4 >> 20) & 0xf][(bb_4 >> 20) & 0xf]][Txor[(cc_4 >> 20) & 0xf][(dd_4 >> 20) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_6 >> 16) & 0xf][(bb_6 >> 16) & 0xf]][Txor[(cc_6 >> 16) & 0xf][(dd_6 >> 16) & 0xf]]) | ((Txor[Txor[(aa_6 >> 20) & 0xf][(bb_6 >> 20) & 0xf]][Txor[(cc_6 >> 20) & 0xf][(dd_6 >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_6 >> 24) & 0xf][(bb_6 >> 24) & 0xf]][Txor[(cc_6 >> 24) & 0xf][(dd_6 >> 24) & 0xf]]) | ((Txor[Txor[(aa_6 >> 28) & 0xf][(bb_6 >> 28) & 0xf]][Txor[(cc_6 >> 28) & 0xf][(dd_6 >> 28) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_5 >> 8) & 0xf][(bb_5 >> 8) & 0xf]][Txor[(cc_5 >> 8) & 0xf][(dd_5 >> 8) & 0xf]]) | ((Txor[Txor[(aa_5 >> 12) & 0xf][(bb_5 >> 12) & 0xf]][Txor[(cc_5 >> 12) & 0xf][(dd_5 >> 12) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_5 >> 0) & 0xf][(bb_5 >> 0) & 0xf]][Txor[(cc_5 >> 0) & 0xf][(dd_5 >> 0) & 0xf]]) | ((Txor[Txor[(aa_5 >> 4) & 0xf][(bb_5 >> 4) & 0xf]][Txor[(cc_5 >> 4) & 0xf][(dd_5 >> 4) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_5 >> 24) & 0xf][(bb_5 >> 24) & 0xf]][Txor[(cc_5 >> 24) & 0xf][(dd_5 >> 24) & 0xf]]) | ((Txor[Txor[(aa_5 >> 28) & 0xf][(bb_5 >> 28) & 0xf]][Txor[(cc_5 >> 28) & 0xf][(dd_5 >> 28) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_5 >> 16) & 0xf][(bb_5 >> 16) & 0xf]][Txor[(cc_5 >> 16) & 0xf][(dd_5 >> 16) & 0xf]]) | ((Txor[Txor[(aa_5 >> 20) & 0xf][(bb_5 >> 20) & 0xf]][Txor[(cc_5 >> 20) & 0xf][(dd_5 >> 20) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_4 >> 0) & 0xf][(bb_4 >> 0) & 0xf]][Txor[(cc_4 >> 0) & 0xf][(dd_4 >> 0) & 0xf]]) | ((Txor[Txor[(aa_4 >> 4) & 0xf][(bb_4 >> 4) & 0xf]][Txor[(cc_4 >> 4) & 0xf][(dd_4 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_4 >> 8) & 0xf][(bb_4 >> 8) & 0xf]][Txor[(cc_4 >> 8) & 0xf][(dd_4 >> 8) & 0xf]]) | ((Txor[Txor[(aa_4 >> 12) & 0xf][(bb_4 >> 12) & 0xf]][Txor[(cc_4 >> 12) & 0xf][(dd_4 >> 12) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int cc_10 = Tyboxes[2][10][out[10]];
    unsigned int bb_10 = Tyboxes[2][9][out[9]];
    unsigned int dd_11 = Tyboxes[2][15][out[15]];
    unsigned int dd_10 = Tyboxes[2][11][out[11]];
    unsigned int bb_11 = Tyboxes[2][13][out[13]];
    unsigned int cc_11 = Tyboxes[2][14][out[14]];
    unsigned int aa_10 = Tyboxes[2][8][out[8]];
    unsigned int aa_11 = Tyboxes[2][12][out[12]];
    unsigned int aa_8 = Tyboxes[2][0][out[0]];
    unsigned int aa_9 = Tyboxes[2][4][out[4]];
    unsigned int bb_8 = Tyboxes[2][1][out[1]];
    unsigned int cc_9 = Tyboxes[2][6][out[6]];
    unsigned int dd_8 = Tyboxes[2][3][out[3]];
    unsigned int cc_8 = Tyboxes[2][2][out[2]];
    unsigned int bb_9 = Tyboxes[2][5][out[5]];
    unsigned int dd_9 = Tyboxes[2][7][out[7]];
    out[13] = (Txor[Txor[(aa_11 >> 8) & 0xf][(bb_11 >> 8) & 0xf]][Txor[(cc_11 >> 8) & 0xf][(dd_11 >> 8) & 0xf]]) | ((Txor[Txor[(aa_11 >> 12) & 0xf][(bb_11 >> 12) & 0xf]][Txor[(cc_11 >> 12) & 0xf][(dd_11 >> 12) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_9 >> 0) & 0xf][(bb_9 >> 0) & 0xf]][Txor[(cc_9 >> 0) & 0xf][(dd_9 >> 0) & 0xf]]) | ((Txor[Txor[(aa_9 >> 4) & 0xf][(bb_9 >> 4) & 0xf]][Txor[(cc_9 >> 4) & 0xf][(dd_9 >> 4) & 0xf]]) << 4);
    out[8] = (Txor[Txor[(aa_10 >> 0) & 0xf][(bb_10 >> 0) & 0xf]][Txor[(cc_10 >> 0) & 0xf][(dd_10 >> 0) & 0xf]]) | ((Txor[Txor[(aa_10 >> 4) & 0xf][(bb_10 >> 4) & 0xf]][Txor[(cc_10 >> 4) & 0xf][(dd_10 >> 4) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_11 >> 0) & 0xf][(bb_11 >> 0) & 0xf]][Txor[(cc_11 >> 0) & 0xf][(dd_11 >> 0) & 0xf]]) | ((Txor[Txor[(aa_11 >> 4) & 0xf][(bb_11 >> 4) & 0xf]][Txor[(cc_11 >> 4) & 0xf][(dd_11 >> 4) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_9 >> 16) & 0xf][(bb_9 >> 16) & 0xf]][Txor[(cc_9 >> 16) & 0xf][(dd_9 >> 16) & 0xf]]) | ((Txor[Txor[(aa_9 >> 20) & 0xf][(bb_9 >> 20) & 0xf]][Txor[(cc_9 >> 20) & 0xf][(dd_9 >> 20) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_9 >> 8) & 0xf][(bb_9 >> 8) & 0xf]][Txor[(cc_9 >> 8) & 0xf][(dd_9 >> 8) & 0xf]]) | ((Txor[Txor[(aa_9 >> 12) & 0xf][(bb_9 >> 12) & 0xf]][Txor[(cc_9 >> 12) & 0xf][(dd_9 >> 12) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_10 >> 24) & 0xf][(bb_10 >> 24) & 0xf]][Txor[(cc_10 >> 24) & 0xf][(dd_10 >> 24) & 0xf]]) | ((Txor[Txor[(aa_10 >> 28) & 0xf][(bb_10 >> 28) & 0xf]][Txor[(cc_10 >> 28) & 0xf][(dd_10 >> 28) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_9 >> 24) & 0xf][(bb_9 >> 24) & 0xf]][Txor[(cc_9 >> 24) & 0xf][(dd_9 >> 24) & 0xf]]) | ((Txor[Txor[(aa_9 >> 28) & 0xf][(bb_9 >> 28) & 0xf]][Txor[(cc_9 >> 28) & 0xf][(dd_9 >> 28) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_8 >> 0) & 0xf][(bb_8 >> 0) & 0xf]][Txor[(cc_8 >> 0) & 0xf][(dd_8 >> 0) & 0xf]]) | ((Txor[Txor[(aa_8 >> 4) & 0xf][(bb_8 >> 4) & 0xf]][Txor[(cc_8 >> 4) & 0xf][(dd_8 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_8 >> 8) & 0xf][(bb_8 >> 8) & 0xf]][Txor[(cc_8 >> 8) & 0xf][(dd_8 >> 8) & 0xf]]) | ((Txor[Txor[(aa_8 >> 12) & 0xf][(bb_8 >> 12) & 0xf]][Txor[(cc_8 >> 12) & 0xf][(dd_8 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_8 >> 16) & 0xf][(bb_8 >> 16) & 0xf]][Txor[(cc_8 >> 16) & 0xf][(dd_8 >> 16) & 0xf]]) | ((Txor[Txor[(aa_8 >> 20) & 0xf][(bb_8 >> 20) & 0xf]][Txor[(cc_8 >> 20) & 0xf][(dd_8 >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_8 >> 24) & 0xf][(bb_8 >> 24) & 0xf]][Txor[(cc_8 >> 24) & 0xf][(dd_8 >> 24) & 0xf]]) | ((Txor[Txor[(aa_8 >> 28) & 0xf][(bb_8 >> 28) & 0xf]][Txor[(cc_8 >> 28) & 0xf][(dd_8 >> 28) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_10 >> 8) & 0xf][(bb_10 >> 8) & 0xf]][Txor[(cc_10 >> 8) & 0xf][(dd_10 >> 8) & 0xf]]) | ((Txor[Txor[(aa_10 >> 12) & 0xf][(bb_10 >> 12) & 0xf]][Txor[(cc_10 >> 12) & 0xf][(dd_10 >> 12) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_11 >> 24) & 0xf][(bb_11 >> 24) & 0xf]][Txor[(cc_11 >> 24) & 0xf][(dd_11 >> 24) & 0xf]]) | ((Txor[Txor[(aa_11 >> 28) & 0xf][(bb_11 >> 28) & 0xf]][Txor[(cc_11 >> 28) & 0xf][(dd_11 >> 28) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_11 >> 16) & 0xf][(bb_11 >> 16) & 0xf]][Txor[(cc_11 >> 16) & 0xf][(dd_11 >> 16) & 0xf]]) | ((Txor[Txor[(aa_11 >> 20) & 0xf][(bb_11 >> 20) & 0xf]][Txor[(cc_11 >> 20) & 0xf][(dd_11 >> 20) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_10 >> 16) & 0xf][(bb_10 >> 16) & 0xf]][Txor[(cc_10 >> 16) & 0xf][(dd_10 >> 16) & 0xf]]) | ((Txor[Txor[(aa_10 >> 20) & 0xf][(bb_10 >> 20) & 0xf]][Txor[(cc_10 >> 20) & 0xf][(dd_10 >> 20) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int cc_13 = Tyboxes[3][6][out[6]];
    unsigned int cc_14 = Tyboxes[3][10][out[10]];
    unsigned int dd_14 = Tyboxes[3][11][out[11]];
    unsigned int bb_12 = Tyboxes[3][1][out[1]];
    unsigned int aa_12 = Tyboxes[3][0][out[0]];
    unsigned int dd_13 = Tyboxes[3][7][out[7]];
    unsigned int cc_12 = Tyboxes[3][2][out[2]];
    unsigned int dd_15 = Tyboxes[3][15][out[15]];
    unsigned int cc_15 = Tyboxes[3][14][out[14]];
    unsigned int bb_15 = Tyboxes[3][13][out[13]];
    unsigned int aa_15 = Tyboxes[3][12][out[12]];
    unsigned int aa_14 = Tyboxes[3][8][out[8]];
    unsigned int bb_14 = Tyboxes[3][9][out[9]];
    unsigned int aa_13 = Tyboxes[3][4][out[4]];
    unsigned int bb_13 = Tyboxes[3][5][out[5]];
    unsigned int dd_12 = Tyboxes[3][3][out[3]];
    out[1] = (Txor[Txor[(aa_12 >> 8) & 0xf][(bb_12 >> 8) & 0xf]][Txor[(cc_12 >> 8) & 0xf][(dd_12 >> 8) & 0xf]]) | ((Txor[Txor[(aa_12 >> 12) & 0xf][(bb_12 >> 12) & 0xf]][Txor[(cc_12 >> 12) & 0xf][(dd_12 >> 12) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_12 >> 0) & 0xf][(bb_12 >> 0) & 0xf]][Txor[(cc_12 >> 0) & 0xf][(dd_12 >> 0) & 0xf]]) | ((Txor[Txor[(aa_12 >> 4) & 0xf][(bb_12 >> 4) & 0xf]][Txor[(cc_12 >> 4) & 0xf][(dd_12 >> 4) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_12 >> 24) & 0xf][(bb_12 >> 24) & 0xf]][Txor[(cc_12 >> 24) & 0xf][(dd_12 >> 24) & 0xf]]) | ((Txor[Txor[(aa_12 >> 28) & 0xf][(bb_12 >> 28) & 0xf]][Txor[(cc_12 >> 28) & 0xf][(dd_12 >> 28) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_12 >> 16) & 0xf][(bb_12 >> 16) & 0xf]][Txor[(cc_12 >> 16) & 0xf][(dd_12 >> 16) & 0xf]]) | ((Txor[Txor[(aa_12 >> 20) & 0xf][(bb_12 >> 20) & 0xf]][Txor[(cc_12 >> 20) & 0xf][(dd_12 >> 20) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_15 >> 8) & 0xf][(bb_15 >> 8) & 0xf]][Txor[(cc_15 >> 8) & 0xf][(dd_15 >> 8) & 0xf]]) | ((Txor[Txor[(aa_15 >> 12) & 0xf][(bb_15 >> 12) & 0xf]][Txor[(cc_15 >> 12) & 0xf][(dd_15 >> 12) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_15 >> 0) & 0xf][(bb_15 >> 0) & 0xf]][Txor[(cc_15 >> 0) & 0xf][(dd_15 >> 0) & 0xf]]) | ((Txor[Txor[(aa_15 >> 4) & 0xf][(bb_15 >> 4) & 0xf]][Txor[(cc_15 >> 4) & 0xf][(dd_15 >> 4) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_13 >> 0) & 0xf][(bb_13 >> 0) & 0xf]][Txor[(cc_13 >> 0) & 0xf][(dd_13 >> 0) & 0xf]]) | ((Txor[Txor[(aa_13 >> 4) & 0xf][(bb_13 >> 4) & 0xf]][Txor[(cc_13 >> 4) & 0xf][(dd_13 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_13 >> 8) & 0xf][(bb_13 >> 8) & 0xf]][Txor[(cc_13 >> 8) & 0xf][(dd_13 >> 8) & 0xf]]) | ((Txor[Txor[(aa_13 >> 12) & 0xf][(bb_13 >> 12) & 0xf]][Txor[(cc_13 >> 12) & 0xf][(dd_13 >> 12) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_14 >> 24) & 0xf][(bb_14 >> 24) & 0xf]][Txor[(cc_14 >> 24) & 0xf][(dd_14 >> 24) & 0xf]]) | ((Txor[Txor[(aa_14 >> 28) & 0xf][(bb_14 >> 28) & 0xf]][Txor[(cc_14 >> 28) & 0xf][(dd_14 >> 28) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_14 >> 16) & 0xf][(bb_14 >> 16) & 0xf]][Txor[(cc_14 >> 16) & 0xf][(dd_14 >> 16) & 0xf]]) | ((Txor[Txor[(aa_14 >> 20) & 0xf][(bb_14 >> 20) & 0xf]][Txor[(cc_14 >> 20) & 0xf][(dd_14 >> 20) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_13 >> 16) & 0xf][(bb_13 >> 16) & 0xf]][Txor[(cc_13 >> 16) & 0xf][(dd_13 >> 16) & 0xf]]) | ((Txor[Txor[(aa_13 >> 20) & 0xf][(bb_13 >> 20) & 0xf]][Txor[(cc_13 >> 20) & 0xf][(dd_13 >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_13 >> 24) & 0xf][(bb_13 >> 24) & 0xf]][Txor[(cc_13 >> 24) & 0xf][(dd_13 >> 24) & 0xf]]) | ((Txor[Txor[(aa_13 >> 28) & 0xf][(bb_13 >> 28) & 0xf]][Txor[(cc_13 >> 28) & 0xf][(dd_13 >> 28) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_15 >> 16) & 0xf][(bb_15 >> 16) & 0xf]][Txor[(cc_15 >> 16) & 0xf][(dd_15 >> 16) & 0xf]]) | ((Txor[Txor[(aa_15 >> 20) & 0xf][(bb_15 >> 20) & 0xf]][Txor[(cc_15 >> 20) & 0xf][(dd_15 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_15 >> 24) & 0xf][(bb_15 >> 24) & 0xf]][Txor[(cc_15 >> 24) & 0xf][(dd_15 >> 24) & 0xf]]) | ((Txor[Txor[(aa_15 >> 28) & 0xf][(bb_15 >> 28) & 0xf]][Txor[(cc_15 >> 28) & 0xf][(dd_15 >> 28) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_14 >> 8) & 0xf][(bb_14 >> 8) & 0xf]][Txor[(cc_14 >> 8) & 0xf][(dd_14 >> 8) & 0xf]]) | ((Txor[Txor[(aa_14 >> 12) & 0xf][(bb_14 >> 12) & 0xf]][Txor[(cc_14 >> 12) & 0xf][(dd_14 >> 12) & 0xf]]) << 4);
    out[8] = (Txor[Txor[(aa_14 >> 0) & 0xf][(bb_14 >> 0) & 0xf]][Txor[(cc_14 >> 0) & 0xf][(dd_14 >> 0) & 0xf]]) | ((Txor[Txor[(aa_14 >> 4) & 0xf][(bb_14 >> 4) & 0xf]][Txor[(cc_14 >> 4) & 0xf][(dd_14 >> 4) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int dd_19 = Tyboxes[4][15][out[15]];
    unsigned int bb_16 = Tyboxes[4][1][out[1]];
    unsigned int cc_16 = Tyboxes[4][2][out[2]];
    unsigned int dd_16 = Tyboxes[4][3][out[3]];
    unsigned int aa_16 = Tyboxes[4][0][out[0]];
    unsigned int aa_18 = Tyboxes[4][8][out[8]];
    unsigned int bb_19 = Tyboxes[4][13][out[13]];
    unsigned int cc_19 = Tyboxes[4][14][out[14]];
    unsigned int aa_17 = Tyboxes[4][4][out[4]];
    unsigned int aa_19 = Tyboxes[4][12][out[12]];
    unsigned int cc_17 = Tyboxes[4][6][out[6]];
    unsigned int bb_17 = Tyboxes[4][5][out[5]];
    unsigned int dd_18 = Tyboxes[4][11][out[11]];
    unsigned int dd_17 = Tyboxes[4][7][out[7]];
    unsigned int bb_18 = Tyboxes[4][9][out[9]];
    unsigned int cc_18 = Tyboxes[4][10][out[10]];
    out[14] = (Txor[Txor[(aa_19 >> 16) & 0xf][(bb_19 >> 16) & 0xf]][Txor[(cc_19 >> 16) & 0xf][(dd_19 >> 16) & 0xf]]) | ((Txor[Txor[(aa_19 >> 20) & 0xf][(bb_19 >> 20) & 0xf]][Txor[(cc_19 >> 20) & 0xf][(dd_19 >> 20) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_19 >> 8) & 0xf][(bb_19 >> 8) & 0xf]][Txor[(cc_19 >> 8) & 0xf][(dd_19 >> 8) & 0xf]]) | ((Txor[Txor[(aa_19 >> 12) & 0xf][(bb_19 >> 12) & 0xf]][Txor[(cc_19 >> 12) & 0xf][(dd_19 >> 12) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_19 >> 0) & 0xf][(bb_19 >> 0) & 0xf]][Txor[(cc_19 >> 0) & 0xf][(dd_19 >> 0) & 0xf]]) | ((Txor[Txor[(aa_19 >> 4) & 0xf][(bb_19 >> 4) & 0xf]][Txor[(cc_19 >> 4) & 0xf][(dd_19 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_16 >> 8) & 0xf][(bb_16 >> 8) & 0xf]][Txor[(cc_16 >> 8) & 0xf][(dd_16 >> 8) & 0xf]]) | ((Txor[Txor[(aa_16 >> 12) & 0xf][(bb_16 >> 12) & 0xf]][Txor[(cc_16 >> 12) & 0xf][(dd_16 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_16 >> 16) & 0xf][(bb_16 >> 16) & 0xf]][Txor[(cc_16 >> 16) & 0xf][(dd_16 >> 16) & 0xf]]) | ((Txor[Txor[(aa_16 >> 20) & 0xf][(bb_16 >> 20) & 0xf]][Txor[(cc_16 >> 20) & 0xf][(dd_16 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_19 >> 24) & 0xf][(bb_19 >> 24) & 0xf]][Txor[(cc_19 >> 24) & 0xf][(dd_19 >> 24) & 0xf]]) | ((Txor[Txor[(aa_19 >> 28) & 0xf][(bb_19 >> 28) & 0xf]][Txor[(cc_19 >> 28) & 0xf][(dd_19 >> 28) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_16 >> 0) & 0xf][(bb_16 >> 0) & 0xf]][Txor[(cc_16 >> 0) & 0xf][(dd_16 >> 0) & 0xf]]) | ((Txor[Txor[(aa_16 >> 4) & 0xf][(bb_16 >> 4) & 0xf]][Txor[(cc_16 >> 4) & 0xf][(dd_16 >> 4) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_17 >> 24) & 0xf][(bb_17 >> 24) & 0xf]][Txor[(cc_17 >> 24) & 0xf][(dd_17 >> 24) & 0xf]]) | ((Txor[Txor[(aa_17 >> 28) & 0xf][(bb_17 >> 28) & 0xf]][Txor[(cc_17 >> 28) & 0xf][(dd_17 >> 28) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_18 >> 24) & 0xf][(bb_18 >> 24) & 0xf]][Txor[(cc_18 >> 24) & 0xf][(dd_18 >> 24) & 0xf]]) | ((Txor[Txor[(aa_18 >> 28) & 0xf][(bb_18 >> 28) & 0xf]][Txor[(cc_18 >> 28) & 0xf][(dd_18 >> 28) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_16 >> 24) & 0xf][(bb_16 >> 24) & 0xf]][Txor[(cc_16 >> 24) & 0xf][(dd_16 >> 24) & 0xf]]) | ((Txor[Txor[(aa_16 >> 28) & 0xf][(bb_16 >> 28) & 0xf]][Txor[(cc_16 >> 28) & 0xf][(dd_16 >> 28) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_18 >> 8) & 0xf][(bb_18 >> 8) & 0xf]][Txor[(cc_18 >> 8) & 0xf][(dd_18 >> 8) & 0xf]]) | ((Txor[Txor[(aa_18 >> 12) & 0xf][(bb_18 >> 12) & 0xf]][Txor[(cc_18 >> 12) & 0xf][(dd_18 >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_18 >> 16) & 0xf][(bb_18 >> 16) & 0xf]][Txor[(cc_18 >> 16) & 0xf][(dd_18 >> 16) & 0xf]]) | ((Txor[Txor[(aa_18 >> 20) & 0xf][(bb_18 >> 20) & 0xf]][Txor[(cc_18 >> 20) & 0xf][(dd_18 >> 20) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_17 >> 0) & 0xf][(bb_17 >> 0) & 0xf]][Txor[(cc_17 >> 0) & 0xf][(dd_17 >> 0) & 0xf]]) | ((Txor[Txor[(aa_17 >> 4) & 0xf][(bb_17 >> 4) & 0xf]][Txor[(cc_17 >> 4) & 0xf][(dd_17 >> 4) & 0xf]]) << 4);
    out[8] = (Txor[Txor[(aa_18 >> 0) & 0xf][(bb_18 >> 0) & 0xf]][Txor[(cc_18 >> 0) & 0xf][(dd_18 >> 0) & 0xf]]) | ((Txor[Txor[(aa_18 >> 4) & 0xf][(bb_18 >> 4) & 0xf]][Txor[(cc_18 >> 4) & 0xf][(dd_18 >> 4) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_17 >> 16) & 0xf][(bb_17 >> 16) & 0xf]][Txor[(cc_17 >> 16) & 0xf][(dd_17 >> 16) & 0xf]]) | ((Txor[Txor[(aa_17 >> 20) & 0xf][(bb_17 >> 20) & 0xf]][Txor[(cc_17 >> 20) & 0xf][(dd_17 >> 20) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_17 >> 8) & 0xf][(bb_17 >> 8) & 0xf]][Txor[(cc_17 >> 8) & 0xf][(dd_17 >> 8) & 0xf]]) | ((Txor[Txor[(aa_17 >> 12) & 0xf][(bb_17 >> 12) & 0xf]][Txor[(cc_17 >> 12) & 0xf][(dd_17 >> 12) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int aa_20 = Tyboxes[5][0][out[0]];
    unsigned int aa_21 = Tyboxes[5][4][out[4]];
    unsigned int bb_21 = Tyboxes[5][5][out[5]];
    unsigned int cc_21 = Tyboxes[5][6][out[6]];
    unsigned int dd_21 = Tyboxes[5][7][out[7]];
    unsigned int dd_22 = Tyboxes[5][11][out[11]];
    unsigned int cc_22 = Tyboxes[5][10][out[10]];
    unsigned int dd_20 = Tyboxes[5][3][out[3]];
    unsigned int cc_20 = Tyboxes[5][2][out[2]];
    unsigned int bb_22 = Tyboxes[5][9][out[9]];
    unsigned int aa_22 = Tyboxes[5][8][out[8]];
    unsigned int cc_23 = Tyboxes[5][14][out[14]];
    unsigned int dd_23 = Tyboxes[5][15][out[15]];
    unsigned int aa_23 = Tyboxes[5][12][out[12]];
    unsigned int bb_23 = Tyboxes[5][13][out[13]];
    unsigned int bb_20 = Tyboxes[5][1][out[1]];
    out[0] = (Txor[Txor[(aa_20 >> 0) & 0xf][(bb_20 >> 0) & 0xf]][Txor[(cc_20 >> 0) & 0xf][(dd_20 >> 0) & 0xf]]) | ((Txor[Txor[(aa_20 >> 4) & 0xf][(bb_20 >> 4) & 0xf]][Txor[(cc_20 >> 4) & 0xf][(dd_20 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_20 >> 8) & 0xf][(bb_20 >> 8) & 0xf]][Txor[(cc_20 >> 8) & 0xf][(dd_20 >> 8) & 0xf]]) | ((Txor[Txor[(aa_20 >> 12) & 0xf][(bb_20 >> 12) & 0xf]][Txor[(cc_20 >> 12) & 0xf][(dd_20 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_20 >> 16) & 0xf][(bb_20 >> 16) & 0xf]][Txor[(cc_20 >> 16) & 0xf][(dd_20 >> 16) & 0xf]]) | ((Txor[Txor[(aa_20 >> 20) & 0xf][(bb_20 >> 20) & 0xf]][Txor[(cc_20 >> 20) & 0xf][(dd_20 >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_20 >> 24) & 0xf][(bb_20 >> 24) & 0xf]][Txor[(cc_20 >> 24) & 0xf][(dd_20 >> 24) & 0xf]]) | ((Txor[Txor[(aa_20 >> 28) & 0xf][(bb_20 >> 28) & 0xf]][Txor[(cc_20 >> 28) & 0xf][(dd_20 >> 28) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_22 >> 24) & 0xf][(bb_22 >> 24) & 0xf]][Txor[(cc_22 >> 24) & 0xf][(dd_22 >> 24) & 0xf]]) | ((Txor[Txor[(aa_22 >> 28) & 0xf][(bb_22 >> 28) & 0xf]][Txor[(cc_22 >> 28) & 0xf][(dd_22 >> 28) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_22 >> 16) & 0xf][(bb_22 >> 16) & 0xf]][Txor[(cc_22 >> 16) & 0xf][(dd_22 >> 16) & 0xf]]) | ((Txor[Txor[(aa_22 >> 20) & 0xf][(bb_22 >> 20) & 0xf]][Txor[(cc_22 >> 20) & 0xf][(dd_22 >> 20) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_21 >> 0) & 0xf][(bb_21 >> 0) & 0xf]][Txor[(cc_21 >> 0) & 0xf][(dd_21 >> 0) & 0xf]]) | ((Txor[Txor[(aa_21 >> 4) & 0xf][(bb_21 >> 4) & 0xf]][Txor[(cc_21 >> 4) & 0xf][(dd_21 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_21 >> 8) & 0xf][(bb_21 >> 8) & 0xf]][Txor[(cc_21 >> 8) & 0xf][(dd_21 >> 8) & 0xf]]) | ((Txor[Txor[(aa_21 >> 12) & 0xf][(bb_21 >> 12) & 0xf]][Txor[(cc_21 >> 12) & 0xf][(dd_21 >> 12) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_22 >> 8) & 0xf][(bb_22 >> 8) & 0xf]][Txor[(cc_22 >> 8) & 0xf][(dd_22 >> 8) & 0xf]]) | ((Txor[Txor[(aa_22 >> 12) & 0xf][(bb_22 >> 12) & 0xf]][Txor[(cc_22 >> 12) & 0xf][(dd_22 >> 12) & 0xf]]) << 4);
    out[8] = (Txor[Txor[(aa_22 >> 0) & 0xf][(bb_22 >> 0) & 0xf]][Txor[(cc_22 >> 0) & 0xf][(dd_22 >> 0) & 0xf]]) | ((Txor[Txor[(aa_22 >> 4) & 0xf][(bb_22 >> 4) & 0xf]][Txor[(cc_22 >> 4) & 0xf][(dd_22 >> 4) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_21 >> 24) & 0xf][(bb_21 >> 24) & 0xf]][Txor[(cc_21 >> 24) & 0xf][(dd_21 >> 24) & 0xf]]) | ((Txor[Txor[(aa_21 >> 28) & 0xf][(bb_21 >> 28) & 0xf]][Txor[(cc_21 >> 28) & 0xf][(dd_21 >> 28) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_21 >> 16) & 0xf][(bb_21 >> 16) & 0xf]][Txor[(cc_21 >> 16) & 0xf][(dd_21 >> 16) & 0xf]]) | ((Txor[Txor[(aa_21 >> 20) & 0xf][(bb_21 >> 20) & 0xf]][Txor[(cc_21 >> 20) & 0xf][(dd_21 >> 20) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_23 >> 16) & 0xf][(bb_23 >> 16) & 0xf]][Txor[(cc_23 >> 16) & 0xf][(dd_23 >> 16) & 0xf]]) | ((Txor[Txor[(aa_23 >> 20) & 0xf][(bb_23 >> 20) & 0xf]][Txor[(cc_23 >> 20) & 0xf][(dd_23 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_23 >> 24) & 0xf][(bb_23 >> 24) & 0xf]][Txor[(cc_23 >> 24) & 0xf][(dd_23 >> 24) & 0xf]]) | ((Txor[Txor[(aa_23 >> 28) & 0xf][(bb_23 >> 28) & 0xf]][Txor[(cc_23 >> 28) & 0xf][(dd_23 >> 28) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_23 >> 0) & 0xf][(bb_23 >> 0) & 0xf]][Txor[(cc_23 >> 0) & 0xf][(dd_23 >> 0) & 0xf]]) | ((Txor[Txor[(aa_23 >> 4) & 0xf][(bb_23 >> 4) & 0xf]][Txor[(cc_23 >> 4) & 0xf][(dd_23 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_23 >> 8) & 0xf][(bb_23 >> 8) & 0xf]][Txor[(cc_23 >> 8) & 0xf][(dd_23 >> 8) & 0xf]]) | ((Txor[Txor[(aa_23 >> 12) & 0xf][(bb_23 >> 12) & 0xf]][Txor[(cc_23 >> 12) & 0xf][(dd_23 >> 12) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int aa_27 = Tyboxes[6][12][out[12]];
    unsigned int bb_27 = Tyboxes[6][13][out[13]];
    unsigned int cc_27 = Tyboxes[6][14][out[14]];
    unsigned int dd_27 = Tyboxes[6][15][out[15]];
    unsigned int bb_26 = Tyboxes[6][9][out[9]];
    unsigned int aa_26 = Tyboxes[6][8][out[8]];
    unsigned int dd_26 = Tyboxes[6][11][out[11]];
    unsigned int bb_25 = Tyboxes[6][5][out[5]];
    unsigned int cc_25 = Tyboxes[6][6][out[6]];
    unsigned int cc_26 = Tyboxes[6][10][out[10]];
    unsigned int aa_25 = Tyboxes[6][4][out[4]];
    unsigned int dd_25 = Tyboxes[6][7][out[7]];
    unsigned int aa_24 = Tyboxes[6][0][out[0]];
    unsigned int dd_24 = Tyboxes[6][3][out[3]];
    unsigned int bb_24 = Tyboxes[6][1][out[1]];
    unsigned int cc_24 = Tyboxes[6][2][out[2]];
    out[6] = (Txor[Txor[(aa_25 >> 16) & 0xf][(bb_25 >> 16) & 0xf]][Txor[(cc_25 >> 16) & 0xf][(dd_25 >> 16) & 0xf]]) | ((Txor[Txor[(aa_25 >> 20) & 0xf][(bb_25 >> 20) & 0xf]][Txor[(cc_25 >> 20) & 0xf][(dd_25 >> 20) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_26 >> 16) & 0xf][(bb_26 >> 16) & 0xf]][Txor[(cc_26 >> 16) & 0xf][(dd_26 >> 16) & 0xf]]) | ((Txor[Txor[(aa_26 >> 20) & 0xf][(bb_26 >> 20) & 0xf]][Txor[(cc_26 >> 20) & 0xf][(dd_26 >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_26 >> 24) & 0xf][(bb_26 >> 24) & 0xf]][Txor[(cc_26 >> 24) & 0xf][(dd_26 >> 24) & 0xf]]) | ((Txor[Txor[(aa_26 >> 28) & 0xf][(bb_26 >> 28) & 0xf]][Txor[(cc_26 >> 28) & 0xf][(dd_26 >> 28) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_27 >> 24) & 0xf][(bb_27 >> 24) & 0xf]][Txor[(cc_27 >> 24) & 0xf][(dd_27 >> 24) & 0xf]]) | ((Txor[Txor[(aa_27 >> 28) & 0xf][(bb_27 >> 28) & 0xf]][Txor[(cc_27 >> 28) & 0xf][(dd_27 >> 28) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_26 >> 8) & 0xf][(bb_26 >> 8) & 0xf]][Txor[(cc_26 >> 8) & 0xf][(dd_26 >> 8) & 0xf]]) | ((Txor[Txor[(aa_26 >> 12) & 0xf][(bb_26 >> 12) & 0xf]][Txor[(cc_26 >> 12) & 0xf][(dd_26 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_24 >> 16) & 0xf][(bb_24 >> 16) & 0xf]][Txor[(cc_24 >> 16) & 0xf][(dd_24 >> 16) & 0xf]]) | ((Txor[Txor[(aa_24 >> 20) & 0xf][(bb_24 >> 20) & 0xf]][Txor[(cc_24 >> 20) & 0xf][(dd_24 >> 20) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_27 >> 0) & 0xf][(bb_27 >> 0) & 0xf]][Txor[(cc_27 >> 0) & 0xf][(dd_27 >> 0) & 0xf]]) | ((Txor[Txor[(aa_27 >> 4) & 0xf][(bb_27 >> 4) & 0xf]][Txor[(cc_27 >> 4) & 0xf][(dd_27 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_27 >> 8) & 0xf][(bb_27 >> 8) & 0xf]][Txor[(cc_27 >> 8) & 0xf][(dd_27 >> 8) & 0xf]]) | ((Txor[Txor[(aa_27 >> 12) & 0xf][(bb_27 >> 12) & 0xf]][Txor[(cc_27 >> 12) & 0xf][(dd_27 >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_27 >> 16) & 0xf][(bb_27 >> 16) & 0xf]][Txor[(cc_27 >> 16) & 0xf][(dd_27 >> 16) & 0xf]]) | ((Txor[Txor[(aa_27 >> 20) & 0xf][(bb_27 >> 20) & 0xf]][Txor[(cc_27 >> 20) & 0xf][(dd_27 >> 20) & 0xf]]) << 4);
    out[8] = (Txor[Txor[(aa_26 >> 0) & 0xf][(bb_26 >> 0) & 0xf]][Txor[(cc_26 >> 0) & 0xf][(dd_26 >> 0) & 0xf]]) | ((Txor[Txor[(aa_26 >> 4) & 0xf][(bb_26 >> 4) & 0xf]][Txor[(cc_26 >> 4) & 0xf][(dd_26 >> 4) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_25 >> 24) & 0xf][(bb_25 >> 24) & 0xf]][Txor[(cc_25 >> 24) & 0xf][(dd_25 >> 24) & 0xf]]) | ((Txor[Txor[(aa_25 >> 28) & 0xf][(bb_25 >> 28) & 0xf]][Txor[(cc_25 >> 28) & 0xf][(dd_25 >> 28) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_24 >> 24) & 0xf][(bb_24 >> 24) & 0xf]][Txor[(cc_24 >> 24) & 0xf][(dd_24 >> 24) & 0xf]]) | ((Txor[Txor[(aa_24 >> 28) & 0xf][(bb_24 >> 28) & 0xf]][Txor[(cc_24 >> 28) & 0xf][(dd_24 >> 28) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_25 >> 0) & 0xf][(bb_25 >> 0) & 0xf]][Txor[(cc_25 >> 0) & 0xf][(dd_25 >> 0) & 0xf]]) | ((Txor[Txor[(aa_25 >> 4) & 0xf][(bb_25 >> 4) & 0xf]][Txor[(cc_25 >> 4) & 0xf][(dd_25 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_24 >> 8) & 0xf][(bb_24 >> 8) & 0xf]][Txor[(cc_24 >> 8) & 0xf][(dd_24 >> 8) & 0xf]]) | ((Txor[Txor[(aa_24 >> 12) & 0xf][(bb_24 >> 12) & 0xf]][Txor[(cc_24 >> 12) & 0xf][(dd_24 >> 12) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_25 >> 8) & 0xf][(bb_25 >> 8) & 0xf]][Txor[(cc_25 >> 8) & 0xf][(dd_25 >> 8) & 0xf]]) | ((Txor[Txor[(aa_25 >> 12) & 0xf][(bb_25 >> 12) & 0xf]][Txor[(cc_25 >> 12) & 0xf][(dd_25 >> 12) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_24 >> 0) & 0xf][(bb_24 >> 0) & 0xf]][Txor[(cc_24 >> 0) & 0xf][(dd_24 >> 0) & 0xf]]) | ((Txor[Txor[(aa_24 >> 4) & 0xf][(bb_24 >> 4) & 0xf]][Txor[(cc_24 >> 4) & 0xf][(dd_24 >> 4) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int bb_28 = Tyboxes[7][1][out[1]];
    unsigned int aa_28 = Tyboxes[7][0][out[0]];
    unsigned int bb_31 = Tyboxes[7][13][out[13]];
    unsigned int aa_31 = Tyboxes[7][12][out[12]];
    unsigned int dd_30 = Tyboxes[7][11][out[11]];
    unsigned int cc_30 = Tyboxes[7][10][out[10]];
    unsigned int dd_28 = Tyboxes[7][3][out[3]];
    unsigned int cc_28 = Tyboxes[7][2][out[2]];
    unsigned int cc_29 = Tyboxes[7][6][out[6]];
    unsigned int dd_29 = Tyboxes[7][7][out[7]];
    unsigned int aa_29 = Tyboxes[7][4][out[4]];
    unsigned int bb_29 = Tyboxes[7][5][out[5]];
    unsigned int dd_31 = Tyboxes[7][15][out[15]];
    unsigned int cc_31 = Tyboxes[7][14][out[14]];
    unsigned int aa_30 = Tyboxes[7][8][out[8]];
    unsigned int bb_30 = Tyboxes[7][9][out[9]];
    out[11] = (Txor[Txor[(aa_30 >> 24) & 0xf][(bb_30 >> 24) & 0xf]][Txor[(cc_30 >> 24) & 0xf][(dd_30 >> 24) & 0xf]]) | ((Txor[Txor[(aa_30 >> 28) & 0xf][(bb_30 >> 28) & 0xf]][Txor[(cc_30 >> 28) & 0xf][(dd_30 >> 28) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_30 >> 16) & 0xf][(bb_30 >> 16) & 0xf]][Txor[(cc_30 >> 16) & 0xf][(dd_30 >> 16) & 0xf]]) | ((Txor[Txor[(aa_30 >> 20) & 0xf][(bb_30 >> 20) & 0xf]][Txor[(cc_30 >> 20) & 0xf][(dd_30 >> 20) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_28 >> 8) & 0xf][(bb_28 >> 8) & 0xf]][Txor[(cc_28 >> 8) & 0xf][(dd_28 >> 8) & 0xf]]) | ((Txor[Txor[(aa_28 >> 12) & 0xf][(bb_28 >> 12) & 0xf]][Txor[(cc_28 >> 12) & 0xf][(dd_28 >> 12) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_28 >> 0) & 0xf][(bb_28 >> 0) & 0xf]][Txor[(cc_28 >> 0) & 0xf][(dd_28 >> 0) & 0xf]]) | ((Txor[Txor[(aa_28 >> 4) & 0xf][(bb_28 >> 4) & 0xf]][Txor[(cc_28 >> 4) & 0xf][(dd_28 >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_30 >> 8) & 0xf][(bb_30 >> 8) & 0xf]][Txor[(cc_30 >> 8) & 0xf][(dd_30 >> 8) & 0xf]]) | ((Txor[Txor[(aa_30 >> 12) & 0xf][(bb_30 >> 12) & 0xf]][Txor[(cc_30 >> 12) & 0xf][(dd_30 >> 12) & 0xf]]) << 4);
    out[8] = (Txor[Txor[(aa_30 >> 0) & 0xf][(bb_30 >> 0) & 0xf]][Txor[(cc_30 >> 0) & 0xf][(dd_30 >> 0) & 0xf]]) | ((Txor[Txor[(aa_30 >> 4) & 0xf][(bb_30 >> 4) & 0xf]][Txor[(cc_30 >> 4) & 0xf][(dd_30 >> 4) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_28 >> 24) & 0xf][(bb_28 >> 24) & 0xf]][Txor[(cc_28 >> 24) & 0xf][(dd_28 >> 24) & 0xf]]) | ((Txor[Txor[(aa_28 >> 28) & 0xf][(bb_28 >> 28) & 0xf]][Txor[(cc_28 >> 28) & 0xf][(dd_28 >> 28) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_28 >> 16) & 0xf][(bb_28 >> 16) & 0xf]][Txor[(cc_28 >> 16) & 0xf][(dd_28 >> 16) & 0xf]]) | ((Txor[Txor[(aa_28 >> 20) & 0xf][(bb_28 >> 20) & 0xf]][Txor[(cc_28 >> 20) & 0xf][(dd_28 >> 20) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_29 >> 16) & 0xf][(bb_29 >> 16) & 0xf]][Txor[(cc_29 >> 16) & 0xf][(dd_29 >> 16) & 0xf]]) | ((Txor[Txor[(aa_29 >> 20) & 0xf][(bb_29 >> 20) & 0xf]][Txor[(cc_29 >> 20) & 0xf][(dd_29 >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_29 >> 24) & 0xf][(bb_29 >> 24) & 0xf]][Txor[(cc_29 >> 24) & 0xf][(dd_29 >> 24) & 0xf]]) | ((Txor[Txor[(aa_29 >> 28) & 0xf][(bb_29 >> 28) & 0xf]][Txor[(cc_29 >> 28) & 0xf][(dd_29 >> 28) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_29 >> 0) & 0xf][(bb_29 >> 0) & 0xf]][Txor[(cc_29 >> 0) & 0xf][(dd_29 >> 0) & 0xf]]) | ((Txor[Txor[(aa_29 >> 4) & 0xf][(bb_29 >> 4) & 0xf]][Txor[(cc_29 >> 4) & 0xf][(dd_29 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_29 >> 8) & 0xf][(bb_29 >> 8) & 0xf]][Txor[(cc_29 >> 8) & 0xf][(dd_29 >> 8) & 0xf]]) | ((Txor[Txor[(aa_29 >> 12) & 0xf][(bb_29 >> 12) & 0xf]][Txor[(cc_29 >> 12) & 0xf][(dd_29 >> 12) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_31 >> 8) & 0xf][(bb_31 >> 8) & 0xf]][Txor[(cc_31 >> 8) & 0xf][(dd_31 >> 8) & 0xf]]) | ((Txor[Txor[(aa_31 >> 12) & 0xf][(bb_31 >> 12) & 0xf]][Txor[(cc_31 >> 12) & 0xf][(dd_31 >> 12) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_31 >> 0) & 0xf][(bb_31 >> 0) & 0xf]][Txor[(cc_31 >> 0) & 0xf][(dd_31 >> 0) & 0xf]]) | ((Txor[Txor[(aa_31 >> 4) & 0xf][(bb_31 >> 4) & 0xf]][Txor[(cc_31 >> 4) & 0xf][(dd_31 >> 4) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_31 >> 16) & 0xf][(bb_31 >> 16) & 0xf]][Txor[(cc_31 >> 16) & 0xf][(dd_31 >> 16) & 0xf]]) | ((Txor[Txor[(aa_31 >> 20) & 0xf][(bb_31 >> 20) & 0xf]][Txor[(cc_31 >> 20) & 0xf][(dd_31 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_31 >> 24) & 0xf][(bb_31 >> 24) & 0xf]][Txor[(cc_31 >> 24) & 0xf][(dd_31 >> 24) & 0xf]]) | ((Txor[Txor[(aa_31 >> 28) & 0xf][(bb_31 >> 28) & 0xf]][Txor[(cc_31 >> 28) & 0xf][(dd_31 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int cc_35 = Tyboxes[8][14][out[14]];
    unsigned int bb_35 = Tyboxes[8][13][out[13]];
    unsigned int dd_34 = Tyboxes[8][11][out[11]];
    unsigned int dd_35 = Tyboxes[8][15][out[15]];
    unsigned int bb_34 = Tyboxes[8][9][out[9]];
    unsigned int cc_34 = Tyboxes[8][10][out[10]];
    unsigned int cc_32 = Tyboxes[8][2][out[2]];
    unsigned int aa_34 = Tyboxes[8][8][out[8]];
    unsigned int dd_33 = Tyboxes[8][7][out[7]];
    unsigned int cc_33 = Tyboxes[8][6][out[6]];
    unsigned int bb_33 = Tyboxes[8][5][out[5]];
    unsigned int aa_33 = Tyboxes[8][4][out[4]];
    unsigned int aa_35 = Tyboxes[8][12][out[12]];
    unsigned int bb_32 = Tyboxes[8][1][out[1]];
    unsigned int aa_32 = Tyboxes[8][0][out[0]];
    unsigned int dd_32 = Tyboxes[8][3][out[3]];
    out[9] = (Txor[Txor[(aa_34 >> 8) & 0xf][(bb_34 >> 8) & 0xf]][Txor[(cc_34 >> 8) & 0xf][(dd_34 >> 8) & 0xf]]) | ((Txor[Txor[(aa_34 >> 12) & 0xf][(bb_34 >> 12) & 0xf]][Txor[(cc_34 >> 12) & 0xf][(dd_34 >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_34 >> 16) & 0xf][(bb_34 >> 16) & 0xf]][Txor[(cc_34 >> 16) & 0xf][(dd_34 >> 16) & 0xf]]) | ((Txor[Txor[(aa_34 >> 20) & 0xf][(bb_34 >> 20) & 0xf]][Txor[(cc_34 >> 20) & 0xf][(dd_34 >> 20) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_35 >> 0) & 0xf][(bb_35 >> 0) & 0xf]][Txor[(cc_35 >> 0) & 0xf][(dd_35 >> 0) & 0xf]]) | ((Txor[Txor[(aa_35 >> 4) & 0xf][(bb_35 >> 4) & 0xf]][Txor[(cc_35 >> 4) & 0xf][(dd_35 >> 4) & 0xf]]) << 4);
    out[8] = (Txor[Txor[(aa_34 >> 0) & 0xf][(bb_34 >> 0) & 0xf]][Txor[(cc_34 >> 0) & 0xf][(dd_34 >> 0) & 0xf]]) | ((Txor[Txor[(aa_34 >> 4) & 0xf][(bb_34 >> 4) & 0xf]][Txor[(cc_34 >> 4) & 0xf][(dd_34 >> 4) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_35 >> 16) & 0xf][(bb_35 >> 16) & 0xf]][Txor[(cc_35 >> 16) & 0xf][(dd_35 >> 16) & 0xf]]) | ((Txor[Txor[(aa_35 >> 20) & 0xf][(bb_35 >> 20) & 0xf]][Txor[(cc_35 >> 20) & 0xf][(dd_35 >> 20) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_32 >> 0) & 0xf][(bb_32 >> 0) & 0xf]][Txor[(cc_32 >> 0) & 0xf][(dd_32 >> 0) & 0xf]]) | ((Txor[Txor[(aa_32 >> 4) & 0xf][(bb_32 >> 4) & 0xf]][Txor[(cc_32 >> 4) & 0xf][(dd_32 >> 4) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_33 >> 16) & 0xf][(bb_33 >> 16) & 0xf]][Txor[(cc_33 >> 16) & 0xf][(dd_33 >> 16) & 0xf]]) | ((Txor[Txor[(aa_33 >> 20) & 0xf][(bb_33 >> 20) & 0xf]][Txor[(cc_33 >> 20) & 0xf][(dd_33 >> 20) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_33 >> 8) & 0xf][(bb_33 >> 8) & 0xf]][Txor[(cc_33 >> 8) & 0xf][(dd_33 >> 8) & 0xf]]) | ((Txor[Txor[(aa_33 >> 12) & 0xf][(bb_33 >> 12) & 0xf]][Txor[(cc_33 >> 12) & 0xf][(dd_33 >> 12) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_33 >> 0) & 0xf][(bb_33 >> 0) & 0xf]][Txor[(cc_33 >> 0) & 0xf][(dd_33 >> 0) & 0xf]]) | ((Txor[Txor[(aa_33 >> 4) & 0xf][(bb_33 >> 4) & 0xf]][Txor[(cc_33 >> 4) & 0xf][(dd_33 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_35 >> 8) & 0xf][(bb_35 >> 8) & 0xf]][Txor[(cc_35 >> 8) & 0xf][(dd_35 >> 8) & 0xf]]) | ((Txor[Txor[(aa_35 >> 12) & 0xf][(bb_35 >> 12) & 0xf]][Txor[(cc_35 >> 12) & 0xf][(dd_35 >> 12) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_32 >> 24) & 0xf][(bb_32 >> 24) & 0xf]][Txor[(cc_32 >> 24) & 0xf][(dd_32 >> 24) & 0xf]]) | ((Txor[Txor[(aa_32 >> 28) & 0xf][(bb_32 >> 28) & 0xf]][Txor[(cc_32 >> 28) & 0xf][(dd_32 >> 28) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_32 >> 16) & 0xf][(bb_32 >> 16) & 0xf]][Txor[(cc_32 >> 16) & 0xf][(dd_32 >> 16) & 0xf]]) | ((Txor[Txor[(aa_32 >> 20) & 0xf][(bb_32 >> 20) & 0xf]][Txor[(cc_32 >> 20) & 0xf][(dd_32 >> 20) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_32 >> 8) & 0xf][(bb_32 >> 8) & 0xf]][Txor[(cc_32 >> 8) & 0xf][(dd_32 >> 8) & 0xf]]) | ((Txor[Txor[(aa_32 >> 12) & 0xf][(bb_32 >> 12) & 0xf]][Txor[(cc_32 >> 12) & 0xf][(dd_32 >> 12) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_34 >> 24) & 0xf][(bb_34 >> 24) & 0xf]][Txor[(cc_34 >> 24) & 0xf][(dd_34 >> 24) & 0xf]]) | ((Txor[Txor[(aa_34 >> 28) & 0xf][(bb_34 >> 28) & 0xf]][Txor[(cc_34 >> 28) & 0xf][(dd_34 >> 28) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_35 >> 24) & 0xf][(bb_35 >> 24) & 0xf]][Txor[(cc_35 >> 24) & 0xf][(dd_35 >> 24) & 0xf]]) | ((Txor[Txor[(aa_35 >> 28) & 0xf][(bb_35 >> 28) & 0xf]][Txor[(cc_35 >> 28) & 0xf][(dd_35 >> 28) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_33 >> 24) & 0xf][(bb_33 >> 24) & 0xf]][Txor[(cc_33 >> 24) & 0xf][(dd_33 >> 24) & 0xf]]) | ((Txor[Txor[(aa_33 >> 28) & 0xf][(bb_33 >> 28) & 0xf]][Txor[(cc_33 >> 28) & 0xf][(dd_33 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    out[13] = Tboxes_[13][out[13]];
    out[14] = Tboxes_[14][out[14]];
    out[1] = Tboxes_[1][out[1]];
    out[0] = Tboxes_[0][out[0]];
    out[15] = Tboxes_[15][out[15]];
    out[9] = Tboxes_[9][out[9]];
    out[8] = Tboxes_[8][out[8]];
    out[7] = Tboxes_[7][out[7]];
    out[6] = Tboxes_[6][out[6]];
    out[5] = Tboxes_[5][out[5]];
    out[4] = Tboxes_[4][out[4]];
    out[3] = Tboxes_[3][out[3]];
    out[2] = Tboxes_[2][out[2]];
    out[12] = Tboxes_[12][out[12]];
    out[11] = Tboxes_[11][out[11]];
    out[10] = Tboxes_[10][out[10]];
}

void aes128_enc_wb_final_unrolled_shuffled_3886914148(unsigned char in[16], unsigned char out[16])
{
    memcpy(out, in, 16);
    ShiftRows(out);
    unsigned int bb_0 = Tyboxes[0][1][out[1]];
    unsigned int aa_1 = Tyboxes[0][4][out[4]];
    unsigned int dd_0 = Tyboxes[0][3][out[3]];
    unsigned int cc_3 = Tyboxes[0][14][out[14]];
    unsigned int cc_0 = Tyboxes[0][2][out[2]];
    unsigned int aa_0 = Tyboxes[0][0][out[0]];
    unsigned int dd_3 = Tyboxes[0][15][out[15]];
    unsigned int bb_2 = Tyboxes[0][9][out[9]];
    unsigned int cc_2 = Tyboxes[0][10][out[10]];
    unsigned int aa_3 = Tyboxes[0][12][out[12]];
    unsigned int aa_2 = Tyboxes[0][8][out[8]];
    unsigned int dd_2 = Tyboxes[0][11][out[11]];
    unsigned int dd_1 = Tyboxes[0][7][out[7]];
    unsigned int bb_3 = Tyboxes[0][13][out[13]];
    unsigned int bb_1 = Tyboxes[0][5][out[5]];
    unsigned int cc_1 = Tyboxes[0][6][out[6]];
    out[8] = (Txor[Txor[(aa_2 >> 0) & 0xf][(bb_2 >> 0) & 0xf]][Txor[(cc_2 >> 0) & 0xf][(dd_2 >> 0) & 0xf]]) | ((Txor[Txor[(aa_2 >> 4) & 0xf][(bb_2 >> 4) & 0xf]][Txor[(cc_2 >> 4) & 0xf][(dd_2 >> 4) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_0 >> 24) & 0xf][(bb_0 >> 24) & 0xf]][Txor[(cc_0 >> 24) & 0xf][(dd_0 >> 24) & 0xf]]) | ((Txor[Txor[(aa_0 >> 28) & 0xf][(bb_0 >> 28) & 0xf]][Txor[(cc_0 >> 28) & 0xf][(dd_0 >> 28) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_0 >> 8) & 0xf][(bb_0 >> 8) & 0xf]][Txor[(cc_0 >> 8) & 0xf][(dd_0 >> 8) & 0xf]]) | ((Txor[Txor[(aa_0 >> 12) & 0xf][(bb_0 >> 12) & 0xf]][Txor[(cc_0 >> 12) & 0xf][(dd_0 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_0 >> 16) & 0xf][(bb_0 >> 16) & 0xf]][Txor[(cc_0 >> 16) & 0xf][(dd_0 >> 16) & 0xf]]) | ((Txor[Txor[(aa_0 >> 20) & 0xf][(bb_0 >> 20) & 0xf]][Txor[(cc_0 >> 20) & 0xf][(dd_0 >> 20) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_0 >> 0) & 0xf][(bb_0 >> 0) & 0xf]][Txor[(cc_0 >> 0) & 0xf][(dd_0 >> 0) & 0xf]]) | ((Txor[Txor[(aa_0 >> 4) & 0xf][(bb_0 >> 4) & 0xf]][Txor[(cc_0 >> 4) & 0xf][(dd_0 >> 4) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_3 >> 0) & 0xf][(bb_3 >> 0) & 0xf]][Txor[(cc_3 >> 0) & 0xf][(dd_3 >> 0) & 0xf]]) | ((Txor[Txor[(aa_3 >> 4) & 0xf][(bb_3 >> 4) & 0xf]][Txor[(cc_3 >> 4) & 0xf][(dd_3 >> 4) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_2 >> 16) & 0xf][(bb_2 >> 16) & 0xf]][Txor[(cc_2 >> 16) & 0xf][(dd_2 >> 16) & 0xf]]) | ((Txor[Txor[(aa_2 >> 20) & 0xf][(bb_2 >> 20) & 0xf]][Txor[(cc_2 >> 20) & 0xf][(dd_2 >> 20) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_3 >> 16) & 0xf][(bb_3 >> 16) & 0xf]][Txor[(cc_3 >> 16) & 0xf][(dd_3 >> 16) & 0xf]]) | ((Txor[Txor[(aa_3 >> 20) & 0xf][(bb_3 >> 20) & 0xf]][Txor[(cc_3 >> 20) & 0xf][(dd_3 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_3 >> 24) & 0xf][(bb_3 >> 24) & 0xf]][Txor[(cc_3 >> 24) & 0xf][(dd_3 >> 24) & 0xf]]) | ((Txor[Txor[(aa_3 >> 28) & 0xf][(bb_3 >> 28) & 0xf]][Txor[(cc_3 >> 28) & 0xf][(dd_3 >> 28) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_1 >> 24) & 0xf][(bb_1 >> 24) & 0xf]][Txor[(cc_1 >> 24) & 0xf][(dd_1 >> 24) & 0xf]]) | ((Txor[Txor[(aa_1 >> 28) & 0xf][(bb_1 >> 28) & 0xf]][Txor[(cc_1 >> 28) & 0xf][(dd_1 >> 28) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_2 >> 8) & 0xf][(bb_2 >> 8) & 0xf]][Txor[(cc_2 >> 8) & 0xf][(dd_2 >> 8) & 0xf]]) | ((Txor[Txor[(aa_2 >> 12) & 0xf][(bb_2 >> 12) & 0xf]][Txor[(cc_2 >> 12) & 0xf][(dd_2 >> 12) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_1 >> 8) & 0xf][(bb_1 >> 8) & 0xf]][Txor[(cc_1 >> 8) & 0xf][(dd_1 >> 8) & 0xf]]) | ((Txor[Txor[(aa_1 >> 12) & 0xf][(bb_1 >> 12) & 0xf]][Txor[(cc_1 >> 12) & 0xf][(dd_1 >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_1 >> 16) & 0xf][(bb_1 >> 16) & 0xf]][Txor[(cc_1 >> 16) & 0xf][(dd_1 >> 16) & 0xf]]) | ((Txor[Txor[(aa_1 >> 20) & 0xf][(bb_1 >> 20) & 0xf]][Txor[(cc_1 >> 20) & 0xf][(dd_1 >> 20) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_3 >> 8) & 0xf][(bb_3 >> 8) & 0xf]][Txor[(cc_3 >> 8) & 0xf][(dd_3 >> 8) & 0xf]]) | ((Txor[Txor[(aa_3 >> 12) & 0xf][(bb_3 >> 12) & 0xf]][Txor[(cc_3 >> 12) & 0xf][(dd_3 >> 12) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_1 >> 0) & 0xf][(bb_1 >> 0) & 0xf]][Txor[(cc_1 >> 0) & 0xf][(dd_1 >> 0) & 0xf]]) | ((Txor[Txor[(aa_1 >> 4) & 0xf][(bb_1 >> 4) & 0xf]][Txor[(cc_1 >> 4) & 0xf][(dd_1 >> 4) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_2 >> 24) & 0xf][(bb_2 >> 24) & 0xf]][Txor[(cc_2 >> 24) & 0xf][(dd_2 >> 24) & 0xf]]) | ((Txor[Txor[(aa_2 >> 28) & 0xf][(bb_2 >> 28) & 0xf]][Txor[(cc_2 >> 28) & 0xf][(dd_2 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int aa_6 = Tyboxes[1][8][out[8]];
    unsigned int aa_4 = Tyboxes[1][0][out[0]];
    unsigned int dd_6 = Tyboxes[1][11][out[11]];
    unsigned int cc_6 = Tyboxes[1][10][out[10]];
    unsigned int dd_7 = Tyboxes[1][15][out[15]];
    unsigned int cc_7 = Tyboxes[1][14][out[14]];
    unsigned int cc_4 = Tyboxes[1][2][out[2]];
    unsigned int bb_4 = Tyboxes[1][1][out[1]];
    unsigned int bb_5 = Tyboxes[1][5][out[5]];
    unsigned int aa_5 = Tyboxes[1][4][out[4]];
    unsigned int dd_5 = Tyboxes[1][7][out[7]];
    unsigned int cc_5 = Tyboxes[1][6][out[6]];
    unsigned int dd_4 = Tyboxes[1][3][out[3]];
    unsigned int aa_7 = Tyboxes[1][12][out[12]];
    unsigned int bb_7 = Tyboxes[1][13][out[13]];
    unsigned int bb_6 = Tyboxes[1][9][out[9]];
    out[8] = (Txor[Txor[(aa_6 >> 0) & 0xf][(bb_6 >> 0) & 0xf]][Txor[(cc_6 >> 0) & 0xf][(dd_6 >> 0) & 0xf]]) | ((Txor[Txor[(aa_6 >> 4) & 0xf][(bb_6 >> 4) & 0xf]][Txor[(cc_6 >> 4) & 0xf][(dd_6 >> 4) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_7 >> 24) & 0xf][(bb_7 >> 24) & 0xf]][Txor[(cc_7 >> 24) & 0xf][(dd_7 >> 24) & 0xf]]) | ((Txor[Txor[(aa_7 >> 28) & 0xf][(bb_7 >> 28) & 0xf]][Txor[(cc_7 >> 28) & 0xf][(dd_7 >> 28) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_7 >> 16) & 0xf][(bb_7 >> 16) & 0xf]][Txor[(cc_7 >> 16) & 0xf][(dd_7 >> 16) & 0xf]]) | ((Txor[Txor[(aa_7 >> 20) & 0xf][(bb_7 >> 20) & 0xf]][Txor[(cc_7 >> 20) & 0xf][(dd_7 >> 20) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_7 >> 8) & 0xf][(bb_7 >> 8) & 0xf]][Txor[(cc_7 >> 8) & 0xf][(dd_7 >> 8) & 0xf]]) | ((Txor[Txor[(aa_7 >> 12) & 0xf][(bb_7 >> 12) & 0xf]][Txor[(cc_7 >> 12) & 0xf][(dd_7 >> 12) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_7 >> 0) & 0xf][(bb_7 >> 0) & 0xf]][Txor[(cc_7 >> 0) & 0xf][(dd_7 >> 0) & 0xf]]) | ((Txor[Txor[(aa_7 >> 4) & 0xf][(bb_7 >> 4) & 0xf]][Txor[(cc_7 >> 4) & 0xf][(dd_7 >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_6 >> 8) & 0xf][(bb_6 >> 8) & 0xf]][Txor[(cc_6 >> 8) & 0xf][(dd_6 >> 8) & 0xf]]) | ((Txor[Txor[(aa_6 >> 12) & 0xf][(bb_6 >> 12) & 0xf]][Txor[(cc_6 >> 12) & 0xf][(dd_6 >> 12) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_4 >> 24) & 0xf][(bb_4 >> 24) & 0xf]][Txor[(cc_4 >> 24) & 0xf][(dd_4 >> 24) & 0xf]]) | ((Txor[Txor[(aa_4 >> 28) & 0xf][(bb_4 >> 28) & 0xf]][Txor[(cc_4 >> 28) & 0xf][(dd_4 >> 28) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_4 >> 16) & 0xf][(bb_4 >> 16) & 0xf]][Txor[(cc_4 >> 16) & 0xf][(dd_4 >> 16) & 0xf]]) | ((Txor[Txor[(aa_4 >> 20) & 0xf][(bb_4 >> 20) & 0xf]][Txor[(cc_4 >> 20) & 0xf][(dd_4 >> 20) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_6 >> 16) & 0xf][(bb_6 >> 16) & 0xf]][Txor[(cc_6 >> 16) & 0xf][(dd_6 >> 16) & 0xf]]) | ((Txor[Txor[(aa_6 >> 20) & 0xf][(bb_6 >> 20) & 0xf]][Txor[(cc_6 >> 20) & 0xf][(dd_6 >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_6 >> 24) & 0xf][(bb_6 >> 24) & 0xf]][Txor[(cc_6 >> 24) & 0xf][(dd_6 >> 24) & 0xf]]) | ((Txor[Txor[(aa_6 >> 28) & 0xf][(bb_6 >> 28) & 0xf]][Txor[(cc_6 >> 28) & 0xf][(dd_6 >> 28) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_5 >> 8) & 0xf][(bb_5 >> 8) & 0xf]][Txor[(cc_5 >> 8) & 0xf][(dd_5 >> 8) & 0xf]]) | ((Txor[Txor[(aa_5 >> 12) & 0xf][(bb_5 >> 12) & 0xf]][Txor[(cc_5 >> 12) & 0xf][(dd_5 >> 12) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_5 >> 0) & 0xf][(bb_5 >> 0) & 0xf]][Txor[(cc_5 >> 0) & 0xf][(dd_5 >> 0) & 0xf]]) | ((Txor[Txor[(aa_5 >> 4) & 0xf][(bb_5 >> 4) & 0xf]][Txor[(cc_5 >> 4) & 0xf][(dd_5 >> 4) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_5 >> 24) & 0xf][(bb_5 >> 24) & 0xf]][Txor[(cc_5 >> 24) & 0xf][(dd_5 >> 24) & 0xf]]) | ((Txor[Txor[(aa_5 >> 28) & 0xf][(bb_5 >> 28) & 0xf]][Txor[(cc_5 >> 28) & 0xf][(dd_5 >> 28) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_5 >> 16) & 0xf][(bb_5 >> 16) & 0xf]][Txor[(cc_5 >> 16) & 0xf][(dd_5 >> 16) & 0xf]]) | ((Txor[Txor[(aa_5 >> 20) & 0xf][(bb_5 >> 20) & 0xf]][Txor[(cc_5 >> 20) & 0xf][(dd_5 >> 20) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_4 >> 0) & 0xf][(bb_4 >> 0) & 0xf]][Txor[(cc_4 >> 0) & 0xf][(dd_4 >> 0) & 0xf]]) | ((Txor[Txor[(aa_4 >> 4) & 0xf][(bb_4 >> 4) & 0xf]][Txor[(cc_4 >> 4) & 0xf][(dd_4 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_4 >> 8) & 0xf][(bb_4 >> 8) & 0xf]][Txor[(cc_4 >> 8) & 0xf][(dd_4 >> 8) & 0xf]]) | ((Txor[Txor[(aa_4 >> 12) & 0xf][(bb_4 >> 12) & 0xf]][Txor[(cc_4 >> 12) & 0xf][(dd_4 >> 12) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int cc_10 = Tyboxes[2][10][out[10]];
    unsigned int bb_10 = Tyboxes[2][9][out[9]];
    unsigned int dd_11 = Tyboxes[2][15][out[15]];
    unsigned int dd_10 = Tyboxes[2][11][out[11]];
    unsigned int bb_11 = Tyboxes[2][13][out[13]];
    unsigned int cc_11 = Tyboxes[2][14][out[14]];
    unsigned int aa_10 = Tyboxes[2][8][out[8]];
    unsigned int aa_11 = Tyboxes[2][12][out[12]];
    unsigned int aa_8 = Tyboxes[2][0][out[0]];
    unsigned int aa_9 = Tyboxes[2][4][out[4]];
    unsigned int bb_8 = Tyboxes[2][1][out[1]];
    unsigned int cc_9 = Tyboxes[2][6][out[6]];
    unsigned int dd_8 = Tyboxes[2][3][out[3]];
    unsigned int cc_8 = Tyboxes[2][2][out[2]];
    unsigned int bb_9 = Tyboxes[2][5][out[5]];
    unsigned int dd_9 = Tyboxes[2][7][out[7]];
    out[13] = (Txor[Txor[(aa_11 >> 8) & 0xf][(bb_11 >> 8) & 0xf]][Txor[(cc_11 >> 8) & 0xf][(dd_11 >> 8) & 0xf]]) | ((Txor[Txor[(aa_11 >> 12) & 0xf][(bb_11 >> 12) & 0xf]][Txor[(cc_11 >> 12) & 0xf][(dd_11 >> 12) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_9 >> 0) & 0xf][(bb_9 >> 0) & 0xf]][Txor[(cc_9 >> 0) & 0xf][(dd_9 >> 0) & 0xf]]) | ((Txor[Txor[(aa_9 >> 4) & 0xf][(bb_9 >> 4) & 0xf]][Txor[(cc_9 >> 4) & 0xf][(dd_9 >> 4) & 0xf]]) << 4);
    out[8] = (Txor[Txor[(aa_10 >> 0) & 0xf][(bb_10 >> 0) & 0xf]][Txor[(cc_10 >> 0) & 0xf][(dd_10 >> 0) & 0xf]]) | ((Txor[Txor[(aa_10 >> 4) & 0xf][(bb_10 >> 4) & 0xf]][Txor[(cc_10 >> 4) & 0xf][(dd_10 >> 4) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_11 >> 0) & 0xf][(bb_11 >> 0) & 0xf]][Txor[(cc_11 >> 0) & 0xf][(dd_11 >> 0) & 0xf]]) | ((Txor[Txor[(aa_11 >> 4) & 0xf][(bb_11 >> 4) & 0xf]][Txor[(cc_11 >> 4) & 0xf][(dd_11 >> 4) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_9 >> 16) & 0xf][(bb_9 >> 16) & 0xf]][Txor[(cc_9 >> 16) & 0xf][(dd_9 >> 16) & 0xf]]) | ((Txor[Txor[(aa_9 >> 20) & 0xf][(bb_9 >> 20) & 0xf]][Txor[(cc_9 >> 20) & 0xf][(dd_9 >> 20) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_9 >> 8) & 0xf][(bb_9 >> 8) & 0xf]][Txor[(cc_9 >> 8) & 0xf][(dd_9 >> 8) & 0xf]]) | ((Txor[Txor[(aa_9 >> 12) & 0xf][(bb_9 >> 12) & 0xf]][Txor[(cc_9 >> 12) & 0xf][(dd_9 >> 12) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_10 >> 24) & 0xf][(bb_10 >> 24) & 0xf]][Txor[(cc_10 >> 24) & 0xf][(dd_10 >> 24) & 0xf]]) | ((Txor[Txor[(aa_10 >> 28) & 0xf][(bb_10 >> 28) & 0xf]][Txor[(cc_10 >> 28) & 0xf][(dd_10 >> 28) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_9 >> 24) & 0xf][(bb_9 >> 24) & 0xf]][Txor[(cc_9 >> 24) & 0xf][(dd_9 >> 24) & 0xf]]) | ((Txor[Txor[(aa_9 >> 28) & 0xf][(bb_9 >> 28) & 0xf]][Txor[(cc_9 >> 28) & 0xf][(dd_9 >> 28) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_8 >> 0) & 0xf][(bb_8 >> 0) & 0xf]][Txor[(cc_8 >> 0) & 0xf][(dd_8 >> 0) & 0xf]]) | ((Txor[Txor[(aa_8 >> 4) & 0xf][(bb_8 >> 4) & 0xf]][Txor[(cc_8 >> 4) & 0xf][(dd_8 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_8 >> 8) & 0xf][(bb_8 >> 8) & 0xf]][Txor[(cc_8 >> 8) & 0xf][(dd_8 >> 8) & 0xf]]) | ((Txor[Txor[(aa_8 >> 12) & 0xf][(bb_8 >> 12) & 0xf]][Txor[(cc_8 >> 12) & 0xf][(dd_8 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_8 >> 16) & 0xf][(bb_8 >> 16) & 0xf]][Txor[(cc_8 >> 16) & 0xf][(dd_8 >> 16) & 0xf]]) | ((Txor[Txor[(aa_8 >> 20) & 0xf][(bb_8 >> 20) & 0xf]][Txor[(cc_8 >> 20) & 0xf][(dd_8 >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_8 >> 24) & 0xf][(bb_8 >> 24) & 0xf]][Txor[(cc_8 >> 24) & 0xf][(dd_8 >> 24) & 0xf]]) | ((Txor[Txor[(aa_8 >> 28) & 0xf][(bb_8 >> 28) & 0xf]][Txor[(cc_8 >> 28) & 0xf][(dd_8 >> 28) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_10 >> 8) & 0xf][(bb_10 >> 8) & 0xf]][Txor[(cc_10 >> 8) & 0xf][(dd_10 >> 8) & 0xf]]) | ((Txor[Txor[(aa_10 >> 12) & 0xf][(bb_10 >> 12) & 0xf]][Txor[(cc_10 >> 12) & 0xf][(dd_10 >> 12) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_11 >> 24) & 0xf][(bb_11 >> 24) & 0xf]][Txor[(cc_11 >> 24) & 0xf][(dd_11 >> 24) & 0xf]]) | ((Txor[Txor[(aa_11 >> 28) & 0xf][(bb_11 >> 28) & 0xf]][Txor[(cc_11 >> 28) & 0xf][(dd_11 >> 28) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_11 >> 16) & 0xf][(bb_11 >> 16) & 0xf]][Txor[(cc_11 >> 16) & 0xf][(dd_11 >> 16) & 0xf]]) | ((Txor[Txor[(aa_11 >> 20) & 0xf][(bb_11 >> 20) & 0xf]][Txor[(cc_11 >> 20) & 0xf][(dd_11 >> 20) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_10 >> 16) & 0xf][(bb_10 >> 16) & 0xf]][Txor[(cc_10 >> 16) & 0xf][(dd_10 >> 16) & 0xf]]) | ((Txor[Txor[(aa_10 >> 20) & 0xf][(bb_10 >> 20) & 0xf]][Txor[(cc_10 >> 20) & 0xf][(dd_10 >> 20) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int cc_13 = Tyboxes[3][6][out[6]];
    unsigned int cc_14 = Tyboxes[3][10][out[10]];
    unsigned int dd_14 = Tyboxes[3][11][out[11]];
    unsigned int bb_12 = Tyboxes[3][1][out[1]];
    unsigned int aa_12 = Tyboxes[3][0][out[0]];
    unsigned int dd_13 = Tyboxes[3][7][out[7]];
    unsigned int cc_12 = Tyboxes[3][2][out[2]];
    unsigned int dd_15 = Tyboxes[3][15][out[15]];
    unsigned int cc_15 = Tyboxes[3][14][out[14]];
    unsigned int bb_15 = Tyboxes[3][13][out[13]];
    unsigned int aa_15 = Tyboxes[3][12][out[12]];
    unsigned int aa_14 = Tyboxes[3][8][out[8]];
    unsigned int bb_14 = Tyboxes[3][9][out[9]];
    unsigned int aa_13 = Tyboxes[3][4][out[4]];
    unsigned int bb_13 = Tyboxes[3][5][out[5]];
    unsigned int dd_12 = Tyboxes[3][3][out[3]];
    out[1] = (Txor[Txor[(aa_12 >> 8) & 0xf][(bb_12 >> 8) & 0xf]][Txor[(cc_12 >> 8) & 0xf][(dd_12 >> 8) & 0xf]]) | ((Txor[Txor[(aa_12 >> 12) & 0xf][(bb_12 >> 12) & 0xf]][Txor[(cc_12 >> 12) & 0xf][(dd_12 >> 12) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_12 >> 0) & 0xf][(bb_12 >> 0) & 0xf]][Txor[(cc_12 >> 0) & 0xf][(dd_12 >> 0) & 0xf]]) | ((Txor[Txor[(aa_12 >> 4) & 0xf][(bb_12 >> 4) & 0xf]][Txor[(cc_12 >> 4) & 0xf][(dd_12 >> 4) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_12 >> 24) & 0xf][(bb_12 >> 24) & 0xf]][Txor[(cc_12 >> 24) & 0xf][(dd_12 >> 24) & 0xf]]) | ((Txor[Txor[(aa_12 >> 28) & 0xf][(bb_12 >> 28) & 0xf]][Txor[(cc_12 >> 28) & 0xf][(dd_12 >> 28) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_12 >> 16) & 0xf][(bb_12 >> 16) & 0xf]][Txor[(cc_12 >> 16) & 0xf][(dd_12 >> 16) & 0xf]]) | ((Txor[Txor[(aa_12 >> 20) & 0xf][(bb_12 >> 20) & 0xf]][Txor[(cc_12 >> 20) & 0xf][(dd_12 >> 20) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_15 >> 8) & 0xf][(bb_15 >> 8) & 0xf]][Txor[(cc_15 >> 8) & 0xf][(dd_15 >> 8) & 0xf]]) | ((Txor[Txor[(aa_15 >> 12) & 0xf][(bb_15 >> 12) & 0xf]][Txor[(cc_15 >> 12) & 0xf][(dd_15 >> 12) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_15 >> 0) & 0xf][(bb_15 >> 0) & 0xf]][Txor[(cc_15 >> 0) & 0xf][(dd_15 >> 0) & 0xf]]) | ((Txor[Txor[(aa_15 >> 4) & 0xf][(bb_15 >> 4) & 0xf]][Txor[(cc_15 >> 4) & 0xf][(dd_15 >> 4) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_13 >> 0) & 0xf][(bb_13 >> 0) & 0xf]][Txor[(cc_13 >> 0) & 0xf][(dd_13 >> 0) & 0xf]]) | ((Txor[Txor[(aa_13 >> 4) & 0xf][(bb_13 >> 4) & 0xf]][Txor[(cc_13 >> 4) & 0xf][(dd_13 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_13 >> 8) & 0xf][(bb_13 >> 8) & 0xf]][Txor[(cc_13 >> 8) & 0xf][(dd_13 >> 8) & 0xf]]) | ((Txor[Txor[(aa_13 >> 12) & 0xf][(bb_13 >> 12) & 0xf]][Txor[(cc_13 >> 12) & 0xf][(dd_13 >> 12) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_14 >> 24) & 0xf][(bb_14 >> 24) & 0xf]][Txor[(cc_14 >> 24) & 0xf][(dd_14 >> 24) & 0xf]]) | ((Txor[Txor[(aa_14 >> 28) & 0xf][(bb_14 >> 28) & 0xf]][Txor[(cc_14 >> 28) & 0xf][(dd_14 >> 28) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_14 >> 16) & 0xf][(bb_14 >> 16) & 0xf]][Txor[(cc_14 >> 16) & 0xf][(dd_14 >> 16) & 0xf]]) | ((Txor[Txor[(aa_14 >> 20) & 0xf][(bb_14 >> 20) & 0xf]][Txor[(cc_14 >> 20) & 0xf][(dd_14 >> 20) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_13 >> 16) & 0xf][(bb_13 >> 16) & 0xf]][Txor[(cc_13 >> 16) & 0xf][(dd_13 >> 16) & 0xf]]) | ((Txor[Txor[(aa_13 >> 20) & 0xf][(bb_13 >> 20) & 0xf]][Txor[(cc_13 >> 20) & 0xf][(dd_13 >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_13 >> 24) & 0xf][(bb_13 >> 24) & 0xf]][Txor[(cc_13 >> 24) & 0xf][(dd_13 >> 24) & 0xf]]) | ((Txor[Txor[(aa_13 >> 28) & 0xf][(bb_13 >> 28) & 0xf]][Txor[(cc_13 >> 28) & 0xf][(dd_13 >> 28) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_15 >> 16) & 0xf][(bb_15 >> 16) & 0xf]][Txor[(cc_15 >> 16) & 0xf][(dd_15 >> 16) & 0xf]]) | ((Txor[Txor[(aa_15 >> 20) & 0xf][(bb_15 >> 20) & 0xf]][Txor[(cc_15 >> 20) & 0xf][(dd_15 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_15 >> 24) & 0xf][(bb_15 >> 24) & 0xf]][Txor[(cc_15 >> 24) & 0xf][(dd_15 >> 24) & 0xf]]) | ((Txor[Txor[(aa_15 >> 28) & 0xf][(bb_15 >> 28) & 0xf]][Txor[(cc_15 >> 28) & 0xf][(dd_15 >> 28) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_14 >> 8) & 0xf][(bb_14 >> 8) & 0xf]][Txor[(cc_14 >> 8) & 0xf][(dd_14 >> 8) & 0xf]]) | ((Txor[Txor[(aa_14 >> 12) & 0xf][(bb_14 >> 12) & 0xf]][Txor[(cc_14 >> 12) & 0xf][(dd_14 >> 12) & 0xf]]) << 4);
    out[8] = (Txor[Txor[(aa_14 >> 0) & 0xf][(bb_14 >> 0) & 0xf]][Txor[(cc_14 >> 0) & 0xf][(dd_14 >> 0) & 0xf]]) | ((Txor[Txor[(aa_14 >> 4) & 0xf][(bb_14 >> 4) & 0xf]][Txor[(cc_14 >> 4) & 0xf][(dd_14 >> 4) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int dd_19 = Tyboxes[4][15][out[15]];
    unsigned int bb_16 = Tyboxes[4][1][out[1]];
    unsigned int cc_16 = Tyboxes[4][2][out[2]];
    unsigned int dd_16 = Tyboxes[4][3][out[3]];
    unsigned int aa_16 = Tyboxes[4][0][out[0]];
    unsigned int aa_18 = Tyboxes[4][8][out[8]];
    unsigned int bb_19 = Tyboxes[4][13][out[13]];
    unsigned int cc_19 = Tyboxes[4][14][out[14]];
    unsigned int aa_17 = Tyboxes[4][4][out[4]];
    unsigned int aa_19 = Tyboxes[4][12][out[12]];
    unsigned int cc_17 = Tyboxes[4][6][out[6]];
    unsigned int bb_17 = Tyboxes[4][5][out[5]];
    unsigned int dd_18 = Tyboxes[4][11][out[11]];
    unsigned int dd_17 = Tyboxes[4][7][out[7]];
    unsigned int bb_18 = Tyboxes[4][9][out[9]];
    unsigned int cc_18 = Tyboxes[4][10][out[10]];
    out[14] = (Txor[Txor[(aa_19 >> 16) & 0xf][(bb_19 >> 16) & 0xf]][Txor[(cc_19 >> 16) & 0xf][(dd_19 >> 16) & 0xf]]) | ((Txor[Txor[(aa_19 >> 20) & 0xf][(bb_19 >> 20) & 0xf]][Txor[(cc_19 >> 20) & 0xf][(dd_19 >> 20) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_19 >> 8) & 0xf][(bb_19 >> 8) & 0xf]][Txor[(cc_19 >> 8) & 0xf][(dd_19 >> 8) & 0xf]]) | ((Txor[Txor[(aa_19 >> 12) & 0xf][(bb_19 >> 12) & 0xf]][Txor[(cc_19 >> 12) & 0xf][(dd_19 >> 12) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_19 >> 0) & 0xf][(bb_19 >> 0) & 0xf]][Txor[(cc_19 >> 0) & 0xf][(dd_19 >> 0) & 0xf]]) | ((Txor[Txor[(aa_19 >> 4) & 0xf][(bb_19 >> 4) & 0xf]][Txor[(cc_19 >> 4) & 0xf][(dd_19 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_16 >> 8) & 0xf][(bb_16 >> 8) & 0xf]][Txor[(cc_16 >> 8) & 0xf][(dd_16 >> 8) & 0xf]]) | ((Txor[Txor[(aa_16 >> 12) & 0xf][(bb_16 >> 12) & 0xf]][Txor[(cc_16 >> 12) & 0xf][(dd_16 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_16 >> 16) & 0xf][(bb_16 >> 16) & 0xf]][Txor[(cc_16 >> 16) & 0xf][(dd_16 >> 16) & 0xf]]) | ((Txor[Txor[(aa_16 >> 20) & 0xf][(bb_16 >> 20) & 0xf]][Txor[(cc_16 >> 20) & 0xf][(dd_16 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_19 >> 24) & 0xf][(bb_19 >> 24) & 0xf]][Txor[(cc_19 >> 24) & 0xf][(dd_19 >> 24) & 0xf]]) | ((Txor[Txor[(aa_19 >> 28) & 0xf][(bb_19 >> 28) & 0xf]][Txor[(cc_19 >> 28) & 0xf][(dd_19 >> 28) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_16 >> 0) & 0xf][(bb_16 >> 0) & 0xf]][Txor[(cc_16 >> 0) & 0xf][(dd_16 >> 0) & 0xf]]) | ((Txor[Txor[(aa_16 >> 4) & 0xf][(bb_16 >> 4) & 0xf]][Txor[(cc_16 >> 4) & 0xf][(dd_16 >> 4) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_17 >> 24) & 0xf][(bb_17 >> 24) & 0xf]][Txor[(cc_17 >> 24) & 0xf][(dd_17 >> 24) & 0xf]]) | ((Txor[Txor[(aa_17 >> 28) & 0xf][(bb_17 >> 28) & 0xf]][Txor[(cc_17 >> 28) & 0xf][(dd_17 >> 28) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_18 >> 24) & 0xf][(bb_18 >> 24) & 0xf]][Txor[(cc_18 >> 24) & 0xf][(dd_18 >> 24) & 0xf]]) | ((Txor[Txor[(aa_18 >> 28) & 0xf][(bb_18 >> 28) & 0xf]][Txor[(cc_18 >> 28) & 0xf][(dd_18 >> 28) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_16 >> 24) & 0xf][(bb_16 >> 24) & 0xf]][Txor[(cc_16 >> 24) & 0xf][(dd_16 >> 24) & 0xf]]) | ((Txor[Txor[(aa_16 >> 28) & 0xf][(bb_16 >> 28) & 0xf]][Txor[(cc_16 >> 28) & 0xf][(dd_16 >> 28) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_18 >> 8) & 0xf][(bb_18 >> 8) & 0xf]][Txor[(cc_18 >> 8) & 0xf][(dd_18 >> 8) & 0xf]]) | ((Txor[Txor[(aa_18 >> 12) & 0xf][(bb_18 >> 12) & 0xf]][Txor[(cc_18 >> 12) & 0xf][(dd_18 >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_18 >> 16) & 0xf][(bb_18 >> 16) & 0xf]][Txor[(cc_18 >> 16) & 0xf][(dd_18 >> 16) & 0xf]]) | ((Txor[Txor[(aa_18 >> 20) & 0xf][(bb_18 >> 20) & 0xf]][Txor[(cc_18 >> 20) & 0xf][(dd_18 >> 20) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_17 >> 0) & 0xf][(bb_17 >> 0) & 0xf]][Txor[(cc_17 >> 0) & 0xf][(dd_17 >> 0) & 0xf]]) | ((Txor[Txor[(aa_17 >> 4) & 0xf][(bb_17 >> 4) & 0xf]][Txor[(cc_17 >> 4) & 0xf][(dd_17 >> 4) & 0xf]]) << 4);
    out[8] = (Txor[Txor[(aa_18 >> 0) & 0xf][(bb_18 >> 0) & 0xf]][Txor[(cc_18 >> 0) & 0xf][(dd_18 >> 0) & 0xf]]) | ((Txor[Txor[(aa_18 >> 4) & 0xf][(bb_18 >> 4) & 0xf]][Txor[(cc_18 >> 4) & 0xf][(dd_18 >> 4) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_17 >> 16) & 0xf][(bb_17 >> 16) & 0xf]][Txor[(cc_17 >> 16) & 0xf][(dd_17 >> 16) & 0xf]]) | ((Txor[Txor[(aa_17 >> 20) & 0xf][(bb_17 >> 20) & 0xf]][Txor[(cc_17 >> 20) & 0xf][(dd_17 >> 20) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_17 >> 8) & 0xf][(bb_17 >> 8) & 0xf]][Txor[(cc_17 >> 8) & 0xf][(dd_17 >> 8) & 0xf]]) | ((Txor[Txor[(aa_17 >> 12) & 0xf][(bb_17 >> 12) & 0xf]][Txor[(cc_17 >> 12) & 0xf][(dd_17 >> 12) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int aa_20 = Tyboxes[5][0][out[0]];
    unsigned int aa_21 = Tyboxes[5][4][out[4]];
    unsigned int bb_21 = Tyboxes[5][5][out[5]];
    unsigned int cc_21 = Tyboxes[5][6][out[6]];
    unsigned int dd_21 = Tyboxes[5][7][out[7]];
    unsigned int dd_22 = Tyboxes[5][11][out[11]];
    unsigned int cc_22 = Tyboxes[5][10][out[10]];
    unsigned int dd_20 = Tyboxes[5][3][out[3]];
    unsigned int cc_20 = Tyboxes[5][2][out[2]];
    unsigned int bb_22 = Tyboxes[5][9][out[9]];
    unsigned int aa_22 = Tyboxes[5][8][out[8]];
    unsigned int cc_23 = Tyboxes[5][14][out[14]];
    unsigned int dd_23 = Tyboxes[5][15][out[15]];
    unsigned int aa_23 = Tyboxes[5][12][out[12]];
    unsigned int bb_23 = Tyboxes[5][13][out[13]];
    unsigned int bb_20 = Tyboxes[5][1][out[1]];
    out[0] = (Txor[Txor[(aa_20 >> 0) & 0xf][(bb_20 >> 0) & 0xf]][Txor[(cc_20 >> 0) & 0xf][(dd_20 >> 0) & 0xf]]) | ((Txor[Txor[(aa_20 >> 4) & 0xf][(bb_20 >> 4) & 0xf]][Txor[(cc_20 >> 4) & 0xf][(dd_20 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_20 >> 8) & 0xf][(bb_20 >> 8) & 0xf]][Txor[(cc_20 >> 8) & 0xf][(dd_20 >> 8) & 0xf]]) | ((Txor[Txor[(aa_20 >> 12) & 0xf][(bb_20 >> 12) & 0xf]][Txor[(cc_20 >> 12) & 0xf][(dd_20 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_20 >> 16) & 0xf][(bb_20 >> 16) & 0xf]][Txor[(cc_20 >> 16) & 0xf][(dd_20 >> 16) & 0xf]]) | ((Txor[Txor[(aa_20 >> 20) & 0xf][(bb_20 >> 20) & 0xf]][Txor[(cc_20 >> 20) & 0xf][(dd_20 >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_20 >> 24) & 0xf][(bb_20 >> 24) & 0xf]][Txor[(cc_20 >> 24) & 0xf][(dd_20 >> 24) & 0xf]]) | ((Txor[Txor[(aa_20 >> 28) & 0xf][(bb_20 >> 28) & 0xf]][Txor[(cc_20 >> 28) & 0xf][(dd_20 >> 28) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_22 >> 24) & 0xf][(bb_22 >> 24) & 0xf]][Txor[(cc_22 >> 24) & 0xf][(dd_22 >> 24) & 0xf]]) | ((Txor[Txor[(aa_22 >> 28) & 0xf][(bb_22 >> 28) & 0xf]][Txor[(cc_22 >> 28) & 0xf][(dd_22 >> 28) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_22 >> 16) & 0xf][(bb_22 >> 16) & 0xf]][Txor[(cc_22 >> 16) & 0xf][(dd_22 >> 16) & 0xf]]) | ((Txor[Txor[(aa_22 >> 20) & 0xf][(bb_22 >> 20) & 0xf]][Txor[(cc_22 >> 20) & 0xf][(dd_22 >> 20) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_21 >> 0) & 0xf][(bb_21 >> 0) & 0xf]][Txor[(cc_21 >> 0) & 0xf][(dd_21 >> 0) & 0xf]]) | ((Txor[Txor[(aa_21 >> 4) & 0xf][(bb_21 >> 4) & 0xf]][Txor[(cc_21 >> 4) & 0xf][(dd_21 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_21 >> 8) & 0xf][(bb_21 >> 8) & 0xf]][Txor[(cc_21 >> 8) & 0xf][(dd_21 >> 8) & 0xf]]) | ((Txor[Txor[(aa_21 >> 12) & 0xf][(bb_21 >> 12) & 0xf]][Txor[(cc_21 >> 12) & 0xf][(dd_21 >> 12) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_22 >> 8) & 0xf][(bb_22 >> 8) & 0xf]][Txor[(cc_22 >> 8) & 0xf][(dd_22 >> 8) & 0xf]]) | ((Txor[Txor[(aa_22 >> 12) & 0xf][(bb_22 >> 12) & 0xf]][Txor[(cc_22 >> 12) & 0xf][(dd_22 >> 12) & 0xf]]) << 4);
    out[8] = (Txor[Txor[(aa_22 >> 0) & 0xf][(bb_22 >> 0) & 0xf]][Txor[(cc_22 >> 0) & 0xf][(dd_22 >> 0) & 0xf]]) | ((Txor[Txor[(aa_22 >> 4) & 0xf][(bb_22 >> 4) & 0xf]][Txor[(cc_22 >> 4) & 0xf][(dd_22 >> 4) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_21 >> 24) & 0xf][(bb_21 >> 24) & 0xf]][Txor[(cc_21 >> 24) & 0xf][(dd_21 >> 24) & 0xf]]) | ((Txor[Txor[(aa_21 >> 28) & 0xf][(bb_21 >> 28) & 0xf]][Txor[(cc_21 >> 28) & 0xf][(dd_21 >> 28) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_21 >> 16) & 0xf][(bb_21 >> 16) & 0xf]][Txor[(cc_21 >> 16) & 0xf][(dd_21 >> 16) & 0xf]]) | ((Txor[Txor[(aa_21 >> 20) & 0xf][(bb_21 >> 20) & 0xf]][Txor[(cc_21 >> 20) & 0xf][(dd_21 >> 20) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_23 >> 16) & 0xf][(bb_23 >> 16) & 0xf]][Txor[(cc_23 >> 16) & 0xf][(dd_23 >> 16) & 0xf]]) | ((Txor[Txor[(aa_23 >> 20) & 0xf][(bb_23 >> 20) & 0xf]][Txor[(cc_23 >> 20) & 0xf][(dd_23 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_23 >> 24) & 0xf][(bb_23 >> 24) & 0xf]][Txor[(cc_23 >> 24) & 0xf][(dd_23 >> 24) & 0xf]]) | ((Txor[Txor[(aa_23 >> 28) & 0xf][(bb_23 >> 28) & 0xf]][Txor[(cc_23 >> 28) & 0xf][(dd_23 >> 28) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_23 >> 0) & 0xf][(bb_23 >> 0) & 0xf]][Txor[(cc_23 >> 0) & 0xf][(dd_23 >> 0) & 0xf]]) | ((Txor[Txor[(aa_23 >> 4) & 0xf][(bb_23 >> 4) & 0xf]][Txor[(cc_23 >> 4) & 0xf][(dd_23 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_23 >> 8) & 0xf][(bb_23 >> 8) & 0xf]][Txor[(cc_23 >> 8) & 0xf][(dd_23 >> 8) & 0xf]]) | ((Txor[Txor[(aa_23 >> 12) & 0xf][(bb_23 >> 12) & 0xf]][Txor[(cc_23 >> 12) & 0xf][(dd_23 >> 12) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int aa_27 = Tyboxes[6][12][out[12]];
    unsigned int bb_27 = Tyboxes[6][13][out[13]];
    unsigned int cc_27 = Tyboxes[6][14][out[14]];
    unsigned int dd_27 = Tyboxes[6][15][out[15]];
    unsigned int bb_26 = Tyboxes[6][9][out[9]];
    unsigned int aa_26 = Tyboxes[6][8][out[8]];
    unsigned int dd_26 = Tyboxes[6][11][out[11]];
    unsigned int bb_25 = Tyboxes[6][5][out[5]];
    unsigned int cc_25 = Tyboxes[6][6][out[6]];
    unsigned int cc_26 = Tyboxes[6][10][out[10]];
    unsigned int aa_25 = Tyboxes[6][4][out[4]];
    unsigned int dd_25 = Tyboxes[6][7][out[7]];
    unsigned int aa_24 = Tyboxes[6][0][out[0]];
    unsigned int dd_24 = Tyboxes[6][3][out[3]];
    unsigned int bb_24 = Tyboxes[6][1][out[1]];
    unsigned int cc_24 = Tyboxes[6][2][out[2]];
    out[6] = (Txor[Txor[(aa_25 >> 16) & 0xf][(bb_25 >> 16) & 0xf]][Txor[(cc_25 >> 16) & 0xf][(dd_25 >> 16) & 0xf]]) | ((Txor[Txor[(aa_25 >> 20) & 0xf][(bb_25 >> 20) & 0xf]][Txor[(cc_25 >> 20) & 0xf][(dd_25 >> 20) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_26 >> 16) & 0xf][(bb_26 >> 16) & 0xf]][Txor[(cc_26 >> 16) & 0xf][(dd_26 >> 16) & 0xf]]) | ((Txor[Txor[(aa_26 >> 20) & 0xf][(bb_26 >> 20) & 0xf]][Txor[(cc_26 >> 20) & 0xf][(dd_26 >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_26 >> 24) & 0xf][(bb_26 >> 24) & 0xf]][Txor[(cc_26 >> 24) & 0xf][(dd_26 >> 24) & 0xf]]) | ((Txor[Txor[(aa_26 >> 28) & 0xf][(bb_26 >> 28) & 0xf]][Txor[(cc_26 >> 28) & 0xf][(dd_26 >> 28) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_27 >> 24) & 0xf][(bb_27 >> 24) & 0xf]][Txor[(cc_27 >> 24) & 0xf][(dd_27 >> 24) & 0xf]]) | ((Txor[Txor[(aa_27 >> 28) & 0xf][(bb_27 >> 28) & 0xf]][Txor[(cc_27 >> 28) & 0xf][(dd_27 >> 28) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_26 >> 8) & 0xf][(bb_26 >> 8) & 0xf]][Txor[(cc_26 >> 8) & 0xf][(dd_26 >> 8) & 0xf]]) | ((Txor[Txor[(aa_26 >> 12) & 0xf][(bb_26 >> 12) & 0xf]][Txor[(cc_26 >> 12) & 0xf][(dd_26 >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_24 >> 16) & 0xf][(bb_24 >> 16) & 0xf]][Txor[(cc_24 >> 16) & 0xf][(dd_24 >> 16) & 0xf]]) | ((Txor[Txor[(aa_24 >> 20) & 0xf][(bb_24 >> 20) & 0xf]][Txor[(cc_24 >> 20) & 0xf][(dd_24 >> 20) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_27 >> 0) & 0xf][(bb_27 >> 0) & 0xf]][Txor[(cc_27 >> 0) & 0xf][(dd_27 >> 0) & 0xf]]) | ((Txor[Txor[(aa_27 >> 4) & 0xf][(bb_27 >> 4) & 0xf]][Txor[(cc_27 >> 4) & 0xf][(dd_27 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_27 >> 8) & 0xf][(bb_27 >> 8) & 0xf]][Txor[(cc_27 >> 8) & 0xf][(dd_27 >> 8) & 0xf]]) | ((Txor[Txor[(aa_27 >> 12) & 0xf][(bb_27 >> 12) & 0xf]][Txor[(cc_27 >> 12) & 0xf][(dd_27 >> 12) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_27 >> 16) & 0xf][(bb_27 >> 16) & 0xf]][Txor[(cc_27 >> 16) & 0xf][(dd_27 >> 16) & 0xf]]) | ((Txor[Txor[(aa_27 >> 20) & 0xf][(bb_27 >> 20) & 0xf]][Txor[(cc_27 >> 20) & 0xf][(dd_27 >> 20) & 0xf]]) << 4);
    out[8] = (Txor[Txor[(aa_26 >> 0) & 0xf][(bb_26 >> 0) & 0xf]][Txor[(cc_26 >> 0) & 0xf][(dd_26 >> 0) & 0xf]]) | ((Txor[Txor[(aa_26 >> 4) & 0xf][(bb_26 >> 4) & 0xf]][Txor[(cc_26 >> 4) & 0xf][(dd_26 >> 4) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_25 >> 24) & 0xf][(bb_25 >> 24) & 0xf]][Txor[(cc_25 >> 24) & 0xf][(dd_25 >> 24) & 0xf]]) | ((Txor[Txor[(aa_25 >> 28) & 0xf][(bb_25 >> 28) & 0xf]][Txor[(cc_25 >> 28) & 0xf][(dd_25 >> 28) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_24 >> 24) & 0xf][(bb_24 >> 24) & 0xf]][Txor[(cc_24 >> 24) & 0xf][(dd_24 >> 24) & 0xf]]) | ((Txor[Txor[(aa_24 >> 28) & 0xf][(bb_24 >> 28) & 0xf]][Txor[(cc_24 >> 28) & 0xf][(dd_24 >> 28) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_25 >> 0) & 0xf][(bb_25 >> 0) & 0xf]][Txor[(cc_25 >> 0) & 0xf][(dd_25 >> 0) & 0xf]]) | ((Txor[Txor[(aa_25 >> 4) & 0xf][(bb_25 >> 4) & 0xf]][Txor[(cc_25 >> 4) & 0xf][(dd_25 >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_24 >> 8) & 0xf][(bb_24 >> 8) & 0xf]][Txor[(cc_24 >> 8) & 0xf][(dd_24 >> 8) & 0xf]]) | ((Txor[Txor[(aa_24 >> 12) & 0xf][(bb_24 >> 12) & 0xf]][Txor[(cc_24 >> 12) & 0xf][(dd_24 >> 12) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_25 >> 8) & 0xf][(bb_25 >> 8) & 0xf]][Txor[(cc_25 >> 8) & 0xf][(dd_25 >> 8) & 0xf]]) | ((Txor[Txor[(aa_25 >> 12) & 0xf][(bb_25 >> 12) & 0xf]][Txor[(cc_25 >> 12) & 0xf][(dd_25 >> 12) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_24 >> 0) & 0xf][(bb_24 >> 0) & 0xf]][Txor[(cc_24 >> 0) & 0xf][(dd_24 >> 0) & 0xf]]) | ((Txor[Txor[(aa_24 >> 4) & 0xf][(bb_24 >> 4) & 0xf]][Txor[(cc_24 >> 4) & 0xf][(dd_24 >> 4) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int bb_28 = Tyboxes[7][1][out[1]];
    unsigned int aa_28 = Tyboxes[7][0][out[0]];
    unsigned int bb_31 = Tyboxes[7][13][out[13]];
    unsigned int aa_31 = Tyboxes[7][12][out[12]];
    unsigned int dd_30 = Tyboxes[7][11][out[11]];
    unsigned int cc_30 = Tyboxes[7][10][out[10]];
    unsigned int dd_28 = Tyboxes[7][3][out[3]];
    unsigned int cc_28 = Tyboxes[7][2][out[2]];
    unsigned int cc_29 = Tyboxes[7][6][out[6]];
    unsigned int dd_29 = Tyboxes[7][7][out[7]];
    unsigned int aa_29 = Tyboxes[7][4][out[4]];
    unsigned int bb_29 = Tyboxes[7][5][out[5]];
    unsigned int dd_31 = Tyboxes[7][15][out[15]];
    unsigned int cc_31 = Tyboxes[7][14][out[14]];
    unsigned int aa_30 = Tyboxes[7][8][out[8]];
    unsigned int bb_30 = Tyboxes[7][9][out[9]];
    out[11] = (Txor[Txor[(aa_30 >> 24) & 0xf][(bb_30 >> 24) & 0xf]][Txor[(cc_30 >> 24) & 0xf][(dd_30 >> 24) & 0xf]]) | ((Txor[Txor[(aa_30 >> 28) & 0xf][(bb_30 >> 28) & 0xf]][Txor[(cc_30 >> 28) & 0xf][(dd_30 >> 28) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_30 >> 16) & 0xf][(bb_30 >> 16) & 0xf]][Txor[(cc_30 >> 16) & 0xf][(dd_30 >> 16) & 0xf]]) | ((Txor[Txor[(aa_30 >> 20) & 0xf][(bb_30 >> 20) & 0xf]][Txor[(cc_30 >> 20) & 0xf][(dd_30 >> 20) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_28 >> 8) & 0xf][(bb_28 >> 8) & 0xf]][Txor[(cc_28 >> 8) & 0xf][(dd_28 >> 8) & 0xf]]) | ((Txor[Txor[(aa_28 >> 12) & 0xf][(bb_28 >> 12) & 0xf]][Txor[(cc_28 >> 12) & 0xf][(dd_28 >> 12) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_28 >> 0) & 0xf][(bb_28 >> 0) & 0xf]][Txor[(cc_28 >> 0) & 0xf][(dd_28 >> 0) & 0xf]]) | ((Txor[Txor[(aa_28 >> 4) & 0xf][(bb_28 >> 4) & 0xf]][Txor[(cc_28 >> 4) & 0xf][(dd_28 >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa_30 >> 8) & 0xf][(bb_30 >> 8) & 0xf]][Txor[(cc_30 >> 8) & 0xf][(dd_30 >> 8) & 0xf]]) | ((Txor[Txor[(aa_30 >> 12) & 0xf][(bb_30 >> 12) & 0xf]][Txor[(cc_30 >> 12) & 0xf][(dd_30 >> 12) & 0xf]]) << 4);
    out[8] = (Txor[Txor[(aa_30 >> 0) & 0xf][(bb_30 >> 0) & 0xf]][Txor[(cc_30 >> 0) & 0xf][(dd_30 >> 0) & 0xf]]) | ((Txor[Txor[(aa_30 >> 4) & 0xf][(bb_30 >> 4) & 0xf]][Txor[(cc_30 >> 4) & 0xf][(dd_30 >> 4) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_28 >> 24) & 0xf][(bb_28 >> 24) & 0xf]][Txor[(cc_28 >> 24) & 0xf][(dd_28 >> 24) & 0xf]]) | ((Txor[Txor[(aa_28 >> 28) & 0xf][(bb_28 >> 28) & 0xf]][Txor[(cc_28 >> 28) & 0xf][(dd_28 >> 28) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_28 >> 16) & 0xf][(bb_28 >> 16) & 0xf]][Txor[(cc_28 >> 16) & 0xf][(dd_28 >> 16) & 0xf]]) | ((Txor[Txor[(aa_28 >> 20) & 0xf][(bb_28 >> 20) & 0xf]][Txor[(cc_28 >> 20) & 0xf][(dd_28 >> 20) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_29 >> 16) & 0xf][(bb_29 >> 16) & 0xf]][Txor[(cc_29 >> 16) & 0xf][(dd_29 >> 16) & 0xf]]) | ((Txor[Txor[(aa_29 >> 20) & 0xf][(bb_29 >> 20) & 0xf]][Txor[(cc_29 >> 20) & 0xf][(dd_29 >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_29 >> 24) & 0xf][(bb_29 >> 24) & 0xf]][Txor[(cc_29 >> 24) & 0xf][(dd_29 >> 24) & 0xf]]) | ((Txor[Txor[(aa_29 >> 28) & 0xf][(bb_29 >> 28) & 0xf]][Txor[(cc_29 >> 28) & 0xf][(dd_29 >> 28) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_29 >> 0) & 0xf][(bb_29 >> 0) & 0xf]][Txor[(cc_29 >> 0) & 0xf][(dd_29 >> 0) & 0xf]]) | ((Txor[Txor[(aa_29 >> 4) & 0xf][(bb_29 >> 4) & 0xf]][Txor[(cc_29 >> 4) & 0xf][(dd_29 >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_29 >> 8) & 0xf][(bb_29 >> 8) & 0xf]][Txor[(cc_29 >> 8) & 0xf][(dd_29 >> 8) & 0xf]]) | ((Txor[Txor[(aa_29 >> 12) & 0xf][(bb_29 >> 12) & 0xf]][Txor[(cc_29 >> 12) & 0xf][(dd_29 >> 12) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_31 >> 8) & 0xf][(bb_31 >> 8) & 0xf]][Txor[(cc_31 >> 8) & 0xf][(dd_31 >> 8) & 0xf]]) | ((Txor[Txor[(aa_31 >> 12) & 0xf][(bb_31 >> 12) & 0xf]][Txor[(cc_31 >> 12) & 0xf][(dd_31 >> 12) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_31 >> 0) & 0xf][(bb_31 >> 0) & 0xf]][Txor[(cc_31 >> 0) & 0xf][(dd_31 >> 0) & 0xf]]) | ((Txor[Txor[(aa_31 >> 4) & 0xf][(bb_31 >> 4) & 0xf]][Txor[(cc_31 >> 4) & 0xf][(dd_31 >> 4) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_31 >> 16) & 0xf][(bb_31 >> 16) & 0xf]][Txor[(cc_31 >> 16) & 0xf][(dd_31 >> 16) & 0xf]]) | ((Txor[Txor[(aa_31 >> 20) & 0xf][(bb_31 >> 20) & 0xf]][Txor[(cc_31 >> 20) & 0xf][(dd_31 >> 20) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_31 >> 24) & 0xf][(bb_31 >> 24) & 0xf]][Txor[(cc_31 >> 24) & 0xf][(dd_31 >> 24) & 0xf]]) | ((Txor[Txor[(aa_31 >> 28) & 0xf][(bb_31 >> 28) & 0xf]][Txor[(cc_31 >> 28) & 0xf][(dd_31 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    unsigned int cc_35 = Tyboxes[8][14][out[14]];
    unsigned int bb_35 = Tyboxes[8][13][out[13]];
    unsigned int dd_34 = Tyboxes[8][11][out[11]];
    unsigned int dd_35 = Tyboxes[8][15][out[15]];
    unsigned int bb_34 = Tyboxes[8][9][out[9]];
    unsigned int cc_34 = Tyboxes[8][10][out[10]];
    unsigned int cc_32 = Tyboxes[8][2][out[2]];
    unsigned int aa_34 = Tyboxes[8][8][out[8]];
    unsigned int dd_33 = Tyboxes[8][7][out[7]];
    unsigned int cc_33 = Tyboxes[8][6][out[6]];
    unsigned int bb_33 = Tyboxes[8][5][out[5]];
    unsigned int aa_33 = Tyboxes[8][4][out[4]];
    unsigned int aa_35 = Tyboxes[8][12][out[12]];
    unsigned int bb_32 = Tyboxes[8][1][out[1]];
    unsigned int aa_32 = Tyboxes[8][0][out[0]];
    unsigned int dd_32 = Tyboxes[8][3][out[3]];
    out[9] = (Txor[Txor[(aa_34 >> 8) & 0xf][(bb_34 >> 8) & 0xf]][Txor[(cc_34 >> 8) & 0xf][(dd_34 >> 8) & 0xf]]) | ((Txor[Txor[(aa_34 >> 12) & 0xf][(bb_34 >> 12) & 0xf]][Txor[(cc_34 >> 12) & 0xf][(dd_34 >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa_34 >> 16) & 0xf][(bb_34 >> 16) & 0xf]][Txor[(cc_34 >> 16) & 0xf][(dd_34 >> 16) & 0xf]]) | ((Txor[Txor[(aa_34 >> 20) & 0xf][(bb_34 >> 20) & 0xf]][Txor[(cc_34 >> 20) & 0xf][(dd_34 >> 20) & 0xf]]) << 4);
    out[12] = (Txor[Txor[(aa_35 >> 0) & 0xf][(bb_35 >> 0) & 0xf]][Txor[(cc_35 >> 0) & 0xf][(dd_35 >> 0) & 0xf]]) | ((Txor[Txor[(aa_35 >> 4) & 0xf][(bb_35 >> 4) & 0xf]][Txor[(cc_35 >> 4) & 0xf][(dd_35 >> 4) & 0xf]]) << 4);
    out[8] = (Txor[Txor[(aa_34 >> 0) & 0xf][(bb_34 >> 0) & 0xf]][Txor[(cc_34 >> 0) & 0xf][(dd_34 >> 0) & 0xf]]) | ((Txor[Txor[(aa_34 >> 4) & 0xf][(bb_34 >> 4) & 0xf]][Txor[(cc_34 >> 4) & 0xf][(dd_34 >> 4) & 0xf]]) << 4);
    out[14] = (Txor[Txor[(aa_35 >> 16) & 0xf][(bb_35 >> 16) & 0xf]][Txor[(cc_35 >> 16) & 0xf][(dd_35 >> 16) & 0xf]]) | ((Txor[Txor[(aa_35 >> 20) & 0xf][(bb_35 >> 20) & 0xf]][Txor[(cc_35 >> 20) & 0xf][(dd_35 >> 20) & 0xf]]) << 4);
    out[0] = (Txor[Txor[(aa_32 >> 0) & 0xf][(bb_32 >> 0) & 0xf]][Txor[(cc_32 >> 0) & 0xf][(dd_32 >> 0) & 0xf]]) | ((Txor[Txor[(aa_32 >> 4) & 0xf][(bb_32 >> 4) & 0xf]][Txor[(cc_32 >> 4) & 0xf][(dd_32 >> 4) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa_33 >> 16) & 0xf][(bb_33 >> 16) & 0xf]][Txor[(cc_33 >> 16) & 0xf][(dd_33 >> 16) & 0xf]]) | ((Txor[Txor[(aa_33 >> 20) & 0xf][(bb_33 >> 20) & 0xf]][Txor[(cc_33 >> 20) & 0xf][(dd_33 >> 20) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa_33 >> 8) & 0xf][(bb_33 >> 8) & 0xf]][Txor[(cc_33 >> 8) & 0xf][(dd_33 >> 8) & 0xf]]) | ((Txor[Txor[(aa_33 >> 12) & 0xf][(bb_33 >> 12) & 0xf]][Txor[(cc_33 >> 12) & 0xf][(dd_33 >> 12) & 0xf]]) << 4);
    out[4] = (Txor[Txor[(aa_33 >> 0) & 0xf][(bb_33 >> 0) & 0xf]][Txor[(cc_33 >> 0) & 0xf][(dd_33 >> 0) & 0xf]]) | ((Txor[Txor[(aa_33 >> 4) & 0xf][(bb_33 >> 4) & 0xf]][Txor[(cc_33 >> 4) & 0xf][(dd_33 >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa_35 >> 8) & 0xf][(bb_35 >> 8) & 0xf]][Txor[(cc_35 >> 8) & 0xf][(dd_35 >> 8) & 0xf]]) | ((Txor[Txor[(aa_35 >> 12) & 0xf][(bb_35 >> 12) & 0xf]][Txor[(cc_35 >> 12) & 0xf][(dd_35 >> 12) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa_32 >> 24) & 0xf][(bb_32 >> 24) & 0xf]][Txor[(cc_32 >> 24) & 0xf][(dd_32 >> 24) & 0xf]]) | ((Txor[Txor[(aa_32 >> 28) & 0xf][(bb_32 >> 28) & 0xf]][Txor[(cc_32 >> 28) & 0xf][(dd_32 >> 28) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa_32 >> 16) & 0xf][(bb_32 >> 16) & 0xf]][Txor[(cc_32 >> 16) & 0xf][(dd_32 >> 16) & 0xf]]) | ((Txor[Txor[(aa_32 >> 20) & 0xf][(bb_32 >> 20) & 0xf]][Txor[(cc_32 >> 20) & 0xf][(dd_32 >> 20) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa_32 >> 8) & 0xf][(bb_32 >> 8) & 0xf]][Txor[(cc_32 >> 8) & 0xf][(dd_32 >> 8) & 0xf]]) | ((Txor[Txor[(aa_32 >> 12) & 0xf][(bb_32 >> 12) & 0xf]][Txor[(cc_32 >> 12) & 0xf][(dd_32 >> 12) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa_34 >> 24) & 0xf][(bb_34 >> 24) & 0xf]][Txor[(cc_34 >> 24) & 0xf][(dd_34 >> 24) & 0xf]]) | ((Txor[Txor[(aa_34 >> 28) & 0xf][(bb_34 >> 28) & 0xf]][Txor[(cc_34 >> 28) & 0xf][(dd_34 >> 28) & 0xf]]) << 4);
    out[15] = (Txor[Txor[(aa_35 >> 24) & 0xf][(bb_35 >> 24) & 0xf]][Txor[(cc_35 >> 24) & 0xf][(dd_35 >> 24) & 0xf]]) | ((Txor[Txor[(aa_35 >> 28) & 0xf][(bb_35 >> 28) & 0xf]][Txor[(cc_35 >> 28) & 0xf][(dd_35 >> 28) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa_33 >> 24) & 0xf][(bb_33 >> 24) & 0xf]][Txor[(cc_33 >> 24) & 0xf][(dd_33 >> 24) & 0xf]]) | ((Txor[Txor[(aa_33 >> 28) & 0xf][(bb_33 >> 28) & 0xf]][Txor[(cc_33 >> 28) & 0xf][(dd_33 >> 28) & 0xf]]) << 4);
    ShiftRows(out);
    out[13] = Tboxes_[13][out[13]];
    out[14] = Tboxes_[14][out[14]];
    out[1] = Tboxes_[1][out[1]];
    out[0] = Tboxes_[0][out[0]];
    out[15] = Tboxes_[15][out[15]];
    out[9] = Tboxes_[9][out[9]];
    out[8] = Tboxes_[8][out[8]];
    out[7] = Tboxes_[7][out[7]];
    out[6] = Tboxes_[6][out[6]];
    out[5] = Tboxes_[5][out[5]];
    out[4] = Tboxes_[4][out[4]];
    out[3] = Tboxes_[3][out[3]];
    out[2] = Tboxes_[2][out[2]];
    out[12] = Tboxes_[12][out[12]];
    out[11] = Tboxes_[11][out[11]];
    out[10] = Tboxes_[10][out[10]];
}

unsigned char tests()
{
    /// AddRoundKey
    {
        unsigned char round_key[16] = { 0xa0, 0xfa, 0xfe, 0x17, 0x88, 0x54, 0x2c, 0xb1, 0x23, 0xa3, 0x39, 0x39, 0x2a, 0x6c, 0x76, 0x05 };
        unsigned char state[16] = { 0x04, 0x66, 0x81, 0xe5, 0xe0, 0xcb, 0x19, 0x9a, 0x48, 0xf8, 0xd3, 0x7a, 0x28, 0x06, 0x26, 0x4c };
        unsigned char expected[16] = { 0xa4, 0x9c, 0x7f, 0xf2, 0x68, 0x9f, 0x35, 0x2b, 0x6b, 0x5b, 0xea, 0x43, 0x02, 0x6a, 0x50, 0x49 };
        printf("> AddRoundKey ..");
        AddRoundKey(round_key, state);
        if (memcmp(state, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// SubBytes
    {
        unsigned char state[16] = { 0x19, 0x3d, 0xe3, 0xbe, 0xa0, 0xf4, 0xe2, 0x2b, 0x9a, 0xc6, 0x8d, 0x2a, 0xe9, 0xf8, 0x48, 0x08 };
        unsigned char expected[16] = { 0xd4, 0x27, 0x11, 0xae, 0xe0, 0xbf, 0x98, 0xf1, 0xb8, 0xb4, 0x5d, 0xe5, 0x1e, 0x41, 0x52, 0x30 };
        printf("> SubBytes ..");
        SubBytes(state);
        if (memcmp(state, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// ShiftRows
    {
        unsigned char state[16] = { 0xd4, 0x27, 0x11, 0xae, 0xe0, 0xbf, 0x98, 0xf1, 0xb8, 0xb4, 0x5d, 0xe5, 0x1e, 0x41, 0x52, 0x30 };
        unsigned char expected[16] = { 0xd4, 0xbf, 0x5d, 0x30, 0xe0, 0xb4, 0x52, 0xae, 0xb8, 0x41, 0x11, 0xf1, 0x1e, 0x27, 0x98, 0xe5 };
        printf("> ShiftRows ..");
        ShiftRows(state);
        if (memcmp(state, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// MixColumns
    {
        unsigned char state[16] = { 0xd4, 0xbf, 0x5d, 0x30, 0xe0, 0xb4, 0x52, 0xae, 0xb8, 0x41, 0x11, 0xf1, 0x1e, 0x27, 0x98, 0xe5 };
        unsigned char expected[16] = { 0x04, 0x66, 0x81, 0xe5, 0xe0, 0xcb, 0x19, 0x9a, 0x48, 0xf8, 0xd3, 0x7a, 0x28, 0x06, 0x26, 0x4c };
        printf("> MixColumns ..");
        MixColumns(state);
        if (memcmp(state, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// AES128ENC
    {
        unsigned char key[16] = { 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c };
        unsigned char out[16] = { 0 };
        unsigned char plain[16] = { 0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34 };
        unsigned char expected[16] = { 0x39, 0x25, 0x84, 0x1d, 0x02, 0xdc, 0x09, 0xfb, 0xdc, 0x11, 0x85, 0x97, 0x19, 0x6a, 0x0b, 0x32 };
        printf("> aes128_enc_base ..");
        aes128_enc_base(plain, out, key);
        if (memcmp(out, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// AES128ENC step 1
    {
        unsigned char key[16] = { 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c };
        unsigned char out[16] = { 0 };
        unsigned char plain[16] = { 0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34 };
        unsigned char expected[16] = { 0x39, 0x25, 0x84, 0x1d, 0x02, 0xdc, 0x09, 0xfb, 0xdc, 0x11, 0x85, 0x97, 0x19, 0x6a, 0x0b, 0x32 };
        printf("> aes128_enc_reorg_step1 ..");
        aes128_enc_reorg_step1(plain, out, key);
        if (memcmp(out, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// AES128ENC step 2
    {
        unsigned char key[16] = { 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c };
        unsigned char out[16] = { 0 };
        unsigned char plain[16] = { 0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34 };
        unsigned char expected[16] = { 0x39, 0x25, 0x84, 0x1d, 0x02, 0xdc, 0x09, 0xfb, 0xdc, 0x11, 0x85, 0x97, 0x19, 0x6a, 0x0b, 0x32 };
        printf("> aes128_enc_reorg_step2 ..");
        aes128_enc_reorg_step2(plain, out, key);
        if (memcmp(out, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// AES128ENC step 3
    {
        unsigned char key[16] = { 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c };
        unsigned char out[16] = { 0 };
        unsigned char plain[16] = { 0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34 };
        unsigned char expected[16] = { 0x39, 0x25, 0x84, 0x1d, 0x02, 0xdc, 0x09, 0xfb, 0xdc, 0x11, 0x85, 0x97, 0x19, 0x6a, 0x0b, 0x32 };
        printf("> aes128_enc_reorg_step3 ..");
        aes128_enc_reorg_step3(plain, out, key);
        if (memcmp(out, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// TO DEBUG
    /*
    {
    unsigned char key[16] = "0vercl0k@doare-e";
    unsigned char out[16] = { 0 };
    unsigned char plain[16] = "whatdup folks???";
    unsigned char expected[16] = { 0xee, 0xee, 0x83, 0xf6, 0xe4, 0x1c, 0x7a, 0x2a, 0xc7, 0xc9, 0xb6, 0x0e, 0xbc, 0x13, 0x1a, 0x57 };
    printf("> aes128_enc_reorg_step3 ..");
    aes128_enc_reorg_step3(plain, out, key);
    if (memcmp(out, expected, 16) != 0)
    {
    printf("FAIL\n");
    return 0;
    }
    printf("OK\n");
    }
    */

    /// AES128ENC wb step 1
    {
        unsigned char out[16] = { 0 };
        unsigned char plain[16] = "whatdup folks???";
        unsigned char expected[16] = { 0xee, 0xee, 0x83, 0xf6, 0xe4, 0x1c, 0x7a, 0x2a, 0xc7, 0xc9, 0xb6, 0x0e, 0xbc, 0x13, 0x1a, 0x57 };
        printf("> aes128_enc_wb_step1 ..");
        aes128_enc_wb_step1(plain, out);
        if (memcmp(out, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// AES128ENC wb step 2
    {
        unsigned char out[16] = { 0 };
        unsigned char plain[16] = "whatdup folks???";
        unsigned char expected[16] = { 0xee, 0xee, 0x83, 0xf6, 0xe4, 0x1c, 0x7a, 0x2a, 0xc7, 0xc9, 0xb6, 0x0e, 0xbc, 0x13, 0x1a, 0x57 };
        printf("> aes128_enc_wb_step2 ..");
        aes128_enc_wb_step2(plain, out);
        if (memcmp(out, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// AES128ENC wb step 3
    {
        unsigned char out[16] = { 0 };
        unsigned char plain[16] = "whatdup folks???";
        unsigned char expected[16] = { 0xee, 0xee, 0x83, 0xf6, 0xe4, 0x1c, 0x7a, 0x2a, 0xc7, 0xc9, 0xb6, 0x0e, 0xbc, 0x13, 0x1a, 0x57 };
        printf("> aes128_enc_wb_step3 ..");
        aes128_enc_wb_step3(plain, out);
        if (memcmp(out, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// AES128ENC wb step 4
    {
        unsigned char out[16] = { 0 };
        unsigned char plain[16] = "whatdup folks???";
        unsigned char expected[16] = { 0xee, 0xee, 0x83, 0xf6, 0xe4, 0x1c, 0x7a, 0x2a, 0xc7, 0xc9, 0xb6, 0x0e, 0xbc, 0x13, 0x1a, 0x57 };
        printf("> aes128_enc_wb_step4 ..");
        aes128_enc_wb_step4(plain, out);
        if (memcmp(out, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// AES128ENC wb step 5
    {
        unsigned char out[16] = { 0 };
        unsigned char plain[16] = "whatdup folks???";
        unsigned char expected[16] = { 0xee, 0xee, 0x83, 0xf6, 0xe4, 0x1c, 0x7a, 0x2a, 0xc7, 0xc9, 0xb6, 0x0e, 0xbc, 0x13, 0x1a, 0x57 };
        printf("> aes128_enc_wb_step5 ..");
        aes128_enc_wb_step5(plain, out);
        if (memcmp(out, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// AES128ENC wb final
    {
        unsigned char out[16] = { 0 };
        unsigned char plain[16] = "whatdup folks???";
        unsigned char expected[16] = { 0xee, 0xee, 0x83, 0xf6, 0xe4, 0x1c, 0x7a, 0x2a, 0xc7, 0xc9, 0xb6, 0x0e, 0xbc, 0x13, 0x1a, 0x57 };
        printf("> aes128_enc_wb_final ..");
        aes128_enc_wb_final(plain, out);
        if (memcmp(out, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// AES128ENC wb final unrolled
    {
        unsigned char out[16] = { 0 };
        unsigned char plain[16] = "whatdup folks???";
        unsigned char expected[16] = { 0xee, 0xee, 0x83, 0xf6, 0xe4, 0x1c, 0x7a, 0x2a, 0xc7, 0xc9, 0xb6, 0x0e, 0xbc, 0x13, 0x1a, 0x57 };
        printf("> aes128_enc_wb_final_unrolled ..");
        aes128_enc_wb_final_unrolled(plain, out);
        if (memcmp(out, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// AES128ENC wb final unrolled unique
    {
        unsigned char out[16] = { 0 };
        unsigned char plain[16] = "whatdup folks???";
        unsigned char expected[16] = { 0xee, 0xee, 0x83, 0xf6, 0xe4, 0x1c, 0x7a, 0x2a, 0xc7, 0xc9, 0xb6, 0x0e, 0xbc, 0x13, 0x1a, 0x57 };
        printf("> aes128_enc_wb_final_unrolled_unique ..");
        aes128_enc_wb_final_unrolled_unique(plain, out);
        if (memcmp(out, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// AES128ENC wb final unrolled unique shuffled 3533280945
    {
        unsigned char out[16] = { 0 };
        unsigned char plain[16] = "whatdup folks???";
        unsigned char expected[16] = { 0xee, 0xee, 0x83, 0xf6, 0xe4, 0x1c, 0x7a, 0x2a, 0xc7, 0xc9, 0xb6, 0x0e, 0xbc, 0x13, 0x1a, 0x57 };
        printf("> aes128_enc_wb_final_unrolled_shuffled_3533280945 ..");
        aes128_enc_wb_final_unrolled_shuffled_3533280945(plain, out);
        if (memcmp(out, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }

    /// AES128ENC wb final unrolled unique shuffled 3886914148
    {
        unsigned char out[16] = { 0 };
        unsigned char plain[16] = "whatdup folks???";
        unsigned char expected[16] = { 0xee, 0xee, 0x83, 0xf6, 0xe4, 0x1c, 0x7a, 0x2a, 0xc7, 0xc9, 0xb6, 0x0e, 0xbc, 0x13, 0x1a, 0x57 };
        printf("> aes128_enc_wb_final_unrolled_shuffled_3886914148 ..");
        aes128_enc_wb_final_unrolled_shuffled_3886914148(plain, out);
        if (memcmp(out, expected, 16) != 0)
        {
            printf("FAIL\n");
            return 0;
        }
        printf("OK\n");
    }
    
    return 1;
}

int main()
{
    // State:
    // +----+----+----+----+
    // | 2B | 28 | AB | 09 |
    // +----+----+----+----+
    // | 7E | AE | F7 | CF |
    // +----+----+----+----+
    // | 15 | D2 | 15 | 4F |
    // +----+----+----+----+
    // | 16 | A6 | 88 | 3C |
    // +----+----+----+----+

    unsigned char key[16] = {
        0x2b, 0x7e, 0x15, 0x16,
        0x28, 0xae, 0xd2, 0xa6,
        0xab, 0xf7, 0x15, 0x88,
        0x09, 0xcf, 0x4f, 0x3c
    };
    unsigned char encrypted[16] = { 0 };
    unsigned char plaintext[16] = {
        0x04, 0x66, 0x81, 0xe5,
        0xe0, 0xcb, 0x19, 0x9a,
        0x48, 0xf8, 0xd3, 0x7a,
        0x28, 0x06, 0x26, 0x4c
    };

    printf("(wb)aes128 -- @0vercl0k\n");
    if (tests() == 0)
        return EXIT_FAILURE;

    aes128_enc_base(plaintext, encrypted, key);
    return EXIT_SUCCESS;
}