#!/bin/bash

for filename in ../streams/*.txt; do
    uudecode $filename
done