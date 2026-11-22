# Voor de andere ode solver


def heun_solver(model, V0, t_start, t_end, dt, parameters):
    """
    Bereken de oplossing van een differentiaalvergelijking met behulp van de Heun-methode

    Parameters
    model = De groeifunctie die de groeisnelheid berekent
    V0 = Het beginvolume van de tumor
    t_start = Het starttijdstip van de berekening
    t_end = Het eindtijdstip van de berekening
    dt = De grootte van iedere tijdstap
    parameters = De parameters die het groeimodel nodig heeft

    Returns
    times = De tijdstippen waarop het tumorvolume is berekend
    volumes = De berekende tumorvolumes op ieder tijdstip
    """

    t = t_start
    V = V0
    times = [t]
    volumes = [V]

    while t < t_end:
        step = min(dt, t_end - t)

        growth1 = model(V, *parameters)
        t1 = t + step
        V1 = V + growth1 * step
        growth2 = model(V1, *parameters)

        t = t + step

        V = V + (growth1 + growth2) / 2 * step


        times.append(t)
        volumes.append(V)

    return times, volumes