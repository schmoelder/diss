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

(batch_elution_study)=
# Batch-elution chromatography

A basic chromatographic batch-elution setup comprises `feed` and `eluent` reservoirs, a pump to deliver the required flow rate against the column's pressure drop, a valve to switch between feed and eluent, the column itself, and one or more valves for fraction collection.
In CADET-Process, this setup is modeled by connecting two {class}`Inlets <CADETProcess.processModel.Inlet>` and a column unit operation (e.g., {class}`~CADETProcess.processModel.LumpedRateModelWithPores`).
In addition, an {class}`~CADETProcess.processModel.Outlet` is added to the {class}`~CADETProcess.processModel.FlowSheet`.
This allows optimal fractionation times to be identified through chromatogram analysis (see {numref}`fractionation`), eliminating the need for predefined fractionation points and demonstrating a key advantage of model-based design.
The flow sheet is demonstrated in {numref}`batch_elution_flow_sheet`.

```{figure} ./figures/flow_sheet.png
:name: batch_elution_flow_sheet

Flow sheet for the batch-elution process.
```

To model the injection, {class}`Events <CADETProcess.dynamicEvents.event.Event>` are introduced that modify the {attr}`~CADETProcess.processModel.Inlet.flow_rate` attribute of the {class}`~CADETProcess.processModel.Inlet` unit operations.
To reduce the degrees of freedom that need to be explicitly specified, event dependencies are added to ensure that either feed or eluent is always flowing through the column.
The events and durations are depicted in {numref}`batch_elution_events`.

```{figure} ./figures/event_dependencies.png
:name: batch_elution_events

Events of batch-elution process with event dependencies.
```

{numref}`fig_batch_elution` shows the chromatogram of a batch-elution process with incomplete separation, simulated using the parameters listed in {numref}`model_parameters` (standard binary Langmuir binding model).

```{code-cell} ipython3
:tags: [remove-cell]

# Setup process
process_demo = setup_process(
    case_module=case_module,
    separation_problem="standard",
    feed_duration=60,
    cycle_time=600,
)

from CADETProcess.simulator import Cadet
process_simulator = Cadet()

simulation_results = process_simulator.simulate(process_demo)
fig_batch_elution, ax = simulation_results.solution.column.outlet.plot()
glue("fig_batch_elution", fig_batch_elution, display=False)
```

```{glue:figure} fig_batch_elution
:name: fig_batch_elution
:figwidth: 300px

Typical chromatogram of a batch-elution process.
```

(batch_elution_validation)=
## Process Validation (Batch-Elution-Process)

To validate the process configuration, simulation results are compared with analytical solutions derived from equilibrium theory (see {numref}`analytical_solutions`).
For this comparison, a linear isotherm with equivalent Henry coefficients $a_i$ is assumed, and all transport-limiting effects are neglected.
{numref}`fig_batch_elution_validation` compares the concentration profile at the column outlet, demonstrating good agreement between the simulation results and the predictions of equilibrium theory.

```{code-cell} ipython3
:tags: [remove-cell]

# Setup process
from operating_modes.main import setup_process
process_validation = setup_process(
    case_module=case_module,
    separation_problem="standard",
    apply_et_assumptions=True,
    cycle_time=600,
)

# Import tools
from operating_modes.et_simulator import compare_cadet_with_et

fig_batch_elution_validation, ax = compare_cadet_with_et(process_validation)
glue("fig_batch_elution_validation", fig_batch_elution_validation, display=False)
```

```{glue:figure} fig_batch_elution_validation
:name: fig_batch_elution_validation
:scale: 100%

Comparison of a batch-elution simulation chromatogram (solid line) with an analytical equilibrium theory solution (dashed line), assuming a linear binding model and neglecting axial dispersion and other transport-limiting effects.
```

---

The following sections present a series of optimization scenarios of increasing complexity:
First, a simple batch-elution case with ideal assumptions is used to validate the optimization framework.
Next, a more realistic separation problem is considered, followed by multi-objective optimization.
The cycle time is then included as an optimization variable.
Finally, the optimization of a ternary separation problem is addressed.
