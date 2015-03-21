#include <stdio.h>
#include <string.h>
#include "..\common\txor.h"
#include "..\common\tyboxes.h"

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

    out[0] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[1] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[2] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[3] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[0][4][out[4]];
    bb = Tyboxes[0][5][out[5]];
    cc = Tyboxes[0][6][out[6]];
    dd = Tyboxes[0][7][out[7]];

    out[4] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[5] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[6] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[7] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[0][8][out[8]];
    bb = Tyboxes[0][9][out[9]];
    cc = Tyboxes[0][10][out[10]];
    dd = Tyboxes[0][11][out[11]];

    out[8] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[9] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
    out[10] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
    out[11] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);

    aa = Tyboxes[0][12][out[12]];
    bb = Tyboxes[0][13][out[13]];
    cc = Tyboxes[0][14][out[14]];
    dd = Tyboxes[0][15][out[15]];

    out[12] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
    out[13] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
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
    out[10] = Tboxes_[10][out[10]];
    out[11] = Tboxes_[11][out[11]];
    out[12] = Tboxes_[12][out[12]];
    out[13] = Tboxes_[13][out[13]];
    out[14] = Tboxes_[14][out[14]];
    out[15] = Tboxes_[15][out[15]];
}

int main(int argc, char *argv[])
{
    unsigned char plain[16] = { 0 };
    unsigned char ciphered[16] = { 0 };
    if (argc != 2)
    {
        printf("./woot <password>\n");
        return -1;
    }

    if (strlen(argv[1]) != 16)
    {
        printf("the password needs to be 16b long\n");
        return -1;
    }

    memcpy(plain, argv[1], 16);
    aes128_enc_wb_final_unrolled(plain, ciphered);
    if (memcmp(ciphered, "\xc5\xae\x9a\x4d\x3f\x69\xa8\x11\x56\x5d\xa2\x36\x6a\x62\x53\xfa", 16) == 0)
        printf("Good boy!\n");
    else
        printf("Keep trying!\n");

    return 0;
}