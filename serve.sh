#!/bin/bash

# Start vLLM server with Tri-7B-Search-preview model

echo "Starting vLLM server with Tri-7B-Search-preview..."
echo "Server will be available at http://localhost:8000"
echo "Press Ctrl+C to stop the server"

mkdir -p logs

uv run vllm serve trillionlabs/Tri-7B-Search-preview \
     --trust-remote-code \
     --tensor-parallel-size 1 \
     --host 0.0.0.0 \
     --port 8000 \
     --max-model-len 16384