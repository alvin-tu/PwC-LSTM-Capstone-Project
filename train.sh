# !/bin/bash

for i in {5..30..5}
do
    python3 ibm.py --in_len 5 --out_len $i --name in_5_out_$i
done
