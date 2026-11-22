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
