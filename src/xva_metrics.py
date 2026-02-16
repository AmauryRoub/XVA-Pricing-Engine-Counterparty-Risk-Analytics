import numpy as np

def compute_exposure(paths, strike):
    """Calcule l'exposition positive (MtM+) à chaque instant."""
    # Pour un Call : max(S - K, 0)
    return np.maximum(paths - strike, 0)

def calculate_cva(exposure_paths, credit_model, T, r):
    """Calcule la CVA par intégration numérique."""
    steps = exposure_paths.shape[0] - 1
    dt = T / steps
    time_grid = np.linspace(0, T, steps + 1)
    
    # EE : Expected Exposure (Moyenne des expositions positives à chaque pas de temps)
    expected_exposure = np.mean(exposure_paths, axis=1)
    
    cva = 0
    for t_idx in range(1, steps + 1):
        t = time_grid[t_idx]
        # Actualisation (Discounting)
        df = np.exp(-r * t)
        # Probabilité de défaut sur l'intervalle [t-dt, t]
        pd = credit_model.survival_probability(t - dt) - credit_model.survival_probability(t)
        # Somme CVA
        cva += (1 - credit_model.recovery_rate) * df * expected_exposure[t_idx] * pd
        
    return cva, expected_exposure


def calculate_sensitivities(market_model, credit_model, T, steps, n_sims, strike):
    """Calcule le Delta, Vega et CS01 de la CVA."""
    
    def get_cva(m_mod, c_mod):
        paths = simulate_paths(m_mod, T, steps, n_sims)
        exposures = np.maximum(paths - strike, 0)
        cva_val, _ = calculate_cva(exposures, c_mod, T, m_mod.r)
        return cva_val

    # 1. Delta (Sensibilité à S0)
    bump_s = market_model.s0 * 0.01 # Bump de 1%
    m_up = MarketModel(market_model.s0 + bump_s, market_model.r, market_model.sigma)
    m_down = MarketModel(market_model.s0 - bump_s, market_model.r, market_model.sigma)
    delta_cva = (get_cva(m_up, credit_model) - get_cva(m_down, credit_model)) / (2 * bump_s)

    # 2. Vega (Sensibilité à Sigma)
    bump_vol = 0.01 # Bump de 1% vol
    m_vol_up = MarketModel(market_model.s0, market_model.r, market_model.sigma + bump_vol)
    vega_cva = (get_cva(m_vol_up, credit_model) - get_cva(market_model, credit_model)) / bump_vol

    # 3. CS01 (Sensibilité au Credit Spread)
    bump_cds = 0.0001 # 1 point de base (bps)
    c_up = CreditModel(credit_model.cds_spread + bump_cds, credit_model.recovery_rate)
    cs01_cva = (get_cva(market_model, c_up) - get_cva(market_model, credit_model))

    return {"Delta": delta_cva, "Vega": vega_cva, "CS01 (1bps)": cs01_cva}