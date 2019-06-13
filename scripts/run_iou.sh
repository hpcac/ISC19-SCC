#!/bin/bash

prediction_dirs="../debug/predictions"
label_dirs="../debug/labels"

python ../utils/evaluate_iou.py --prediction_dirs=${prediction_dirs} --label_dirs=${label_dirs} --frequencies 1. 1. 1.