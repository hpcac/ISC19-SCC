#!/bin/bash

module load tensorflow/gpu-1.13.1-py36

prediction_dirs="./run_deeplab_ngpus1/output_test"
label_dirs="/project/projectdirs/mpccc/tkurth/DataScience/gb2018/data/segm_h5_v3_new_split_maeve/test_labels"

python ../utils/evaluate_iou.py --prediction_dirs=${prediction_dirs} --label_dirs=${label_dirs}
