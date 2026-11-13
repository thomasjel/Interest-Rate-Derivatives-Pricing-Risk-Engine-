from python.fixed_income.yield_curve import YieldCurve


def fra_value(curve, notional, t1, t2, fixed_rate, alpha):
    """
    Value a receive-fixed/pay-floating FRA with advance settlement.

    The floating forward rate is inferred from the supplied discount curve.
    Single-curve assumption: the same curve is used to infer the forward
    and to discount the settlement amount.
    """
    if notional <= 0 or alpha <= 0:
        raise ValueError("Notional and alpha must be positive.")
    if t1 < 0 or t2 <= t1:
        raise ValueError("Require 0 <= t1 < t2.")

    forward = curve.simple_forward_rate(t1, t2, alpha)
    d1 = curve.discount_factor(t1)

    value = (
        notional * alpha * d1
        * (fixed_rate - forward)
        / (1.0 + alpha * forward)
    )
    return float(value)


if __name__ == "__main__":
    curve = YieldCurve(
        maturities=[1, 2, 3, 5, 7, 10],
        spot_rates=[0.04, 0.045, 0.048, 0.051, 0.053, 0.055],
    )

    value = fra_value(
        curve=curve,
        notional=100_000_000,
        t1=1.0,
        t2=2.0,
        fixed_rate=0.08,
        alpha=1.0,
    )

    print("FRA valuation (receive fixed / pay floating)")
    print(f"FRA value: ${value:,.2f}")
