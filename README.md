# Interest Rate Derivatives Pricing & Risk Engine

**A quantitative framework for interest rate modeling, derivatives pricing, and risk analysis.**

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![C++](https://img.shields.io/badge/C%2B%2B-17-blue)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

## Overview

This project aims to develop a quantitative framework for the construction of interest rate yield curves, pricing of fixed-income instruments and interest rate derivatives, and quantitative risk analysis.

The main objective is to implement financial models from their mathematical foundations, combining analytical methods, numerical techniques, and computational tools.

The project will initially focus on Python for model development, numerical experimentation, and validation, followed by C++17 implementations for computationally intensive components.

## Project Objectives

The framework is designed to cover the following areas:

- **Yield Curve Construction:** Discount factors, zero-coupon rates, forward rates, and bootstrapping methods.
- **Fixed Income Instruments:** Bond valuation, cash flow modeling, and interest rate conventions.
- **Interest Rate Derivatives:** Pricing of Forward Rate Agreements (FRAs), interest rate swaps, caps, floors, and swaptions.
- **Interest Rate Models:** Short-rate models, including Vasicek and Hull–White.
- **Numerical Methods:** Numerical integration, Monte Carlo simulation, and computational optimization.
- **Risk Management:** DV01/PV01, duration, convexity, sensitivity analysis, and stress testing.

## Mathematical Framework

The project will be developed around the following mathematical concepts:

### 1. Yield Curve and Discount Factors

The present value of future cash flows is calculated using discount factors:

\[
P(0)=\sum_{i=1}^{N} CF_i D(0,t_i)
\]

where:

- \(CF_i\) represents the cash flow at time \(t_i\).
- \(D(0,t_i)\) is the discount factor associated with maturity \(t_i\).

Zero-coupon rates and forward rates will be derived from the discount curve using appropriate compounding conventions.

### 2. Interest Rate Derivatives

The framework will incorporate pricing methodologies for interest rate derivatives, including:

- Forward Rate Agreements (FRAs).
- Interest Rate Swaps (IRS).
- Interest Rate Caps and Floors.
- Swaptions.

### 3. Short-Rate Models

Stochastic interest rate models will be implemented to describe the evolution of interest rates.

The initial models will include:

- Vasicek model.
- Hull–White one-factor model.

These models will provide a foundation for analytical pricing and Monte Carlo simulation.

### 4. Quantitative Risk Analysis

Risk measures will be implemented to evaluate the sensitivity of portfolio values to changes in market variables.

The main metrics will include:

- DV01 / PV01.
- Modified duration.
- Convexity.
- Interest rate sensitivity.
- Scenario analysis and stress testing.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Financial modeling and numerical analysis |
| NumPy / SciPy | Numerical computation and optimization |
| Matplotlib | Data visualization |
| C++17 | Computationally efficient implementations |
| Git / GitHub | Version control and project development |
| Pytest | Unit testing and validation |

## Repository Structure

The repository is organized to separate financial models, numerical methods, and testing.

```text
InterestRateDerivatives/
│
├── cpp/
│   ├── yield_curve/
│   ├── instruments/
│   └── pricing/
│
├── python/
│   ├── yield_curve/
│   ├── models/
│   ├── monte_carlo/
│   ├── risk/
│   └── visualization/
│
├── notebooks/
│   └── 01_yield_curves.ipynb
│
├── tests/
│   └── test_yield_curve.py
│
├── README.md
└── requirements.txt
```

*Note: Some directories and modules represent planned development components and will be added progressively.*

## Development Roadmap

| Module | Description | Status |
|---|---|---|
| 01 | Yield Curve Construction | In progress |
| 02 | Fixed Income Instruments and Bootstrapping | Planned |
| 03 | FRAs and Interest Rate Swaps | Planned |
| 04 | Caps, Floors and Swaptions | Planned |
| 05 | Vasicek and Hull–White Models | Planned |
| 06 | Monte Carlo Simulation | Planned |
| 07 | Risk Measures and Sensitivity Analysis | Planned |
| 08 | C++17 Implementation and Optimization | Planned |

## Methodology

The development process will follow a quantitative and computational approach:

1. Derive the mathematical framework behind each financial model.
2. Implement the model using Python.
3. Validate numerical results against analytical solutions and financial no-arbitrage relationships whenever possible.
4. Develop unit tests to ensure numerical consistency.
5. Implement computationally intensive components in C++17.
6. Document assumptions, conventions, and limitations.

## Current Development

The initial implementation focuses on yield curve fundamentals, including:

- Discount factor calculation.
- Zero-coupon rate calculations.
- Forward rate derivation.
- Basic numerical interpolation.

The project is currently under active development.

## Author

**Tomas J. Escamilla Lara**

Physics graduate and PhD researcher at the National Autonomous University of Mexico (UNAM), with interests in quantitative finance, mathematical modeling, numerical methods, and computational finance.

- GitHub: [thomasjel](https://github.com/thomasjel)
- LinkedIn: [Profile](https://www.linkedin.com/in/tomas-j-escamilla-11262b239/)

---

*This project is developed for educational, research, and quantitative finance portfolio purposes. It is not intended as investment advice or a production trading system.*