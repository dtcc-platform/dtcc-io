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
    protobuf-compiler

./install_py_libs.sh
./install_assimp.sh