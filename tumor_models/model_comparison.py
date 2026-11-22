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


def compare_models(t_data, V_data, models, solvers,
                   start_parameters, dt=1):
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