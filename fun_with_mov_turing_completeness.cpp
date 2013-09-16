/*
    fun_with_mov_turing_completeness.c - Just having fun with ideas taken from that paper:
    http://www.cl.cam.ac.uk/~sd601/papers/mov.pdf
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
    
    If you are interested in about the turing completeness, you may want
    to read a relevant discusion on reddit with rolfr & PaxTeam here:
     -> http://www.reddit.com/r/ReverseEngineering/comments/1lfm21/mov_is_turingcomplete_by_stephen_dolan_pdf/

    I'm quite sure if Walter Bishop was a computer science guy, he would have loved to play
    with that crazy machine.

    So, Walter, please accept this gift.

    ______________ ______________                                     
    \__    ___/   |   \_   _____/                                     
      |    | /    ~    \    __)_                                      
      |    | \    Y    /        \                                     
      |____|  \___|_  /_______  /                                     
                    \/        \/                                      
    __________.___  _________ ___ ___ ________ __________             
    \______   \   |/   _____//   |   \\_____  \\______   \            
     |    |  _/   |\_____  \/    ~    \/   |   \|     ___/            
     |    |   \   |/        \    Y    /    |    \    |                
     |______  /___/_______  /\___|_  /\_______  /____|                
            \/            \/       \/         \/                      
       _____      _____  _________   ___ ___ .___ _______  ___________
      /     \    /  _  \ \_   ___ \ /   |   \|   |\      \ \_   _____/
     /  \ /  \  /  /_\  \/    \  \//    ~    \   |/   |   \ |    __)_ 
    /    Y    \/    |    \     \___\    Y    /   /    |    \|        \
    \____|__  /\____|__  /\______  /\___|_  /|___\____|__  /_______  /
            \/         \/        \/       \/             \/        \/

    Special thanks to Stephen Dolan for the discussions by emails.

    Example output for the lazy ones:
        D:\Codes\fun_with_mov_turing_completeness\Release>fun_with_mov_turing_completeness.exe
        OK, mem allocated @ 00935FE8
        S0=0x00935fe8, S1=0x00935fec
        OK, here's the initial tape (0087F704)
        0 1 1 1 0 1 1 0
        N=0x00935ff0, @S=0x0087f700, @L=0x0087f6f8, @R=0x0087f6f4
        Q0=0x0087f6cc, Q0_=0x0087f668, Q0__=0x0087f58c
        Q1=0x0087f694, Q1_=0x0087f65c, Q1__=0x0087f57c
        Q2=0x0087f68c, Q2_=0x0087f650, Q2__=0x0087f56c
        Q3=0x0087f644, Q3_=0x0087f55c
        Q4=0x0087f6d4, Q4_=0x0087f684, Q4__=0x0087f54c
        c1=0x0087f6ac, c2=0x0087f6bc, c3=0x0087f69c, c4=0x0087f6e4
        c5=0x0087f6dc, c6=0x0087f6b4, c7=0x0087f6a4, c8=0x0087f6c4
        c9=0x0087f52c
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 [1] 1 1 0 1 1 0
        [0x00935ff0] [0x0087f6ac] [0x0087f6e4] [0x0087f6dc] [0x0087f6b4] [0x0087f6a4] [0x0087f6c4] [0x0087f52c]
        S=0x0087f6bc, L=0x0087f6ac, R=0x0087f69c, T=0x0087f668
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 1 [1] 1 0 1 1 0
        [0x00935ff0] [0x0087f6ac] [0x0087f6e4] [0x0087f6dc] [0x0087f6b4] [0x0087f6a4] [0x0087f6c4] [0x0087f52c]
        S=0x0087f69c, L=0x0087f6bc, R=0x0087f6e4, T=0x0087f694
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 1 1 [1] 0 1 1 0
        [0x00935ff0] [0x0087f6ac] [0x0087f6bc] [0x0087f6dc] [0x0087f6b4] [0x0087f6a4] [0x0087f6c4] [0x0087f52c]
        S=0x0087f6e4, L=0x0087f69c, R=0x0087f6dc, T=0x0087f694
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 1 1 1 [0] 1 1 0
        [0x00935ff0] [0x0087f6ac] [0x0087f6bc] [0x0087f69c] [0x0087f6b4] [0x0087f6a4] [0x0087f6c4] [0x0087f52c]
        S=0x0087f6dc, L=0x0087f6e4, R=0x0087f6b4, T=0x0087f694
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 1 1 1 [0] 1 1 0
        [0x00935ff0] [0x0087f6ac] [0x0087f6bc] [0x0087f69c] [0x0087f6e4] [0x0087f6a4] [0x0087f6c4] [0x0087f52c]
        S=0x0087f6dc, L=0x0087f6e4, R=0x0087f6b4, T=0x0087f65c
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 1 1 1 1 [1] 1 0
        [0x00935ff0] [0x0087f6ac] [0x0087f6bc] [0x0087f69c] [0x0087f6e4] [0x0087f6a4] [0x0087f6c4] [0x0087f52c]
        S=0x0087f6b4, L=0x0087f6dc, R=0x0087f6a4, T=0x0087f68c
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 1 1 1 1 1 [1] 0
        [0x00935ff0] [0x0087f6ac] [0x0087f6bc] [0x0087f69c] [0x0087f6e4] [0x0087f6dc] [0x0087f6c4] [0x0087f52c]
        S=0x0087f6a4, L=0x0087f6b4, R=0x0087f6c4, T=0x0087f68c
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 1 1 1 1 1 1 [0]
        [0x00935ff0] [0x0087f6ac] [0x0087f6bc] [0x0087f69c] [0x0087f6e4] [0x0087f6dc] [0x0087f6b4] [0x0087f52c]
        S=0x0087f6c4, L=0x0087f6a4, R=0x0087f52c, T=0x0087f68c
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 1 1 1 1 1 1 [0]
        [0x00935ff0] [0x0087f6ac] [0x0087f6bc] [0x0087f69c] [0x0087f6e4] [0x0087f6dc] [0x0087f6b4] [0x0087f6a4]
        S=0x0087f6c4, L=0x0087f6a4, R=0x0087f52c, T=0x0087f650
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 1 1 1 1 1 [1] 0
        [0x00935ff0] [0x0087f6ac] [0x0087f6bc] [0x0087f69c] [0x0087f6e4] [0x0087f6dc] [0x0087f6b4] [0x0087f52c]
        S=0x0087f6a4, L=0x0087f6b4, R=0x0087f6c4, T=0x0087f644
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 1 1 1 1 [1] 0 0
        [0x00935ff0] [0x0087f6ac] [0x0087f6bc] [0x0087f69c] [0x0087f6e4] [0x0087f6dc] [0x0087f6c4] [0x0087f52c]
        S=0x0087f6b4, L=0x0087f6dc, R=0x0087f6a4, T=0x0087f6d4
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 1 1 1 [1] 1 0 0
        [0x00935ff0] [0x0087f6ac] [0x0087f6bc] [0x0087f69c] [0x0087f6e4] [0x0087f6a4] [0x0087f6c4] [0x0087f52c]
        S=0x0087f6dc, L=0x0087f6e4, R=0x0087f6b4, T=0x0087f6d4
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 1 1 [1] 1 1 0 0
        [0x00935ff0] [0x0087f6ac] [0x0087f6bc] [0x0087f69c] [0x0087f6b4] [0x0087f6a4] [0x0087f6c4] [0x0087f52c]
        S=0x0087f6e4, L=0x0087f69c, R=0x0087f6dc, T=0x0087f6d4
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 1 [1] 1 1 1 0 0
        [0x00935ff0] [0x0087f6ac] [0x0087f6bc] [0x0087f6dc] [0x0087f6b4] [0x0087f6a4] [0x0087f6c4] [0x0087f52c]
        S=0x0087f69c, L=0x0087f6bc, R=0x0087f6e4, T=0x0087f6d4
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        0 [1] 1 1 1 1 0 0
        [0x00935ff0] [0x0087f6ac] [0x0087f6e4] [0x0087f6dc] [0x0087f6b4] [0x0087f6a4] [0x0087f6c4] [0x0087f52c]
        S=0x0087f6bc, L=0x0087f6ac, R=0x0087f69c, T=0x0087f6d4
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        [0] 1 1 1 1 1 0 0
        [0x00935ff0] [0x0087f69c] [0x0087f6e4] [0x0087f6dc] [0x0087f6b4] [0x0087f6a4] [0x0087f6c4] [0x0087f52c]
        S=0x0087f6ac, L=0x00935ff0, R=0x0087f6bc, T=0x0087f6d4
        ------------------------------------
        -----------DEBUG--------------------
        OK, done, inspecting the tape now..
        [0] 1 1 1 1 1 0 0
        [0x0087f6bc] [0x0087f69c] [0x0087f6e4] [0x0087f6dc] [0x0087f6b4] [0x0087f6a4] [0x0087f6c4] [0x0087f52c]
        S=0x0087f6ac, L=0x00935ff0, R=0x0087f6bc, T=0x0087f684
        ------------------------------------
        OK, machine done, inspecting the tape now..
        0 [1] 1 1 1 1 0 0
*/
#include <stdio.h>
#include <windows.h>

