#!/bin/bash
diff accesslog-A.txt accesslog-B.txt --unified | grep -Eo '^[+-].' |grep -Ev '^[+-]([1-9])$' | sed 's/[+-]//g' | tr -d '\n'
echo ''
diff -c accesslog-A.txt accesslog-B.txt | grep -E '^[+-] .' | cut -d ' ' -f 2 | grep -Ev '\S{2}' | cut -c 1 | tr -d '\n'
