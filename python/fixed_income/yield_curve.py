import numpy as np


class YieldCurve:
    """
    Curva de tasas cero cupón con capitalización efectiva anual.

    Convenciones:
    - maturities: vencimientos expresados en años.
    - spot_rates: tasas cero cupón en formato decimal.
    - discount factors: D(0,t) = 1 / (1 + z(t))**t.
    - Interpolación lineal de factores de descuento.
    """

    def __init__(self, maturities, spot_rates):
        self.maturities = np.asarray(maturities, dtype=float)
        self.spot_rates = np.asarray(spot_rates, dtype=float)

        if self.maturities.ndim != 1 or self.spot_rates.ndim != 1:
            raise ValueError("Maturities and spot_rates must be one-dimensional.")

        if len(self.maturities) == 0 or len(self.maturities) != len(self.spot_rates):
            raise ValueError("Maturities and spot_rates must have equal non-zero length.")

        if np.any(self.maturities <= 0):
            raise ValueError("Maturities must be positive.")

        if np.any(np.diff(self.maturities) <= 0):
            raise ValueError("Maturities must be strictly increasing.")

        if np.any(1.0 + self.spot_rates <= 0):
            raise ValueError("Spot rates must be greater than -100%.")

    def discount_factors(self):
        """Return D(0,t) using annual-effective compounding."""
        return 1.0 / (1.0 + self.spot_rates) ** self.maturities

    def zero_rates(self):
        """Recover annual-effective zero rates from discount factors."""
        discounts = self.discount_factors()
        return discounts ** (-1.0 / self.maturities) - 1.0

    def discount_factor(self, t):
        """
        Interpolate D(0,t) linearly.

        np.interp holds endpoint values outside the supplied maturity range.
        This endpoint behavior is only a temporary educational convention,
        not a market-standard extrapolation method.
        """
        if t < 0:
            raise ValueError("Maturity must be non-negative.")
        if t == 0:
            return 1.0

        maturities = np.insert(self.maturities, 0, 0.0)
        discounts = np.insert(self.discount_factors(), 0, 1.0)
        return float(np.interp(t, maturities, discounts))

    def forward_rate(self, t1, t2):
        """
        Return the annual-effective forward rate for [t1,t2].
        """
        if t1 < 0 or t2 <= t1:
            raise ValueError("Require 0 <= t1 < t2.")

        d1 = self.discount_factor(t1)
        d2 = self.discount_factor(t2)
        return (d1 / d2) ** (1.0 / (t2 - t1)) - 1.0

    def simple_forward_rate(self, t1, t2, alpha):
        """
        Return the simple-compounded forward rate for [t1,t2].

        alpha is the contractual year fraction, which need not equal t2-t1.
        """
        if t1 < 0 or t2 <= t1 or alpha <= 0:
            raise ValueError("Require t1 >= 0, t2 > t1 and alpha > 0.")

        d1 = self.discount_factor(t1)
        d2 = self.discount_factor(t2)
        return (d1 / d2 - 1.0) / alpha


if __name__ == "__main__":
    curve = YieldCurve(
        maturities=[1, 2, 3, 5, 7, 10],
        spot_rates=[0.04, 0.045, 0.048, 0.051, 0.053, 0.055],
    )

    print("Discount factors:", curve.discount_factors())
    print("Zero rates:", curve.zero_rates())
    print(f"Annual-effective forward (1Y-2Y): {curve.forward_rate(1, 2):.4%}")
    print(f"Simple forward (1Y-2Y): {curve.simple_forward_rate(1, 2, 1.0):.4%}")
