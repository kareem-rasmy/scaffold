---
id: bs-call
kind: definition
title: C
statement: call price, eq. (3.3)
expr: Add(Mul(Integer(-1), Symbol('K', positive=True), Add(Mul(Rational(1, 2), erf(Mul(Rational(1, 2),
  Pow(Integer(2), Rational(1, 2)), Add(Mul(Integer(-1), Symbol('sigma', positive=True), Pow(Symbol('tau',
  positive=True), Rational(1, 2))), Mul(Pow(Symbol('sigma', positive=True), Integer(-1)), Pow(Symbol('tau',
  positive=True), Rational(-1, 2)), Add(Mul(Symbol('tau', positive=True), Add(Symbol('r', positive=True),
  Mul(Rational(1, 2), Pow(Symbol('sigma', positive=True), Integer(2))))), log(Mul(Pow(Symbol('K', positive=True),
  Integer(-1)), Symbol('S', positive=True))))))))), Rational(1, 2)), exp(Mul(Integer(-1), Symbol('r',
  positive=True), Symbol('tau', positive=True)))), Mul(Symbol('S', positive=True), Add(Mul(Rational(1,
  2), erf(Mul(Rational(1, 2), Pow(Integer(2), Rational(1, 2)), Pow(Symbol('sigma', positive=True), Integer(-1)),
  Pow(Symbol('tau', positive=True), Rational(-1, 2)), Add(Mul(Symbol('tau', positive=True), Add(Symbol('r',
  positive=True), Mul(Rational(1, 2), Pow(Symbol('sigma', positive=True), Integer(2))))), log(Mul(Pow(Symbol('K',
  positive=True), Integer(-1)), Symbol('S', positive=True))))))), Rational(1, 2))))
status: stated
sources:
- paper: BS-numeraire
  label: C
latex: '- K \left(\frac{\operatorname{erf}{\left(\frac{\sqrt{2} \left(- \sigma \sqrt{\tau} + \frac{\tau
  \left(r + \frac{\sigma^{2}}{2}\right) + \log{\left(\frac{S}{K} \right)}}{\sigma \sqrt{\tau}}\right)}{2}
  \right)}}{2} + \frac{1}{2}\right) e^{- r \tau} + S \left(\frac{\operatorname{erf}{\left(\frac{\sqrt{2}
  \left(\tau \left(r + \frac{\sigma^{2}}{2}\right) + \log{\left(\frac{S}{K} \right)}\right)}{2 \sigma
  \sqrt{\tau}} \right)}}{2} + \frac{1}{2}\right)'
---

$$
- K \left(\frac{\operatorname{erf}{\left(\frac{\sqrt{2} \left(- \sigma \sqrt{\tau} + \frac{\tau \left(r + \frac{\sigma^{2}}{2}\right) + \log{\left(\frac{S}{K} \right)}}{\sigma \sqrt{\tau}}\right)}{2} \right)}}{2} + \frac{1}{2}\right) e^{- r \tau} + S \left(\frac{\operatorname{erf}{\left(\frac{\sqrt{2} \left(\tau \left(r + \frac{\sigma^{2}}{2}\right) + \log{\left(\frac{S}{K} \right)}\right)}{2 \sigma \sqrt{\tau}} \right)}}{2} + \frac{1}{2}\right)
$$
