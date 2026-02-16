import numpy as np

def simulate_paths(model, T, steps, n_sims):
    """Génère des trajectoires de prix via Monte Carlo."""
    dt = T / steps
    # Simulation vectorisée (beaucoup plus rapide qu'une boucle for)
    Z = np.random.standard_normal((steps, n_sims))
    
    paths = np.zeros((steps + 1, n_sims))
    paths[0] = model.s0
    
    for t in range(1, steps + 1):
        paths[t] = paths[t-1] * np.exp(
            (model.r - 0.5 * model.sigma**2) * dt + 
            model.sigma * np.sqrt(dt) * Z[t-1]
        )
    return paths