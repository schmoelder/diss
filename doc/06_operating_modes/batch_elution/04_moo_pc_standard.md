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

print("update 3")

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
    ignore_failed=True,
)
```

(batch-elution_moo-pc)=
# Multi-objective optimization of a binary Langmuir separation problem including cycle time

In this case study, the cycle time is included as a second optimization variable.
Because interactions between successive injections on the column may occur, cyclic stationarity must be ensured (see {numref}`stationarity`).
A linear constraint is also imposed to guarantee that the cycle time exceeds the duration of fresh feed injection.
The problem is summarized in {numref}`batch-elution_moo-pc_overview`.

```{code-cell} ipython3
:tags: [remove-cell]

case = cases.get(f"{operating_mode}_standard_multi-objective-per-component")
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

{numref}`batch-elution_moo-pc_fig_obj` depicts the evaluated objective function values as a function of both feed duration and cycle time.
In contrast to the previous multi-objective study ({numref}`batch-elution_auto-cycle_moo-pc_fig_obj`), each variable value now corresponds to multiple objective values, reflecting the two-dimensional optimization space.
Consistent trends are observed: productivity shows a distinct optimum with respect to feed duration, while maximum yield is attained for short injections.
A minimum cycle time is required to avoid excessive cycle-to-cycle overlap.
Eluent consumption peaks as a function of cycle time but plateaus with increasing feed duration.
The lack of evaluated points near this plateau for large feed durations, evident from the lighter color of early-generation evaluations (versus the darker blue of later generations), indicates that the optimizer ceased exploration in this region due to limited expected improvement for other objectives.
(@TODO: Check if that's true.)

The optimal variable values and KPIs for all Pareto edge points are summarized in {numref}`batch-elution_moo-pc_kpi`.
Compared to the previous study, where cycle-to-cycle overlaps were not accounted for ({numref}`batch-elution_auto-cycle_moo-pc_kpi`), higher KPI values could be achieved.
Notably, productivity and eluent consumption are significantly improved, as the tailing end of component $B$ partially elutes into the subsequent peaks of component $A$, enhancing overall performance (see {numref}`batch-elution_moo-pc_fig_chrom`).

```{glue:figure} moo_fig_obj
:name: batch-elution_moo-pc_fig_obj
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
:name: batch-elution_moo-pc_fig_chrom
:scale: 100%

{glue:text}`moo_fig_chrom_caption`
```
