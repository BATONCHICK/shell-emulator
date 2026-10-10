#!/bin/bash

cd "$(dirname "$0")/.."

python3 src/main.py \
    --vfs ./vfs_examples/nested \
    --script ./start_stage3.txt