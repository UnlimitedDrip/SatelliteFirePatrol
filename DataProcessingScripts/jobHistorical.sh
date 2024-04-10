#!/bin/bash

#SBATCH --job-name=capstone_data

#SBATCH --output=/scratch/zmh47/HistoricalResult.txt # change zmh47 to your nau id
#SBATCH --error=/scratch/zmh47/HistoricalResult.err # change zmh47 to your nau id
#SBATCH --time=24:00:00
#SBATCH --mem=2G

module load anaconda3
conda activate capstone
python getHistoricalData.py
