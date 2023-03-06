#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
pushd ${SCRIPT_DIR}

echo "Running C++ unit tests"
echo "======================"
./cpp/bin/run-unittests

echo "Running Python unit tests"
echo "========================="
python3 -m unittest discover python

popd
