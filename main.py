from tumor_models.data_loader import load_tumor_data
from tumor_models.models import (linear, exponential, mendelsohn_growth, exponential_smooth, logistic, montroll, allee_effect)
from tumor_models.solver_heun import heun_solver
from tumor_models.solver_euler import euler_solver
from tumor_models.model_comparison import compare_models


models = {
    "Linear": linear,
    "Exponential": exponential,
    "Mendelsohn": mendelsohn_growth,
    "Exponential smooth": exponential_smooth,
    "Logistic": logistic,
    "Montroll": montroll,
    "Allee": allee_effect
    }

solvers = {"Heun": heun_solver, "Euler": euler_solver}


def get_start_parameters(model_name, times, volumes):
    """
    Bepaal beginwaarden voor de parameters van een groeimodel.
    """

    V0 = volumes[0]
    growth_rate = (volumes[-1] - volumes[0]) / (times[-1] - times[0])

    Vmax = max(volumes) * 1.5
    Vmin = min(volumes) * 0.5

    if model_name == "Linear":
        return {"c": growth_rate}

    elif model_name == "Exponential":
        return {"c": growth_rate / V0}

    elif model_name == "Mendelsohn":
        d = 1.0
        return {"c": growth_rate / (V0 ** d), "d": d}

    elif model_name == "Exponential smooth":
        return {"c": growth_rate / (Vmax - V0), "Vmax": Vmax}

    elif model_name == "Logistic":
        return {"c": growth_rate / (V0 * (Vmax - V0)), "Vmax": Vmax}

    elif model_name == "Montroll":
        d = 1.0
        return {
            "c": growth_rate / (V0 * (Vmax ** d - V0 ** d)),
            "d": d,
            "Vmax": Vmax}

    elif model_name == "Allee":
        return {
            "c": growth_rate / ((V0 - Vmin) * (Vmax - V0)),
            "Vmin": Vmin,
            "Vmax": Vmax}


def main():
    tumor_data = load_tumor_data("Data/tumorgrowth.xlsx")
    for group, mice in tumor_data.items():
        print("\nBehandelgroep:", group)
        for mouse, measurements in mice.items():
            times = measurements["times"]
            volumes = measurements["volumes"]
            print("\nMuis:", mouse)
            start_parameters = {}

            for model_name in models:
                start_parameters[model_name] = get_start_parameters(
                    model_name, times, volumes)

            results = compare_models(
                times,
                volumes,
                models,
                solvers,
                start_parameters)

            for result in results[:3]:
                print(result["model"], result["solver"], "AICc:", result["AICc"], "AIC:", result["AIC"], "BIC:", result["BIC"])

if __name__ == "__main__":
    main()