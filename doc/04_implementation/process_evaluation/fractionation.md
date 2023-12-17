---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
execution:
  timeout: 300
---


(fractionation_guide)=
# Product Fractionation

As mentioned in {numref}`chapter %s <kpi>`, key information for evaluating the separation performance of a chromatographic process is the amounts of the target components in the collected product fractions.
In **CADET-Process**, the {mod}`~CADETProcess.fractionation` module provides methods to calculate these performance indicators.

## Fractionator

The {class}`~CADETProcess.fractionation.Fractionator` allows slicing the solution and pool fractions for the individual components.
It enables evaluating multiple chromatograms at once and multiple fractions per component per chromatogram.

The most basic strategy is to manually set all fractionation times manually.
To demonstrate the strategy, consider a simple {ref}`batch-elution example<batch_elution_example>`.

```{code-cell} ipython3
:tags: [remove-cell]

from examples.batch_elution.process import process
```

To enable the calculation of the process parameters, it is necessary to specify which of the inlets should be considered for the feed and eluent consumption.
Moreover, the outlet(s) which are used for evaluation need to be defined.

```
flow_sheet.add_feed_inlet('feed')
flow_sheet.add_eluent_inlet('eluent')
flow_sheet.add_product_outlet('outlet')
```

```{code-cell} ipython3
:tags: [remove-cell]

from CADETProcess.simulator import Cadet
process_simulator = Cadet()
simulation_results = process_simulator.simulate(process)
```

For reference, this is the chromatogram at the outlet that needs to be fractionated:

```{code-cell} ipython3
_ = simulation_results.solution.outlet.outlet.plot()
```

After import, the {class}`~CADETProcess.fractionation.Fractionator` is instantiated with the simulation results.

```{code-cell} ipython3
from CADETProcess.fractionation import Fractionator
fractionator = Fractionator(simulation_results)
```

To add a fractionation event, the following arguments need to be provided:

- `event_name`: Name of the event.
- `target`: Pool to which fraction is added. `-1` indicates waste.
- `time`: Time of the event
- `chromatogram`: Name of the chromatogram. Optional if only one outlet is set as `product_outlet`.

Here, component $A$ seems to have sufficient purity between $5 \colon 00~min$ and $5 \colon 45~min$ and component $B$ between $6 \colon 30~min$ and $9 \colon 00~min$.

```{code-cell} ipython3
fractionator.add_fractionation_event('start_A', 0, 5*60, 'outlet')
fractionator.add_fractionation_event('end_A', -1, 5.75*60)
fractionator.add_fractionation_event('start_B', 1, 6.5*60)
fractionator.add_fractionation_event('end_B', -1, 9*60)
```

The {class}`~CADETProcess.performance.Performance` object of the {class}`~CADETProcess.fractionation.Fractionator` contains the parameters:

```{code-cell} ipython3
print(fractionator.performance)
```

With these fractionation times, the both component fractions reach a purity of $99.7~\%$, and $97.2~\%$  respectively.
The recovery yields are $65.2~\%$ and $63.4~\%$.

The chromatogram can be plotted with the fraction times overlaid:

```{code-cell} ipython3
_ = fractionator.plot_fraction_signal()
```

## Optimization of Fractionation Times

The {mod}`~CADETProcess.fractionation` module also provides a method to set up an {class}`~CADETProcess.optimization.OptimizationProblem` which automatically determines optimal cut times.
For every component, different purity requirements can be specified, and any function may be applied as objective.

For the objective and constraint functions, fractions are pooled from all {class}`Outlets <CADETProcess.processModel.Outlet>` of the {class}`~CADETProcess.processModel.FlowSheet` (see equations {eq}`mass` and {eq}`purity`) that have been marked as `product_outlet`.
For more information about configuring the {class}`~CADETProcess.processModel.FlowSheet`, refer to {ref}`flow_sheet_guide`.

As initial values for the optimization, areas of the chromatogram with sufficient local purity are identified, i.e., intervals where $PU_i(t)=c_i(t)/\sum_j c_j(t)\geq PU_{min,i}$ {cite}`Shan2004`.
These initial intervals are then expanded by the optimizer towards regions of lower purity while meeting the cumulative purity constraints.
In the current implementation, {class}`~CADETProcess.optimization.COBYLA` {cite}`Powell1994` of the **SciPy** {cite}`SciPyContributors2020` library is used as optimizer.
Yet, any other solver or heuristic algorithm may be used.

