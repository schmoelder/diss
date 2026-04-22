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
  timeout: 1200
---

% Create custom role for inserting raw latex
```{role} raw-latex(raw)
:format: latex
```

```{code-cell} ipython3
:tags: [remove-cell]

%matplotlib inline
%config InlineBackend.figure_format = 'retina'

import importlib
from pathlib import Path
import sys

from IPython.display import display, Markdown
from git import Repo
import matplotlib.pyplot as plt
from myst_nb import glue

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
study_root = diss_root / "studies" / "operating_modes"
sys.path.insert(0, str(study_root))

# Setup cases for operating mode
from operating_modes.main import setup_process
from operating_modes.post_processing import (
    get_cases_by_operating_mode,
    process_soo_results,
    process_moo_results,
    setup_overview,
)
```

```{code-cell} ipython3
:tags: [remove-cell]

operating_mode = "batch-elution"
case_module = importlib.import_module(
    f"operating_modes.{operating_mode.lower().replace('-', '_')}"
)
cases = get_cases_by_operating_mode(
    operating_mode,
    index_by_name=True,
    work_dir=study_root,
)
```

(batch-elution_ternary_moo-pc)=
# Multi-objective optimization of a ternary Langmuir separation problem including cycle time

In this case study, a third component is introduced (see {numref}`model_parameters`).
Again, the cycle time is considered as a design parameter.
The full optimization problem is summarized in {numref}`batch-elution_ternary_moo-pc_overview`.

```{code-cell} ipython3
:tags: [remove-cell]

case = cases.get(f"{operating_mode}_ternary_multi-objective-per-component")
overview = setup_overview(case)

(
    (moo_fig_obj, _, moo_fig_obj_caption),
    (moo_fig_chrom, _, moo_fig_chrom_caption),
    moo_table,
    moo_results,
    simulation_results,
    fractionators,
) = process_moo_results(
    case,
    load_kwargs={"allow_commit_hash_mismatch": True},
    return_results=True,
)

glue("moo_fig_obj", moo_fig_obj, display=False)
glue("moo_fig_obj_caption", moo_fig_obj_caption)

glue("moo_fig_chrom", moo_fig_chrom, display=False)
glue("moo_fig_chrom_caption", moo_fig_chrom_caption)
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(overview))
```

{numref}`batch-elution_ternary_moo-pc_fig_obj` depicts the evaluated objective function values as a function of both feed duration and cycle time.
The optimal variable values and KPIs for all Pareto edge points are summarized in {numref}`batch-elution_moo-pc_kpi`, with the corresponding chromatograms provided in {numref}`batch-elution_ternary_moo-pc_fig_chrom`.


```{glue:figure} moo_fig_obj
:name: batch-elution_ternary_moo-pc_fig_obj
:scale: 100%

{glue:text}`moo_fig_obj_caption`
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_table))
```

```{glue:figure} moo_fig_chrom
:name: batch-elution_ternary_moo-pc_fig_chrom
:scale: 100%

{glue:text}`moo_fig_chrom_caption`
```

Interestingly, the optimization landscape now exhibits a more complex structure.
For the specific productivity of component $A$, three distinct optima are observed.
This behavior becomes clear upon analyzing the chromatograms corresponding to these optima ({numref}`batch-elution_ternary_moo-pc_fig_nodes`):
- The longest cycle time ($\alpha$) resembles the previous scenario, where the tail of component $C$ overlaps with the leading edge of component $A$ from the subsequent injection.
- At a shorter cycle time ($\beta$), components $A$ and $B$ overtake component $C$ from the previous injection, resulting in the $C$ peak being interlocked between the $B$ and $A$ peaks of consecutive injections.
- With the shortest cycle time ($\gamma$), components $A$ and $B$ overtake the $C$ peak from *two* previous injections.
This creates a highly efficient operational scenario, as components $B$ and $C$, neither of which are target components, are effectively managed to minimize their impact on the process.

