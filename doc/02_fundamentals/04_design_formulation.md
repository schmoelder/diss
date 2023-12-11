---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

(design_formulation)=
# Formulation of chromatographic design problems

The formulation of chromatographic design problems typically involves the determination of different parameters: {cite}`SchmidtTraub2020`

*Model parameters* are parameters inherent to the chosen chromatographic system.
They describe its physical and chemical properties and include parameters describing the thermodynamics, fluid dynamics, dispersion effects, and mass transfer resistance of the system.
These parameters can usually either be measured directly or need to be determined using the inverse method, where they are adjusted to align with experimental data or other sources of information.
The accurate determination of model parameters is a crucial step in developing precise chromatographic process models.
However, as previously mentioned, for the scope of this work, it is assumed that these model parameters have already been estimated through prior research or experiments

*Design parameters* determine the overall setup and operational approach of a chromatographic plant, and these parameters remain fixed during operation.
This includes decisions about various operating modes, such as batch elution or recycling techniques, and the sequence of operations.
Additionally, design parameters encompass aspects like column geometry (length and diameter), the choice of adsorbent, and, in the case of Simulated Moving Bed (SMB) plants, the zone configuration, including the number of columns in each SMB zone.
The selection of the operating mode itself is a significant design parameter.
This choice can be systematically addressed via superstructure optimization, which employs discrete decision variables to evaluate different operational configurations.
Although selecting the most suitable operating mode is a crucial aspect of chromatographic process design, the primary focus of this work is on optimizing existing processes rather than on the selection of an optimal operating mode.

*Operating parameters* refer to those variables that can be adjusted during the operation of a chromatographic plant.
These include parameters such as flow rate, concentrations, and valve switch times, which are essential for fine-tuning the process to achieve optimal performance.
The investigation and optimization of these operating parameters will be the primary focus of this work.
Detailed case studies demonstrating the application and impact of these parameters in real-world scenarios are presented in {numref}`section %s <case_studies>`.

In the following section, several key performance indicators (KPIs) are introduced, which are commonly used to evaluate the performance of separation processes.
These KPIs will later be employed as objectives or constraints when formulating various optimization problems.
Such optimization methods can assist in identifying the best separation process design that meets desired performance criteria.
Finally, the merits and drawbacks of single and multi-objective optimization approaches will be discussed.
These approaches are crucial for identifying the optimal trade-off between competing performance criteria, such as maximizing product purity while minimizing operating costs.

(kpi)=
## Key performance indicators

Key performance indicators (KPI) are metrics used to evaluate the performance of a given system.
In the context of chromatography, product purity, yield, productivity, and eluent consumption as well as operating costs, and environmental impact are considered key performance
indicators.
KPIs are often used in process optimization studies to help identify areas for improvement and to evaluate the effectiveness of different process scenarios.

The most important information for evaluating the separation performance of a chromatographic process are the amounts of the target components in the collected product fractions $j$ (see eq. {eq}`mass`).
In a strict sense, a chromatogram is given at the outlet of a single column.
Note that here this term is used more generally for concentration profiles $c_{i,k}\left(t\right)$ at the outlets $k$ of a process.
The times for the start, $t_{start, j}$, and the end, $t_{end, j}$, of a product fraction $j$ have to be chosen such that constraints on product purity are met.
{numref}`Figure %s <fractionation>` shows an example chromatogram of a batch elution process where suitable fractions have been selected.

```{code-cell} ipython3
:tags: [remove-cell]

from myst_nb import glue

from examples.batch_elution.process import process

from CADETProcess.simulator import Cadet

simulator = Cadet()
simulation_results = simulator.simulate(process)

from CADETProcess.fractionation import Fractionator
fractionator = Fractionator(simulation_results)

fractionator.add_fractionation_event('start_A', 0, 5*60, 'outlet')
fractionator.add_fractionation_event('end_A', -1, 5.75*60)
fractionator.add_fractionation_event('start_B', 1, 6.5*60)
fractionator.add_fractionation_event('end_B', -1, 9*60)

from CADETProcess import plotting

fig, ax = fractionator.plot_fraction_signal(style='small', show=False)
glue("fractionation", fig, display=False)
```

```{glue:figure} fractionation
:name: "fractionation"
:figwidth: 300px

Fractionation of a chromatogram.
Grey areas represent waste fractions.
Blue: Target fraction of component $A$.
Red: Target fraction of component $B$.
```

