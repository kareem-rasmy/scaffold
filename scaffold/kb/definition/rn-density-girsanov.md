---
id: rn-density-girsanov
kind: definition
title: Z
statement: Radon–Nikodym density process
expr: exp(Add(Mul(Integer(-1), Symbol('W_t', real=True), Symbol('theta', real=True)), Mul(Integer(-1),
  Rational(1, 2), Symbol('t', positive=True), Pow(Symbol('theta', real=True), Integer(2)))))
status: stated
sources:
- paper: SC-book
  label: Z
  where: §5.2
latex: e^{- W_{t} \theta - \frac{t \theta^{2}}{2}}
---

$$
e^{- W_{t} \theta - \frac{t \theta^{2}}{2}}
$$
