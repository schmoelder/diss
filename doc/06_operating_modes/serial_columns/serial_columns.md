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

```{code-cell} ipython3
:tags: [remove-cell]

%matplotlib inline
%config InlineBackend.figure_format = 'retina'

from pathlib import Path
import sys

from IPython.display import display, Markdown
from git import Repo
import matplotlib.pyplot as plt
from myst_nb import glue

# Import the study module
diss_root = Path(Repo(search_parent_directories=True).working_dir)
studies_root = diss_root / "studies" / "operating_modes"
sys.path.insert(0, str(studies_root))

from run_all import create_figure_and_table, setup_study
study = setup_study(studies_root, "serial_columns")

variable_units={
    r"\Delta t_{\text{cycle}}": r"\text{s}",
    r"\Delta t_{\text{feed}}": r"\text{s}",
    r"t_{\text{serial,off}}": r"\text{s}",
    r"t_{\text{serial,on}}": r"\text{s}",
    r"L_{\text{c,1}}": r"\text{m}",
    r"L_{\text{c,2}}": r"\text{m}",
}
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

from CADETProcess.simulator import Cadet

from process import setup_process, plot_results

process = setup_process()

process.flow_sheet.column_1.length = 0.2
process.flow_sheet.column_2.length = 0.4

process.cycle_time = 600
process.feed_duration.time = 60
process.serial_off.time = 200
process.serial_on.time = 420

process_simulator = Cadet()
process_simulator.evaluate_stationarity = False

simulation_results = process_simulator.simulate(process)

fig, axs = plot_results(simulation_results)

glue("serial_columns", fig, display=False)
```

```{glue:figure} serial_columns
:name: serial_columns_chromatogram
:scale: 50%

**Left:** Concentration profile at outlet of first column.
**Center:** Concentration profile at first system outlet.
**Right:** Concentration profile at the second column outlet.
```

(serial_columns_evaluation)=
## Process evaluation

After simulation, the {class}`~CADETProcess.simulationResults.SimulationResults` can be analyzed to determine optimal fractionation times using the {mod}`~CADETProcess.fractionation` module.

(serial_columns_optimization)=
## Process optimization

- Feed duration
- serial_on
- serial_off
- cycle time
- column_1.length
- column_2.length

For this purpose, an {class}`~CADETProcess.optimization.OptimizationProblem` is formulated to maximize process performance.

(serial_columns_single)=
## Single-objective optimization

Here we do some single-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

soo_chrom, ax, soo_table, soo_obj = create_figure_and_table(
    studies_root,
    "serial_columns",
    "single-objective",
    variable_units=variable_units,
)
glue("serial_columns_soo_chrom", soo_chrom, display=False)
```

{numref}`serial_columns_soo_objectives` shows objective function values.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_obj))
```

{numref}`serial_columns_soo_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(soo_table))
```

{numref}`serial_columns_soo_chrom` shows chromatogram of best value.

```{glue:figure} serial_columns_soo_chrom
:name: serial_columns_soo_chrom
:scale: 100%

Optimal chromatogram of single-objective optimization of serial columns process.
```

(serial_columns_multi)=
## Multi-objective optimization

Here we do some multi-objective optimization.

```{code-cell} ipython3
:tags: [remove-cell]

moo_chrom, ax, moo_table, moo_obj = create_figure_and_table(
    studies_root,
    "serial_columns",
    "multi-objective",
    variable_units=variable_units,
)
glue("serial_columns_moo_chrom", moo_chrom, display=False)
```

{numref}`serial_columns_moo_objectives` shows objective function values.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_obj))
```

{numref}`serial_columns_moo_kpi` summarizes results.

```{code-cell} ipython3
---
mystnb:
  markdown_format: myst
  remove_code_source: true
---
display(Markdown(moo_table))
```

{numref}`serial_columns_moo_chrom` shows optimal chromatograms.

```{glue:figure} serial_columns_moo_chrom
:name: serial_columns_moo_chrom
:scale: 100%

Optimal chromatogram of multi-objective optimization of serial columns process.
```
