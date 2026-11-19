# voor de modellen/formules

def mendelsohn_growth(V, c, d):
    """
    Mendelsohn groeimodel.

    V = huidig tumorvolume
    c = groeiparameter
    d = exponent
    """
    return c * V**d

def exponential(V, c):
    """
    Exponentiële groeimodel.

    V = huidig tumorvolume
    c = groeiparameter
    """
    return c * V

def linear(c):
    """
    Lineaire groeimodel.

    c = groeiparameter
    """
    return c

def exponential_smooth(c, V, Vmax):
    """
    Exponentële afvlakkende groeimodel.

    V = huidig tumorvolume
    c = groeiparameter
    Vmax = maximale tumorvolume
    """
    return c * (Vmax - V)

def logistic(c, V, Vmax):
    """
    Logistische groeimodel.

    V = huidig tumorvolume
    c = groeiparameter
    Vmax = maximale tumorvolume
    """
    return c * V * (Vmax - V)

def montroll(c, V, d, Vmax):
    """
    Mendelsohn groeimodel.

    V = huidig tumorvolume
    c = groeiparameter
    Vmax = maximale tumorvolume
    d = exponent
    """
    return c * V * (Vmax**d - V**d)

def allee_effect(c, V, Vmin, Vmax):
    """
    Mendelsohn groeimodel.

    V = huidig tumorvolume
    c = groeiparameter
    d = exponent
    Vmax = maximale tumorvolume
    Vmin = minimale tumorvolume
    """
    return c * (V - Vmin) * (Vmax - V)