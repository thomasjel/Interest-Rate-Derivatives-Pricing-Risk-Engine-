import numpy as np


class YieldCurve:
    """
    Convention:
        Annual compounding for spot rates.
        Time expressed in years.
    """

    def __init__(self, maturities, spot_rates):

        self.maturities = np.asarray(maturities, dtype=float)
        self.spot_rates = np.asarray(spot_rates, dtype=float)

        if len(self.maturities) != len(self.spot_rates):
            raise ValueError("Maturities and rates must have equal length.")

        if np.any(self.maturities <= 0):
            raise ValueError("Maturities must be positive.")

        if np.any(np.diff(self.maturities) <= 0):
            raise ValueError("Maturities must be strictly increasing.")

    def discount_factors(self):

        return 1.0 / (1.0 + self.spot_rates) ** self.maturities

    def zero_rates(self):

        discounts = self.discount_factors()

        return discounts ** (-1.0 / self.maturities) - 1.0

    def forward_rate(self, t1, t2):

        if t1 < 0 or t2 <= t1:
            raise ValueError("Require 0 <= t1 < t2.")

        discounts = self.discount_factors()

        d1 = np.interp(
            t1,
            np.insert(self.maturities, 0, 0.0),
            np.insert(discounts, 0, 1.0)
        )

        d2 = np.interp(
            t2,
            np.insert(self.maturities, 0, 0.0),
            np.insert(discounts, 0, 1.0)
        )

        return (d1 / d2) ** (1.0 / (t2 - t1)) - 1.0


if __name__ == "__main__":

    maturities = [1, 2, 3, 5, 7, 10]
    spot_rates = [0.04, 0.045, 0.048, 0.051, 0.053, 0.055]

    curve = YieldCurve(maturities, spot_rates)

    print("Discount factors:")
    print(curve.discount_factors())

    print("\nSpot rates:")
    print(curve.zero_rates())

    print("\nForward rate (1Y-2Y):")
    print(curve.forward_rate(1, 2))
