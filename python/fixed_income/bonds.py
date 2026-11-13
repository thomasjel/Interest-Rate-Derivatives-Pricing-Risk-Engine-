import numpy as np


def bond_cashflows(face_value, coupon_rate, maturity, frequency=1):
    """
    Generate coupon and principal cash flows.

    coupon_rate is an annual coupon rate in decimal form.
    maturity is in years; frequency is coupon payments per year.
    """
    if face_value <= 0 or maturity <= 0 or frequency <= 0:
        raise ValueError("Face value, maturity and frequency must be positive.")
    if coupon_rate < 0:
        raise ValueError("Coupon rate cannot be negative.")

    periods = int(round(maturity * frequency))
    if not np.isclose(periods, maturity * frequency):
        raise ValueError("Maturity * frequency must be an integer.")

    times = np.arange(1, periods + 1) / frequency
    cashflows = np.full(periods, face_value * coupon_rate / frequency)
    cashflows[-1] += face_value
    return times, cashflows


def bond_price(face_value, coupon_rate, maturity, ytm, frequency=1):
    """Price a fixed-rate bond using a nominal annual YTM compounded at frequency."""
    if frequency <= 0 or 1.0 + ytm / frequency <= 0:
        raise ValueError("Invalid frequency or yield.")

    times, cashflows = bond_cashflows(face_value, coupon_rate, maturity, frequency)
    periods = np.arange(1, len(cashflows) + 1)
    return float(np.sum(cashflows / (1.0 + ytm / frequency) ** periods))


def macaulay_duration(face_value, coupon_rate, maturity, ytm, frequency=1):
    """Macaulay duration in years."""
    times, cashflows = bond_cashflows(face_value, coupon_rate, maturity, frequency)
    periods = np.arange(1, len(cashflows) + 1)
    discount_factors = 1.0 / (1.0 + ytm / frequency) ** periods
    present_values = cashflows * discount_factors
    price = np.sum(present_values)
    return float(np.sum(times * present_values) / price)


def modified_duration(face_value, coupon_rate, maturity, ytm, frequency=1):
    """Modified duration in years, for the stated compounding convention."""
    d_mac = macaulay_duration(
        face_value, coupon_rate, maturity, ytm, frequency
    )
    return float(d_mac / (1.0 + ytm / frequency))


def convexity(face_value, coupon_rate, maturity, ytm, frequency=1):
    """
    Discrete convexity with respect to the nominal annual YTM.

    This definition is consistent with the price formula in bond_price().
    """
    times, cashflows = bond_cashflows(face_value, coupon_rate, maturity, frequency)
    periods = np.arange(1, len(cashflows) + 1)
    base = 1.0 + ytm / frequency
    if base <= 0:
        raise ValueError("Invalid yield for the selected compounding frequency.")

    price = bond_price(face_value, coupon_rate, maturity, ytm, frequency)
    weighted = cashflows * periods * (periods + 1) / (frequency ** 2 * base ** (periods + 2))
    return float(np.sum(weighted) / price)


def dv01(face_value, coupon_rate, maturity, ytm, frequency=1, bump=1e-4):
    """
    Approximate DV01 using a central finite difference.

    Returns the absolute price change for a 1 bp yield move.
    """
    if bump <= 0:
        raise ValueError("Bump must be positive.")

    p_down = bond_price(face_value, coupon_rate, maturity, ytm - bump, frequency)
    p_up = bond_price(face_value, coupon_rate, maturity, ytm + bump, frequency)
    return float(abs(p_down - p_up) / 2.0)


if __name__ == "__main__":
    face = 1000.0
    coupon = 0.08
    maturity = 5
    ytm = 0.08

    price = bond_price(face, coupon, maturity, ytm)
    d_mac = macaulay_duration(face, coupon, maturity, ytm)
    d_mod = modified_duration(face, coupon, maturity, ytm)
    conv = convexity(face, coupon, maturity, ytm)
    risk = dv01(face, coupon, maturity, ytm)

    print(f"Bond price: ${price:,.2f}")
    print(f"Macaulay duration: {d_mac:.4f} years")
    print(f"Modified duration: {d_mod:.4f}")
    print(f"Convexity: {conv:.4f}")
    print(f"DV01: ${risk:,.4f}")
