// Axel '0vercl0k' Souchet - 7-Apr-2018
#define _CRT_SECURE_NO_WARNINGS

#include <Windows.h>
#include <stdint.h>
#include <intrin.h>
#include <stdio.h>
#include <string.h>
#include <thread>

using Slot_t = __m128i;

const size_t sboxes_size = 11534336;
const long sboxes_off = 0x3620;

__m128i mask, mask3, shiftedmask;
uint8_t sboxes[sboxes_size];

const uint8_t mul2[256] {
    0x00, 0x02, 0x04, 0x06, 0x08, 0x0a, 0x0c, 0x0e,
    0x10, 0x12, 0x14, 0x16, 0x18, 0x1a, 0x1c, 0x1e,
    0x20, 0x22, 0x24, 0x26, 0x28, 0x2a, 0x2c, 0x2e,
    0x30, 0x32, 0x34, 0x36, 0x38, 0x3a, 0x3c, 0x3e,
    0x40, 0x42, 0x44, 0x46, 0x48, 0x4a, 0x4c, 0x4e,
    0x50, 0x52, 0x54, 0x56, 0x58, 0x5a, 0x5c, 0x5e,
    0x60, 0x62, 0x64, 0x66, 0x68, 0x6a, 0x6c, 0x6e,
    0x70, 0x72, 0x74, 0x76, 0x78, 0x7a, 0x7c, 0x7e,
    0x80, 0x82, 0x84, 0x86, 0x88, 0x8a, 0x8c, 0x8e,
    0x90, 0x92, 0x94, 0x96, 0x98, 0x9a, 0x9c, 0x9e,
    0xa0, 0xa2, 0xa4, 0xa6, 0xa8, 0xaa, 0xac, 0xae,
    0xb0, 0xb2, 0xb4, 0xb6, 0xb8, 0xba, 0xbc, 0xbe,
    0xc0, 0xc2, 0xc4, 0xc6, 0xc8, 0xca, 0xcc, 0xce,
    0xd0, 0xd2, 0xd4, 0xd6, 0xd8, 0xda, 0xdc, 0xde,
    0xe0, 0xe2, 0xe4, 0xe6, 0xe8, 0xea, 0xec, 0xee,
    0xf0, 0xf2, 0xf4, 0xf6, 0xf8, 0xfa, 0xfc, 0xfe,
    0x1b, 0x19, 0x1f, 0x1d, 0x13, 0x11, 0x17, 0x15,
    0x0b, 0x09, 0x0f, 0x0d, 0x03, 0x01, 0x07, 0x05,
    0x3b, 0x39, 0x3f, 0x3d, 0x33, 0x31, 0x37, 0x35,
    0x2b, 0x29, 0x2f, 0x2d, 0x23, 0x21, 0x27, 0x25,
    0x5b, 0x59, 0x5f, 0x5d, 0x53, 0x51, 0x57, 0x55,
    0x4b, 0x49, 0x4f, 0x4d, 0x43, 0x41, 0x47, 0x45,
    0x7b, 0x79, 0x7f, 0x7d, 0x73, 0x71, 0x77, 0x75,
    0x6b, 0x69, 0x6f, 0x6d, 0x63, 0x61, 0x67, 0x65,
    0x9b, 0x99, 0x9f, 0x9d, 0x93, 0x91, 0x97, 0x95,
    0x8b, 0x89, 0x8f, 0x8d, 0x83, 0x81, 0x87, 0x85,
    0xbb, 0xb9, 0xbf, 0xbd, 0xb3, 0xb1, 0xb7, 0xb5,
    0xab, 0xa9, 0xaf, 0xad, 0xa3, 0xa1, 0xa7, 0xa5,
    0xdb, 0xd9, 0xdf, 0xdd, 0xd3, 0xd1, 0xd7, 0xd5,
    0xcb, 0xc9, 0xcf, 0xcd, 0xc3, 0xc1, 0xc7, 0xc5,
    0xfb, 0xf9, 0xff, 0xfd, 0xf3, 0xf1, 0xf7, 0xf5,
    0xeb, 0xe9, 0xef, 0xed, 0xe3, 0xe1, 0xe7, 0xe5,
};

const uint8_t mul3[256] {
    0x00, 0x03, 0x06, 0x05, 0x0c, 0x0f, 0x0a, 0x09,
    0x18, 0x1b, 0x1e, 0x1d, 0x14, 0x17, 0x12, 0x11,
    0x30, 0x33, 0x36, 0x35, 0x3c, 0x3f, 0x3a, 0x39,
    0x28, 0x2b, 0x2e, 0x2d, 0x24, 0x27, 0x22, 0x21,
    0x60, 0x63, 0x66, 0x65, 0x6c, 0x6f, 0x6a, 0x69,
    0x78, 0x7b, 0x7e, 0x7d, 0x74, 0x77, 0x72, 0x71,
    0x50, 0x53, 0x56, 0x55, 0x5c, 0x5f, 0x5a, 0x59,
    0x48, 0x4b, 0x4e, 0x4d, 0x44, 0x47, 0x42, 0x41,
    0xc0, 0xc3, 0xc6, 0xc5, 0xcc, 0xcf, 0xca, 0xc9,
    0xd8, 0xdb, 0xde, 0xdd, 0xd4, 0xd7, 0xd2, 0xd1,
    0xf0, 0xf3, 0xf6, 0xf5, 0xfc, 0xff, 0xfa, 0xf9,
    0xe8, 0xeb, 0xee, 0xed, 0xe4, 0xe7, 0xe2, 0xe1,
    0xa0, 0xa3, 0xa6, 0xa5, 0xac, 0xaf, 0xaa, 0xa9,
    0xb8, 0xbb, 0xbe, 0xbd, 0xb4, 0xb7, 0xb2, 0xb1,
    0x90, 0x93, 0x96, 0x95, 0x9c, 0x9f, 0x9a, 0x99,
    0x88, 0x8b, 0x8e, 0x8d, 0x84, 0x87, 0x82, 0x81,
    0x9b, 0x98, 0x9d, 0x9e, 0x97, 0x94, 0x91, 0x92,
    0x83, 0x80, 0x85, 0x86, 0x8f, 0x8c, 0x89, 0x8a,
    0xab, 0xa8, 0xad, 0xae, 0xa7, 0xa4, 0xa1, 0xa2,
    0xb3, 0xb0, 0xb5, 0xb6, 0xbf, 0xbc, 0xb9, 0xba,
    0xfb, 0xf8, 0xfd, 0xfe, 0xf7, 0xf4, 0xf1, 0xf2,
    0xe3, 0xe0, 0xe5, 0xe6, 0xef, 0xec, 0xe9, 0xea,
    0xcb, 0xc8, 0xcd, 0xce, 0xc7, 0xc4, 0xc1, 0xc2,
    0xd3, 0xd0, 0xd5, 0xd6, 0xdf, 0xdc, 0xd9, 0xda,
    0x5b, 0x58, 0x5d, 0x5e, 0x57, 0x54, 0x51, 0x52,
    0x43, 0x40, 0x45, 0x46, 0x4f, 0x4c, 0x49, 0x4a,
    0x6b, 0x68, 0x6d, 0x6e, 0x67, 0x64, 0x61, 0x62,
    0x73, 0x70, 0x75, 0x76, 0x7f, 0x7c, 0x79, 0x7a,
    0x3b, 0x38, 0x3d, 0x3e, 0x37, 0x34, 0x31, 0x32,
    0x23, 0x20, 0x25, 0x26, 0x2f, 0x2c, 0x29, 0x2a,
    0x0b, 0x08, 0x0d, 0x0e, 0x07, 0x04, 0x01, 0x02,
    0x13, 0x10, 0x15, 0x16, 0x1f, 0x1c, 0x19, 0x1a
};
__m128i crc;

