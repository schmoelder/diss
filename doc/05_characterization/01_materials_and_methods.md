---
jupytext:
  formats: md:myst,py:percent
  main_language: python
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3
  name: python3
execution:
  timeout: 600
---

```{code-cell} ipython3
:tags: [remove-cell]

from pathlib import Path
import sys

from git import Repo
from myst_nb import glue
%config InlineBackend.figure_format = 'retina'

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
sys.path.insert(0, str(diss_root / "studies" / "parameter_estimation" ))
sys.path.insert(0, str(diss_root / "studies" / "parameter_estimation" / "parameter_estimation" ))
```

(materials_and_methods)=
# Materials and methods

All experiments were conducted by Lukas Thiel at the laboratory of Institute of Fluid Process Engineering at RWTH Aachen.
The chromatography system used in this thesis is a *Knauer* system. @TODO: Which model?
{numref}`knauer_pid` shows the process and instrumentation diagram of the *Knauer* chromatography system used in this work.
The system consists of two buffer flasks ($A$ and $B$) with different salt concentrations.
Each buffer is connected to a pump via tubing.
Both pumps are further connected to a static mixer.
The valve is equipped with a $50~\text{mL}$ sample loop to inject a well-defined amount of sample into the system.
The valve is connected to a *SP Sepharose HP* column.
The column is a strong cation exchanger with an $\ce{SO_3}^{-}$ functional group and a column volume (CV) of $4.7~\text{mL}$.
The average particle size, $d50v$, is provided by the manufacturer *Cytiva* as $34~\text{µm}$, with an ionic capacity between $0.15$ and $0.2~\text{mmol}~\ce{H}^{+}~\text{mL}_{\text{packed bed}}^{-1}$.
The column outlet is connected to a UV detector which measures the absorbance at $280~\text{nm}$ to detect tracer and protein.
The outlet of the UV sensor is connected to a conductivity sensor to measure ionic strength.
The outflow of the system is then sent to a waste flask.
A computer is connected to the system with the software *PurityChrom 5* to operate the system, capture, process, and view the measured data {cite}`PurityChrom5`.
All internal tubing has an inner diameter of $0.75~\text{mm}$.
All experiments were conducted at $0.5~\text{mL}~\text{min}^{-1}$.

```{figure} ./figures/knauer_pid.png
:name: knauer_pid

P&ID of Knauer system.
```

Acetone and Blue Dextran $2000~\text{kDa}$ were used as tracers in this thesis, along with lysozyme from chicken egg white with a molar weight of $14.3~\text{kDa}$.
The buffers consist of a low salt buffer $A$ with $20~\text{mM}$ sodium acetate ($\ce{C_2H_3NaO_2}$), whereas the high salt buffer $B$ consists of $20~\text{mM}$ sodium acetate and additional $1~\text{M}$ sodium chloride ($\ce{NaCl}$).
Both buffers are adjusted with hydrochloric acid ($\ce{HCl}$) of $4~\text{M}$ and sodium hydroxide ($\ce{NaOH}$) of $1~\text{M}$ to the desired pH.
Furthermore, acetic acid with a pH of 3 is used in this thesis for resin titration.
Information on the chemicals used can be found in {numref}`materials`.

```{table} Materials used in characterization experiments
:name: materials
:align: center

| Material          | Purity/ Concentration  | Manufacturer            |
| ----------------- | ---------------------- | ----------------------- |
| Acetic Acid       | $\geq~99.7\%$          | Merck KGaA              |
| Acetone           | $\geq~99.5\%$          | Carl Roth GmbH & Co. KG |
| Blue Dextran      |                        | Merck KGaA              |
| Hydrochloric Acid | $4~\text{M} \pm~0.2\%$ | Carl Roth GmbH & Co. KG |
| Lysozyme          | $\geq~90\%$            | Carl Roth GmbH & Co. KG |
| Sodium Acetate    | $\geq~99\%$            | Merck KGaA              |
| Sodium Chloride   | $\geq~99\%$            | Carl Roth GmbH & Co. KG |
| Sodium Hydroxide  | $1~\text{M} \pm~0.2\%$ | Carl Roth GmbH & Co. KG |
```

