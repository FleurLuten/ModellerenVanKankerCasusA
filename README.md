# Tumour Growth Modelling

## 1. Introduction

This repository contains a Python package for modelling tumour growth with ordinary differential equations (ODEs). 
The package provides several mathematical growth models and numerical methods for calculating tumour-volume trajectories 
over time. It also contains code for parameter optimisation and model comparison.  
The project was developed for the Dynamic Modelling (ODEs) case study in the Bioinformatics programme at Hanze 
University of Applied Sciences.  
The models are simplified mathematical descriptions of tumour growth. They can be used to explore how different 
assumptions and parameter values affect a predicted growth curve. They should not be interpreted as complete biological 
descriptions of tumour development.

## 2. Repository structure

```text
ModellerenVanKankerCasusA/
├── Data/
│   └── tumorgrowth.xlsx
├── Logboek/
│   ├── Fleur.ipynb
│   ├── Vincent.ipynb
│   └── tumorgrowthlogboek.xlsx
├── tumor_models/
│   ├── __init__.py
│   ├── models.py
│   ├── euler_models.py
│   ├── solver_euler.py
│   ├── solver_heun.py
│   ├── monte_carlo.py
│   ├── optimization.py
│   └── model_comparison.py
├── use_case.ipynb
└── README.md
```

### Package modules

| Module | Purpose |
|---|---|
| `models.py` | Defines the seven tumour growth rate functions. |
| `euler_models.py` | Provides an overview of wrapper functions and a dictionary of models intended for use with the Euler solver. |
| `solver_euler.py` | Implements the Euler method for numerically solving a growth ODE. |
| `solver_heun.py` | Implements the Heun method for numerically solving a growth ODE. |
| `monte_carlo.py` | Contains a random-search procedure that varies model parameters and retains parameter sets that reduce the squared error. |
| `optimization.py` | Contains an alternative random-search implementation and an MSE calculation. |
| `model_comparison.py` | Calculates AIC, AICc and BIC and contains a function for comparing models and solvers using the Monte Carlo routine. |
| `data_loader.py` | Contains a loader for an Excel layout with grouped mouse columns. |

## 3. Installation and requirements

The code is written in Python. The modules use the following third-party packages:
- NumPy
- Pandas
- Matplotlib (for plotting in notebooks)
- Openpyxl (for reading Excel files with Pandas)
- Jupyter Notebook (for running the notebooks)

Install the packages with:
```bash
pip install numpy pandas matplotlib openpyxl jupyter
```

Download or clone the repository and open the project directory in an IDE or terminal. Run notebooks from the project 
root so that relative paths to the `Data` directory resolve as expected.

## 4. Tumour growth models

The models describe the rate of change of tumour volume over time. Their general form is:

`dV/dt = f(V)`

where:

- V is the current tumour volume;
- t is time;
- f(V) is the growth rate defined by the selected model.

The current implementation contains seven models.

### 4.1 Linear growth

dV/dt = c

The tumour volume changes at a constant rate. The growth rate does not depend on the current volume.

### 4.2 Exponential growth

dV/dt = c × V

The growth rate is proportional to the current tumour volume. As the volume increases, the absolute growth rate also increases.

### 4.3 Mendelsohn growth

dV/dt = c × Vᵈ

This model uses an exponent \(d\) to determine how the growth rate depends on tumour volume.

### 4.4 Exponential smooth growth

dV/dt = c × (Vmax − V)

The growth rate decreases as the tumour volume approaches the limiting volume \(V_{\max}\).

### 4.5 Logistic growth

dV/dt = c × V × (Vmax − V)

The growth rate depends on both the current tumour volume and the difference between the current volume and the limiting volume. With positive parameters and an initial volume between zero and \(V_{\max}\), the growth rate decreases as the tumour approaches \(V_{\max}\).

### 4.6 Montroll growth

dV/dt = c × V × (Vmaxᵈ − Vᵈ)

This model includes a limiting-volume term and an exponent \(d\), which changes the shape of the growth curve.

### 4.7 Allee effect growth

dV/dt = c × (V − Vmin) × (Vmax − V)

This model includes a minimum volume \(V_{\min}\) and a maximum volume \(V_{\max}\). The growth rate depends on the position of the current volume relative to these two values.

### Model parameters

| Parameter | Meaning |
|---|---|
| `c` | Growth-rate parameter. |
| `d` | Exponent that affects the relationship between volume and growth rate. |
| `Vmin` | Minimum volume used in the Allee-effect model. |
| `Vmax` | Limiting or maximum volume used in the relevant models. |

