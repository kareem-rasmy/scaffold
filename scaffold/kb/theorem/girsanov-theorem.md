---
id: girsanov-theorem
kind: theorem
title: Girsanov theorem
statement: If dQ/dP = E(-theta . W)_T, then W_t + int_0^t theta ds is a Q-Brownian motion.
status: open
sources:
- paper: SC-book
  label: Thm 5.2.3
  where: §5.2
depends_on:
- rn-density-girsanov
tags:
- stochastic-calculus
- measure-change
checked_in: books/sc_book.py
curated: true
---

Needs Novikov (or Kazamaki) for the stochastic exponential to be a true martingale.