```{code-cell} ipython3
from CADETProcess.fractionation import FractionationOptimizer
fractionation_optimizer = FractionationOptimizer()
```

By default, the mass of the components is maximized under purity constraints.
However, other objective functions can be used.

To automatically optimize the fractionation times, pass the simulation results to the {meth}`~CADETProcess.fractionation.FractionationOptimizer.optimize_fractionation` method.
Depending on the separation problem at hand, different purity requirements can be specified.
For example, here only the first component is relevant, and requires a purity $\ge 95~\%$:

```{code-cell} ipython3
fractionator = fractionation_optimizer.optimize_fractionation(simulation_results, purity_required=[0.95, 0])
```

The results are stored in a {class}`~CADETProcess.performance.Performance` object.

```{code-cell} ipython3
print(fractionator.performance)
```

The chromatogram can also be plotted with the fraction times overlaid:

```{code-cell} ipython3
_ = fractionator.plot_fraction_signal()
```

For comparison, this is the results if only the second component is relevant:

```{code-cell} ipython3
fractionator = fractionation_optimizer.optimize_fractionation(simulation_results, purity_required=[0, 0.95])

print(fractionator.performance)
_ = fractionator.plot_fraction_signal()
```

But of course, also both components can be valuable.
Here, the required purity is also reduced to demonstrate that overlapping fractions are automatically avoided by internally introducing linear constraints.

```{code-cell} ipython3
fractionator = fractionation_optimizer.optimize_fractionation(simulation_results, purity_required=[0.8, 0.8])

print(fractionator.performance)
_ = fractionator.plot_fraction_signal()
```

To set an alternative objective, a function needs to be passed that takes a {class}`~CADETProcess.performance.Performance` as an input.
In this example, not only the total mass is considered important but also the concentration of the fraction.
As previously mentioned, `COBYLA` only handles single objectives.
Hence, a {class}`~CADETProcess.performance.RankedPerformance` is used which transforms the {class}`~CADETProcess.performance.Performance` object by adding a weight $w_i$ to each component.

$$
p = \frac{\sum_i^{n_{comp}}w_i \cdot p_i}{\sum_i^{n_{comp}}(w_i)}
$$

It is also important to remember that by convention, objectives are minimized.
Since in this example, the product of mass and concentration should be maximized, the value of the objective function is multiplied by $-1$.
Also, the number of objectives the function returns needs to be specified.

```{code-cell} ipython3
from CADETProcess.performance import RankedPerformance
ranking = [1, 1]
def alternative_objective(performance):
 performance = RankedPerformance(performance, ranking)
 return - performance.mass * performance.concentration

fractionator = fractionation_optimizer.optimize_fractionation(
 simulation_results, purity_required=[0.95, 0.95],
 obj_fun=alternative_objective,
    n_objectives=1,
)

print(fractionator.performance)
_ = fractionator.plot_fraction_signal()
```

The resulting fractionation times show that in this case, it is advantageous to discard some slices of the peak in order not to dilute the overall product fraction.

## Exclude Components

In some situations, not all components are relevant for fractionation.
For example, salt used for elution usually does not affect the purity of a component.
For this purpose, a subset of components can be specified.

To demonstrate the strategy, consider the {ref}`LWE example<lwe_example>`.
Here, the `Salt` component should not be used for fractionation.

```{code-cell} ipython3
:tags: [remove-cell]

from examples.load_wash_elute.lwe_flow_rate import process

from CADETProcess.simulator import Cadet
process_simulator = Cadet()
simulation_results = process_simulator.simulate(process)
```

```{code-cell} ipython3
fractionator = fractionation_optimizer.optimize_fractionation(
    simulation_results,
    components=['A', 'B', 'C'],
    purity_required=[0.95, 0.95, 0.95]
)
print(fractionator.performance)
_ = fractionator.plot_fraction_signal()
```

## Sum species

Note that by default the sum-signal of all component {class}`~CADETProcess.processModel.Species` is used for fractionation.
To disable this feature, set `use_total_concentration_components=False`.
For more information on {class}`~CADETProcess.processModel.Species`, refer to {ref}`component_system_guide`.
