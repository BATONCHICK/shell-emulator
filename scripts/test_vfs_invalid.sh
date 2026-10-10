#!/bin/bash

cd "$(dirname "$0")/.."

python3 src/main.py \
    --vfs ./vfs_examples/not_exists