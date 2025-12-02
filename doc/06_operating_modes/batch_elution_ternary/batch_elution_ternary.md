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

from IPython.display import display, Markdown
from git import Repo
import matplotlib.pyplot as plt
from myst_nb import glue

from cadetrdm import Study

# Get the root directory of the Git repository
diss_root = Path(Repo(search_parent_directories=True).working_dir)
studies_root = diss_root / "studies" / "operating_modes"
sys.path.insert(0, str(studies_root))

from run_all import (
    setup_study,
    setup_cases,
    load_optimization_config,
    load_optimization_results,
    simulate_results,
    fractionate_results,
    process_so_results,
    setup_so_results_table,
)
study = setup_study(studies_root, "batch_elution_ternary")
cases = setup_cases(study)

# Dummy figure to avoid
fig_dummy, ax = plt.subplots()
glue("fig_dummy", fig_dummy, display=False)
```

(batch_elution_ternary_study)=
# Ternary Batch Elution Chromatography

(batch_elution_ternary_single)=
## Single-objective Optimziation

Here we do some single-objective  optimization.
<!-- ```{figure} ./results_single/single-objective/figures/objectives.png -->
<!-- :name: batch_elution_single_objectives -->

<!-- Objective space; each dot represents an evaluation. -->
<!-- ``` -->

```{code-cell} ipython3
:tags: [remove-cell]

so = cases["single-objective"]
so_problem, _ = load_optimization_config(so)
so_results = load_optimization_results(so)

simulation_results = simulate_results(so_problem, so_results.x[0])
fractionator = fractionate_results(so_problem, simulation_results)
so_batch_elution_ternary_fig, ax = fractionator.plot_fraction_signal()

glue("so_batch_elution_ternary_fig", so_batch_elution_ternary_fig, display=False)

so_batch_elution_ternary_table = setup_so_results_table(so_results, fractionator)
```

```{glue:figure} so_batch_elution_ternary_fig
:name: so_batch_elution_ternary_chromatogram
:scale: 50%

Optimal chromatogram of single-objective optimization of ternary batch elution process.
```

TODO: why is this figure not properly showing?

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(so_batch_elution_ternary_table))
```

{numref}`so_batch_elution_ternary_kpi` shows some values.

(batch_elution_ternary_multi)=
## Multi-objective optimization

Here we do some multi-objective optimization.

<!-- ```{figure} ./results_multi/multi-objective/figures/objectives.png -->
<!-- :name: batch_elution_multi_objectives -->

<!-- Objective space; each dot represents an evaluation. -->
<!-- ``` -->

<!-- ```{figure} ./results_multi/multi-objective/figures/pareto.png -->
<!-- :name: batch_elution_multi_pareto -->

<!-- Pareto Front -->
<!-- ``` -->
