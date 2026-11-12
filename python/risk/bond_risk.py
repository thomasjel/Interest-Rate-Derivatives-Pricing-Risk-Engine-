import numpy as np
from python.yield_curve.curve import YieldCurve

# Generate bond cash flows
def bond_cashflows(face_value, coupon_rate, maturity):

    if maturity <= 0 or int(maturity) != maturity:
        raise ValueError("Maturity must be a positive integer.")

    # Annual coupon payments
    coupon = face_value * coupon_rate

    times = np.arange(1, maturity + 1)

    cashflows = np.full(maturity, coupon, dtype=float)

    # Add principal to the final payment
    cashflows[-1] += face_value

    return times, cashflows


# Calculate bond price
def bond_price(face_value, coupon_rate, maturity, ytm):

    if ytm <= -1:
        raise ValueError("YTM must be greater than -100%.")

    times, cashflows = bond_cashflows(
        face_value, coupon_rate, maturity
    )

    # Discount each cash flow
    discounts = 1.0 / (1.0 + ytm) ** times

    return np.sum(cashflows * discounts)

def bond_price_from_curve(face_value, coupon_rate, maturity, curve):

    times, cashflows = bond_cashflows(
        face_value, coupon_rate, maturity
    )

    curve_times = np.insert(curve.maturities, 0, 0.0)
    discounts = np.insert(curve.discount_factors(), 0, 1.0)

    if maturity > curve.maturities[-1]:
        raise ValueError("Curve must cover the bond maturity.")

    bond_discounts = np.interp(
        times, curve_times, discounts
    )

    return np.sum(cashflows * bond_discounts)

# Calculate Macaulay duration
def macaulay_duration(face_value, coupon_rate, maturity, ytm):

    times, cashflows = bond_cashflows(
        face_value, coupon_rate, maturity
    )

    # Calculate present values
    discounts = 1.0 / (1.0 + ytm) ** times
    present_values = cashflows * discounts

    # Calculate bond price
    price = np.sum(present_values)

    # Calculate weighted average payment time
    duration = np.sum(times * present_values) / price

    return duration

# Calculate modified duration
def modified_duration(face_value, coupon_rate, maturity, ytm):

    duration = macaulay_duration(
        face_value, coupon_rate, maturity, ytm
    )

    return duration / (1.0 + ytm)


# Calculate bond convexity
def convexity(face_value, coupon_rate, maturity, ytm):

    times, cashflows = bond_cashflows(
        face_value, coupon_rate, maturity
    )

    discounts = 1.0 / (1.0 + ytm) ** times
    present_values = cashflows * discounts

    price = np.sum(present_values)

    convexity_value = np.sum(
        times * (times + 1) * present_values
        / (1.0 + ytm) ** 2
    ) / price

    return convexity_value


# Calculate DV01
def dv01(face_value, coupon_rate, maturity, ytm):

    price = bond_price(
        face_value, coupon_rate, maturity, ytm
    )

    duration = modified_duration(
        face_value, coupon_rate, maturity, ytm
    )

    return price * duration * 1e-4

# Calculate DV01
def dv01(face_value, coupon_rate, maturity, ytm):

    price = bond_price(
        face_value, coupon_rate, maturity, ytm
    )

    duration = modified_duration(
        face_value, coupon_rate, maturity, ytm
    )

    return price * duration * 1e-4

# Calculate key rate duration
def key_rate_duration(
    face_value,
    coupon_rate,
    maturity,
    curve,
    node_index,
    bump=0.0001
):

    price_0 = bond_price_from_curve(
        face_value, coupon_rate, maturity, curve
    )

    rates_up = curve.spot_rates.copy()
    rates_down = curve.spot_rates.copy()

    rates_up[node_index] += bump
    rates_down[node_index] -= bump

    curve_up = YieldCurve(curve.maturities, rates_up)
    curve_down = YieldCurve(curve.maturities, rates_down)

    price_up = bond_price_from_curve(
        face_value, coupon_rate, maturity, curve_up
    )

    price_down = bond_price_from_curve(
        face_value, coupon_rate, maturity, curve_down
    )

    return -(price_up - price_down) / (2 * price_0 * bump)

def all_key_rate_durations(
    face_value, coupon_rate, maturity, curve
):

    results = {}

    for i, tenor in enumerate(curve.maturities):

        results[tenor] = key_rate_duration(
            face_value,
            coupon_rate,
            maturity,
            curve,
            node_index=i
        )

    return results

def parallel_curve_duration(
    face_value,
    coupon_rate,
    maturity,
    curve,
    bump=0.0001
):

    price_0 = bond_price_from_curve(
        face_value, coupon_rate, maturity, curve
    )

    rates_up = curve.spot_rates + bump
    rates_down = curve.spot_rates - bump

    curve_up = YieldCurve(curve.maturities, rates_up)
    curve_down = YieldCurve(curve.maturities, rates_down)

    price_up = bond_price_from_curve(
        face_value, coupon_rate, maturity, curve_up
    )

    price_down = bond_price_from_curve(
        face_value, coupon_rate, maturity, curve_down
    )

    return -(price_up - price_down) / (2 * price_0 * bump)


# Main execution

if __name__ == "__main__":

    face_value = 1000
    coupon_rate = 0.08
    maturity = 5
    ytm = 0.08

    price = bond_price(face_value, coupon_rate, maturity, ytm)
    macaulay = macaulay_duration(face_value, coupon_rate, maturity, ytm)
    modified = modified_duration(face_value, coupon_rate, maturity, ytm)
    convex = convexity(face_value, coupon_rate, maturity, ytm)
    risk_dv01 = dv01(face_value, coupon_rate, maturity, ytm)

    print(f"Bond price: ${price:,.2f}")
    print(f"Macaulay duration: {macaulay:.4f} years")
    print(f"Modified duration: {modified:.4f}")
    print(f"Convexity: {convex:.4f}")
    print(f"DV01: ${risk_dv01:.4f}")


    # Price sensitivity analysis
    new_ytm = 0.09
    delta_y = new_ytm - ytm

    new_price = bond_price(
        face_value, coupon_rate, maturity, new_ytm
    )

    duration_change = -modified * delta_y

    duration_convexity_change = (
        -modified * delta_y
        + 0.5 * convex * delta_y**2
    )

    print("\nInterest rate shock: +100 bps")
    print(f"Actual new price: ${new_price:,.2f}")
    print(
        f"Duration estimate: "
        f"${price * (1 + duration_change):,.2f}"
    )
    print(
        f"Duration + convexity estimate: "
        f"${price * (1 + duration_convexity_change):,.2f}"
    )


    from python.yield_curve.curve import YieldCurve

    maturities = [1, 2, 3, 5, 7, 10]
    spot_rates = [0.04, 0.045, 0.048, 0.051, 0.053, 0.055]

    curve = YieldCurve(maturities, spot_rates)

    curve_price = bond_price_from_curve(
        face_value, coupon_rate, maturity, curve
    )

    krds = all_key_rate_durations(
        face_value, coupon_rate, maturity, curve
    )

    print("\nCurve-based bond valuation")
    print(f"Bond price: ${curve_price:,.2f}")

    print("\nKey Rate Durations")
    for tenor, value in krds.items():
        print(f"{tenor:>4.0f}Y: {value:.6f}")

parallel_duration = parallel_curve_duration(
    face_value, coupon_rate, maturity, curve
)

print(f"\nParallel curve duration: {parallel_duration:.6f}")
print(f"Sum of KRDs: {sum(krds.values()):.6f}")