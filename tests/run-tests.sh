#!/usr/bin/env bash


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
pushd ${SCRIPT_DIR}
echo "Running C++ unit tests!"
echo "-----------------------"

#./unittests_cpp/bin/run-unittests

#echo ${SCRIPT_DIR}/unittests_py/test.py

echo "Running Python unit tests!"
echo "-----------------------"

python3 -m unittest discover unittests_py

popd