void round(const uint32_t nround, Slot_t *Slot) {
    uint64_t v7; // rbp
    uint64_t v8; // r12
    uint64_t v9; // r10
    uint64_t v10; // r11
    uint8_t v11; // r9
    uint8_t v12; // cl
    uint8_t v13; // cl
    uint64_t v14; // r9
    uint64_t v15; // rdi
    uint8_t v16; // cl
    uint64_t v17; // r12
    uint8_t v18; // cl
    uint64_t v19; // r11
    uint8_t v20; // si
    uint8_t v21; // cl
    uint64_t v22; // r9
    uint8_t v23; // si
    uint8_t v24; // cl
    uint64_t v25; // rdi
    uint8_t v26; // si
    uint8_t v27; // cl
    uint64_t v28; // r12
    uint8_t v29; // si
    uint8_t v30; // cl
    uint64_t v31; // r11
    uint8_t v32; // si
    uint8_t v33; // cl
    uint64_t v34; // r9
    uint8_t v35; // si
    uint8_t v36; // cl
    uint64_t v37; // rdi
    uint8_t v38; // si
    uint8_t v39; // r8
    uint8_t v40; // cl
    uint8_t v42; // di
    uint8_t v43; // cl
    uint8_t v44; // r8
    uint8_t v45; // si
    uint8_t v46; // di
    uint8_t v47; // r8
    uint8_t v48; // cl
    uint8_t v49; // si
    uint8_t v50; // di
    uint8_t v51; // r8
    uint8_t v52; // cl
    uint64_t v54; // rdx
    uint64_t v55; // r8
    uint64_t v56; // rdi
    uint8_t *v57; // r10
    uint64_t v58; // rdi
    uint64_t v60; // rdi
    uint8_t *v61; // r12
    uint64_t v62; // rdi
    uint64_t v64; // rdi
    uint64_t v65; // rdi
    uint8_t *v66; // r11
    uint64_t v67; // rdi
    uint8_t *v68; // r8
    uint64_t v69; // rdi
    uint64_t v70; // rdi
    uint64_t v71; // rdi
    uint64_t v72; // rdi
    uint64_t v73; // rdi
    __m128i v77; // [rsp+10h] [rbp-138h]
    uint64_t v79; // [rsp+28h] [rbp-120h]
    uint8_t *v80; // [rsp+30h] [rbp-118h]
    uint64_t v81; // [rsp+38h] [rbp-110h]
    uint8_t *v83; // [rsp+48h] [rbp-100h]
    uint8_t *v84; // [rsp+50h] [rbp-F8h]
    uint8_t *v85; // [rsp+58h] [rbp-F0h]
    uint64_t v88; // [rsp+70h] [rbp-D8h]
    uint8_t *v89; // [rsp+78h] [rbp-D0h]
    uint64_t v90; // [rsp+80h] [rbp-C8h]
    uint8_t *v91; // [rsp+88h] [rbp-C0h]
    uint64_t v92; // [rsp+90h] [rbp-B8h]
    uint8_t *v93; // [rsp+98h] [rbp-B0h]
    uint64_t v94; // [rsp+A0h] [rbp-A8h]
    uint8_t *v95; // [rsp+A8h] [rbp-A0h]
    uint64_t v96; // [rsp+B0h] [rbp-98h]
    uint8_t *v97; // [rsp+B8h] [rbp-90h]
    uint64_t v98; // [rsp+C0h] [rbp-88h]
    uint8_t *v99; // [rsp+C8h] [rbp-80h]
    uint64_t v100; // [rsp+D0h] [rbp-78h]
    uint8_t *v101; // [rsp+D8h] [rbp-70h]
    switch (nround)
    {
        case 0: {
            *Slot = _mm_xor_si128(_mm_load_si128(Slot), mask);
            break;
        }
        case 1:
        case 5:
        case 9:
        case 13:
        case 17:
        case 21:
        case 25:
        case 29:
        case 33:
        case 37: {
            v54 = nround >> 2;
            v55 = Slot->m128i_u8[0];
            v77.m128i_u64[0] = mask.m128i_u8[0];
            v56 = v54;
            v54 <<= 20;
            v79 = mask.m128i_u8[1];
            v81 = mask.m128i_u8[2];
            v57 = &sboxes[256 * (v55 + (v56 << 12))];
            v58 = Slot->m128i_u8[1];
            v80 = &sboxes[256 * v58 + v54];
            v60 = Slot->m128i_u8[2];
            v61 = &sboxes[256 * v60 + v54];
            v62 = Slot->m128i_u8[3];
            v83 = &sboxes[256 * v62 + v54];
            v64 = Slot->m128i_u8[4];
            v84 = &sboxes[256 * v64 + v54];
            v65 = Slot->m128i_u8[6];
            v85 = &sboxes[256 * uint64_t(Slot->m128i_u8[5]) + v54];
            v66 = &sboxes[256 * v65 + v54];
            v67 = Slot->m128i_u8[7];
            v68 = &sboxes[256 * v67 + v54];
            v69 = Slot->m128i_u8[8];
            v88 = mask.m128i_u8[8];
            v89 = &sboxes[256 * v69 + v54];
            v90 = mask.m128i_u8[9];
            v70 = v54 + (uint64_t(Slot->m128i_u8[9]) << 8);
            v92 = mask.m128i_u8[10];
            v91 = &sboxes[v70];
            v71 = Slot->m128i_u8[10];
            v94 = mask.m128i_u8[11];
            v96 = mask.m128i_u8[12];
            v93 = &sboxes[256 * v71 + v54];
            v72 = Slot->m128i_u8[11];
            v98 = mask.m128i_u8[13];
            v95 = &sboxes[256 * v72 + v54];
            v73 = Slot->m128i_u8[12];
            v100 = mask.m128i_u8[14];
            v97 = &sboxes[256 * v73 + v54];
            v99 = &sboxes[256 * uint64_t(Slot->m128i_u8[13]) + v54];
            v101 = &sboxes[256 * uint64_t(Slot->m128i_u8[14]) + v54];
            Slot->m128i_u8[0] = v57[mask.m128i_u8[0]];
            Slot->m128i_u8[1] = v80[mask.m128i_u8[1] + 0x10000];
            Slot->m128i_u8[2] = v61[mask.m128i_u8[2] + 0x20000];
            Slot->m128i_u8[3] = v83[mask.m128i_u8[3] + 196608];
            Slot->m128i_u8[4] = v84[mask.m128i_u8[4] + 0x40000];
            Slot->m128i_u8[5] = v85[mask.m128i_u8[5] + 327680];
            Slot->m128i_u8[6] = v66[mask.m128i_u8[6] + 393216];
            Slot->m128i_u8[7] = v68[mask.m128i_u8[7] + 458752];
            Slot->m128i_u8[8] = v89[mask.m128i_u8[8] + 0x80000];
            Slot->m128i_u8[9] = v91[mask.m128i_u8[9] + 589824];
            Slot->m128i_u8[10] = v93[mask.m128i_u8[10] + 655360];
            Slot->m128i_u8[11] = v95[mask.m128i_u8[11] + 720896];
            Slot->m128i_u8[12] = v97[mask.m128i_u8[12] + 786432];
            Slot->m128i_u8[13] = v99[mask.m128i_u8[13] + 851968];
            Slot->m128i_u8[14] = v101[mask.m128i_u8[14] + 917504];
            Slot->m128i_u8[15] = sboxes[256 * uint64_t(Slot->m128i_u8[15]) + 983040 + v54 + mask.m128i_u8[15]];
            *Slot = _mm_xor_si128(*Slot, crc);
            break;
        }
        case 2:
        case 6:
        case 10:
        case 14:
        case 18:
        case 22:
        case 26:
        case 30:
        case 34:
        case 38: {
            v42 = Slot->m128i_u8[6];
            v43 = Slot->m128i_u8[4];
            v44 = Slot->m128i_u8[5];
            Slot->m128i_u8[6] = Slot->m128i_u8[7];
            Slot->m128i_u8[5] = v42;
            v45 = Slot->m128i_u8[8];
            v46 = Slot->m128i_u8[11];
            Slot->m128i_u8[4] = v44;
            Slot->m128i_u8[7] = v43;
            v47 = Slot->m128i_u8[10];
            v48 = Slot->m128i_u8[9];
            Slot->m128i_u8[10] = v45;
            Slot->m128i_u8[9] = v46;
            v49 = Slot->m128i_u8[13];
            v50 = Slot->m128i_u8[12];
            Slot->m128i_u8[8] = v47;
            Slot->m128i_u8[11] = v48;
            v51 = Slot->m128i_u8[15];
            v52 = Slot->m128i_u8[14];
            Slot->m128i_u8[13] = v50;
            Slot->m128i_u8[14] = v49;
            Slot->m128i_u8[12] = v51;
            Slot->m128i_u8[15] = v52;
            break;
        }
        case 3:
        case 7:
        case 11:
        case 15:
        case 19:
        case 23:
        case 27:
        case 31:
        case 35: {
            v7 = Slot->m128i_u8[0];
            v8 = Slot->m128i_u8[4];
            v9 = Slot->m128i_u8[1];
            v10 = Slot->m128i_u8[5];
            v11 = Slot->m128i_u8[14] ^ Slot->m128i_u8[10];
            v12 = mul3[v8] ^ mul2[v7] ^ Slot->m128i_u8[12] ^ Slot->m128i_u8[8];
            v81 = Slot->m128i_u8[3];
            uint8_t v78x = v12;
            uint8_t v79x = mul3[v10] ^ mul2[v9] ^ Slot->m128i_u8[13] ^ Slot->m128i_u8[9];
            v77.m128i_u64[0] = Slot->m128i_u8[2];
            v13 = mul2[v77.m128i_u64[0]] ^ v11;
            v14 = Slot->m128i_u8[6];
            uint8_t v80x = mul3[v14] ^ v13;
            v15 = Slot->m128i_u8[7];
            uint8_t v82x = mul3[v15] ^ mul2[v81] ^ Slot->m128i_u8[15] ^ Slot->m128i_u8[11];
            v16 = mul2[v8] ^ Slot->m128i_u8[12] ^ Slot->m128i_u8[0];
            v17 = Slot->m128i_u8[8];
            uint8_t v83x = mul3[v17] ^ v16;
            v18 = mul2[v10] ^ Slot->m128i_u8[13] ^ Slot->m128i_u8[1];
            v19 = Slot->m128i_u8[9];
            v20 = Slot->m128i_u8[14] ^ Slot->m128i_u8[2];
            uint8_t v84x = mul3[v19] ^ v18;
            v21 = mul2[v14] ^ v20;
            v22 = Slot->m128i_u8[10];
            v23 = Slot->m128i_u8[15] ^ Slot->m128i_u8[3];
            uint8_t v85x = mul3[v22] ^ v21;
            v24 = mul2[v15] ^ v23;
            v25 = Slot->m128i_u8[11];
            v26 = Slot->m128i_u8[4] ^ Slot->m128i_u8[0];
            uint8_t v86x = mul3[v25] ^ v24;
            v27 = mul2[v17] ^ v26;
            v28 = Slot->m128i_u8[12];
            v29 = Slot->m128i_u8[5] ^ Slot->m128i_u8[1];
            uint8_t v87x = mul3[v28] ^ v27;
            v30 = mul2[v19] ^ v29;
            v31 = Slot->m128i_u8[13];
            v32 = Slot->m128i_u8[6] ^ Slot->m128i_u8[2];
            uint8_t v88x = mul3[v31] ^ v30;
            v33 = mul2[v22] ^ v32;
            v34 = Slot->m128i_u8[14];
            v35 = Slot->m128i_u8[7] ^ Slot->m128i_u8[3];
            uint8_t v89x = mul3[v34] ^ v33;
            v36 = mul2[v25] ^ v35;
            v37 = Slot->m128i_u8[15];
            v38 = Slot->m128i_u8[8] ^ Slot->m128i_u8[4];
            uint8_t v90x = mul3[v37] ^ v36;
            uint8_t v7x = mul2[v28] ^ v38 ^ mul3[v7];
            v9 = mul2[v31] ^ Slot->m128i_u8[9] ^ Slot->m128i_u8[5] ^ mul3[v9];
            v39 = mul3[v77.m128i_u64[0]] ^ mul2[v34] ^ Slot->m128i_u8[10] ^ Slot->m128i_u8[6];
            v40 = mul3[v81] ^ Slot->m128i_u8[11] ^ Slot->m128i_u8[7] ^ mul2[v37];
            Slot->m128i_u8[0] = v78x;
            Slot->m128i_u8[1] = v79x;
            Slot->m128i_u8[2] = v80x;
            Slot->m128i_u8[3] = v82x;
            Slot->m128i_u8[4] = v83x;
            Slot->m128i_u8[5] = v84x;
            Slot->m128i_u8[6] = v85x;
            Slot->m128i_u8[7] = v86x;

            Slot->m128i_u8[8] = v87x;
            Slot->m128i_u8[9] = v88x;
            Slot->m128i_u8[10] = v89x;
            Slot->m128i_u8[11] = v90x;
            Slot->m128i_u8[12] = v7x;
            Slot->m128i_u8[13] = uint8_t(v9);
            Slot->m128i_u8[14] = v39;
            Slot->m128i_u8[15] = v40;
            break;
        }

        case 4:
        case 8:
        case 12:
        case 16:
        case 20:
        case 24:
        case 28:
        case 32:
        case 36: {
            *Slot = _mm_xor_si128(_mm_load_si128(Slot), mask3);
            break;
        }
        case 39: {
            *Slot = _mm_xor_si128(_mm_load_si128(Slot), shiftedmask);
            break;
        }
    default:
        break;
    }
}

