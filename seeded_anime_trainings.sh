#!/bin/bash

python train_DenseVAE_on_anime.py
python train_DenseVAE_DenseLogReg_on_anime.py
python train_ConvVAE_on_anime.py
python train_ConvVAE_ConvDisc_LeakyReLU_on_anime.py
python train_ConvVAE_ResNet_on_anime.py

s