void turing_machine_simple()
{
    // This is a simple way to add two number via a turing machine
    // Comes from http://turingmaschine.klickagent.ch/einband/?&lang=en#2_+_3
    // Each transition is written this way: (TriggeringSymbol, NewSymbol, Direction)

    // +--+(0,0,R)   +--+(1,1,R)
    // |  |          |  |
    // |  v          |  v
    // +--+   (1,1,R)+--+   (0,1,R)
    // |00+--------->|01|---------+
    // +--+          +--+         |
    //                            |
    //                            v
    // +--+ (1,1,L)              +--+-------+
    // |  |                      |02|       |(1,1,R)
    // |  |                      +--+<------+
    // |  v                        |
    // +--+  (1,0,L) +--+   (0,0,L)|
    // |04|<---------+03|<---------+
    // ++-+          +--+
    //  |
    //  |(0,0,R)
    //  v
    // +--+
    // |05|
    // +--+

    ///// SETUP THE MACHINE
    unsigned int *mem = (unsigned int*)malloc(3 * sizeof(unsigned int));
    printf("OK, mem allocated @ %p\n", mem);

    unsigned int S0 = (unsigned int)mem;
    unsigned int S1 = (unsigned int)(mem + 1);
    unsigned int N = (unsigned int)(mem + 2);

    unsigned int DirR = 1, DirL = 0;

    printf("S0=%#.8x, S1=%#.8x\n", S0, S1);

    //// Building the transition table now
    unsigned int Q0[2], Q0_[2], Q0__[2];
    unsigned int Q1[2], Q1_[2], Q1__[2];
    unsigned int Q2[2], Q2_[2], Q2__[2];
    unsigned int Q3[2], Q3_[2];
    unsigned int Q4[2], Q4_[2], Q4__[2];

    /// Q0
    // This one represent the transition (0, 0, R) from Q0
    // Q0[0] -> 0 -> 0 -> 1 -> Q0
    unsigned int Q0_first_trans[2];
    Q0[0] = (unsigned int)Q0_first_trans;
    Q0_first_trans[0] = S0;
    unsigned int Q0_first_trans_[2];
    Q0_first_trans[1] = (unsigned int)Q0_first_trans_;
    Q0_first_trans_[0] = S0;
    unsigned int Q0_first_trans__[2];
    Q0_first_trans_[1] = (unsigned int)Q0_first_trans__;
    Q0_first_trans__[0] = DirR;
    unsigned int Q0_first_trans___;
    Q0_first_trans__[1] = (unsigned int)&Q0_first_trans___;
    Q0_first_trans___ = (unsigned int)Q0;
    // This one represent the transition (1, 1, R) from Q0
    // Q0[1] -> 1 -> 1 -> 1 -> Q1
    unsigned int Q0_second_trans[2];
    Q0[1] = (unsigned int)Q0_;
    Q0_[0] = (unsigned int)Q0_second_trans; 
    Q0_second_trans[0] = S1;
    unsigned int Q0_second_trans_[2];
    Q0_second_trans[1] = (unsigned int)Q0_second_trans_;
    Q0_second_trans_[0] = S1;
    unsigned int Q0_second_trans__[2];
    Q0_second_trans_[1] = (unsigned int)Q0_second_trans__;
    Q0_second_trans__[0] = DirR;
    unsigned int Q0_second_trans___;
    Q0_second_trans__[1] = (unsigned int)&Q0_second_trans___;
    Q0_second_trans___ = (unsigned int)Q1;
    // end
    Q0_[1] = (unsigned int)Q0__;
    Q0__[0] = N;

    /// Q1
    // This one represent the transition (1, 1, R) from Q1
    // Q1[0] -> 1 -> 1 -> R -> Q1
    unsigned int Q1_first_trans[2];
    Q1[0] = (unsigned int)Q1_first_trans;
    Q1_first_trans[0] = S1;
    unsigned int Q1_first_trans_[2];
    Q1_first_trans[1] = (unsigned int)Q1_first_trans_;
    Q1_first_trans_[0] = S1;
    unsigned int Q1_first_trans__[2];
    Q1_first_trans_[1] = (unsigned int)Q1_first_trans__;
    Q1_first_trans__[0] = DirR;
    unsigned int Q1_first_trans___;
    Q1_first_trans__[1] = (unsigned int)&Q1_first_trans___;
    Q1_first_trans___ = (unsigned int)Q1;
    // This one represent the transition (0, 1, R) from Q1
    // Q1[1] -> 0 -> 1 -> 1 -> Q2
    unsigned int Q1_second_trans[2];
    Q1[1] = (unsigned int)Q1_;
    Q1_[0] = (unsigned int)Q1_second_trans;
    Q1_second_trans[0] = S0;
    unsigned int Q1_second_trans_[2];
    Q1_second_trans[1] = (unsigned int)Q1_second_trans_;
    Q1_second_trans_[0] = S1;
    unsigned int Q1_second_trans__[2];
    Q1_second_trans_[1] = (unsigned int)Q1_second_trans__;
    Q1_second_trans__[0] = DirR;
    unsigned int Q1_second_trans___;
    Q1_second_trans__[1] = (unsigned int)&Q1_second_trans___;
    Q1_second_trans___ = (unsigned int)Q2;
    // end
    Q1_[1] = (unsigned int)Q1__;
    Q1__[0] = N;

    /// Q2
    // This one represent the transition (1, 1, R) from Q2
    // Q2[0] -> 1 -> 1 -> R -> Q2
    unsigned int Q2_first_trans[2];
    Q2[0] = (unsigned int)Q2_first_trans;
    Q2_first_trans[0] = S1;
    unsigned int Q2_first_trans_[2];
    Q2_first_trans[1] = (unsigned int)Q2_first_trans_;
    Q2_first_trans_[0] = S1;
    unsigned int Q2_first_trans__[2];
    Q2_first_trans_[1] = (unsigned int)Q2_first_trans__;
    Q2_first_trans__[0] = DirR;
    unsigned int Q2_first_trans___;
    Q2_first_trans__[1] = (unsigned int)&Q2_first_trans___;
    Q2_first_trans___ = (unsigned int)Q2;
    // This one represent the transition (0, 0, L) from Q2
    // Q2[1] -> 0 -> 0 -> L -> Q3
    unsigned int Q2_second_trans[2];
    Q2[1] = (unsigned int)Q2_;
    Q2_[0] = (unsigned int)Q2_second_trans;
    Q2_second_trans[0] = S0;
    unsigned int Q2_second_trans_[2];
    Q2_second_trans[1] = (unsigned int)Q2_second_trans_;
    Q2_second_trans_[0] = S0;
    unsigned int Q2_second_trans__[2];
    Q2_second_trans_[1] = (unsigned int)Q2_second_trans__;
    Q2_second_trans__[0] = DirL;
    unsigned int Q2_second_trans___;
    Q2_second_trans__[1] = (unsigned int)&Q2_second_trans___;
    Q2_second_trans___ = (unsigned int)Q3;
    // end
    Q2_[1] = (unsigned int)Q2__;
    Q2__[0] = N;

    /// Q3
    // This one represent the transition (1, 0, L) from Q3
    // Q3[0] -> 1 -> 0 -> L -> Q4
    unsigned int Q3_first_trans[2];
    Q3[0] = (unsigned int)Q3_first_trans;
    Q3_first_trans[0] = S1;
    unsigned int Q3_first_trans_[2];
    Q3_first_trans[1] = (unsigned int)Q3_first_trans_;
    Q3_first_trans_[0] = S0;
    unsigned int Q3_first_trans__[2];
    Q3_first_trans_[1] = (unsigned int)Q3_first_trans__;
    Q3_first_trans__[0] = DirL;
    unsigned int Q3_first_trans___;
    Q3_first_trans__[1] = (unsigned int)&Q3_first_trans___;
    Q3_first_trans___ = (unsigned int)Q4;
    // end
    Q3[1] = (unsigned int)Q3_;
    Q3_[0] = N;

    /// Q4
    // This one represent the transition (1, 1, R) from Q4
    // Q4[0] -> 1 -> 1 -> L -> Q4
    unsigned int Q4_first_trans[2];
    Q4[0] = (unsigned int)Q4_first_trans;
    Q4_first_trans[0] = S1;
    unsigned int Q4_first_trans_[2];
    Q4_first_trans[1] = (unsigned int)Q4_first_trans_;
    Q4_first_trans_[0] = S1;
    unsigned int Q4_first_trans__[2];
    Q4_first_trans_[1] = (unsigned int)Q4_first_trans__;
    Q4_first_trans__[0] = DirL;
    unsigned int Q4_first_trans___;
    Q4_first_trans__[1] = (unsigned int)&Q4_first_trans___;
    Q4_first_trans___ = (unsigned int)Q4;
    // This one represent the transition (0, 0, R) from Q4
    // Q4[1] -> 0 -> 0 -> R -> N
    unsigned int Q4_second_trans[2];
    Q4[1] = (unsigned int)Q4_;
    Q4_[0] = (unsigned int)Q4_second_trans;
    Q4_second_trans[0] = S0;
    unsigned int Q4_second_trans_[2];
    Q4_second_trans[1] = (unsigned int)Q4_second_trans_;
    Q4_second_trans_[0] = S0;
    unsigned int Q4_second_trans__[2];
    Q4_second_trans_[1] = (unsigned int)Q4_second_trans__;
    Q4_second_trans__[0] = DirR;
    unsigned int Q4_second_trans___;
    Q4_second_trans__[1] = (unsigned int)&Q4_second_trans___;
    Q4_second_trans___ = N;
    // end
    Q4_[1] = (unsigned int)Q4__;
    Q4__[0] = N;

    // Now we have to build the tape -- it's supposed to be infinite, but no for our simple PoC
    unsigned int cell1[2], cell2[2], cell3[2], cell4[2], cell5[2], cell6[2], cell7[2], cell8[2], cell9[2];
    unsigned int tape[8] = {
        (unsigned int)cell1, (unsigned int)cell2,
        (unsigned int)cell3, (unsigned int)cell4,
        (unsigned int)cell5, (unsigned int)cell6,
        (unsigned int)cell7, (unsigned int)cell8
    };

    // At the begining we have
    // S = cell2
    // L = cell1
    // R = cell3 (cell3->cell4->cell5->cell6->cell7->cell8)
    // 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0
    // 3 + 2
    //
    // At the end the tape should look:
    // .. | 1 | 1 | 1 | 1 | 1 | 0

    // L
    cell1[0] = S0;
    cell1[1] = N;
    // S
    cell2[0] = S1;
    cell2[1] = 0xdeadbeef;
    // R
    cell3[0] = S1;
    cell3[1] = (unsigned int)cell4;
    cell4[0] = S1;
    cell4[1] = (unsigned int)cell5;
    cell5[0] = S0;
    cell5[1] = (unsigned int)cell6;
    cell6[0] = S1;
    cell6[1] = (unsigned int)cell7;
    cell7[0] = S1;
    cell7[1] = (unsigned int)cell8;
    cell8[0] = S0;
    cell8[1] = (unsigned int)cell9;

    printf("OK, here's the initial tape (%p)\n", tape);
    for(unsigned int i = 0; i < sizeof(tape) / sizeof(tape[0]); ++i)
        printf("%d ", ((((unsigned int*)tape[i])[0] & 4) == 0 ? 0 : 1));
    printf("\n");

    // We use a register T to hold the current transition to be tested, and a
    // register S to hold a cell containing the current symbol.
    unsigned int T, S;

    // The register L holds the list representing the part of the tape to the left of the
    // current position, and the register R holds the list representing the part to the right.
    unsigned int R, L;

    printf("N=%#.8x, @S=%#.8x, @L=%#.8x, @R=%#.8x\n", N, &S, &L, &R);
    printf("Q0=%#.8x, Q0_=%#.8x, Q0__=%#.8x\n", Q0, Q0_, Q0__);
    printf("Q1=%#.8x, Q1_=%#.8x, Q1__=%#.8x\n", Q1, Q1_, Q1__);
    printf("Q2=%#.8x, Q2_=%#.8x, Q2__=%#.8x\n", Q2, Q2_, Q2__);
    printf("Q3=%#.8x, Q3_=%#.8x\n", Q3, Q3_);
    printf("Q4=%#.8x, Q4_=%#.8x, Q4__=%#.8x\n", Q4, Q4_, Q4__);
    printf("c1=%#.8x, c2=%#.8x, c3=%#.8x, c4=%#.8x\n", cell1, cell2, cell3, cell4);
    printf("c5=%#.8x, c6=%#.8x, c7=%#.8x, c8=%#.8x\n", cell5, cell6, cell7, cell8);
    printf("c9=%#.8x\n", cell9);

    // At program startup, T holds the address Q0
    // Q0 is the program startup state
    T = (unsigned int)Q0;
    // S holds the address T1
    S = (unsigned int)cell2;
    // The register L holds the address N, and R holds the address T2
    L = (unsigned int)cell1;
    R = (unsigned int)cell3;
    ///// LAUNCH THE MACHINE
    __try
    {
        here_we_go:
        __asm
        {
            pushad

            ; First, we check whether the current transition should ﬁre, by
            ; comparing S and the symbol on the current transition T.
            mov eax, T
            mov eax, [eax]   ;; get transition
            mov eax, [eax]   ;; get trigger symbol, eax got a real symbol now
            mov ebx, S
            mov ebx, [ebx]   ;; get current symbol, ebx got the current symbol
            mov dword ptr [ebx], 0     ;; we write @ ebx 0
            mov dword ptr [eax], 1     ;; we write @ eax 1
            mov ecx, [ebx]   ;; ecx is 1 if the transition matches, and 0 otherwise.


            ; After this sequence, the register M (ecx) is 1 if the transition matches,
            ; and 0 otherwise. Next, we update S: if the transition matches, we
            ; use the transition’s new symbol, otherwise we leave it unchanged
            mov eax, T
            mov eax, [eax]         ;; get transition
            mov eax, [eax + 4]     ;; skip trigger symbol
            mov eax, [eax]         ;; get new symbol
            mov ebx, S
            mov ebx, [ebx]         ;; get current symbol
            ; another trick to select between eax & ebx based on the previous comparaison
            mov edx, N
            mov [edx], ebx
            mov [edx + 4], eax
            ; we will load in edx, either ebx (current symbol) if ecx = 0 (current symbol != triggering symbol), or
            ; eax (new symbol) if ecx = 1 (current symbol == triggering symbol)
            mov edx, [edx + ecx * 4]
            mov ebx, S
            mov [ebx], edx ;; write the new symbol


            ; This updates S if the transition matches. Next, if the transition
            ; matches, we need to advance the tape in the appropriate direction.
            ; We do this in two stages. First, we push the cell S to one of the
            ; tape stacks, and then we pop a new S from the other tape stack.
            ; If the transition does not match, we push and pop S from the same
            ; tape stack, which has no effect. To determine whether the transition
            ; moves left or right, we use the following sequence:
            mov eax, T
            mov eax, [eax]         ;; get transition
            mov eax, [eax + 4]     ;; skip the trigger symbol
            mov eax, [eax + 4]     ;; skip the new symbol
            mov eax, [eax]         ;; load direction


            ; After this, the register D holds the direction of tape movement:
            ; 0 for left, and 1 for right. If we are to move left, then the cell S
            ; must be added to the tape stack R, and vice versa. Adding the cell
            ; to a tape stack is done by ﬁrst writing the tape stack’s current top
            ; to [S+1], and then modifying the tape stack register to point at S.
            mov ebx, N             ;; select new value for [S+1]
            mov edx, R
            mov [ebx], edx
            mov edx, L
            mov [ebx + 4], edx
            mov edi, [ebx + eax * 4]
            mov edx, S
            mov [edx + 4], edi
            mov edx, L
            mov [ebx], edx         ;; select new value for L
            mov edx, S
            mov [ebx + 4], edx
            mov edx, [ebx + eax * 4]
            mov L, edx
            mov edx, S
            mov [ebx], edx         ;; select new value for R
            mov edx, R
            mov [ebx + 4], edx
            mov edx, [ebx + eax * 4]
            mov R, edx


            ; We must ensure that no movement of the tape happens if the
            ; transition does not match (that is, if M = 0). To this end, we ﬂip the
            ; value of D if the transition does not match, so that we pop the cell
            ; we just pushed.
            mov ebx, N
            mov dword ptr [ebx], 1            ;; set X = not D
            mov dword ptr [ebx + 4], 0
            mov edi, [ebx + eax * 4]
            mov [ebx], edi          ;; select between D and X
            mov [ebx + 4], eax
            mov eax, [ebx + ecx * 4]


            ; Next, we pop a cell from a direction indicated by D: if D = 0,
            ; we pop a cell from L, and if D = 1 we pop one from R.
            mov ebx, N
            mov edi, L
            mov [ebx], edi          ;; select new value of S
            mov edi, R
            mov [ebx + 4], edi
            mov edx, [ebx + eax * 4]
            mov S, edx
            mov edx, [edx + 4]      ;; get new start of L or R
            mov [ebx], edx          ;; select new value of L
            ; WARNING: I believe this is a typo in the reference paper ; instead of 'mov edi, R', it is 'mov edi, L' (confirmed with the author)
            mov edi, L
            mov [ebx + 4], edi
            mov edi, [ebx + eax * 4]
            mov L, edi
            mov edi, R
            mov [ebx], edi          ;; select new value for R
            mov [ebx + 4], edx
            mov edi, [ebx + eax * 4]
            mov R, edi


            ; So, if the current transition matches, this code writes a symbol to
            ; the tape and advances in the appropriate direction. If the transition
            ; doesn’t match, this code has no effect.
            ; All that remains is to ﬁnd the next transition to consider. If the
            ; current transition matches, then we should look at the next state’s
            ; list of transitions. Otherwise, we continue to the next transition in
            ; the current state.
            mov eax, T
            mov eax, [eax + 4] ;; get next transition of this state
            mov ebx, T
            mov ebx, [ebx]     ;; get current transition
            mov ebx, [ebx + 4] ;; skip trigger symbol
            mov ebx, [ebx + 4] ;; skip new symbol
            mov ebx, [ebx + 4] ;; skip direction
            mov ebx, [ebx]     ;; load transition list of the next state
            mov edx, N
            mov [edx], eax
            mov [edx + 4], ebx
            mov edi, [edx + ecx * 4]
            mov T, edi


            ; This ﬁnds the next transition our Turing machine should consider.
            ; If T has the value N, then this means there are no more transitions to consider:
            ;     either we got to the end of a state’s list of transitions with no matches,
            ;     or we just transitioned to a state that has no outgoing transitions.
            ; Either way, the machine should halt in this case.
            ; First, we check whether this is the case by setting the register H to 1 if T is N
            mov eax, T
            mov eax, [eax]
            mov ebx, N
            mov dword ptr [ebx], 0
            mov ecx, T
            mov dword ptr [ecx], 1
            mov edi, [ebx]
            mov [ecx], eax


            ; If H is 1, we must halt the machine. We do so by reading from
            ; the invalid memory address 0:
            ; WARNING: there is an error in the paper ; the code and the comments
            ; are doing exactly the contrary. (got a confirmation from the author)
            ; That is why I did:
            ;     mov dword ptr [edx], edx
            ;     mov dword ptr [edx + 4], 0
            ; Instead of (as stated in the paper):
            ;     mov dword ptr [edx], 0
            ;     mov dword ptr [edx + 4], edx
            mov edx, N
            mov dword ptr [edx], edx
            mov dword ptr [edx + 4], 0
            mov eax, [edx + edi * 4]
            mov eax, [eax]

            popad
        }

        printf("-----------DEBUG--------------------\n");
        printf("OK, done, inspecting the tape now..\n");
        for(unsigned int i = 0; i < sizeof(tape) / sizeof(tape[0]); ++i)
        {
            unsigned int value = (((unsigned int*)tape[i])[0]) == S0 ? 0 : 1;
            if(S == tape[i])
                printf("[%d] ", value);
            else
                printf("%d ", value);
        }
        printf("\n");

        for(unsigned int i = 0; i < sizeof(tape) / sizeof(tape[0]); ++i)
            printf("[%#.8x] ", ((unsigned int*)tape[i])[1]);
        printf("\n");

        printf("S=%#.8x, L=%#.8x, R=%#.8x, T=%#.8x\n", S, L, R, T);
        printf("------------------------------------\n");
        goto here_we_go;
    }
    __except(EXCEPTION_EXECUTE_HANDLER)
    {}

    printf("OK, machine done, inspecting the tape now..\n");
    for(unsigned int i = 0; i < sizeof(tape) / sizeof(tape[0]); ++i)
    {
        unsigned int value = (((unsigned int*)tape[i])[0]) == S0 ? 0 : 1;
        if(S == tape[i])
            printf("[%d] ", value);
        else
            printf("%d ", value);
    }
    printf("\n");
    free(mem);
}

