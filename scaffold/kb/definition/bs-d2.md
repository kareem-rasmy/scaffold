---
id: bs-d2
kind: definition
title: d2
statement: eq. (3.2)
expr: Add(Mul(Integer(-1), Symbol('sigma', positive=True), Pow(Symbol('tau', positive=True), Rational(1,
  2))), Mul(Pow(Symbol('sigma', positive=True), Integer(-1)), Pow(Symbol('tau', positive=True), Rational(-1,
  2)), Add(Mul(Symbol('tau', positive=True), Add(Symbol('r', positive=True), Mul(Rational(1, 2), Pow(Symbol('sigma',
  positive=True), Integer(2))))), log(Mul(Pow(Symbol('K', positive=True), Integer(-1)), Symbol('S', positive=True))))))
status: stated
sources:
- paper: BS-numeraire
  label: d2
latex: '- \sigma \sqrt{\tau} + \frac{\tau \left(r + \frac{\sigma^{2}}{2}\right) + \log{\left(\frac{S}{K}
  \right)}}{\sigma \sqrt{\tau}}'
---

$$
- \sigma \sqrt{\tau} + \frac{\tau \left(r + \frac{\sigma^{2}}{2}\right) + \log{\left(\frac{S}{K} \right)}}{\sigma \sqrt{\tau}}
$$
