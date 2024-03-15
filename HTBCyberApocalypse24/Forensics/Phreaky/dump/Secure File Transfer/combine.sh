#!/bin/bash

for i in $(seq 1 15); do
  cat phreaks_plan.pdf.part$i >> phreaks_plan.pdf
done