It is important to note, that in advanced chromatographic process configurations, outlet chromatograms can be much more complex than the example shown in {numref}`Fig. %s <fractionation>` and that multiple sections of the chromatogram may represent suitable fractions $j$ for collecting one target component $i$.
Moreover, flow sheets can have multiple outlets $k$ that have to be fractionated simultaneously, and the volumetric flow rate $Q_k$ at the outlets may depend on time.
These aspects are considered by defining the total product amount of a component $i$ as

```{math}
:label: mass
m_{i} = \sum_{k=1}^{n_{chrom}} \sum_{j=1}^{n_{frac, k}^{i}}\int_{t_{start, j}}^{t_{end, j}} Q_k(t) \cdot c_{i,k}(t) dt, \\
```

where $n_{frac, k}^{i}$ is the number of fractions considered for component $i$ in chromatogram $k$, and $n_{chrom}$ is the number of chromatograms that is evaluated.

Further performance criteria typically used for evaluation and optimization of chromatographic performance are the specific productivity, $PR_i$, the recovery yield, $Y_i$, and the specific solvent consumption, $EC_i$, which all depend on the product amounts:

```{math}
:label: productivity
PR_{i} = \frac{m_i}{V_{solid} \cdot \Delta t_{cycle}},\\
```

```{math}
:label: yield
Y_{i} = \frac{m_i}{m_{feed, i}},\\
```

```{math}
:label: eluent_consumption
EC_{i} = \frac{V_{solvent}}{m_i},\\
```

with $V_{solid}$ being the volume of stationary phase, $V_{solvent}$ that of the solvent introduced during a cycle with duration $\Delta t_{cycle}$, and $m_{feed}$ the injected amount of mixture to be separated. Multiple sources can be considered for the amounts of consumed feed and solvent,

```{math}
:label: solvent_in
V_{solvent} = \sum_{s=1}^{n_{solvents}} \int_{0}^{t_{cycle}} Q_s(t) dt,\\
```

```{math}
:label: feed_in
m_{feed,i} = \sum_{f=1}^{n_{feeds}} \int_{0}^{t_{cycle}} Q_f(t) \cdot c_{f,i}(t) dt.\\
```

For the cumulative product purities $PU_i$ holds

```{math}
:label: purity
PU_{i} = \frac{m_{i}^{i}}{\sum_{l=1}^{n_{comp}} m_{l}^{i}},\\
```

where $n_{comp}$ is the number of mixture components and $m_{l}^{i}$ is the mass of component $l$ in target fraction $i$.

Alongside process performance indicators, economic criteria can also play an important role in evaluating the performance of a chromatographic separation process.
However, the calculation of total separation costs is complex due to various influencing parameters and cost structures, which can vary depending on the specific situation and site-related factors.
For example, the physical properties of the separation system, such as column size and resin type, can affect the cost of adsorbent, eluent, and other materials used in the separation process.
Similarly, plant design factors, such as the number of columns used in the process and the type of chromatography system, can impact the fixed costs associated with the separation process, such as capital investment, labor, and maintenance costs.
Moreover, site-related parameters, such as the availability and cost of utilities like water and electricity, can impact the total separation costs as well.

The total separation costs associated with a given chromatographic separation process $C_{i, total}$ can be determined by adding the fixed and variable costs.
Fixed costs are specific to each company and include operating costs $C_{operating}$, which are associated with overhead expenses such as wages and maintenance, as well as depreciation costs $C_{depreciation}$, which reflect the allocation of investment costs over the years.
On the other hand, variable costs include the costs of operation such as eluent cost, feed cost, and adsorbent cost, which are dependent on the materials used in the chromatographic separation process.
This simple calculation provides a rough estimate of the total separation costs associated with a given chromatographic separation process and can be used as a starting point for evaluating the economic performance of the process {cite}`Nicoud2015`:

```{math}
:label: total_cost
C_{i, total} = C_{operating} + C_{depreciation} + C_{i, ads} + C_{i, Cel} + C_{i, feed}
```

The cost associated with the eluent $C_{i, el}$, which is the solvent used to elute the target product from the adsorbent, can be calculated using the following equation:

```{math}
:label: eluent_cost
C_{i, el} = EC_{i} \cdot \dot{m}_{i, annual} \cdot f_{el}
```

where $EC_{i}$ is the eluent consumption in $m^3$ per kg of product, $\dot{m}_{i, annual}$ is the annual production rate in kg per year, and $f_{el}$ is the eluent price in $\euro$ per $m^3$.

