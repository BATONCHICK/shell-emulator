#!/bin/bash
cd "$(dirname "$0")/.."
printf "exit\n" | python3 src/main.py --vfs ./test_vfs --script ./start_error.txt