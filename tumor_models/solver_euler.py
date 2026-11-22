# voor de ODE-solvers


def euler_solver(model, V0, t_start, t_end, dt, parameters):
    """
       Bereken de oplossing van een differentiaalvergelijking met behulp van de Euler-methode.

       Parameters
       model = De groeifunctie die de groeisnelheid berekent.
       V0 = Het beginvolume van de tumor.
       t_start = Het starttijdstip van de berekening.
       t_end = Het eindtijdstip van de berekening.
       dt = De grootte van iedere tijdstap.
       parameters =  De parameters die het groeimodel nodig heeft.

       Returns
       times = De tijdstippen waarop het tumorvolume is berekend.
       volumes = De berekende tumorvolumes op ieder tijdstip.
       """
    # Lijsten voor resultaten opslaan en beginwaardes
    times = [t_start]
    volumes = [V0]
    t = t_start
    V = V0

    while t < t_end:
        step = min(dt, t_end - t)

        # Bereken de groeisnelheid met het gekozen groeimodel
        growth = model(V, *parameters)

        # Bereken het nieuwe tumorvolume volgens Euler
        V = V + step * growth

        t = t + step

        times.append(t)
        volumes.append(V)

    return times, volumes
