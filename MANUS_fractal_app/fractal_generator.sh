#!/bin/bash
echo "フラクタルジェネレータを起動中..."
python3 "$(dirname "$0")/bin/fractal_generator.py" "$@"
