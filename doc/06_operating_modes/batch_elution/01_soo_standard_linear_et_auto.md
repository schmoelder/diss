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

print("update 7")

import importlib
from pathlib import Path
import sys

from IPython.display import display, Markdown
from git import Repo
import matplotlib.pyplot as plt
from myst_nb import glue

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
print(diss_root)
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

(batch_elution_linear_et_auto-cycle-time_soo)=
# Single-objective optimization of an idealized system

To validate the framework and ensure the optimizer can recover the expected operating conditions, at first idealized scenario is evaluated: the binary model system with linear binding and ET assumptions.
Here, the process is optimized by varying the feed duration using a single objective function with equal weights for all KPIs {eq}`weighted_objective`.
While $100\%$ purity would be ideal, the targeted purity is set to $99.9\%$ to mitigate performance issues arising from numerical dispersion and the finite accuracy of the automatic fractionation algorithm.
The problem is summarized in {numref}`batch-elution_linear_et_auto-cycle_soo_overview`.

```{code-cell} ipython3
:tags: [remove-cell]

case = cases.get(f"{operating_mode}_standard_linear_et_auto-cycle-time_single-objective")
overview = setup_overview(case)

(
    (soo_fig_obj, _, soo_fig_obj_caption),
    (soo_fig_chrom, _, soo_fig_chrom_caption),
    soo_table,
    soo_results,
    simulation_results,
    fractionator,
) = process_soo_results(
    case,
    load_kwargs={"allow_commit_hash_mismatch": True},
    return_results=True,
)
glue("soo_fig_obj", soo_fig_obj, display=False)
glue("soo_fig_obj_caption", soo_fig_obj_caption)

glue("soo_fig_chrom", soo_fig_chrom, display=False)
glue("soo_fig_chrom_caption", soo_fig_chrom_caption)

from operating_modes.post_processing import format_mm_ss

feed_duration = rf"${format_mm_ss(soo_results.x[0])}~\text{{min}}$"
glue("feed_duration", feed_duration)

cycle_time_expected = rf"${format_mm_ss(2*soo_results.x[0])}~\text{{min}}$"
glue("cycle_time_expected", cycle_time_expected)

cycle_time = rf"${format_mm_ss(fractionator.cycle_time)}~\text{{min}}$"
glue("cycle_time", cycle_time)
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(overview))
```

The cycle time, required for KPI calculation, is automatically derived from the resulting chromatograms.
To ensure complete elution, each simulation is initialized with a sufficiently large cycle time.
The final cycle time is then determined by truncating regions where the chromatogram concentration drops below $0.1\%$ of the feed concentration, thereby effectively simulating stacked injection with touching-band separation.
Under optimal conditions, the feed duration is expected to produce two pure component peaks with a cycle time that equals exactly twice the feed duration, as the injection volume is maximized until the eluting peaks just touch at the column outlet.

<!-- @Note: It is currently not possible to use inline glue with LaEeX/Math formatting.  -->
```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---

display(Markdown(rf"""
{{numref}}`batch-elution_linear_et_auto-cycle_soo_fig_obj` shows the evaluated objective function values as a function of the feed duration, with a clear maximum at {feed_duration}.
"""))
```

```{glue:figure} soo_fig_obj
:name: batch-elution_linear_et_auto-cycle_soo_fig_obj
:scale: 100%

{glue:text}`soo_fig_obj_caption`
```

<!-- @Note: It is currently not possible to use inline glue with LaEeX/Math formatting.  -->
```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---

display(Markdown(rf"""
{{numref}}`batch-elution_linear_et_auto-cycle_soo_kpi` summarizes the results.
Although the required purity is met, the yield is slightly below $100\%$ due to numerical dispersion causing band broadening, resulting in a small waste fraction.
Consequently, also the determined cycle time of {cycle_time} is slightly larger than the expected time of {cycle_time_expected}, as illustrated in the corresponding chromatogram ({{numref}}`batch-elution_linear_et_auto-cycle_soo_fig_chrom`).
"""))
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_table))
```

```{glue:figure} soo_fig_chrom
:name: batch-elution_linear_et_auto-cycle_soo_fig_chrom
:scale: 100%

{glue:text}`soo_fig_chrom_caption`
```
