"""Shared helpers for the tutorials: imports that work in both repo layouts,
and pretty section headers."""
import sys
from pathlib import Path

import scaffold.src as lib
from scaffold.src.build import build

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def project_root() -> Path:
    """Folder that contains papers/, books/ and concepts.py."""
    return Path(lib.__file__).resolve().parents[1]


def section(title):
    print("\n" + "=" * 72 + f"\n{title}\n" + "=" * 72)


def show(label, value):
    print(f"  {label:<34} {value}")
