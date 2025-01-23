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
---

(lwe_process)=

# Load-Wash-Elute

A typical process to separate a mixture of components using ion exchange chromatography is the load-wash-elute process (LWE).
The first step is to load the sample onto the stationary phase.
The column is then washed with a solvent that removes any impurities or unwanted components that may be present.
Finally, the bound compound is eluted using a solvent that displaces the compound from the stationary phase (usually with high salt concentration).

For this purpose, often gradients are employed.
In gradient chromatography, the concentration of one or more components of the mobile phase is systematically changed over time.
The gradient can be linear or non-linear, and the change in solvent strength can be accomplished by changing the proportion of different solvents in the mobile phase, by adjusting the pH or ionic strength of the mobile phase, or by other means.
Gradient chromatography is particularly useful when separating complex mixtures of compounds with similar physical and chemical properties.
By gradually changing the mobile phase, the separation can be optimized to separate the various components of the mixture, leading to better resolution and higher quality separation.

For example, the following shows a typical concentration profile for a linear gradient.

<!-- ```{code-cell} -->
<!-- :tags: [remove-input] -->

<!-- from lwe_concentration import process -->

<!-- from CADETProcess.simulator import Cadet -->
<!-- process_simulator = Cadet() -->

<!-- simulation_results = process_simulator.simulate(process) -->

<!-- from CADETProcess.plotting import SecondaryAxis -->
<!-- sec = SecondaryAxis() -->
<!-- sec.components = ['Salt'] -->
<!-- sec.y_label = '$c_{salt}$' -->

<!-- _ = simulation_results.solution.column.inlet.plot(secondary_axis=sec) -->
<!-- ``` -->

In **CADET-Process**, gradients can be used by either changing the concentration profile of an {class}`~CADETProcess.processModel.Inlet` or by adding multiple inlets and dynamically adjusting their flow rates.
Here, only the process with multiple inlets is highlighted.

```{figure} ./figures/flow_sheet_flow_rate.png
Flow sheet for load-wash-elute process using a separate inlets for buffers.
```

```{figure} ./figures/events_flow_rate.png
Events of load-wash-elute process using multiple inlets and mofifying their flow rates.
```
