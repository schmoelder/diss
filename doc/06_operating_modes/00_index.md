---
jupytext:
  formats: md:myst,py:percent
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
execution:
  timeout: 600
---

```{code-cell} ipython3
:tags: [remove-cell]

import sys
from pathlib import Path

from git import Repo

# Set up working directory
diss_root = Path(Repo(search_parent_directories=True).working_dir)
studies_root = diss_root / "studies" / "operating_modes"
studies_root.mkdir(parents=True, exist_ok=True)

# Import the run_all module
sys.path.insert(0, str(studies_root))
from run_all import setup_studies, setup_cases

# Fetch all data
studies = setup_studies(studies_root)

cases = {
    name: setup_cases(study, debug=True, push=False)
    for name, study in studies.items()
}

for study, study_cases in cases.items():
    print(study)
    for name, case in study_cases.items():
        case.load()
```

(operating_modes)=
# Optimization of advanced operating concepts

To demonstrate the application and capabilities of the framework, several case studies were conducted.
The scripts to recreate the simulations and optimizations reported below can be found in the supplementary material and online: (@TODO: add links)
In the case studies, preparative separations of mixtures with two or three components were considered using processes of different complexity and different optimization variables.
In all cases, a lumped rate model with pores (see {numref}`lumped_rate_model_without_pores`) with competitive Langmuir binding (see {numref}`langmuir_model`) in rapid equilibrium.
All processes are run in flow-through mode and the solvent does not have any impact on the binding.
The parameters used are summarized in {numref}`model_parameters`.
With the applied moderately nonlinear conditions and an axial dispersion coefficient that corresponds to several theoretical stages of around 400 and 2000, respectively, the separation difficulty of the examples can be regarded as “modest” (@TODO: check number).
Independent of this, the optimization of such processes is always challenging, even for simple separations.
For all optimization cases, the pymoo package (@TODO:cite) with a non-dominated sorting genetic algorithm was used.


```{table} Parameters of column geometry, mass transport and binding of the model molecules ($i \in \{A, B\}$).
:name: model_parameters
:align: center

| Catalog       | Symbol          | Description               | Value                | Unit                                   |
| ------------- | --------------- | ------------------------- | -------------------- | -------------------------------------- |
| **Geometry**  | $L$             | Column length             | $0.6$                | $\text{m}$                             |
|               | $d$             | Column diameter           | $0.024$              | $\text{m}$                             |
|               | $d_r$           | Particle radius           | $1.0 \times 10^{-5}$ | $\text{m}$                             |
|               | $\varepsilon_b$ | Bed porosity              | $0.3$                | –                                      |
|               | $\varepsilon_p$ | Particle porosity         | $0.6$                | –                                      |
| **Transport** | $D_{ax,i}$      | Axial dispersion coeff.   | $1.0 \times 10^{-6}$ | $\text{m}^{2}~\text{s}^{-1}$           | 
|               | $k_{f,i}$       | Film mass transfer coeff. | $1.0 \times 10^{-3}$ | $\text{m}~\text{s}^{-1}$               |
| **Binding**   | $k_{eq,i}$      | Equilibrium constant      | $[0.02, 0.03]$       | $\text{m}^{3}~\text{mol}^{-1}$         |
|               | $q_{max,i}$     | Saturation capacities     | $[100, 100]$         | $\text{mol}~\text{m}_{\text{sp}}^{-1}$ |
| **Process**   | $Q$             | Flow rate                 | $[0.01, 0.05]$       | $\text{m}^{3}~\text{s}^{-1}$           |
```

To validate the processes, equilibrium theory is applied.
An equivalent lumped rate model without pores but with the same total porosity is used.
The equations are solved using an independent implementation of the analytic solution described in {cite}`Siitonen2011`.
