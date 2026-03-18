@echo off
echo Building wheel file for scaffold
python setup.py bdist_wheel --dist-dir=whl
rmdir /s /q scaffold.egg-info
rmdir /s /q build