The meaning and scale of a parameter depend on the selected model and on the units used for time and tumour volume.

## 5. Numerical ODE solvers

The package contains two numerical methods: the Euler method and the Heun method. 
Both solvers use a selected growth model to estimate tumour volume over a specified time interval.

### 5.1 Euler method

The Euler method estimates the volume at the next time point using the growth rate at the beginning of the time step:

Vₙ₊₁ = Vₙ + Δt × f(Vₙ)

Here, \(V_n\) is the current volume and \(\Delta t\) is the time-step size. The method is straightforward to implement, 
but its accuracy depends on the chosen time step.

### 5.2 Heun method

The Heun method first calculates an Euler prediction and then evaluates the growth rate again at that predicted volume. 
It uses the average of the two growth-rate estimates:

k₁ = f(Vₙ)

k₂ = f(Vₙ + Δt × k₁)

Vₙ₊₁ = Vₙ + (Δt / 2) × (k₁ + k₂)

Because it uses a second growth-rate estimate within each time step, the Heun method can provide a more accurate 
approximation than the basic Euler method for many problems. The accuracy should still be checked for the selected 
model and time step.

## 6. Parameter optimisation

Model parameters determine the shape and scale of the predicted tumour growth curve. 
To compare a model with measured data, parameter values can be adjusted to reduce the difference between measured and 
predicted tumour volumes.  
The repository contains a Monte Carlo random-search implementation in `monte_carlo.py`. 
It starts from supplied parameter values, generates alternative values using random changes, 
and keeps a new parameter set when it produces a lower error.  
The error used by this implementation is the mean squared error (MSE):

MSE = (1/n) × Σ(Vᵢ − V̂ᵢ)²

where:
- \(n\) is the number of measurements;
- \(V_i\) is a measured tumour volume;
- \(\hat V_i\) is the corresponding predicted tumour volume.

A lower MSE means that the predictions are, on average, closer to the measured values in squared-error terms. 
MSE alone does not account for the number of parameters in a model.

**Implementation note:** the current `random_search_monte_carlo` function uses a fixed random step scale of `0.01` 
for each parameter and does not enforce parameter bounds. Its comparison of predictions and measurements also assumes 
that measurement times correspond to indices on the solver's time grid. 
Choose `dt` accordingly and validate the output before interpreting the fitted parameters. 
These implementation details should be reconsidered if the measurement intervals are irregular or parameter scales 
differ substantially.

## 7. Model comparison

A model with a lower MSE does not automatically provide the best overall explanation of the data. \
A model with more parameters may fit the available measurements more closely, but it may also be unnecessarily complex.  
The `model_comparison.py` module provides three information criteria:
- Akaike Information Criterion (AIC);
- corrected Akaike Information Criterion (AICc);
- Bayesian Information Criterion (BIC).

In the current implementation, the criteria are calculated from the model error, 
the number of observations \(n\), and the number of model parameters \(k\):

AIC = n × ln(MSE) + 2k

AICc = n × ln(MSE) + (2kn / (n − k − 1))

BIC = n × ln(MSE) + k × ln(n)

For these criteria, lower values indicate a better trade-off between fit and model complexity when the models are 
evaluated on the same data using a consistent error definition. AICc includes a correction for smaller sample sizes 
and requires \(n>k+1\).  
Differences between information-criterion values can be used to assess how strongly the criteria distinguish between 
candidate models. A difference of approximately two or less is often treated as indicating similar support, rather 
than proof that the models are statistically identical.

## 8. Use case

The `use_case.ipynb` notebook demonstrates how the growth models and numerical solvers can be applied to measured 
tumour-volume data. The aim is to compare the predicted growth curves produced by the seven models and by the Euler 
and Heun solvers, and to identify which combinations describe the selected mouse data most closely.

### 8.1 Dataset and selected mouse

The use case uses the *Tumor Growth Dataset*, contributed by Constantine Daskalakis and available through the 
TSHS Resources Portal. The dataset contains tumour-volume measurements from mice in four treatment groups: 
Control, Drug, Radiation, and Drug + Radiation.  
For this analysis, mouse 101 from the control group was selected. The control group was used to avoid introducing 
an additional treatment variable into this example. Mouse 101 was selected because its measurements are relatively 
evenly distributed over the observation period.  
The notebook loads the Excel dataset and selects the measurement day and the control-group columns for mice 101–108. 
It then extracts the measurement days and tumour volumes for mouse 101. The first measurement is used as the initial 
tumour volume, and the simulation runs from the first to the last measurement day.  
The solver time step (`dt`) is set to one tenth of the smallest interval between consecutive measurements. 
This provides a finer time grid for the numerical calculations.

