#
#    Dockerfile Kryptonite - Set up everything you need to play with Kryptonite in a vanilla debian jessie.
#    Prefer an x64 based Host/Container to have both the x86/x64 versions compiled & ready to go.
#    Copyright (C) 2015 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    overclok@wildout:~/dev$ mkdir kryptonite && cd kryptonite
#    overclok@wildout:~/dev/kryptonite$ sudo docker build --tag=kryptonite .
#    [...]
#    Successfully built bf9140f60d0a
#    overclok@wildout:~/dev/kryptonite$ sudo docker images
#    REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
#    kryptonite          latest              b97b2d28f05e        13 seconds ago      954.6 MB
#    overclok@wildout:~/dev/kryptonite$ sudo docker run -ti kryptonite /bin/bash
#    [...]

FROM debian:jessie
MAINTAINER Axel "0vercl0k" Souchet <0vercl0k[at]tuxfamily[dot]org>

# Install basic stuff we might need
RUN apt-get update && apt-get install -y git wget xz-utils python2.7 gdb gcc g++ zlib1g-dev g++-multilib gcc-multilib

# Setup a dummy user
RUN echo 'root:root' | chpasswd
RUN adduser --quiet --disabled-password over

USER over

# Exporting llvm3.5 binaries in both env & bashrc
WORKDIR /home/over
ENV PATH /home/over/tools/clang+llvm-3.5.0-x86_64-linux-gnu/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN mkdir tools dev
RUN echo 'export PATH=/home/over/tools/clang+llvm-3.5.0-x86_64-linux-gnu/bin:$PATH' >> .bashrc

# Downloading, bziping them in a tool directory
WORKDIR /home/over/tools
RUN wget http://llvm.org/releases/3.5.0/clang+llvm-3.5.0-x86_64-linux-gnu-ubuntu-14.04.tar.xz -O /home/over/tools/clang+llvm-3.5.tar.xz > /dev/null 2>&1 && tar xvf clang+llvm-3.5.tar.xz > /dev/null 2>&1 && rm clang+llvm-3.5.tar.xz

# Cloning stuffz
WORKDIR /home/over/dev
RUN git clone https://github.com/0vercl0k/stuffz.git

# Finally, building the llvm pass, kryptonite, optimizing the crackme 3 times & stripping the output
WORKDIR /home/over/dev/stuffz/llvm-funz/kryptonite
RUN clang++ llvm-functionpass-kryptonite-obfuscater.cpp `llvm-config --cxxflags --ldflags` -shared -o llvm-functionpass-kryptonite-obfuscater.so
RUN clang -S -emit-llvm kryptonite-crackme.c -o kryptonite-crackme.original.ll
RUN cp kryptonite-crackme.original.ll kryptonite-crackme.ll ; \
    opt -S -load ./llvm-functionpass-kryptonite-obfuscater.so -kryptonite -heavy-add-obfu kryptonite-crackme.ll -o kryptonite-crackme.opti.ll && \
    mv kryptonite-crackme.opti.ll kryptonite-crackme.ll ; \
    opt -S -load ./llvm-functionpass-kryptonite-obfuscater.so -kryptonite -heavy-add-obfu kryptonite-crackme.ll -o kryptonite-crackme.opti.ll && \
    mv kryptonite-crackme.opti.ll kryptonite-crackme.ll ; \
    llc -O0 -filetype=obj -march=x86 kryptonite-crackme.ll -o kryptonite-crackme.x86.o && \
    clang -m32 -static kryptonite-crackme.x86.o -o kryptonite-crackme.x86 && \
    strip --strip-all ./kryptonite-crackme.x86 ; \
    llc -O0 -filetype=obj -march=x86-64 kryptonite-crackme.ll -o kryptonite-crackme.x64.o && \
    clang -static kryptonite-crackme.x64.o -o kryptonite-crackme.x64 && \
    strip --strip-all ./kryptonite-crackme.x64 ;
