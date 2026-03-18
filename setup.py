import os
import shutil
import pathlib
from setuptools import setup, find_packages

home = pathlib.Path(__file__).parent
version = (home / "scaffold/version.txt").read_text()
setup(
    name="scaffold",
    version=version,
    author="Kareem Rasmy",
    author_email="Kareem.Rasmy@gmail.com",
    description="Math Library",
    url="https://github.com/kareem-rasmy/scaffold.git",
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=[
        "networkx"
    ]
)

egg_info_dir = "scaffold.egg-info"
if os.path.exists(egg_info_dir):
    print(f"Removing {egg_info_dir} ...")
    shutil.rmtree(egg_info_dir)
