#!/usr/bin/env sh
set -e
echo "Building wheel file for scaffold"
python -m build --wheel --outdir whl
rm -rf scaffold.egg-info build
echo "Build succeeded"
