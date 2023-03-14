#!/usr/bin/env bash

echo "Running C++ tests"
echo "================="
./cpp/bin/run-tests

echo "Running Python tests"
echo "===================="
python -m unittest discover python
