def exponential(V, c):
    return c * V

def linear(c):
    return c

def mendelsohn(c, V, d):
    return c * V**d

def exponential_smooth(c, V, Vmax):
    return c * (Vmax - V)

def logistic(c, V, Vmax):
    return c * V * (Vmax - V)

def montroll(c, V, d, Vmax):
    return c * V * (Vmax**d - V**d)

def allee_effect(c, V, Vmin, Vmax):
    return c * (V - Vmin) * (Vmax - V)