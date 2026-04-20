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

print("update 0")

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

operating_mode = "serial-columns"
case_module = importlib.import_module(
    f"operating_modes.{operating_mode.lower().replace('-', '_')}"
)
cases = get_cases_by_operating_mode(
    operating_mode,
    index_by_name=True,
    work_dir=study_root,
)
```

(serial_columns)=
# Serial columns

In situations where one of the components exhibits very strong interaction with the stationary phase, the use of a short pre-column can be advantageous.
By adding such a column, the strongly adsorbing component can be retained before entering the main column, thus avoiding excessively long elution times and reducing the risk of irreversible binding.
As soon as breakthrough of the bound impurity is imminent, the pre-column can be regenerated, replaced, or repacked {cite}`SchmidtTraub2020`.
Alternatively, the output of the pre-column can be dynamically directed either to waste or to the second column, depending on the component currently eluting.

(serial_columns_process)=
## Process model

{numref}`serial_columns_flow_sheet` shows the flow sheet for a process with columns connected in series.
To prevent periods where no flow occurs through a column, a second eluent {class}`~CADETProcess.processModel.Inlet` is added to the system.
This inlet becomes active whenever flow is directed from the first column to the outlet.

This case also illustrates that multiple chromatograms can be fractionated simultaneously to evaluate process performance.
One strategy to increase productivity is to "shave off" sufficiently separated fractions of the mixture and allow only the unresolved portion to migrate through an additional column.

```{figure} ./figures/flow_sheet.png
:name: serial_columns_flow_sheet

Flow sheet for the serial columns process.
```

To model the injection, {class}`Events <CADETProcess.dynamicEvents.Event>` are introduced to modify the {attr}`~CADETProcess.processModel.Inlet.flow_rate` attribute of the {class}`~CADETProcess.processModel.Inlet` unit operations.
To reduce the number of event times that need to be specified, event dependencies are defined to ensure that either feed or eluent is always flowing through the column.

```{figure} ./figures/event_dependencies.png
Events of serial columns process with event dependencies.
```
```{code-cell} ipython3
:tags: [remove-cell]

# Setup process
process_demo = setup_process(
    case_module=case_module,
    separation_problem="ternary",
    split_ratio=1/3,
    feed_duration=0.75*60,
    t_serial_off=2.6*60,
    t_serial_on=5.5*60,
    cycle_time=15*60,
)

from CADETProcess.simulator import Cadet
process_simulator = Cadet()

simulation_results = process_simulator.simulate(process_demo)
fig_serial_columns, _ = case_module.plot_results(simulation_results)
glue("fig_serial_columns", fig_serial_columns, display=False)
```

For this study a ternary separation problem with a Langmuir isotherm is considered (see {numref}`model_parameters`).
{numref}`fig_serial_columns` shows the chromatogram of a process with columns in series.

```{glue:figure} fig_serial_columns
:name: fig_serial_columns
:figwidth: 300px

Typical chromatogram of a serial columns process.
**Left:** Concentration profile at outlet of first column.
**Center:** Concentration profile at first system outlet.
**Right:** Concentration profile at the second column outlet.
```

(serial_columns_validation)=
## Process validation

{numref}`serial_columns_chromatogram` compares the concentration profiles at both system outlets under ideal model assumptions, demonstrating good agreement between the simulation and equilibrium theory.
The ternary separation is validated simultaneously at both measurement points: the first outlet captures the early-eluting fraction collected directly from the first column, while the second column outlet shows the further resolved remaining components.

```{code-cell} ipython3
:tags: [remove-cell]

# Setup process
process_validation = setup_process(
    case_module=case_module,
    separation_problem="ternary",
    apply_et_assumptions=True,
    split_ratio=1/3,
    feed_duration=0.75*60,
    t_serial_off=2.6*60,
    t_serial_on=5.5*60,
    cycle_time=15*60,
)

from operating_modes.et_simulator import compare_cadet_with_et
fig_serial_validation, ax = compare_cadet_with_et(process_validation)
glue("fig_serial_validation", fig_serial_validation, display=False)
```

```{glue:figure} fig_serial_validation
:name: serial_columns_chromatogram
:scale: 50%

