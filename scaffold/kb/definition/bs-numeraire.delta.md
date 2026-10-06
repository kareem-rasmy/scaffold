---
id: bs-numeraire.delta
kind: definition
title: Delta
statement: delta
expr: -sqrt(2)*K*exp(-r*tau)*exp(-(-sigma*sqrt(tau) + (tau*(r + sigma**2/2) + log(S/K))/(sigma*sqrt(tau)))**2/2)/(2*sqrt(pi)*S*sigma*sqrt(tau)) + erf(sqrt(2)*(tau*(r + sigma**2/2) + log(S/K))/(2*sigma*sqrt(tau)))/2 + 1/2 + sqrt(2)*exp(-(tau*(r + sigma**2/2) + log(S/K))**2/(2*sigma**2*tau))/(2*sqrt(pi)*sigma*sqrt(tau))
symbols:
  K: positive
  S: positive
  d1: ''
  d2: ''
  r: positive
  sigma: positive
  tau: positive
compact: -sqrt(2)*K*exp(-d2**2/2)*exp(-r*tau)/(2*sqrt(pi)*S*sigma*sqrt(tau)) + erf(sqrt(2)*d1/2)/2 + 1/2 + sqrt(2)*exp(-d1**2/2)/(2*sqrt(pi)*sigma*sqrt(tau))
status: stated
sources:
- paper: BS-numeraire
  label: Delta
---

$$
\Delta = - \frac{\sqrt{2} K e^{- \frac{d_{2}^{2}}{2}} e^{- r \tau}}{2 \sqrt{\pi} S \sigma \sqrt{\tau}} + \frac{\operatorname{erf}{\left(\frac{\sqrt{2} d_{1}}{2} \right)}}{2} + \frac{1}{2} + \frac{\sqrt{2} e^{- \frac{d_{1}^{2}}{2}}}{2 \sqrt{\pi} \sigma \sqrt{\tau}}
$$