void hexdump(FILE * stream, void const * data, unsigned int len)
{
    unsigned int i;
    unsigned int r, c;

    if (!stream)
        return;
    if (!data)
        return;

    for (r = 0, i = 0; r<(len / 16 + (len % 16 != 0)); r++, i += 16)
    {
        fprintf(stream, "%04X:   ", i); /* location of first byte in line */

        for (c = i; c<i + 8; c++) /* left half of hex dump */
            if (c<len)
                fprintf(stream, "%02X ", ((unsigned char const *)data)[c]);
            else
                fprintf(stream, "   "); /* pad if short line */

        fprintf(stream, "  ");

        for (c = i + 8; c<i + 16; c++) /* right half of hex dump */
            if (c<len)
                fprintf(stream, "%02X ", ((unsigned char const *)data)[c]);
            else
                fprintf(stream, "   "); /* pad if short line */

        fprintf(stream, "   ");

        for (c = i; c<i + 16; c++) /* ASCII dump */
            if (c<len)
                if (((unsigned char const *)data)[c] >= 32 &&
                    ((unsigned char const *)data)[c]<127)
                    fprintf(stream, "%c", ((char const *)data)[c]);
                else
                    fprintf(stream, "."); /* put this for non-printables */
            else
                fprintf(stream, " "); /* pad if short line */

        fprintf(stream, "\n");
    }

    fflush(stream);
}