Feed cost $C_{i, feed}$, which reflects the cost of the feed material processed in the separation, can be calculated using the following equation:

```{math}
:label: feed_cost
C_{i, feed} = \frac{1 - Y_i}{Y_i} \cdot \dot{m}_{i, annual} \cdot f_{feed}
```

where $Y_i$ is the product yield and $f_{feed}$ is the feed price in $\euro$ per $m^3$.

Adsorbent cost $C_{i, ads}$, which reflects the cost of the adsorbent material used in the separation, can be calculated using the following equation:

```{math}
:label: adsorbent_cost
C_{i, ads} = \frac{1}{PR_i} \cdot \dot{m}_{i, annual} \cdot \frac{f_{ads}}{t_{life}}
```

where $PR_i$ is the productivity in terms of kg of product per $m^3$ of adsorbent, $f_{ads}$ is the adsorbent price in $euro$ per $m^3$, and $t_{life}$ is the lifetime of the adsorbent material.

## Objective functions

In optimization, an objective function is used to quantify the quality of a solution.
Simple objective functions are often used that combine criteria such as those introduced in {numref}`kpi`.
However, more detailed cost functions may also be applied to directly maximize the profit of a separation.
For discussions on useful objective functions see, for example, {cite}`SchmidtTraub2020,Nicoud2015,Dienstbier2020`.

A common equation that combines specific productivity, recovery yield, and eluent consumption into a single objective is shown below:

```{math}
:label: ranked_objective
f(x) = \frac{PR_{ranked}(x) \cdot Y_{ranked}(x)}{EC_{ranked}(x)}
```

The individual values of the target components are combined using a weighting factor $w_i$, which is then used to calculate a ranked performance $P$:

```{math}
:label: ranked_performance
P_{ranked} = \frac{\sum_{i=1}^{n_comp} w_i \cdot P_i}{\sum_{i=1}^{n_comp} w_i}
```

## Multi-objective optimization

In recent years, there has been growing interest in using multi-objective optimization (MOO) instead of single-objective optimization (SOO) in various fields, including chromatography.
This is because SOO can sometimes result in information loss, as the optimization process focuses on a single objective and may overlook other important factors.
In contrast, MOO considers multiple objectives simultaneously, providing a more comprehensive analysis of the design space {cite}`Heymann2022`.

In the context of chromatography optimization, one advantage of MOO is that it usually does not require significantly additional computational power compared to SOO.
This is primarily because most of the computational time is spent on evaluating the model, rather than the optimization process itself.
Moreover, in many cases, multiple objectives are calculated during the optimization process and then "reduced" to a single objective in SOO.
However, this essentially "throws away" information.
In contrast, MOO provides a more comprehensive analysis of the solution space.

However, it is important to note that not all optimization algorithms used for SOO can be directly applied to MOO.
While some algorithms, particularly evolutionary algorithms such as genetic algorithms (GA), can be employed for both SOO and MOO, other optimization techniques may not be suitable for handling multiple objectives.
For example, gradient-based optimization methods, like the Gradient Descent algorithm, are generally designed for single-objective problems and may require adaptation for multi-objective problems.
Nonetheless, MOO has demonstrated great potential for improving the design of chromatographic processes, particularly for optimizing multiple objectives that are difficult to combine into a single objective function.

Furthermore, even in situations where there exists supposedly only a single best value (e.g., parameter fit), formulating the problem as multi-objective problem still be beneficial.
In some cases, MOO can converge to a single solution faster than SOO because the optimizer can work on different aspects simultaneously.
This allows the algorithm to explore the solution space more efficiently, leading to quicker convergence to an optimal solution {cite}`Deb2002.
Moreover, especially when multiple datasets are involved, MOO can help identify conflicting datasets or ill-posed optimization problems, such as when a problem is overdetermined.
By considering multiple objectives, MOO can reveal inconsistencies in the data or the optimization problem formulation, which may not be readily apparent when using SOO.
This can be particularly useful in situations where the data sources are unreliable or where the optimization problem is inherently complex, as it enables a more robust evaluation of the solution space and a deeper understanding of the underlying issues.

<!-- 2.4.1. Was  wollen wir wissen -->
<!-- 2.4.2. Wie bewerten wie es -->
<!-- 2.4.3. Single objective vs multi objective? -->