(conductivity_calibration)=
## Calibration of conductivity sensor

A conductivity detector is integrated into the chromatographic system to monitor salt concentration in real time during chromatography experiments.
Conductivity $\kappa$ describes a solution's ability to conduct electricity and is defined as

$$
\kappa = \frac{l}{A \cdot R},
$$

where $A$ is the conductor’s cross-sectional area, $l$ is its length, and $R$ is the resistance.
Conductivity is measured in Siemens per meter ($\text{S}~\text{m}^{-1}$), where $[\text{S}] = [\Omega^{-1}] = [\text{A/V}]$.

To quantify the relationship between salt concentration and conductivity, a calibration curve is recorded by measuring the conductivity of solutions with varying salt concentrations at a constant pH of 5.
Conductivity values are recorded over one minute at predefined salt concentrations ($20~\text{mM}$, $270~\text{mM}$, $570~\text{mM}$, $770~\text{mM}$, and $1020~\text{mM}$).
Since the relationship between salt concentration and conductivity is nonlinear, a quadratic function is fitted to the measured data using the least squares method.
This function is then used to determine salt concentration from conductivity in subsequent analyses.

```{code-cell} ipython3
:tags: [remove-cell]

from e0 import plot
fig, ax = plot()
glue("fig_conductivity", fig, display=False)
```

```{glue:figure} fig_conductivity
:name: fig_conductivity
:scale: 50%

Calibration curve for conductivity sensor.
```

(uv_calibration)=
## Rescaling of the UV signal

To compare simulations with experimental data, the UV signal must be converted into concentration values.
For each experiment, a known amount of protein was injected into the column, and the UV signal was rescaled so that its integral matched this amount.
Peak boundaries were defined by start and stop times, and baseline correction was applied where necessary.

(experiments)=
## Experiments

{numref}`tab_experiments` summarizes all experiments performed in this study.
The individual results will be discussed in the following chapters.
Note, for this work, all experiments, except where noted, were performed at pH 5.

```{table} Overview of experiments performed for model calibration
:name: tab_experiments

| ID  | Goal                                 | Parameters                                                             | Bypass                               | Injected component              | Volume         | Eluent                                               |
| --- | ------------------------------------ | ---------------------------------------------------------------------- | ------------------------------------ | ------------------------------- | -------------- | ---------------------------------------------------- |
| E1  | Determine tubing characteristics     | Tubing length and axial dispersion                                     | column, post-column tubing, detector | $1\%~\text{w/w}$ Acetone        | $50~\text{µL}$ | $A$                                                  |
| E2  | Determine tubing characteristics     | Tubing length and axial dispersion                                     | column, detector                     | $1\%~\text{w/w}$ Acetone        | $50~\text{µL}$ | $A$                                                  |
| E3  | Determine tubing characteristics     | Tubing length and axial dispersion                                     | column                               | $1020~\text{mM}$ Salt           | $50~\text{µL}$ | $A$                                                  |
| E4  | Determine mixer characteristics      | Mixer volume, tubing length and axial dispersion                       | column                               | $1020~\text{mM}$ Salt           | -              | $A \rightarrow B$ (step)                             |
| E5  | Determine bed properties             | Bed porosity and axial dispersion                                      | -                                    | $0.0005~\text{mM}$ Blue Dextran | $50~\text{µL}$ | $A$                                                  |
| E6  | Determine particle properties        | Particle porosity, total porosity, axial dispersion                    | -                                    | $1\%~\text{w/w}$ Acetone        | $50~\text{µL}$ | $B$                                                  |
| E7  | Determine diffusion characteristics  | Particle porosity, film diffusion, pore diffusion                      | -                                    | $0.2~\text{mM}$ Lysozyme        | $50~\text{µL}$ | $B$                                                  |
| E8  | Determine capacity                   | Capacity                                                               | -                                    | -                               | -              | $A$                                                  |
| E9  | Determine adsorption characteristics | Adsorption rate, desorption rate, characteristic charge, steric factor | -                                    | $0.2~\text{mM}$ Lysozyme        | $50~\text{µL}$ | $A \rightarrow B$ (Gradient: 4, 6, 8, 12, 14, 16 CV) |
```
