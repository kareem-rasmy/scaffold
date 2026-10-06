---
id: bs-call
kind: definition
title: C
statement: call price, eq. (3.3)
expr: -K*(erf(sqrt(2)*(-sigma*sqrt(tau) + (tau*(r + sigma**2/2) + log(S/K))/(sigma*sqrt(tau)))/2)/2 + 1/2)*exp(-r*tau) + S*(erf(sqrt(2)*(tau*(r + sigma**2/2) + log(S/K))/(2*sigma*sqrt(tau)))/2 + 1/2)
symbols:
  K: positive
  S: positive
  d1: ''
  d2: ''
  r: positive
  sigma: positive
  tau: positive
compact: -K*(erf(sqrt(2)*d2/2)/2 + 1/2)*exp(-r*tau) + S*(erf(sqrt(2)*d1/2)/2 + 1/2)
status: stated
sources:
- paper: BS-numeraire
  label: C
---

$$
C = - K \left(\frac{\operatorname{erf}{\left(\frac{\sqrt{2} d_{2}}{2} \right)}}{2} + \frac{1}{2}\right) e^{- r \tau} + S \left(\frac{\operatorname{erf}{\left(\frac{\sqrt{2} d_{1}}{2} \right)}}{2} + \frac{1}{2}\right)
$$
