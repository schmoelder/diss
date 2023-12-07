(design_formulation)=
# Formulation of chromatographic design problems
<!-- 2.4.1. Was  wollen wir wissen -->
<!-- 2.4.2. Wie bewerten wie es -->
<!-- 2.4.3. Single objective vs multi objective? -->
The formulation of chromatographic design problems typically involves the determination of different parameters: {cite}`SchmidtTraub2020`

*Model parameters* are system inherent parameters that result from the choice of chromatographic system.
They describe the physical and chemical properties of the system and include parameters such as thermodynamics, fluid dynamics, dispersion effects, and mass transfer resistance.
These parameters can usually either be measured directly or need to be determined using an inverse method.
In an inverse method, the model parameters are adjusted to best match experimental data or other sources of information.
The determination of model parameters is an important step in developing accurate chromatographic process models.
As previously mentioned, for the purposes of this work, it is assumed that the model parameters have already been estimated in previous research or experiments.

*Design parameters* define the general configuration and operating mode of a chromatographic plant and cannot be changed during operation.
Examples of design parameters include column geometry (length and diameter), adsorbent choice, and in the case of *SMB* plants, the zone configuration (e.g. the number of columns in each *SMB* zone).
The selection of the operating mode itself could also be considered a design parameter, for which a superstructure optimization problem with discrete decision variables can be used.
This involves selecting between different operating modes, such as batch elution or recycling techniques, or determining the order of operations.
While the selection of the best operating mode is an important step in chromatographic process design, the focus of this work is mainly on optimizing the given process rather than selecting the optimal operating mode.

*Operating parameters* are adjustable during the operation of the plant and include parameters such as flow rate, concentrations, and valve switch times.
This will be the focus of this work and case studies are presented in {numref}`case_studies`.

In the following key performance indicators are introduced that are commonly used to evaluate the performance of separation processes.
Then, several approaches will be presented that can be used to formulate an optimization problem using the KPIs.
These optimization methods can help identify the best separation process design that satisfies the desired performance criteria.
Finally, merits and drawbacks of single and multi-objective optimization approaches will be discussed.
These approaches are crucial in identifying the optimal trade-off between competing performance criteria, such as maximizing product purity while minimizing operating costs.

(kpi)=
## Key performance indicators

Key performance indicators (KPI) are essential metrics that are used to evaluate the performance of a given system, usually by measuring how well it meets certain objectives or targets.
In the context of chromatography, KPIs can be used to evaluate the performance of a separation process, such as product purity, yield, and productivity, as well as operating costs, and environmental impact.
KPIs are often used in process optimization studies to help identify areas for improvement and to evaluate the effectiveness of different process scenarios.

Critical information for evaluating the separation performance of a chromatographic process is the amounts of the target components in the collected product fractions.
To define corresponding fractionation intervals, the chromatograms, i.e., the concentration profiles $c_{i,k}\left(t\right)$ at the outlet(s) of the process must be evaluated.
In a strict sense, a chromatogram is only given at the outlet of a single column. Note that here this term is used more generally for the concentration profiles at the outlets of a flow sheet, which only accounts for material leaving the process.
The times for the start, $t_{start, j}$, and the end, $t_{end, j}$, of a product fraction $j$ have to be chosen such that constraints on product purity are met.
It is important to note, that in advanced chromatographic process configurations, outlet chromatograms can be much more complex than the example shown in {numref}`fractionation` and that multiple sections of the chromatogram may represent suitable fractions $j$ for collecting one target component $i$.
Moreover, flow sheets can have multiple outlets $k$ that have to be fractionated simultaneously, and the volumetric flow rate $Q_k$ at the outlets may depend on time.
These aspects are considered by defining the total product amount of a component $i$ as

@todo: figure fractionation

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

The total separation costs associated with a given chromatographic separation process $C_{i, total}$ can be determined by adding the fixed and variable costs together.
Fixed costs are specific to each company and include operating costs $C_{operating}$, which are associated with overhead expenses such as wages and maintenance, as well as depreciation costs $C_{depreciation}$, which reflect the allocation of investment costs over the years
On the other hand, variable costs include eluent cost, feed cost, and adsorbent cost, which are dependent on the materials used in the chromatographic separation process.
This simple calculation provides a rough estimate of the total separation costs associated with a given chromatographic separation process and can be used as a starting point for evaluating the economic performance of the process.

@todo: citation

```{math}
:label: total_cost
C_{i, total} = C_{operating} + C_{depreciation} + C_{i, ads} + C_{i, Cel} + C_{i, feed}
```

The cost associated with the eluent $C_{i, el}$, which is the solvent used to elute the target product from the adsorbent, can be calculated using the following equation:

```{math}
:label: eluent_cost
C_{i, el} = EC_{i} \cdot \dot{m}_{i, annual} \cdot f_{el}
```

where $EC_{i}$ is the eluent consumption in $m^3$ per kg of product, $\dot{m}{i, annual}$ is the annual production rate in kg per year, and $f{el}$ is the eluent price in $\euro$ per $m^3$.

Feed cost $C_{i, feed}$, which reflects the cost of the feed material processed in the separation, can be calculated using the following equation:

```{math}
:label: feed_cost
C_{i, feed} = \frac{1 - Y_i}{Y_i} \cdot \dot{m}_{i, annual} \cdot f_{feed}
```

where $Y_i$ is the product yield and $f{feed}$ is the feed price in euros per $m^3$.

Adsorbent cost $C_{i, ads}$, which reflects the cost of the adsorbent material used in the separation, can be calculated using the following equation:

```{math}
:label: adsorbent_cost
C_{i, ads} = \frac{1}{PR_i} \cdot \dot{m}_{i, annual} \cdot \frac{f_{ads}}{t_{life}}
```

where $PR_i$ is the productivity in terms of kg of product per $m^3$ of adsorbent, $f{ads}$ is the adsorbent price in euros per $m^3$, and $t_{life}$ is the lifetime of the adsorbent material.

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
@todo: cite