void reverse_0(Slot_t &Output, Slot_t &Input) {
    Input = _mm_xor_si128(_mm_load_si128(&Output), mask);
}

void reverse_35(Slot_t &Output, Slot_t &Input) {
    uint8_t final_result[16];
    std::thread t0([Output, &final_result]() {
        Slot_t Input;
        for (uint64_t a = 0; a < 0x100; ++a) {
            for (uint64_t b = 0; b < 0x100; ++b) {
                for (uint64_t c = 0; c < 0x100; ++c) {
                    for (uint64_t d = 0; d < 0x100; ++d) {
                        Input.m128i_u8[0] = uint8_t(a);
                        Input.m128i_u8[4] = uint8_t(b);
                        Input.m128i_u8[8] = uint8_t(c);
                        Input.m128i_u8[12] = uint8_t(d);
                        round(35, &Input);
                        if (Input.m128i_u8[0] == Output.m128i_u8[0] && Input.m128i_u8[4] == Output.m128i_u8[4] &&
                            Input.m128i_u8[8] == Output.m128i_u8[8] && Input.m128i_u8[12] == Output.m128i_u8[12]) {

                            final_result[0] = uint8_t(a);
                            final_result[4] = uint8_t(b);
                            final_result[8] = uint8_t(c);
                            final_result[12] = uint8_t(d);
                            return;
                        }
                    }
                }
            }
        }
    });
    std::thread t1([Output, &final_result]() {
        Slot_t Input;
        for (uint64_t a = 0; a < 0x100; ++a) {
            for (uint64_t b = 0; b < 0x100; ++b) {
                for (uint64_t c = 0; c < 0x100; ++c) {
                    for (uint64_t d = 0; d < 0x100; ++d) {
                        Input.m128i_u8[1] = uint8_t(a);
                        Input.m128i_u8[5] = uint8_t(b);
                        Input.m128i_u8[9] = uint8_t(c);
                        Input.m128i_u8[13] = uint8_t(d);
                        round(35, &Input);
                        if (Input.m128i_u8[1] == Output.m128i_u8[1] && Input.m128i_u8[5] == Output.m128i_u8[5] &&
                            Input.m128i_u8[9] == Output.m128i_u8[9] && Input.m128i_u8[13] == Output.m128i_u8[13]) {

                            final_result[1] = uint8_t(a);
                            final_result[5] = uint8_t(b);
                            final_result[9] = uint8_t(c);
                            final_result[13] = uint8_t(d);
                            return;
                        }
                    }
                }
            }
        }
    });
    std::thread t2([Output, &final_result]() {
        Slot_t Input;
        for (uint64_t a = 0; a < 0x100; ++a) {
            for (uint64_t b = 0; b < 0x100; ++b) {
                for (uint64_t c = 0; c < 0x100; ++c) {
                    for (uint64_t d = 0; d < 0x100; ++d) {
                        Input.m128i_u8[2] = uint8_t(a);
                        Input.m128i_u8[6] = uint8_t(b);
                        Input.m128i_u8[10] = uint8_t(c);
                        Input.m128i_u8[14] = uint8_t(d);
                        round(35, &Input);
                        if (Input.m128i_u8[2] == Output.m128i_u8[2] && Input.m128i_u8[6] == Output.m128i_u8[6] &&
                            Input.m128i_u8[10] == Output.m128i_u8[10] && Input.m128i_u8[14] == Output.m128i_u8[14]) {

                            final_result[2] = uint8_t(a);
                            final_result[6] = uint8_t(b);
                            final_result[10] = uint8_t(c);
                            final_result[14] = uint8_t(d);
                            return;
                        }
                    }
                }
            }
        }
    });
    std::thread t3([Output, &final_result]() {
        Slot_t Input;
        for (uint64_t a = 0; a < 0x100; ++a) {
            for (uint64_t b = 0; b < 0x100; ++b) {
                for (uint64_t c = 0; c < 0x100; ++c) {
                    for (uint64_t d = 0; d < 0x100; ++d) {
                        Input.m128i_u8[3] = uint8_t(a);
                        Input.m128i_u8[7] = uint8_t(b);
                        Input.m128i_u8[11] = uint8_t(c);
                        Input.m128i_u8[15] = uint8_t(d);
                        round(35, &Input);
                        if (Input.m128i_u8[3] == Output.m128i_u8[3] && Input.m128i_u8[7] == Output.m128i_u8[7] &&
                            Input.m128i_u8[11] == Output.m128i_u8[11] && Input.m128i_u8[15] == Output.m128i_u8[15]) {

                            final_result[3] = uint8_t(a);
                            final_result[7] = uint8_t(b);
                            final_result[11] = uint8_t(c);
                            final_result[15] = uint8_t(d);
                            return;
                        }
                    }
                }
            }
        }
    });
   
    t0.join();
    t1.join();
    t2.join();
    t3.join();
    memcpy(Input.m128i_u8, final_result, 16);
    return;
}