```{code-cell} ipython3
:tags: [remove-cell]

from CADETProcess import plotting
from operating_modes.post_processing import (
    convert_mm_ss_to_s,
    get_best_individual,
    simulate_and_plot,
    slice_population
)

fig_nodes, axs = plotting.setup_figure(nrows=3, ncols=2, scale_with_subplots=True)
optimization_problem = moo_results.optimization_problem
pop_all = moo_results.population_all

# %% Longest cycle_time = [6:30-10:00]

pop_2 = slice_population(
    pop_all,
    target="x",
    index=0,
    lb=convert_mm_ss_to_s("6:30"),
    ub=convert_mm_ss_to_s("10:00"),
)
ind_2 = get_best_individual(pop_2, 0)
sim_results_2, frac_2, *_ = simulate_and_plot(
    optimization_problem,
    ind_2.x,
    comp_index=0,
    ax=axs[0, 1],
    return_results=True
)
sim_results_2.solution.outlet.outlet.plot(ax=axs[0, 0])
plotting.add_text(axs[0, 0], r"$\alpha$")


# %% Medium cycle_time = [3:10-5:50]

pop_1 = slice_population(
    pop_all,
    target="x",
    index=0,
    lb=convert_mm_ss_to_s("3:10"),
    ub=convert_mm_ss_to_s("5:50"),
)
ind_1 = get_best_individual(pop_1, 0)
sim_results_1, frac_1, *_ = simulate_and_plot(
    optimization_problem,
    ind_1.x,
    comp_index=0,
    ax=axs[1, 1],
    return_results=True
)
sim_results_1.solution.outlet.outlet.plot(ax=axs[1, 0])
plotting.add_text(axs[1, 0], r"$\beta$")

# %% Shortest cycle_time = [2:00-2:50]

pop_0 = slice_population(
    pop_all,
    target="x",
    index=0,
    lb=convert_mm_ss_to_s("2:00"),
    ub=convert_mm_ss_to_s("2:50"),
)
ind_0 = get_best_individual(pop_0, 0)
sim_results_0, frac_0, *_ = simulate_and_plot(
    optimization_problem,
    ind_0.x,
    comp_index=0,
    ax=axs[2, 1],
    return_results=True
)
sim_results_0.solution.outlet.outlet.plot(ax=axs[2, 0])
plotting.add_text(axs[2, 0], r"$\gamma$")

# %% Finalize layout and glue figure

for i, label in enumerate([r'$\alpha$', r'$\beta$', r'$\gamma$']):
    # Add text annotation to the left of the first subplot in each row
    axs[i, 0].annotate(
        label,
        xy=(-0.3, 0.5),  # Position relative to the subplot (x, y)
        xycoords='axes fraction',
        fontsize=14,
        fontweight='bold',
        va='center',
        ha='right'
    )

fig_nodes.subplots_adjust(left=0.1, wspace=0.2, hspace=0.2)
fig_nodes.tight_layout()

glue("moo_fig_nodes", fig_nodes, display=False)
```

```{glue:figure} moo_fig_nodes
:name: batch-elution_ternary_moo-pc_fig_nodes
:scale: 100%

Comparison of local productivity optima for component $A$ across different cycle times.
Each row corresponds to a distinct cycle time scenario:
- $\alpha$: $\Delta t_{\text{cycle}} = \text{07:47}~\text{min}$,
- $\beta$: $\Delta t_{\text{cycle}} = \text{03:47}~\text{min}$,
- $\gamma$: $\Delta t_{\text{cycle}} = \text{02:17}~\text{min}$.

**Left column:** Chromatograms for all cycles until cyclic stationarity is reached.
**Right column:** Chromatograms for the last cycle, including fractionation times.
```

Similarly, the objectives for the KPIs of the other components also exhibit multiple local optima, which can be attributed to the same overlapping and overtaking behavior of peaks across injections.
Due to the high dimensionality and complexity of the objective space, optimizers may struggle to fully sample these sometimes sharp regions, resulting in sparse sampling.
Refinement of the parameter space could potentially yield further improvements in process parameters.
It is worth noting that alternative tools, such as surrogate models, may be better suited if the primary goal is to understand the underlying optimization landscape rather than targeting a specific KPI.
In this case, the use of a genetic algorithm, a somewhat inefficient but robust "brute force" approach, enabled effective exploration of the parameter space and revealed these complex behaviors.
Gradient-based algorithms, for instance, would likely fail due to the presence of many local optima and their dependence on initial values.

Bayesian optimization presents a promising alternative, as it balances exploration of the parameter space with exploitation of known high-performing regions.
However, at the time of writing, such algorithms have not yet been fully integrated into the CADET-Process framework.

---

**Summary**

This section introduced model-based process optimization using batch-elution chromatography as a starting point.
Beginning from an idealized linear system, the framework was validated against equilibrium theory before gradually increasing complexity: realistic nonlinear binding, multi-objective formulation, cycle time as a design variable, and finally a ternary separation.
At each step, results were discussed in terms of KPI trade-offs and physical interpretability.
The progression demonstrates that the framework can recover known optimal solutions under simplified conditions and scale to more complex, practically relevant problems where the optimization landscape itself reveals non-obvious operating strategies.
