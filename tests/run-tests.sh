#!/usr/bin/env bash

echo "Running C++ unit tests"
echo "======================"
./cpp/bin/run-unittests

echo "Running Python unit tests"
echo "========================="
python -m unittest discover python
