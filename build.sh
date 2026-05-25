#!/bin/bash

echo "Building wheel file for scaffold"
python3 setup.py bdist_wheel --dist-dir=whl

rm -rf scaffold.egg-info
rm -rf build