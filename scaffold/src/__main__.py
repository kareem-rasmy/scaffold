"""
Command-line interface for scaffold.

    scaffold build                                  check all sources, render, update kb/
    scaffold check papers/bs_measures.py            run one or more files' checks
    scaffold find --kind exercise --status open     query the knowledge base
    scaffold deps girsanov-theorem                  what depends on an entry
    scaffold describe papers/bs_measures.py measures
    scaffold where                                  show which notes folder is used

`python -m scaffold.src <command>` works the same way.

The notes folder (holding papers/, books/, kb/, concepts.py) is found in this
order:
    1. --root PATH
    2. the SCAFFOLD_NOTES environment variable
    3. the current directory, or ./scaffold, if it contains papers/ or books/
    4. the folder next to this package (editable installs)
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .build import build, check_file
from .kb import KnowledgeBase

ENV_VAR = "SCAFFOLD_NOTES"
MARKERS = ("papers", "books")          # a stray kb/ alone doesn't make a notes folder
EXIT_OK, EXIT_FAILED, EXIT_USAGE = 0, 1, 2


# --------------------------------------------------------------------------- #
# Locating the notes folder
# --------------------------------------------------------------------------- #
def _looks_like_notes_root(path: Path) -> bool:
    return any((path / m).is_dir() for m in MARKERS)


def find_notes_root(explicit: str | None = None) -> tuple[Path, str]:
    """Return (notes root, how it was found). Raises FileNotFoundError."""
    if explicit:
        return Path(explicit).resolve(), "--root"
    if os.environ.get(ENV_VAR):
        return Path(os.environ[ENV_VAR]).resolve(), f"${ENV_VAR}"
    cwd = Path.cwd()
    for cand in (cwd, cwd / "scaffold"):
        if _looks_like_notes_root(cand):
            return cand.resolve(), "current directory"
    pkg = Path(__file__).resolve().parents[1]
    if _looks_like_notes_root(pkg):
        return pkg, "package folder"
    raise FileNotFoundError(
        "No notes folder found. Run from a folder containing papers/ or books/, "
        f"pass --root PATH, or set {ENV_VAR}.")


def resolve_file(name: str, root: Path) -> Path:
    """Accept paths relative to the current directory or to the notes root."""
    for cand in (Path(name), root / name):
        if cand.is_file():
            return cand.resolve()
    raise FileNotFoundError(f"{name} (looked in {Path.cwd()} and {root})")


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
def cmd_build(args, root: Path) -> int:
    report = build(root)
    print(report.summary())
    if not report.statuses and not report.errors:
        print(f"warning: no notes files found under {root / 'papers'} or {root / 'books'}")
    return EXIT_FAILED if report.failed or report.errors else EXIT_OK


def cmd_check(args, root: Path) -> int:
    failed = 0
    for name in args.files:
        _, notes = check_file(resolve_file(name, root))
        print(name)
        for label, claim in notes.claims.items():
            print(f"  {label:<14} {claim.status.value}")
            failed += claim.status.value == "FAILED"
    return EXIT_FAILED if failed else EXIT_OK


def cmd_find(args, root: Path) -> int:
    kb = KnowledgeBase(root / "kb")
    hits = kb.find(kind=args.kind, tag=args.tag, paper=args.paper,
                   status=args.status, text=args.text)
    for e in hits:
        print(f"{e.kind:<12} {e.status:<13} {e.id:<36} {e.title}")
    if not hits:
        print("(no matches)")
    return EXIT_OK


def cmd_deps(args, root: Path) -> int:
    kb = KnowledgeBase(root / "kb")
    if args.id not in kb:
        print(f"no entry with id {args.id!r}", file=sys.stderr)
        return EXIT_USAGE
    deps = kb.dependents(args.id)
    print("\n".join(deps) if deps else "(nothing depends on it)")
    return EXIT_OK


def cmd_describe(args, root: Path) -> int:
    _, notes = check_file(resolve_file(args.file, root))
    if args.diagram not in notes.diagrams:
        names = ", ".join(notes.diagrams) or "none"
        print(f"no diagram {args.diagram!r}; available: {names}", file=sys.stderr)
        return EXIT_USAGE
    print(notes.describe(args.diagram))
    return EXIT_OK


def cmd_where(args, root: Path, how: str = "") -> int:
    print(f"notes root: {root}  (from {how})")
    for m in (*MARKERS, "kb", "concepts.py"):
        print(f"  {m:<12} {'found' if (root / m).exists() else 'missing'}")
    return EXIT_OK


# --------------------------------------------------------------------------- #
# Argument parsing
# --------------------------------------------------------------------------- #
def make_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", help=f"notes folder (default: auto-detect, or ${ENV_VAR})")

    p = argparse.ArgumentParser(prog="scaffold", parents=[common],
                                description="Checkable SymPy notes and knowledge base.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("build", parents=[common], help="check all sources, render, update kb/")

    c = sub.add_parser("check", parents=[common], help="run the checks in notes files")
    c.add_argument("files", nargs="+")

    f = sub.add_parser("find", parents=[common], help="query the knowledge base")
    for opt in ("kind", "tag", "paper", "status", "text"):
        f.add_argument(f"--{opt}")

    d = sub.add_parser("deps", parents=[common], help="entries that depend on ID")
    d.add_argument("id")

    s = sub.add_parser("describe", parents=[common], help="print a diagram from a notes file")
    s.add_argument("file")
    s.add_argument("diagram")

    sub.add_parser("where", parents=[common], help="show which notes folder is used")
    return p


COMMANDS = {"build": cmd_build, "check": cmd_check, "find": cmd_find,
            "deps": cmd_deps, "describe": cmd_describe, "where": cmd_where}


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):            # Windows consoles default to cp1252
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    args = make_parser().parse_args(argv)
    try:
        root, how = find_notes_root(args.root)
        if args.cmd == "where":
            return cmd_where(args, root, how)
        return COMMANDS[args.cmd](args, root)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
