#!/bin/bash
#SBATCH -J single-server
#SBATCH --output=server.%j.out
#SBATCH --nodes=1
#SBATCH -A ia1
#SBATCH --partition=debug
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1

echo $CUDA_VISIBLE_DEVICES

source ~/.bashrc
source activate gap

# Define the ports to use
PORTS=($1)

# Fetch the list of available GPU IDs
GPU_IDS=($(nvidia-smi --query-gpu=index --format=csv,noheader))

# Check if the number of GPUs matches the number of ports
if [ ${#GPU_IDS[@]} -lt ${#PORTS[@]} ]; then
  echo "Error: Not enough GPUs available."
  exit 1
fi

# Loop through the ports and start a server on each with a different GPU
for i in "${!PORTS[@]}"
do
  PORT=${PORTS[$i]}
  GPU=${GPU_IDS[$i]}
  echo "Starting server on port $PORT with GPU $GPU"
  CUDA_VISIBLE_DEVICES=$GPU python -m vllm.entrypoints.openai.api_server \
      --model $2 \
      --tensor-parallel-size 1 \
      --dtype auto --port $PORT &
done

wait
