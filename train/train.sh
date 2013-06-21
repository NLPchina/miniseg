#!/bin/bash
python gen_prob.py
python gen_feature.py
python train_bayes_model.py
cp bayes_model.marshal ../miniseg
cp prob_*.py ../miniseg


