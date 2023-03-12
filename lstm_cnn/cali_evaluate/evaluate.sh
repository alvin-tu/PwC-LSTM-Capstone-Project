#"!/bin/bash

evaluation_datas=(
    "/home/capstone22/WildFIrePrediction/agni/cali_data/evaluation_data/01/"
    "/home/capstone22/WildFIrePrediction/agni/cali_data/evaluation_data/03/"
    "/home/capstone22/WildFIrePrediction/agni/cali_data/evaluation_data/06/"
    "/home/capstone22/WildFIrePrediction/agni/cali_data/evaluation_data/08/"
    "/home/capstone22/WildFIrePrediction/agni/cali_data/evaluation_data/10/"
    "/home/capstone22/WildFIrePrediction/agni/cali_data/evaluation_data/11/"
)

models=(
    "model_cali.hdf5" 
    "model_cali_3month.hdf5" 
    "model_cali_6month.hdf5" 
    "model_cali_9month.hdf5" 
)



# Loop over the models and evaluation data, and call the appropriate evaluation script for each combination
for model in "${models[@]}"
do
    for eval_data_path in "${evaluation_datas[@]}"
    do
        python evaluation_script_50_epoch_stride1.py --model "$model" --eval_path "$eval_data_path"
    done
done

# evaluate using auc score

# pred_file_folder="/home/capstone22/WildFIrePrediction/agni/evaluation_scripts/results"

# for file_path in $pred_file_folder/*; do
#     python ./auc_calculation/auc_calculation.py --pred_file $file_path
# done