/*
void reverse_35_st(Slot_t &Output, Slot_t &Input) {
    uint8_t is[16];
    for (uint64_t a = 0; a < 0x100; ++a) {
        for (uint64_t b = 0; b < 0x100; ++b) {
            for (uint64_t c = 0; c < 0x100; ++c) {
                for (uint64_t d = 0; d < 0x100; ++d) {
                    Input.m128i_u8[0] = uint8_t(a);
                    Input.m128i_u8[4] = uint8_t(b);
                    Input.m128i_u8[8] = uint8_t(c);
                    Input.m128i_u8[12] = uint8_t(d);
                    round(35, &Input);
                    if (Input.m128i_u8[0] == Output.m128i_u8[0] && Input.m128i_u8[4] == Output.m128i_u8[4] &&
                        Input.m128i_u8[8] == Output.m128i_u8[8] && Input.m128i_u8[12] == Output.m128i_u8[12]) {

                        is[0] = uint8_t(a);
                        is[4] = uint8_t(b);
                        is[8] = uint8_t(c);
                        is[12] = uint8_t(d);
                        goto x;
                    }
                }
            }
        }
    }
x:
    for (uint64_t a = 0; a < 0x100; ++a) {
        for (uint64_t b = 0; b < 0x100; ++b) {
            for (uint64_t c = 0; c < 0x100; ++c) {
                for (uint64_t d = 0; d < 0x100; ++d) {
                    Input.m128i_u8[1] = uint8_t(a);
                    Input.m128i_u8[5] = uint8_t(b);
                    Input.m128i_u8[9] = uint8_t(c);
                    Input.m128i_u8[13] = uint8_t(d);
                    round(35, &Input);
                    if (Input.m128i_u8[1] == Output.m128i_u8[1] && Input.m128i_u8[5] == Output.m128i_u8[5] &&
                        Input.m128i_u8[9] == Output.m128i_u8[9] && Input.m128i_u8[13] == Output.m128i_u8[13]) {

                        is[1] = uint8_t(a);
                        is[5] = uint8_t(b);
                        is[9] = uint8_t(c);
                        is[13] = uint8_t(d);
                        goto xx;
                    }
                }
            }
        }
    }
xx:
    for (uint64_t a = 0; a < 0x100; ++a) {
        for (uint64_t b = 0; b < 0x100; ++b) {
            for (uint64_t c = 0; c < 0x100; ++c) {
                for (uint64_t d = 0; d < 0x100; ++d) {
                    Input.m128i_u8[2] = uint8_t(a);
                    Input.m128i_u8[6] = uint8_t(b);
                    Input.m128i_u8[10] = uint8_t(c);
                    Input.m128i_u8[14] = uint8_t(d);
                    round(35, &Input);
                    if (Input.m128i_u8[2] == Output.m128i_u8[2] && Input.m128i_u8[6] == Output.m128i_u8[6] &&
                        Input.m128i_u8[10] == Output.m128i_u8[10] && Input.m128i_u8[14] == Output.m128i_u8[14]) {

                        is[2] = uint8_t(a);
                        is[6] = uint8_t(b);
                        is[10] = uint8_t(c);
                        is[14] = uint8_t(d);
                        goto xxx;
                    }
                }
            }
        }
    }
xxx:
    for (uint64_t a = 0; a < 0x100; ++a) {
        for (uint64_t b = 0; b < 0x100; ++b) {
            for (uint64_t c = 0; c < 0x100; ++c) {
                for (uint64_t d = 0; d < 0x100; ++d) {
                    Input.m128i_u8[3] = uint8_t(a);
                    Input.m128i_u8[7] = uint8_t(b);
                    Input.m128i_u8[11] = uint8_t(c);
                    Input.m128i_u8[15] = uint8_t(d);
                    round(35, &Input);
                    if (Input.m128i_u8[3] == Output.m128i_u8[3] && Input.m128i_u8[7] == Output.m128i_u8[7] &&
                        Input.m128i_u8[11] == Output.m128i_u8[11] && Input.m128i_u8[15] == Output.m128i_u8[15]) {

                        is[3] = uint8_t(a);
                        is[7] = uint8_t(b);
                        is[11] = uint8_t(c);
                        is[15] = uint8_t(d);
                        goto xxxx;
                    }
                }
            }
        }
    }
xxxx:
    memcpy(Input.m128i_u8, is, 16);
    return;
}
*/

void reverse_36(Slot_t &Output, Slot_t &Input) {
    Input = _mm_xor_si128(_mm_load_si128(&Output), mask3);
}

void reverse_37(const uint32_t nround, Slot_t &Output, Slot_t &Input) {
    uint8_t is[16];
    for (uint32_t i = 0; i < 16; ++i) {
        for (uint32_t c = 0; c < 0x100; ++c) {
            Input.m128i_u8[i] = c;
            round(nround, &Input);
            if (Input.m128i_u8[i] == Output.m128i_u8[i]) {
                is[i] = c;
                break;
            }
        }
    }
    memcpy(Input.m128i_u8, is, 16);
}

