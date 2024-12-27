#!/bin/bash

python ./gen.py >extract_script
peepdf -s extract_script about-git.pdf
