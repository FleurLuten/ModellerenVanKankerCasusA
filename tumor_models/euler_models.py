# Voor het omzetten van de modellen om het met de Euler methode makkelijker uit te voeren.

from tumor_models.models import (
    mendelsohn_growth,
    exponential,
    linear,
    exponential_smooth,
    logistic,
    montroll,
    allee_effect
)


# Mendelsohn
def mendelsohn_euler(V, c, d):
    return mendelsohn_growth(V, c, d)


# Exponential
def exponential_euler(V, c):
    return exponential(V, c)


# Linear
def linear_euler(V, c):
    return linear(c)


# Exponential smooth
def exponential_smooth_euler(V, c, Vmax):
    return exponential_smooth(c, V, Vmax)


# Logistic
def logistic_euler(V, c, Vmax):
    return logistic(c, V, Vmax)


# Montroll
def montroll_euler(V, c, d, Vmax):
    return montroll(c, V, d, Vmax)


# Allee effect
def allee_effect_euler(V, c, Vmin, Vmax):
    return allee_effect(c, V, Vmin, Vmax)


# Overzicht van alle modellen
EULER_MODELS = {
    "Mendelsohn": mendelsohn_euler,
    "Exponential": exponential_euler,
    "Linear": linear_euler,
    "Exponential smooth": exponential_smooth_euler,
    "Logistic": logistic_euler,
    "Montroll": montroll_euler,
    "Allee effect": allee_effect_euler
}
