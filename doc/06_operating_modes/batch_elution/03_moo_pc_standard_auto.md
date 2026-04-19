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

print("update 10")

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


In this case study, the process optimization is formulated as a multi-objective problem.
Since the majority of the evaluation cost lies in the simulation, and all KPIs are computed even for single-objective optimization, this information is leveraged more effectively in a multi-objective framework rather than being discarded.
While the multi-objective problem could be formulated such that only a combined fractionation is performed for each simulation, ranking both components equally, here, the KPIs are evaluated for each component separately.
This approach, denoted as "multi-objective-per-component," requires individual fractionation optimizations for each component while excluding the other via the `ranking` parameter.
To enable direct comparison with the previously performed single-objective study, a meta-score is included in the optimization problem to compute the same objective function value for each candidate as before.
Importantly, the optimizer does not treat this meta-score as an additional objective.
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
As multi-objective optimization results in a Pareto front containing infinitely many trade-off solutions, the discussion is limited here to the Pareto edge points, i.e., the solutions at the extremes of the Pareto front, each optimal for a single objective.
Unlike in single-objective studies, the location of those local maxima now depends on the individual objective.
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
For yield maximization, very small injections are employed to ensure baseline separation and near-complete recovery (c, d).
Visual inspection of these chromatograms suggests complete product capture, indicating the slight recovery deviation from 100% (values ≥ 99.8%) likely results from the fractionation algorithm's numerical precision limits rather than physical separation issues.
Eluent consumption minimization is achieved through even higher feed durations, resulting in injection plateaus (e, f).
Although product is wasted, this approach does not affect the objective value; instead, more feed is beneficial because no eluent is used during feeding.
"""))
```

The chromatogram corresponding to the optimal meta-score (g) is essentially identical to the single-objective result ({numref}`batch-elution_auto-cycle_moo-pc_fig_chrom`).
Comparison with the single-objective results ({numref}`batch-elution_auto-cycle_moo-pc_kpi`) reveals that the multi-objective optimization not only recovers the previous solutions but also identifies strictly better candidates for each KPI.
This demonstrates that the MOO framework can fully replace the SOO approach, capturing all previous solutions while providing improved performance across all objectives.

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
