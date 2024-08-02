#!/bin/bash
#SBATCH --j=Optimize%j
#SBATCH --ntasks=1
#SBATCH --time=1:00:00
#SBATCH --mem=16gb
#SBATCH --error=/home/r/rrmoreno/524-proj/slurm-logs/Optimize%j.err
#SBATCH --output=/home/r/rrmoreno/524-proj/slurm-logs/Optimize%j.out

# Launch via:
# sbatch launch_optimization_slurm.sh

python brute_force_model.py