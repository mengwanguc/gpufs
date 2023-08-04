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
echo "(1) Minio done"

echo "Running (2) -- Async"
./run-async.sh
echo "(2) Async done"

echo "Running (3) -- Minio + Async"
./run-minio-async.sh
echo "(3) Minio + Async done"

echo "Running (4) -- Default"
./run-normal.sh
echo "(4) Default done"

echo "... all runs completed"