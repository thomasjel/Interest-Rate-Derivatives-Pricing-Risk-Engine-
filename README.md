# Interest Rate Derivatives Pricing & Risk Engine

Educational Python project focused on the mathematical foundations of fixed income
and interest-rate derivatives.

## Current scope

### Implemented
- Zero-coupon yield curve with annual-effective compounding.
- Discount factors, zero rates and forward rates.
- Linear interpolation of discount factors.
- Fixed-rate bond cash flows and pricing.
- Macaulay duration, modified duration, convexity and DV01.
- Receive-fixed/pay-floating FRA valuation under a single-curve assumption.

### Deliberately not included yet
- Parallel curve sensitivity and key-rate duration.
- Advanced curve interpolation/extrapolation.
- Full market bootstrapping.
- Multi-curve discounting and forwarding.
- Swaps, options, stochastic models and credit products.

These topics can be added when they become part of the learning sequence.
The goal is to keep the code compact and aligned with the theory being studied.

## Conventions and limitations

- Time is measured in years.
- Rates are decimals (e.g. `0.05` means 5%).
- Yield curve spot rates use annual-effective compounding.
- Bond YTM uses nominal annual compounding with the specified coupon frequency.
- FRA uses a simple-compounded forward rate and advance settlement.
- FRA valuation currently uses one curve for both forward projection and discounting.
- Curve interpolation is linear in discount factors.
- `numpy.interp` holds endpoint values outside the curve range; this is not a
  production-quality extrapolation method.

## Run examples

From the project root:

```bash
python -m python.fixed_income.yield_curve
python -m python.fixed_income.bonds
python -m python.derivatives.fra
```

## Dependencies

```bash
pip install numpy
```