Comparison of serial columns simulation chromatograms (solid lines) with the analytical equilibrium theory solution (dashed lines), assuming a linear binding model and neglecting axial dispersion and other transport-limiting effects.
**Left:** Concentration profile at first system outlet.
**Right:** Concentration profile at second column outlet.
```

(serial_columns_optimization)=
## Process Optimization

To optimize the process with columns connected in series, the decision variables include both the times at which the serial connection is cut and reconnected, as well as the individual column lengths.
The total column length is kept constant during optimization.
To aid the optimizer with the optimization, a variable dependency is introduced to calculate $t_{serial,on}$ from both $t_{serial,off}$ and $\Delta t_{serial}$.
The problem is summarized in {numref}`serial-columns_ternary_auto-cycle_moo-pc_overview`.

```{code-cell} ipython3
:tags: [remove-cell]

case = cases.get(f"{operating_mode}_ternary_auto-cycle-time_multi-objective-per-component")
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

{numref}`serial-columns_ternary_auto-cycle_moo-pc_fig_obj` depicts the evaluated objective function values across all decision variables.
The Pareto-optimal solutions, including variable and KPI values, are documented in {numref}`serial-columns_ternary_auto-cycle_moo-pc_kpi`.
The associated chromatograms are provided in {numref}`serial-columns_ternary_auto-cycle_moo-pc_fig_chrom`.

The multi-objective optimization reveals several characteristics of serial-column operation.
Well-defined optima emerge for most objectives and decision variables.
Interestingly, the serial duration variable shows no significant sensitivity improvement compared to the individual $t_{\text{serial,on}}$ variable, contrasting with observations for MR-SSR in {numref}`mrssr_auto-cycle_moo-pc_fig_obj`.
This reduced sensitivity can be attributed to the added complexity of the ternary separation problem.
Across all Pareto-optimal solutions, the chromatograms show successful ternary separation with baseline resolution between all components.
Particularly notable is the strong dependence of the eluent consumption objective on the serial switching times, which results from extreme overloading conditions experienced by component $C$ in certain operating regimes.
The optimization also reveals potential for tuning geometric column parameters: the optimal column length ratio depends on both the target component and the dominant performance indicator.

```{glue:figure} moo_fig_obj
:name: serial-columns_ternary_auto-cycle_moo-pc_fig_obj
:scale: 100%

{glue:text}`moo_fig_obj_caption`
```

```{raw} latex
\pagebreak
\begin{landscape}
```

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_table))
```

```{raw} latex
\end{landscape}
\pagebreak
```

```{glue:figure} moo_fig_chrom
:name: serial-columns_ternary_auto-cycle_moo-pc_fig_chrom
:scale: 100%

{glue:text}`moo_fig_chrom_caption`
```

**Summary**

This case study demonstrates that the framework can optimize processes with multiple columns and simultaneous fractionation at several outlets.
The ternary separation benefits from tuning both the serial switching times and the column length ratio, with the optimal configuration depending on the chosen performance objective.
Eluent consumption is particularly sensitive to the switching times, driven by column overloading under high-feed-volume conditions.

---

This chapter demonstrates the framework's capability to handle a wide range of chromatographic operating modes, ranging from simple batch elution to complex multi-column setups with recycling.
All implemented processes have been validated against equilibrium theory, confirming the correctness of the process models and event structures.

Multi-objective optimization consistently reveals non-trivial trade-offs between productivity, yield, and eluent consumption.
The framework naturally identifies sophisticated operational strategies, including:
- waste fractions,
- stacked injections,
- cycle-to-cycle peak overlaps, and
- peak interlocking.

A notable finding across the recycling case studies is that batch elution emerges as the productivity-optimal limiting case of more complex recycling processes.
This behavior confirms the framework's robustness and points to its suitability for superstructure optimization, where the operating mode itself is a design variable.
For processes with different objectives, such as minimizing eluent consumption, recycling or serial-column configurations can provide clear advantages, underscoring that process selection depends on both the separation system and the priority given to each performance indicator.