int main()
{
    turing_machine_simple();
    return 0;
}
/*
If like me, you didn't really understand how the tape was working, here is
an email Stephen sent me, it explains perfectly:
"""
    Here's an example. The tape contains cells c0, c1, c2, c3 and c4. The
    current cell is c2. I'll write c2 -> c3 to mean that c2's next pointer
    (that is, [c2 + 1]) points to c3. Currently, we have:
    S = c2
    L = c1
    c1 -> c0
    R = c3
    c3 -> c4

    Suppose we're moving right. We want to end up with c2 -> c1 -> c0, L =
    c2, S = c3, R = c4. First, we need to hook up the c2 -> c1 link, by
    doing "mov [S+1], c1" (where c1 is the old value of L). Next, we need
    to update L (by making it point to c2, the old value of S) and update
    R (by leaving it unchanged). This completes the PUSH phase, and we end
    up with:
    S = c2
    L = c2
    c2 -> c1 -> c0
    R = c3
    c3 -> c4

    We've pushed the S cell onto the left tape, but haven't popped a new
    cell from the right yet. So, we set S to be the old value of R (c3),
    and set X to be the new value of R by "mov X, [S+1]". Then, we update
    R (by setting it to c3), and update L (by leaving it unchanged). We're
    left with:

    S = c3
    L = c2
    c2 -> c1 -> c0
    R = c4
"""
*/