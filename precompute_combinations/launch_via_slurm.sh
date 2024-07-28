#!/bin/bash

slurm_script_path="partial_computation.slurm.sh"

echo "#############################################"
echo "###   SUBMITTING COMPUTATIONS TO SLURM   ####"
echo "#############################################"
echo ""

# Computing each minute of the period separately
for i in $(seq 1 20); do
    n_start=$(( (i - 1) * 60 ))
    n_end=$(( i * 60 ))

    # Compute combinations
    echo "Submitting slurm job to compute combinations for n=${n_start} to n=${n_end}"
    slurm_job_name="Comb_${n_start}-${n_end}_%j"

    sbatch --job-name=$slurm_job_name --export ALL,n_start=$n_start,n_end=$n_end $slurm_script_path
done