### 8.2 Model fitting and solver comparison

All seven growth models are evaluated with both numerical solvers:
- Euler method.
- Heun method.

This results in fourteen model-and-solver combinations. For each combination, the notebook uses a Monte Carlo random 
search to adjust the model parameters. The search starts from an initial parameter set, generates new parameter values 
by adding random changes, and keeps a new set when it produces a lower mean squared error (MSE). 
The search stops after 1,000 consecutive attempts without an improvement.  
The MSE is calculated by comparing the measured tumour volumes with the predicted volumes at the corresponding 
measurement times. A lower MSE indicates a closer fit to the selected measurements. The notebook also calculates 
AIC, AICc, and BIC to compare model fit while accounting for the number of parameters.

### 8.3 Results

In the saved run shown in the notebook, the Montroll model with the Euler solver produced the lowest MSE 
(approximately 7,207.79) and the lowest information-criterion values. The Logistic model with the Heun solver was the 
next strongest combination in the saved comparison, with an MSE of approximately 9,344.48. The Montroll model with the 
Heun solver also performed relatively well.  
The information criteria show that the best-scoring combinations are relatively close. For example, the difference 
in BIC between Montroll with Euler (approximately 150.44) and Logistic with Heun (approximately 151.83) is about 1.38. 
A difference of around two or less is commonly interpreted as similar support for the compared models. 
Therefore, the saved results do not provide strong evidence that one of these two combinations is clearly superior.  
The notebook also plots the measured data together with the predicted curves. These plots make it possible to visually 
inspect how well the models follow the observed growth pattern, rather than relying only on the numerical scores.

### 8.4 Interpretation and limitations of the use case

The results suggest that the Logistic and Montroll models describe the growth pattern of mouse 101 better than the other 
models in this particular analysis. Both models include a limiting-volume term, allowing the predicted growth rate to 
decrease as the tumour approaches a maximum volume. This is consistent with the observed curve, which grows more slowly 
at the beginning, increases more rapidly in the middle of the observation period, and then starts to level off.  
The results should be interpreted with care. The Monte Carlo search uses random parameter changes, so the exact fitted 
parameters and scores can differ between runs. In the current notebook implementation, the same fixed 
random step scale (0.01) is used for every parameter, and parameter bounds are not enforced. Some parameter combinations 
can also produce numerical overflow. In addition, the comparison assumes that measurement times correspond to indices 
on the solver's time grid. The time step should therefore be chosen so that the measurement times are represented 
accurately.  
Finally, this use case analyses only one mouse from the control group. The best-performing model for this mouse is not 
necessarily the best model for other mice or treatment groups. The analysis is an example of how the package can be used 
to compare mathematical growth models, not a general conclusion about tumour growth in all mice.


## 9. Limitations

The models in this package are simplified mathematical representations of tumour growth. 
The equations do not explicitly describe all biological processes that may influence tumour development, 
such as tumour heterogeneity, angiogenesis, immune responses or treatment effects.  
The numerical results also depend on the quality and sampling frequency of the data, the selected model, the initial 
parameter values, the optimisation procedure and the solver time step. A good fit to one tumour dataset does not 
necessarily mean that the same model will predict the growth of other tumours accurately.

## 10 References

Used dataset: Constantine Daskalakis, “Tumor Growth Dataset”, TSHS Resources Portal (2016). https://www.causeweb.org/tshs/tumor-growth/.

Murphy H, Jaafari H, Dobrovolny HM. Differences in predictions of ODE models of tumor growth: a cautionary example. 
BMC Cancer. 2016 Feb 26;16:163. doi: 10.1186/s12885-016-2164-x. PMID: 26921070; PMCID: PMC4768423. https://pmc.ncbi.nlm.nih.gov/articles/PMC4768423/

D.R.M. Langers, “Casus Dynamic Modelling (ODEs)” Brightspace, 2025. https://brightspace.hanze.nl/d2l/le/lessons/71129/topics/1040474

The SciPy community, Resampling and Monte Carlo methods tutorials, 2008. https://docs.scipy.org/doc/scipy/tutorial/stats/resampling.html

