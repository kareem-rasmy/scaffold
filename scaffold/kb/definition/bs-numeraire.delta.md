---
id: bs-numeraire.delta
kind: definition
title: Delta
statement: delta
expr: Add(Mul(Integer(-1), Rational(1, 2), Pow(Integer(2), Rational(1, 2)), Pow(pi, Rational(-1, 2)),
  Symbol('K', positive=True), Pow(Symbol('S', positive=True), Integer(-1)), Pow(Symbol('sigma', positive=True),
  Integer(-1)), Pow(Symbol('tau', positive=True), Rational(-1, 2)), exp(Mul(Integer(-1), Symbol('r', positive=True),
  Symbol('tau', positive=True))), exp(Mul(Integer(-1), Rational(1, 2), Pow(Add(Mul(Integer(-1), Symbol('sigma',
  positive=True), Pow(Symbol('tau', positive=True), Rational(1, 2))), Mul(Pow(Symbol('sigma', positive=True),
  Integer(-1)), Pow(Symbol('tau', positive=True), Rational(-1, 2)), Add(Mul(Symbol('tau', positive=True),
  Add(Symbol('r', positive=True), Mul(Rational(1, 2), Pow(Symbol('sigma', positive=True), Integer(2))))),
  log(Mul(Pow(Symbol('K', positive=True), Integer(-1)), Symbol('S', positive=True)))))), Integer(2))))),
  Mul(Rational(1, 2), erf(Mul(Rational(1, 2), Pow(Integer(2), Rational(1, 2)), Pow(Symbol('sigma', positive=True),
  Integer(-1)), Pow(Symbol('tau', positive=True), Rational(-1, 2)), Add(Mul(Symbol('tau', positive=True),
  Add(Symbol('r', positive=True), Mul(Rational(1, 2), Pow(Symbol('sigma', positive=True), Integer(2))))),
  log(Mul(Pow(Symbol('K', positive=True), Integer(-1)), Symbol('S', positive=True))))))), Rational(1,
  2), Mul(Rational(1, 2), Pow(Integer(2), Rational(1, 2)), Pow(pi, Rational(-1, 2)), Pow(Symbol('sigma',
  positive=True), Integer(-1)), Pow(Symbol('tau', positive=True), Rational(-1, 2)), exp(Mul(Integer(-1),
  Rational(1, 2), Pow(Symbol('sigma', positive=True), Integer(-2)), Pow(Symbol('tau', positive=True),
  Integer(-1)), Pow(Add(Mul(Symbol('tau', positive=True), Add(Symbol('r', positive=True), Mul(Rational(1,
  2), Pow(Symbol('sigma', positive=True), Integer(2))))), log(Mul(Pow(Symbol('K', positive=True), Integer(-1)),
  Symbol('S', positive=True)))), Integer(2))))))
status: stated
sources:
- paper: BS-numeraire
  label: Delta
latex: '- \frac{\sqrt{2} K e^{- r \tau} e^{- \frac{\left(- \sigma \sqrt{\tau} + \frac{\tau \left(r + \frac{\sigma^{2}}{2}\right)
  + \log{\left(\frac{S}{K} \right)}}{\sigma \sqrt{\tau}}\right)^{2}}{2}}}{2 \sqrt{\pi} S \sigma \sqrt{\tau}}
  + \frac{\operatorname{erf}{\left(\frac{\sqrt{2} \left(\tau \left(r + \frac{\sigma^{2}}{2}\right) + \log{\left(\frac{S}{K}
  \right)}\right)}{2 \sigma \sqrt{\tau}} \right)}}{2} + \frac{1}{2} + \frac{\sqrt{2} e^{- \frac{\left(\tau
  \left(r + \frac{\sigma^{2}}{2}\right) + \log{\left(\frac{S}{K} \right)}\right)^{2}}{2 \sigma^{2} \tau}}}{2
  \sqrt{\pi} \sigma \sqrt{\tau}}'
---

$$
- \frac{\sqrt{2} K e^{- r \tau} e^{- \frac{\left(- \sigma \sqrt{\tau} + \frac{\tau \left(r + \frac{\sigma^{2}}{2}\right) + \log{\left(\frac{S}{K} \right)}}{\sigma \sqrt{\tau}}\right)^{2}}{2}}}{2 \sqrt{\pi} S \sigma \sqrt{\tau}} + \frac{\operatorname{erf}{\left(\frac{\sqrt{2} \left(\tau \left(r + \frac{\sigma^{2}}{2}\right) + \log{\left(\frac{S}{K} \right)}\right)}{2 \sigma \sqrt{\tau}} \right)}}{2} + \frac{1}{2} + \frac{\sqrt{2} e^{- \frac{\left(\tau \left(r + \frac{\sigma^{2}}{2}\right) + \log{\left(\frac{S}{K} \right)}\right)^{2}}{2 \sigma^{2} \tau}}}{2 \sqrt{\pi} \sigma \sqrt{\tau}}
$$
