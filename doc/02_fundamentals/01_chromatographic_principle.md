---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

(chromtographic_principle)=
# Principles of preparative chromatography

Chromatography is a thermal separation process widely used for purifying mixtures of (bio-)chemical species.
In this process, the mixture's components are dissolved in a solvent, known as mobile phase, and then transported through a column packed with a porous material, also referred to as the stationary phase.
As the solvent flows through the column, each component exhibits a distinct level of interaction with the stationary phase material.
Consequently, components that interact more strongly with the surface of the stationary phase are retained for a longer duration and, as a result, elute later than components that only interact weakly.
The differential retention and elution time enable the effective separation of the mixture's components at
the column outlet.

These interactions can be characterized by various retention mechanisms.
Most chromatographic separations are based on the principle of adsorption, which involves the adhesion and accumulation of molecules on the surface of the stationary phase.
This phenomenon is influenced by several forces.
Given that chromatography relies on the reversibility of the adsorption step, it primarily involves physisorption.
Physisorption refers to the weak binding of molecules based on van der Waals interactions, such as dipole-dipole interactions.
Besides van der Waals forces, hydrophobic and electrostatic interactions may also play a role between the stationary phase and the components being separated.
Moreover, specific interactions with affinity ligands immobilized on the stationary phase can serve as another retention mechanism.
For instance, separation can be based on specific interactions such as between an enzyme and its substrate, a receptor and its ligand, or an antibody and its antigen.
Size exclusion also contributes to the separation process in chromatography.
In this mechanism, larger molecules cannot penetrate as deeply into the pores of the stationary phase as smaller molecules, leading to differential retention times.
The attachment of molecules to a solid surface in chromatography can be quantitatively described using adsorption isotherm models.
For more detailed information on different retention models, see section {numref}`isotherm_models`.

Chromatographic separations can be classified based on different criteria, as outlined in Schmidt-Traub (2020) {cite}`SchmidtTraub2020`.
One common classification criterion is the state of aggregation of the fluid phase.
When the fluid phase is a gas, the process is referred to as gas chromatography (GC).
Conversely, if the fluid phase is a liquid, the technique is known as liquid chromatography (LC).
In cases where the liquid is maintained under temperature and pressure conditions above its critical point, the process is termed supercritical fluid chromatography (SFC).

Another way to categorize chromatographic separations is by their separation objectives, distinguishing between preparative and analytical processes.
Analytical chromatography involves separating small quantities of substance mixtures for the purpose of identifying or quantifying the components.
Preparative chromatography, on the other hand, is employed for the purification of larger quantities of a substance mixture, aiming to isolate a specific product.

This work primarily focusses on studying preparative liquid chromatography.
Specifically, it aims to provide a comprehensive framework for modeling and optimizing the performance of different operating modes in which preparative liquid chromatography is performed.
To introduce some fundamental concepts that are relevant for all chromatographic processes, consider a simple batch elution process.
In a batch elution process, small quantities of a mixture are injected onto a chromatographic column.
Following the injection, an eluent is pumped through the column, facilitating the separation of components based on the retention mechanisms previously discussed.
As a result, these components elute from the column's outlet as distinct peaks.
{numref}`Figure %s <batch_elution_flow_sheet_intro>` shows a typical flow sheet for a batch elution process.

```{figure} ../05_case_studies/01_batch_elution/figures/flow_sheet.png
:name: batch_elution_flow_sheet_intro

Flow sheet for batch elution process.
The flow sheet is comprised of feed and eluent reservoirs, each with a pump capable of delivering the required flow rate against the pressure drop of the packed column, a valve for selecting whether feed or eluent is introduced into the column, the chromatographic column itself, and an outlet.
```

The concentration profile of the separated components at the column outlet is typically recorded using various detectors, and this profile is commonly referred to as a chromatogram.
{numref}`Figure %s <chromatogram>` depicts a typical chromatogram, as measured at the outlet of the chromatographic column.

```{code-cell} ipython3
:tags: [remove-cell]

from myst_nb import glue

from examples.batch_elution.process import process

from CADETProcess.simulator import Cadet

simulator = Cadet()
simulation_results = simulator.simulate(process)

import matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

simulation_results.solution.column.inlet.plot(fig=fig, ax=ax1, show=False)

simulation_results.solution.column.outlet.plot(fig=fig, ax=ax2, show=False)
glue("chromatogram", fig, display=False)
```

```{glue:figure} chromatogram
:name: "chromatogram"
:figwidth: 300px

Left: Concentration profile at the column inlet.
Right: Chromatogram recorded at the column outlet with components $A$ and $B$ partially separated.
```

By selecting appropriate operating conditions, such as the amount of injected material and the flow rate, an efficient operating scenario can be realized in which the stationary phase is utilized with high efficiency.
High product recoveries are typically achieved through 'baseline separation', a state where the component peaks from the same injection do not overlap when exiting the column.
In addition, productivity and eluent consumption can be improved by minimizing the interval between two successive injections.
Productivity and eluent consumption may be further improved by strategically collecting waste fractions between product fractions or between peaks of consecutive injections, albeit at the cost of lower recovery.
Consequently, these operating conditions are subject to optimization.
Such optimization can be accomplished using model-based design which allows balancing the different performance metrics.

If parts of the component mixture are not completely separated after passing through the column, the separation can also be enhanced by expanding the operating mode.
In such cases, frequently used concepts include different recycling techniques as well as processes with several columns.
Additionally, process concepts such as flip flow can be applied to increase the productivity of the processes.
Examples for advanced operating modes be discussed in more detail in {numref}`section %s <operating_modes>`.
