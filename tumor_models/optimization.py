
import numpy as np
from random import gauss
from tumor_models.solver_euler import euler_solver


def bereken_mse(model, parameters, V0, t_start, meetdagen, meetwaarden, dt=0.1):

    try:
        # De Euler-methode uitvoeren met de opgegeven parameters
        with np.errstate(over="ignore", invalid="ignore"):
            times, volumes = euler_solver(
                model=model,
                V0=V0,
                t_start=t_start,
                t_end=max(meetdagen),
                dt=dt,
                parameters=parameters
            )

            # De voorspelde tumorgroottes omzetten naar NumPy-arrays
            volumes = np.array(volumes, dtype=float)
            meetwaarden = np.array(meetwaarden, dtype=float)

            # Controleren of de voorspellingen geldige getallen zijn
            if not np.all(np.isfinite(volumes)):
                return float("inf")

            # Extreem grote voorspellingen afwijzen
            if np.any(np.abs(volumes) > 1e100):
                return float("inf")

            # De voorspelde tumorgrootte bepalen op de dagen waar metingen zijn gedaan
            voorspellingen = np.interp(meetdagen, times, volumes)

            # Het verschil tussen de metingen en voorspellingen berekenen
            verschillen = meetwaarden - voorspellingen

            # De Mean Squared Error berekenen
            mse = np.mean(verschillen ** 2)

            # Controleren of de MSE een geldig getal is
            if not np.isfinite(mse):
                return float("inf")

            return mse

    # Ongeldige berekeningen afwijzen
    except (ValueError, OverflowError, ZeroDivisionError):
        return float("inf")



def random_search(
    model,
    start_parameters,
    stapgroottes,
    V0,
    t_start,
    meetdagen,
    meetwaarden,
    dt=0.1,
    max_tries=1000,
    grenzen=None
):
    """
    Zoekt naar parameterwaarden met een zo laag mogelijke MSE.
    """

    # Startwaarden bewaren
    parameters = dict(start_parameters)

    # Begin-MSE berekenen
    mse = bereken_mse(
        model,
        tuple(parameters.values()),
        V0,
        t_start,
        meetdagen,
        meetwaarden,
        dt
    )

    beste_parameters = parameters.copy()
    beste_mse = mse

    tries = 0

    while tries < max_tries:
        tries += 1

        # Nieuwe parameters maken met willekeurige veranderingen
        nieuwe_parameters = {
            naam: waarde + gauss(0, stapgroottes[naam])
            for naam, waarde in parameters.items()
        }

        # Eventuele parametergrenzen controleren
        if grenzen is not None:
            geldig = all(
                grenzen[naam][0] <= waarde <= grenzen[naam][1]
                for naam, waarde in nieuwe_parameters.items()
            )

            if not geldig:
                continue

        nieuwe_mse = bereken_mse(
            model,
            tuple(nieuwe_parameters.values()),
            V0,
            t_start,
            meetdagen,
            meetwaarden,
            dt
        )

        # Alleen betere parameters bewaren
        if nieuwe_mse < mse:
            parameters = nieuwe_parameters
            mse = nieuwe_mse

            beste_parameters = parameters.copy()
            beste_mse = mse

            # Opnieuw tellen na een verbetering
            tries = 0

    return beste_parameters, beste_mse