void reverse_38(Slot_t &Output, Slot_t &Input) {
    uint8_t s4 = Output.m128i_u8[4];
    Output.m128i_u8[4] = Output.m128i_u8[7];
    uint8_t s5 = Output.m128i_u8[5];
    Output.m128i_u8[5] = s4;
    uint8_t s6 = Output.m128i_u8[6];
    Output.m128i_u8[6] = s5;
    uint8_t s7 = Output.m128i_u8[7];
    Output.m128i_u8[7] = s6;
    uint8_t s8 = Output.m128i_u8[8];
    Output.m128i_u8[8] = Output.m128i_u8[10];
    uint8_t s9 = Output.m128i_u8[9];
    Output.m128i_u8[9] = Output.m128i_u8[11];
    Output.m128i_u8[10] = s8;
    Output.m128i_u8[11] = s9;
    uint8_t s12 = Output.m128i_u8[12];
    Output.m128i_u8[12] = Output.m128i_u8[13];
    uint8_t s13 = Output.m128i_u8[13];
    Output.m128i_u8[13] = Output.m128i_u8[14];
    Output.m128i_u8[14] = Output.m128i_u8[15];
    Output.m128i_u8[15] = s12;
    memcpy(Input.m128i_u8, Output.m128i_u8, 16);
}

void reverse_39(Slot_t &Output, Slot_t &Input) {
    Input = _mm_xor_si128(_mm_load_si128(&Output), shiftedmask);
}

void unround(const uint32_t nround, Slot_t &Output, Slot_t &Input) {
    switch (nround)
    {
    case 0: {
        reverse_0(Output, Input);
        break;
    }
    case 1:
    case 5:
    case 9:
    case 13:
    case 17:
    case 21:
    case 25:
    case 29:
    case 33:
    case 37: {
        reverse_37(nround, Output, Input);
        break;
    }
    case 2:
    case 6:
    case 10:
    case 14:
    case 18:
    case 22:
    case 26:
    case 30:
    case 34:
    case 38: {
        reverse_38(Output, Input);
        break;
    }
    case 3:
    case 7:
    case 11:
    case 15:
    case 19:
    case 23:
    case 27:
    case 31:
    case 35: {
        reverse_35(Output, Input);
        break;
    }

    case 4:
    case 8:
    case 12:
    case 16:
    case 20:
    case 24:
    case 28:
    case 32:
    case 36: {
        reverse_36(Output, Input);
        break;
    }
    case 39: {
        reverse_39(Output, Input);
        break;
    }
    default:
        break;
    }
}

void init_globals() {

    const uint8_t crc_bytes[] {
        0x9b, 0x04, 0x57, 0x44, 0xe5, 0x1f, 0xf0, 0xf9,
        0xe8, 0x4a, 0x54, 0xda, 0x68, 0xe0, 0x52, 0xb8,
    };
    // variables

    // x/16bx &mask
    const uint8_t mask_bytes[]{
        0x77, 0xf5, 0xa5, 0x08, 0x9e, 0x31, 0x63, 0xa0,
        0x9e, 0xf9, 0x91, 0xe3, 0x77, 0x22, 0xcf, 0x9c,
    };
    // x/16bx &mask3
    const uint8_t mask3_bytes[]{
        0xc7, 0x35, 0xb3, 0x97, 0xbf, 0x4b, 0x06, 0x50,
        0x5e, 0x2b, 0xd5, 0xd6, 0x6d, 0x48, 0x41, 0x66,
    };
    // x/16bx &shiftedmask
    const uint8_t shiftedmask_bytes[16]{
        0x77, 0xf5, 0xa5, 0x08, 0x31, 0x63, 0xa0, 0x9e,
        0x91, 0xe3, 0x9e, 0xf9, 0x9c, 0x77, 0x22, 0xcf,
    };

    memcpy(crc.m128i_u8, crc_bytes, 16);
    memcpy(mask.m128i_u8, mask_bytes, 16);
    memcpy(mask3.m128i_u8, mask3_bytes, 16);
    memcpy(shiftedmask.m128i_u8, shiftedmask_bytes, 16);

    FILE *fin = fopen(R"(C:\work\challenges\ledgerctf\ctf2\ctf2)", "rb");
    fseek(fin, sboxes_off, SEEK_SET);
    fread(sboxes, sboxes_size, 1, fin);
    fclose(fin);
}

void encrypt(Slot_t *States) {
    for (uint32_t i = 0; i < 15; ++i) {
        for (uint32_t j = 0; j < 40; ++j) {
            round(j, &States[i]);
        }
    }
}

void recover_state(Slot_t &Output, Slot_t &Input) {
    for (int32_t i = 39; i > -1; --i) {
        unround(i, Output, Input);
        memcpy(Output.m128i_u8, Input.m128i_u8, 16);
    }
}

void slot2password(const uint8_t *Ptr, uint8_t Password[16]) {
    Password[0] = Ptr[0];
    Password[1] = Ptr[4];
    Password[2] = Ptr[8];
    Password[3] = Ptr[0xc];
    Password[4] = Ptr[1];
    Password[5] = Ptr[5];
    Password[6] = Ptr[9];
    Password[7] = Ptr[0xd];
    Password[8] = Ptr[2];
    Password[9] = Ptr[6];
    Password[10] = Ptr[0xa];
    Password[11] = Ptr[0xe];
    Password[12] = Ptr[3];
    Password[13] = Ptr[7];
    Password[14] = Ptr[0xb];
    Password[15] = Ptr[0xf];
}

void pwn() {
    const uint8_t WantedOutputBytes[16] {
        0x13, 0x13, 0x13, 0x13, 0x37, 0x37, 0x37, 0x37, 0x69, 0x69, 0x69, 0x69, 0x42, 0x42, 0x42, 0x42,
    };
    Slot_t WantedOutput, Input;
    memcpy(WantedOutput.m128i_u8, WantedOutputBytes, 16);
    recover_state(WantedOutput, Input);
    hexdump(stdout, Input.m128i_u8, 16);
    uint8_t Password[16];
    slot2password(Input.m128i_u8, Password);
    for (size_t i = 0; i < 16; ++i) {
        printf("%.2X", Password[i]);
    }
    printf("\n");
}

void recover_key() {
    uint8_t Input[16];
    for (uint8_t i = 0; i < 16; ++i) {
        Input[i] = i;
    }

    printf("Cleartext:\n");
    hexdump(stdout, Input, 16);

    Slot_t InputSlot;
    memcpy(InputSlot.m128i_u8, Input, 16);
    for (uint32_t i = 1; i < 3; ++i) {
        round(i, &InputSlot);
    }

    Slot_t Key;
    memcpy(Key.m128i_u8, Input, 16);
    for (uint32_t i = 1; i < 4; ++i) {
        round(i, &Key);
    }

    for (size_t i = 0; i < 16; ++i) {
        Key.m128i_u8[i] ^= InputSlot.m128i_u8[i];
    }

    printf("Key?\n");
    hexdump(stdout, Key.m128i_u8, 16);
    
    Slot_t Cipher;
    memcpy(Cipher.m128i_u8, Input, 16);
    for (uint32_t i = 0; i < 40; ++i) {
        round(i, &Cipher);
    }

    printf("Ciphered:\n");
    hexdump(stdout, Cipher.m128i_u8, 16);
}

