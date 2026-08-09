---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

(chromatographic_principle)=
# Principles of preparative chromatography

Chromatography is a thermal separation process widely used for the separation and purification of mixtures of (bio-)chemical species.
In this process, the mixture's components are dissolved in a solvent, known as the mobile phase, and transported through a column packed with a porous material, also referred to as the stationary phase.
As the mobile phase flows through the column, each component exhibits a distinct level of interaction with the stationary phase material.
Consequently, components that interact more strongly with the surface of the stationary phase are retained for a longer duration and, as a result, elute later than components that interact weakly.
The differential retention and elution times enable the effective separation of the mixture's components at the column outlet.

These interactions can be characterized by various retention mechanisms.
Most chromatographic separations are based on the principle of adsorption, which involves the accumulation of molecules on the surface of the stationary phase.
This phenomenon is influenced by several forces.
Given that chromatography relies on the reversibility of the adsorption step, it is governed by sorption interactions, ranging from physisorption (weak van der Waals and hydrophobic forces) to chemisorption as in ion exchange chromatography.
Physisorption refers to the weak binding of molecules through van der Waals interactions, such as dipole-dipole interactions.
In addition to van der Waals forces, hydrophobic interactions may also contribute to retention.
Moreover, specific interactions with affinity ligands immobilized on the stationary phase can serve as another retention mechanism.
For example, separation may be based on specific interactions such as those between an enzyme and its substrate, a receptor and its ligand, or an antibody and its antigen.
The size exclusion mechanism can also contribute to chromatographic separation.
In this mechanism, larger molecules are unable to penetrate as deeply into the pores of the stationary phase as smaller molecules, leading to differential retention times.
These solute-stationary phase interactions are collectively referred to as *binding* in this work.
The attachment of molecules to a solid surface in chromatography can be quantitatively described using adsorption isotherm models.
For more detailed information on different retention models, see {numref}`isotherm_models`.

Chromatographic separations can be classified based on different criteria, as outlined in Schmidt-Traub (2020) {cite}`SchmidtTraub2020`.
One common classification criterion is the state of aggregation of the fluid phase.
When the fluid phase is a gas, the process is referred to as gas chromatography (GC).
Conversely, if the fluid phase is a liquid, the technique is known as liquid chromatography (LC).
In cases where the liquid is maintained under temperature and pressure conditions above its critical point, the process is termed supercritical fluid chromatography (SFC).

Another way to categorize chromatographic separations is by their separation objectives, distinguishing between preparative and analytical processes.
Analytical chromatography involves separating small quantities of substance mixtures for the purpose of identifying or quantifying components.
Preparative chromatography, on the other hand, is employed for the purification of larger quantities of a substance mixture, aiming to isolate a specific product.
This work primarily focuses on studying preparative liquid chromatography.
Specifically, it aims to provide a comprehensive framework for modeling and optimizing the performance of different operating modes in which preparative liquid chromatography is performed.

To introduce some fundamental concepts that are relevant for all chromatographic processes, consider a simple batch-elution process.
In a batch-elution process, small quantities of a mixture are injected onto a chromatographic column.
Following the injection, an eluent is pumped through the column, facilitating the separation of components based on the retention mechanisms previously discussed.
As a result, these components elute from the column's outlet as distinct peaks.
{numref}`batch_elution_flow_sheet_intro` shows a typical flow sheet for a batch-elution process.

```{figure} ./figures/flow_sheet.png
:name: batch_elution_flow_sheet_intro

Flow sheet for batch-elution process.
The flow sheet is comprised of feed and eluent reservoirs, each with a pump capable of delivering the required flow rate against the pressure drop of the packed column, a volume-less mixer to merge feed and eluent streams entering the column, the chromatographic column itself, and an outlet.
```

The concentration profile measured at the column outlet is referred to as a chromatogram.
In practice, this signal can be detected using various methods, such as UV or conductivity detectors.
{numref}`chromatogram` illustrates a typical example, showing the inlet concentration pulse on the left and the resulting chromatogram on the right.

```{code-cell} ipython3
:tags: [remove-cell]

%config InlineBackend.figure_format = 'retina'
from myst_nb import glue
%config InlineBackend.figure_format = 'retina'

from examples.batch_elution.process import process

from CADETProcess.simulator import Cadet

simulator = Cadet()
simulation_results = simulator.simulate(process)

import matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

simulation_results.solution.column.inlet.plot(ax=ax1, show=False)

simulation_results.solution.column.outlet.plot(ax=ax2, show=False)
glue("chromatogram", fig, display=False)
```

```{glue:figure} chromatogram
:name: "chromatogram"
:scale: 100%

Left: Concentration profile at the column inlet.
Right: Chromatogram recorded at the column outlet with components $A$ and $B$ partially separated.
```

High product recoveries are typically achieved through *baseline separation*, a state where the component peaks from the same injection do not overlap as they exit the column.
By carefully selecting operating conditions, such as the amount of injected material and the flow rate, the stationary phase can be utilized efficiently.
Productivity can be increased, and eluent consumption reduced, by minimizing the interval between successive injections.
Further gains in productivity and eluent efficiency can be realized by strategically collecting waste fractions between product fractions or between peaks of consecutive injections, although this may come at the expense of slightly lower recovery rates.

If components in the mixture are not fully separated after passing through the column, more advanced operating modes can be employed to enhance separation.
Popular concepts include fractional recycling techniques and multi-column processes, which are particularly effective for improving separation efficiency and overall performance.
Innovative process concepts, such as flip-flow operations, can also significantly increase process productivity.
These advanced operating modes are discussed in more detail in {numref}`operating_modes`.
To describe these processes quantitatively, the following chapter introduces mathematical models for the relevant retention and transport phenomena.
