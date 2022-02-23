#!/bin/bash
# Install dependencies
set -eo pipefail
PY_DIR='build/python'
pip3 install -r requirements.txt --no-deps --target $PY_DIR

# zip up dependencies
cd build
zip -r ../packages.zip .