bool tests() {
    bool Worked = true;
     {
        const uint8_t RawBytes[15 * sizeof(Slot_t)]{
            0x66, 0xcc, 0x33, 0x55, 0x88, 0xee, 0x77, 0x00, 0xdd, 0x22, 0x99, 0x11, 0xff, 0xbb, 0x44, 0xaa,
            0xff, 0xcc, 0x66, 0xaa, 0x99, 0x55, 0x22, 0x00, 0x77, 0x11, 0x88, 0xbb, 0xdd, 0x33, 0xee, 0x44,
            0xaa, 0x33, 0xdd, 0xcc, 0x66, 0xee, 0x11, 0x44, 0xbb, 0x55, 0x77, 0xff, 0x22, 0x00, 0x88, 0x99,
            0xaa, 0x55, 0x33, 0x11, 0xbb, 0xdd, 0x66, 0xcc, 0x22, 0xff, 0x44, 0x88, 0xee, 0x77, 0x99, 0x00,
            0x00, 0x66, 0xbb, 0x77, 0xff, 0x55, 0x88, 0x33, 0x11, 0x44, 0x99, 0x22, 0xcc, 0xdd, 0xaa, 0xee,
            0x22, 0x00, 0x33, 0xbb, 0xcc, 0x88, 0x44, 0xdd, 0x77, 0x55, 0xaa, 0x11, 0x66, 0xff, 0xee, 0x99,
            0xcc, 0xff, 0x00, 0x44, 0xbb, 0x66, 0xaa, 0x11, 0x99, 0x55, 0xee, 0x33, 0x22, 0x77, 0x88, 0xdd,
            0x00, 0x44, 0x88, 0xcc, 0x11, 0x55, 0x99, 0xdd, 0x22, 0x66, 0xaa, 0xee, 0x33, 0x77, 0xbb, 0xff,
            0x66, 0xcc, 0x33, 0x55, 0x88, 0xee, 0x77, 0x00, 0xdd, 0x22, 0x99, 0x11, 0xff, 0xbb, 0x44, 0xaa,
            0xff, 0xcc, 0x66, 0xaa, 0x99, 0x55, 0x22, 0x00, 0x77, 0x11, 0x88, 0xbb, 0xdd, 0x33, 0xee, 0x44,
            0xaa, 0x33, 0xdd, 0xcc, 0x66, 0xee, 0x11, 0x44, 0xbb, 0x55, 0x77, 0xff, 0x22, 0x00, 0x88, 0x99,
            0xaa, 0x55, 0x33, 0x11, 0xbb, 0xdd, 0x66, 0xcc, 0x22, 0xff, 0x44, 0x88, 0xee, 0x77, 0x99, 0x00,
            0x00, 0x66, 0xbb, 0x77, 0xff, 0x55, 0x88, 0x33, 0x11, 0x44, 0x99, 0x22, 0xcc, 0xdd, 0xaa, 0xee,
            0x22, 0x00, 0x33, 0xbb, 0xcc, 0x88, 0x44, 0xdd, 0x77, 0x55, 0xaa, 0x11, 0x66, 0xff, 0xee, 0x99,
            0xcc, 0xff, 0x00, 0x44, 0xbb, 0x66, 0xaa, 0x11, 0x99, 0x55, 0xee, 0x33, 0x22, 0x77, 0x88, 0xdd,
        };
        const uint8_t ExpectedPassword[16] = {
            0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff
        };
        uint8_t Password[16];
        slot2password(&RawBytes[7 * 16], Password);
        Worked = Worked && memcmp(Password, ExpectedPassword, 16) == 0;
        printf("states2password: %s\n", Worked ? ":)" : ":(");
        if (!Worked) {
            printf("Resulting password:\n");
            hexdump(stdout, Password, 16);
            printf("Expected password:\n");
            hexdump(stdout, ExpectedPassword, 16);
        }
    }
    {
        Slot_t Output, Input;
        const uint8_t Bytes[16] = {
            0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF
        };
        memcpy(Output.m128i_u8, Bytes, 16);
        round(0, &Output);
        reverse_0(Output, Input);
        Worked = Worked && memcmp(Bytes, Input.m128i_u8, 16) == 0;
        printf("reverse_0: %s\n", Worked ? ":)" : ":(");
        if (!Worked) {
            printf("Result:\n");
            hexdump(stdout, Input.m128i_u8, 16);
            printf("Expected result:\n");
            hexdump(stdout, Bytes, 16);
        }
    }
    {
        Slot_t Output, Input;
        const uint8_t Bytes[16] = {
            0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF
        };
        memcpy(Output.m128i_u8, Bytes, 16);
        round(35, &Output);
        reverse_35(Output, Input);
        Worked = Worked && memcmp(Bytes, Input.m128i_u8, 16) == 0;
        printf("reverse_35: %s\n", Worked ? ":)" : ":(");
        if (!Worked) {
            printf("Result:\n");
            hexdump(stdout, Input.m128i_u8, 16);
            printf("Expected result:\n");
            hexdump(stdout, Bytes, 16);
        }
    }
    {
        Slot_t Output, Input;
        const uint8_t Bytes[16] = {
            0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF
        };
        memcpy(Output.m128i_u8, Bytes, 16);
        round(37, &Output);
        reverse_37(37, Output, Input);
        Worked = Worked && memcmp(Bytes, Input.m128i_u8, 16) == 0;
        printf("reverse_37: %s\n", Worked ? ":)" : ":(");
        if (!Worked) {
            printf("Result:\n");
            hexdump(stdout, Input.m128i_u8, 16);
            printf("Expected result:\n");
            hexdump(stdout, Bytes, 16);
        }
    }
    {
        Slot_t Output, Input;
        const uint8_t Bytes[16] = {
            0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF
        };
        memcpy(Output.m128i_u8, Bytes, 16);
        round(38, &Output);
        reverse_38(Output, Input);
        Worked = Worked && memcmp(Bytes, Input.m128i_u8, 16) == 0;
        printf("reverse_38: %s\n", Worked ? ":)" : ":(");
        if (!Worked) {
            printf("Result:\n");
            hexdump(stdout, Input.m128i_u8, 16);
            printf("Expected result:\n");
            hexdump(stdout, Bytes, 16);
        }
    }
    {
        Slot_t Output, Input;
        const uint8_t Bytes[16] = {
            0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF
        };
        memcpy(Output.m128i_u8, Bytes, 16);
        round(39, &Output);
        reverse_39(Output, Input);
        Worked = Worked && memcmp(Bytes, Input.m128i_u8, 16) == 0;
        printf("reverse_39: %s\n", Worked ? ":)" : ":(");
        if (!Worked) {
            printf("Result:\n");
            hexdump(stdout, Input.m128i_u8, 16);
            printf("Expected result:\n");
            hexdump(stdout, Bytes, 16);
        }
    }
    {
        // pie breakpoint *0x114c
        // raw for 00112233445566778899AABBCCDDEEFF
        // x/256bx &states
        const uint8_t RawBytes[15 * sizeof(Slot_t)]{
            0x66, 0xcc, 0x33, 0x55, 0x88, 0xee, 0x77, 0x00,
            0xdd, 0x22, 0x99, 0x11, 0xff, 0xbb, 0x44, 0xaa,
            0xff, 0xcc, 0x66, 0xaa, 0x99, 0x55, 0x22, 0x00,
            0x77, 0x11, 0x88, 0xbb, 0xdd, 0x33, 0xee, 0x44,
            0xaa, 0x33, 0xdd, 0xcc, 0x66, 0xee, 0x11, 0x44,
            0xbb, 0x55, 0x77, 0xff, 0x22, 0x00, 0x88, 0x99,
            0xaa, 0x55, 0x33, 0x11, 0xbb, 0xdd, 0x66, 0xcc,
            0x22, 0xff, 0x44, 0x88, 0xee, 0x77, 0x99, 0x00,
            0x00, 0x66, 0xbb, 0x77, 0xff, 0x55, 0x88, 0x33,
            0x11, 0x44, 0x99, 0x22, 0xcc, 0xdd, 0xaa, 0xee,
            0x22, 0x00, 0x33, 0xbb, 0xcc, 0x88, 0x44, 0xdd,
            0x77, 0x55, 0xaa, 0x11, 0x66, 0xff, 0xee, 0x99,
            0xcc, 0xff, 0x00, 0x44, 0xbb, 0x66, 0xaa, 0x11,
            0x99, 0x55, 0xee, 0x33, 0x22, 0x77, 0x88, 0xdd,
            0x00, 0x44, 0x88, 0xcc, 0x11, 0x55, 0x99, 0xdd,
            0x22, 0x66, 0xaa, 0xee, 0x33, 0x77, 0xbb, 0xff,
            0x66, 0xcc, 0x33, 0x55, 0x88, 0xee, 0x77, 0x00,
            0xdd, 0x22, 0x99, 0x11, 0xff, 0xbb, 0x44, 0xaa,
            0xff, 0xcc, 0x66, 0xaa, 0x99, 0x55, 0x22, 0x00,
            0x77, 0x11, 0x88, 0xbb, 0xdd, 0x33, 0xee, 0x44,
            0xaa, 0x33, 0xdd, 0xcc, 0x66, 0xee, 0x11, 0x44,
            0xbb, 0x55, 0x77, 0xff, 0x22, 0x00, 0x88, 0x99,
            0xaa, 0x55, 0x33, 0x11, 0xbb, 0xdd, 0x66, 0xcc,
            0x22, 0xff, 0x44, 0x88, 0xee, 0x77, 0x99, 0x00,
            0x00, 0x66, 0xbb, 0x77, 0xff, 0x55, 0x88, 0x33,
            0x11, 0x44, 0x99, 0x22, 0xcc, 0xdd, 0xaa, 0xee,
            0x22, 0x00, 0x33, 0xbb, 0xcc, 0x88, 0x44, 0xdd,
            0x77, 0x55, 0xaa, 0x11, 0x66, 0xff, 0xee, 0x99,
            0xcc, 0xff, 0x00, 0x44, 0xbb, 0x66, 0xaa, 0x11,
            0x99, 0x55, 0xee, 0x33, 0x22, 0x77, 0x88, 0xdd,
        };

        // For 00112233445566778899AABBCCDDEEFF
        // pie breakpoint *0x11c9
        // p $xmm0
        const uint8_t ExpectedCipher[16]{
            0x17, 0x81, 0x31, 0x40, 0xa6, 0xde, 0xc4, 0x6d, 0xdb, 0xa1, 0x8, 0x53, 0x69, 0x8c, 0x1c, 0x88
        };

        Slot_t States[15];
        memcpy(States, RawBytes, 16 * 15);
        encrypt(States);
        hexdump(stdout, States, 240);
        __m128i Cipher;
        memset(Cipher.m128i_u8, 0, 16);
        for (size_t i = 0; i < 15; ++i) {
            Cipher = _mm_xor_si128(Cipher, States[i]);
        }

        Worked = Worked && memcmp(Cipher.m128i_u8, ExpectedCipher, 16) == 0;
        printf("unrolled_encrypt: %s\n", Worked ? ":)" : ":(");
        if (!Worked) {
            printf("Resulting cipher:\n");
            hexdump(stdout, Cipher.m128i_u8, 16);
            printf("Expected cipher:\n");
            hexdump(stdout, ExpectedCipher, 16);
        }
    }
    {
        Slot_t Output, Input;
        const uint8_t Bytes[16] = {
            0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF
        };
        memcpy(Output.m128i_u8, Bytes, 16);
        for (uint32_t i = 0; i < 10; ++i) {
            Slot_t Cpy;
            memcpy(Cpy.m128i_u8, Output.m128i_u8, 16);
            round(i, &Output);
            unround(i, Output, Input);
            printf(".");
            Worked = Worked && memcmp(Cpy.m128i_u8, Input.m128i_u8, 16) == 0;
            if (!Worked) {
                printf("Result:\n");
                hexdump(stdout, Input.m128i_u8, 16);
                printf("Expected result:\n");
                hexdump(stdout, Bytes, 16);
                break;
            }
        }
        printf("\nunround: %s\n", Worked ? ":)" : ":(");
    }
    return Worked;
}

int main(int argc, char *argv[]) {
    init_globals();
    if (argc > 1) {
        if (!tests()) {
            return EXIT_FAILURE;
        }
        return EXIT_SUCCESS;
    }

    uint64_t t0 = GetTickCount64();
    pwn();
    uint64_t t1 = GetTickCount64();
    uint64_t ms = t1 - t0;
    printf("%llx min elapsed\n", (ms / 1000) / 60);
    return 0;
}