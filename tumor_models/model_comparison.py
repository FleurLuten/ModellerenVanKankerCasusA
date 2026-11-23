# Dit is voor alles uit workshop 4

from math import log
from .monte_carlo import random_search_monte_carlo


def calculate_aic(error, n, k):
    """
    Bereken de AIC

    Parameters
    error = De gemiddelde kwadraat fout van het model
    n = Het aantal meetingen
    k = Het aantal parameters van het model

    Returns
    aic = De berekende AIC waarde
    """
    return n * log(error) + 2 * k


def calculate_aicc(error, n, k):
    """
    Bereken de corrected AICc

    Parameters
    error = De gemiddelde kwadraar fout van het model
    n = Het aantal meetingen
    k = Het aantal parameters van het model

    Returns
    aicc = De berekende AICc waarde.
    """
    return n * log(error) + (2 * k * n) / (n - k - 1)


def calculate_bic(error, n, k):
    """
    Bereken de BIC

    Parameters
    error = De gemiddelde kwadraat fout van het model
    n = Het aantal meetingen
    k = Het aantal parameters van het model

    Returns
    bic = De berekende BIC waarde
    """
    return n * log(error) + k * log(n)


def compare_models(t_data, V_data, models, solvers, start_parameters, dt=1):
    """
    Vergelijk de verschillende tumorgroeimodellen en solvers

    Parameters
    models = Dictionary met de namen en groeifuncties
    solvers = Dictionary met de namen en solvers
    t_data = De tijdstippen van de gemeten tumorvolumes
    V_data = De gemeten tumorvolumes
    start_parameters = Dictionary met beginparameters van elk groeimodel
    dt = De grootte van iedere tijdstap

    Returns
    results = Een lijst met de fout, parameters en vergelijkingsscores van iedere combinatie van groeimodel en solver
    """

    results = []
    n = len(t_data)

    for model_name, model in models.items():
        for solver_name, solver in solvers.items():
            error, params = random_search_monte_carlo(t_data, V_data, model, solver, dt,**start_parameters[model_name])
            k = len(params)

            if error > 0:
                aic = calculate_aic(error, n, k)
                aicc = calculate_aicc(error, n, k)
                bic = calculate_bic(error, n, k)
            else:
                aic = None
                aicc = None
                bic = None

            results.append({"model": model_name, "solver": solver_name, "error": error, "parameters": params,
            "AIC": aic, "AICc": aicc, "BIC": bic})

    return results

import numpy as np


def bereken_informatiecriteria(mse, n, k):
    """
    Berekent de AIC, AICc en BIC voor een groeimodel.

    mse = Mean Squared Error van het model
    n = aantal meetpunten
    k = aantal modelparameters
    """

    # Controleren of de MSE geldig is
    if not np.isfinite(mse) or mse <= 0:
        raise ValueError("De MSE moet een positief, eindig getal zijn.")

    # Controleren of er genoeg meetpunten zijn voor AICc
    if n <= k + 1:
        raise ValueError("Er zijn te weinig meetpunten voor de AICc.")

    # BIC berekenen
    bic = n * np.log(mse) + k * np.log(n)

    # AIC berekenen
    aic = n * np.log(mse) + 2 * k

    # AICc berekenen volgens de formule uit workshop 4
    aicc = n * np.log(mse) + (2 * k * n) / (n - k - 1)

    # De drie criteria teruggeven
    return aic, aicc, bic