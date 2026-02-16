import numpy as np

class MarketModel:
    """Simule le prix d'un actif sous Black-Scholes."""
    def __init__(self, s0, r, sigma):
        self.s0 = s0
        self.r = r
        self.sigma = sigma

class CreditModel:
    """Gère les probabilités de défaut à partir des spreads CDS."""
    def __init__(self, cds_spread, recovery_rate=0.4):
        self.cds_spread = cds_spread
        self.recovery_rate = recovery_rate
        # Intensité de défaut (Hazard Rate) λ ≈ Spread / (1 - R)
        self.hazard_rate = cds_spread / (1 - recovery_rate)

    def survival_probability(self, t):
        """Probabilité que la contrepartie soit encore en vie à l'instant t."""
        return np.exp(-self.hazard_rate * t)

    def default_density(self, t):
        """Probabilité de défaut entre t et t+dt."""
        return self.hazard_rate * np.exp(-self.hazard_rate * t)