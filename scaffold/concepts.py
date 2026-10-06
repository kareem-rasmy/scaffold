"""Your own general entries, independent of any single source.
Runs first on every build, so the wording here wins over imported labels."""


def register(kb):
    kb.add("girsanov-theorem", "theorem", "Girsanov theorem",
           statement="If dQ/dP = E(-theta . W)_T, then W_t + int_0^t theta ds is a Q-Brownian motion.",
           tags=["stochastic-calculus", "measure-change"],
           notes="Needs Novikov (or Kazamaki) for the stochastic exponential to be a true martingale.")
    # the paper's P -> Q change of measure rests on Girsanov
    kb.add("change-P-to-Q", "morphism", "girsanov", depends_on=["girsanov-theorem"])
