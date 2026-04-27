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

(batch-elution_auto-cycle_moo-pc)=
# Multi-objective optimization of a binary Langmuir separation problem

In this case study, the same separation problem is reformulated as a multi-objective optimization.
Since all KPIs are derived from the same simulation run, no additional simulations are required compared to the single-objective case; the information that was previously aggregated into a single scalar is now retained as separate objectives (see {numref}`multi_objective_optimization`).
Here, a separate fractionation optimizer is configured for each component, using the `ranking` parameter to restrict evaluation to that component's KPIs; this approach is denoted "multi-objective-per-component".
To enable direct comparison with the single-objective study, a meta-score that computes the same aggregated objective is included; it is used purely for post-processing and is not treated as an optimization objective (see {numref}`meta_scores`).
The problem is summarized in {numref}`batch-elution_auto-cycle_moo-pc_overview`.

```{code-cell} ipython3
:tags: [remove-cell]

case = cases.get(f"{operating_mode}_standard_auto-cycle-time_multi-objective-per-component")
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

from operating_modes.post_processing import format_mm_ss

feed_duration_prod_0 = rf"${format_mm_ss(fractionators[0].process.feed_duration.time)}~\text{{min}}$"
glue("feed_duration_prod_0", feed_duration_prod_0)
feed_duration_prod_1 = rf"${format_mm_ss(fractionators[1].process.feed_duration.time)}~\text{{min}}$"
glue("feed_duration_prod_1", feed_duration_prod_1)
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(overview))
```

{numref}`batch-elution_auto-cycle_moo-pc_fig_obj` shows the evaluated objective function values as a function of feed duration.
As multi-objective optimization results in a Pareto front containing (in theory) infinitely many trade-off solutions, the discussion is limited here to the Pareto edge points, i.e., the solutions at the extremes of the Pareto front, each optimal for a single objective.
Unlike in the single-objective case, the optimal feed duration now differs depending on which KPI is being maximized.
The optimal variable values and KPIs for these edge points are summarized in {numref}`batch-elution_auto-cycle_moo-pc_kpi`.

<!-- @Note: It is currently not possible to use inline glue with LaEeX/Math formatting.  -->
```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---

display(Markdown(rf"""
When productivity is maximized, relatively large feed durations are selected ({feed_duration_prod_0} for component $A$ and {feed_duration_prod_1} for component $B$).
This increases throughput but leads to overlapping peaks and reduced recovery, as visible in the corresponding chromatograms (a, b).
For yield maximization, very small injections are employed to ensure baseline separation and complete recovery (c, d).
Eluent consumption minimization is achieved through even higher feed durations, resulting in injection plateaus (e, f).
Although product is wasted in this case, increasing the feed duration leaves the eluent consumption objective unchanged, since no eluent is used during the feed phase.
"""))
```

The chromatogram corresponding to the optimal meta-score (g) is essentially identical to the single-objective result ({numref}`batch-elution_auto-cycle_moo-pc_fig_chrom`).
Comparison with the single-objective results ({numref}`batch-elution_auto-cycle_moo-pc_kpi`) shows that the multi-objective results strictly improve upon the single-objective solution: the previous optimum is recovered while candidates with better individual KPI performance are identified at the same time.

```{glue:figure} moo_fig_obj
:name: batch-elution_auto-cycle_moo-pc_fig_obj
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
:name: batch-elution_auto-cycle_moo-pc_fig_chrom
:scale: 100%

{glue:text}`moo_fig_chrom_caption`
```
