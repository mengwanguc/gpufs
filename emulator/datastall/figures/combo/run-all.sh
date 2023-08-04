#!/bin/bash
set -e

echo "Running all scripts..."
echo "  1. Minio"
echo "  2. Async"
echo "  3. Minio + Async"
echo "  4. Default"
echo ""

echo "Running (1) -- Minio"
./run-minio.sh

echo "Running (2) -- Async"
./run-async.sh

echo "Running (3) -- Minio + Async"
./run-minio-async.sh

echo "Running (4) -- Default"
./run-normal.sh