#!/bin/bash
set -e
cd "$(dirname "$0")"
echo "[INFO] Installing dependencies..."
npm install
echo "[INFO] Starting backend..."
npm start