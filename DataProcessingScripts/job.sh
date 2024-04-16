#!/bin/bash

#SBATCH --job-name=capstone_data

#SBATCH --output=/scratch/zmh47/result.txt # change zmh47 to your nau id
#SBATCH --error=/scratch/zmh47/result.err # change zmh47 to your nau id
#SBATCH --time=01:00:00
#SBATCH --mem=8G

module load anaconda3
conda activate capstone
python alertSystemManager.py # Get alert system database
python processDataManager.py # Process new data

sbatch --begin=now+24hours $0
