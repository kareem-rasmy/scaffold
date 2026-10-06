"""
Command line:
  python -m scaffold build                 check everything, render, update kb/
  python -m scaffold check papers/x.py     run one file's checks only
  python -m scaffold find --kind theorem --text girsanov
  python -m scaffold deps girsanov-theorem
  python -m scaffold describe papers/bs_measures.py measures
"""
import argparse
import sys
from pathlib import Path

from .build import build, check_file
from .kb import KnowledgeBase


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):          # Windows consoles default to cp1252
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(prog="scaffold")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="check all sources, render, update the KB")
    b.add_argument("--root", default=".")

    c = sub.add_parser("check", help="run the checks in one or more notes files")
    c.add_argument("files", nargs="+")

    f = sub.add_parser("find", help="query the KB")
    for opt in ("kind", "tag", "paper", "status", "text"):
        f.add_argument(f"--{opt}")
    f.add_argument("--kb", default="kb")

    d = sub.add_parser("deps", help="everything that depends on an entry")
    d.add_argument("id")
    d.add_argument("--kb", default="kb")

    s = sub.add_parser("describe", help="print a diagram from a notes file")
    s.add_argument("file")
    s.add_argument("diagram")

    a = p.parse_args(argv)

    if a.cmd == "build":
        r = build(a.root)
        print(r.summary())
        return 1 if r.failed or r.errors else 0
    if a.cmd == "check":
        bad = 0
        for fn in a.files:
            _, n = check_file(Path(fn))
            print(fn)
            for lbl, cl in n.claims.items():
                print(f"  {lbl:<14} {cl.status.value}")
                bad += cl.status.value == "FAILED"
        return 1 if bad else 0
    if a.cmd == "find":
        kb = KnowledgeBase(a.kb)
        for e in kb.find(a.kind, a.tag, a.paper, a.status, a.text):
            print(f"{e.kind:<12} {e.status:<13} {e.id:<32} {e.title}")
        return 0
    if a.cmd == "deps":
        print("\n".join(KnowledgeBase(a.kb).dependents(a.id)) or "(nothing depends on it)")
        return 0
    if a.cmd == "describe":
        _, n = check_file(Path(a.file))
        print(n.describe(a.diagram))
        return 0


if __name__ == "__main__":
    sys.exit(main())
