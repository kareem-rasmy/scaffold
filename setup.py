import pathlib
from setuptools import setup, find_packages

home = pathlib.Path(__file__).parent
version_file = home / "scaffold/version.txt"
version = version_file.read_text().strip() if version_file.exists() else "0.0.0"
setup(
    name="scaffold",
    version=version,
    author="Kareem Rasmy",
    author_email="Kareem.Rasmy@gmail.com",
    description="Math Library",
    url="https://github.com/kareem-rasmy/scaffold.git",
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=[
        "networkx",
        "matplotlib"
    ]
)
