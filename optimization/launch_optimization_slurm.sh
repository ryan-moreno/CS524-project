# Launch via:
# sbatch \
#     --job-name=optimize \
#     --output=/home/r/rrmoreno/524-proj/slurm-logs/Optimize%j.log \
#     --error=/home/r/rrmoreno/524-proj/slurm-logs/Optimize%j.err \
#     launch_optimization_slurm.sh

python optimization_model.py