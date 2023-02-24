#!/usr/bin/bash
apt-get update && apt-get install -y locales \
    sudo \
    build-essential \
    git cmake \
    clang-format \
    clang-tidy \
    libprotobuf-dev \
    python3 \
    python3-pip \
    python3-dev \
    libassimp-dev \
    protobuf-compiler

./install_py_libs.sh
#./install_assimp.sh

ln -s /usr/lib/x86_64-linux-gnu/libassimp.so.5 /usr/lib/
ln -s /usr/lib/aarch64-linux-gnu/libassimp.so.5 /usr/lib/