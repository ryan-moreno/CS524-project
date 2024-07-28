#!/bin/bash
#SBATCH --j=Comb%j
#SBATCH --ntasks=1
#SBATCH --time=1:00:00
#SBATCH --mem=2gb
#SBATCH --error=/home/r/rrmoreno/524-proj/slurm-logs/Comb%j.err
#SBATCH --output=/home/r/rrmoreno/524-proj/slurm-logs/Comb%j.out

# Ensure slurm output folders exist
slurm_output_folder="/home/r/rrmoreno/524-proj/slurm-logs"
if [ ! -d $slurm_output_folder ]; then
    mkdir $slurm_output_folder
fi  

command="python precompute_combinations_slurm.py $n_start $n_end"

echo ""
echo "command used:"
echo $command
echo ""

$command

echo "Finished computing combinations"
