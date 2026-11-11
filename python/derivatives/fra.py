import numpy as np


def fra_value(curve, notional, t1, t2, fixed_rate, alpha):

    # Obtener factores de descuento
    discounts = curve.discount_factors()
    maturities = np.insert(curve.maturities, 0, 0.0)
    discounts = np.insert(discounts, 0, 1.0)

    d1 = np.interp(t1, maturities, discounts)
    d2 = np.interp(t2, maturities, discounts)

    # Calcular tasa forward simple
    forward = (d1 / d2 - 1.0) / alpha

    # Valuar FRA: recibir fijo y pagar flotante
    value = (
        notional * alpha * d1 *
        (fixed_rate - forward) /
        (1.0 + alpha * forward)
    )
    return value, forward    


if __name__ == "__main__":

    from python.yield_curve.curve import YieldCurve

    # Construir curva
    maturities = [1, 2, 3, 5, 7, 10]
    spot_rates = [0.04, 0.045, 0.048, 0.051, 0.053, 0.055]

    curve = YieldCurve(maturities, spot_rates)

    # Parámetros del FRA
    notional = 100_000_000
    t1 = 1.0
    t2 = 2.0
    alpha = 1.0
    fixed_rate = 0.08

    # Calcular valor
    value, forward = fra_value(
        curve, notional, t1, t2, fixed_rate, alpha
    )

    print("FRA valuation")
    print(f"Fixed rate: {fixed_rate:.2%}")
    print(f"Forward rate: {forward:.2%}")
    print(f"FRA value: ${value:,.2f}")
