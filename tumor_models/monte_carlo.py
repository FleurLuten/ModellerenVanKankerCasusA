# De monte carlo voor optimisatie

from random import gauss


def random_search_monte_carlo(t_data, V_data, model, solver, dt=1, **start_params):
    """
    Bepaal de beste parameters voor een groeimodel met behulp van monte carlo

    Parameters
    t_data = De tijdstippen van de gemeten tumorvolumes
    V_data = De gemeten tumorvolumes
    model = Het groeimodel dat gebruikt wordt
    solver = De solver methode die gebruikt wordt (Heun/Euler)
    dt = De grootte van iedere tijdstap
    **start_params = De beginwaarden van de parameters van het groeimodel

    Returns
    error = De gemiddelde kwadraat fout tussen de gemeten en berekende tumorvolumes
    params = De parameters die de kleinste fout opleverden
    """

    params = start_params.copy()
    parameters = list(params.values())

    times, predicted_volumes = solver(model, V_data[0], t_data[0], t_data[-1], dt, parameters)
    error = 0

    for i in range(len(t_data)):
        index = int(round((t_data[i] - t_data[0]) / dt))
        difference = V_data[i] - predicted_volumes[index]
        error += difference ** 2

    error = error / len(t_data)
    tries = 0

    while tries < 1000:
        tries += 1
        new_params = {
            key: val + gauss(0, 0.01)
            for key, val in params.items()}
        new_parameters = list(new_params.values())
        times, predicted_volumes = solver(model, V_data[0], t_data[0], t_data[-1], dt, new_parameters)
        new_error = 0

        for i in range(len(t_data)):
            index = int(round((t_data[i] - t_data[0]) / dt))
            difference = V_data[i] - predicted_volumes[index]
            new_error += difference ** 2

        new_error = new_error / len(t_data)

        if new_error < error:
            params = new_params
            error = new_error
            tries = 0

    return error, params