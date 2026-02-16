import numpy as np
import matplotlib.pyplot as plt
from src.models import MarketModel, CreditModel
from src.engine import simulate_paths
from src.xva_metrics import compute_exposure, calculate_cva
from src.xva_metrics import calculate_sensitivities

# 1. Configuration des paramètres
S0, K, T, R, SIGMA = 100, 100, 1.0, 0.03, 0.2
CDS_SPREAD = 0.02 # 200 bps
N_SIMS = 10000
STEPS = 252

# 2. Instanciation des modèles
market = MarketModel(S0, R, SIGMA)
credit = CreditModel(CDS_SPREAD)

# 3. Simulation & Calculs
print(f"Simulation de {N_SIMS} trajectoires...")
paths = simulate_paths(market, T, STEPS, N_SIMS)
exposures = compute_exposure(paths, K)
cva_value, ee_profile = calculate_cva(exposures, credit, T, R)


print(f"CVA calculée : {cva_value:.4f}")

print("\n--- Analyse de Sensibilité (Grecques XVA) ---")
sensies = calculate_sensitivities(market, credit, T, STEPS, N_SIMS, K)

for greek, value in sensies.items():
    print(f"{greek}: {value:.6f}")

print("\nInterprétation :")
print(f"Si le spread de crédit de la contrepartie s'élargit de 10bps, "
      f"votre P&L XVA impactera le desk de {sensies['CS01 (1bps)'] * 10:.4f} EUR.")

# 4. Visualisation (Profil d'exposition)
plt.figure(figsize=(10, 6))
plt.plot(ee_profile, label='Expected Exposure (EE)')
plt.fill_between(range(STEPS+1), ee_profile, alpha=0.3)
plt.title("Profil d'Exposition Attendue (EE) sur 1 an")
plt.xlabel("Pas de temps (jours)")
plt.ylabel("Exposition")
plt.legend()
plt.grid(True)
plt.show()