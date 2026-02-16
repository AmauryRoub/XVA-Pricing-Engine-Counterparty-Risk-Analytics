# XVA Monte Carlo Pricing Engine

Ce projet implémente un moteur de calcul de **CVA (Credit Valuation Adjustment)** pour un produit dérivé (Option d'achat) en utilisant des simulations de Monte Carlo vectorisées en Python.

## Objectif du Projet
L'objectif est de quantifier le risque de crédit de contrepartie en simulant :
1. La diffusion du facteur de risque de marché (Modèle Black-Scholes).
2. La probabilité de défaut de la contrepartie (via les spreads CDS).
3. L'ajustement de valeur (CVA) résultant de l'exposition positive.

## Mathématiques et Méthodologie
La CVA est calculée via la formule suivante :
$$\text{CVA} = (1 - R) \int_{0}^{T} B(0, t) \cdot \text{EE}(t) \cdot d\text{PD}(0, t)$$

Où :
* $R$ : Taux de recouvrement (Recovery Rate).
* $B(0, t)$ : Facteur d'actualisation.
* $EE(t)$ : Exposition attendue (Expected Exposure).
* $PD$ : Probabilité de défaut cumulée.

## Gestion des Risques & Sensibilités (Greeks)
Le moteur calcule les sensibilités de la CVA pour permettre une gestion active du P&L (Hedging) :
* **Delta CVA** : Sensibilité aux variations du sous-jacent.
* **Vega CVA** : Exposition au régime de volatilité du marché.
* **CS01 (Credit Spread 01)** : Impact d'une variation de 1 point de base du spread de crédit de la contrepartie.

Cette approche par "Bump & Reval" est standard sur les desks de trading pour le pilotage quotidien des risques.

## Fonctionnalités
- **Simulation de trajectoires** : Utilisation de NumPy pour une performance optimale.
- **Modélisation du crédit** : Conversion de spreads CDS en Hazard Rates.
- **Profil d'exposition** : Calcul de l'EE et de la PFE (Potential Future Exposure).

## Installation
```bash
pip install -r requirements.txt
python main.py