#!/bin/bash

for i in {41..56}
do
    # python preprocessing_script_new_mask_fire_only.py $i &
    python preprocessing_script_new_mask.py $i &
done