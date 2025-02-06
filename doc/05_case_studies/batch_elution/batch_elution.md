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
---

(batch_elution_study)=
# Batch Elution Chromatography

A basic chromatographic batch-elution setup is comprised of `feed` and `eluent` reservoirs, a pump that can deliver the necessary flow rate against the pressure drop of the packed column, a valve to select whether feed or eluent are pumped into the column, the column itself, and one or more valves for the collection of fractions.

In **CADET-Process**, this can be modelled by connecting two {class}`Inlets <CADETProcess.processModel.Inlet>`, a column model (e.g. {class}`~CADETProcess.processModel.LumpedRateModelWithoutPores`), and an {class}`~CADETProcess.processModel.Outlet`.

```{figure} ./figures/flow_sheet.png
:name: batch_elution_flow_sheet

Flow sheet for batch elution process.
```

To model the injection valve, {class}`Events <CADETProcess.processModel.Event>` are introduced that modify the {attr}`~CADETProcess.procesModel.Inlet.flow_rate` attribute of the {class}`~CADETProcess.processModel.Inlet` unit operations.

```{figure} ./figures/events.png
Events of batch elution process.
```

To reduce the number of event times that need to be specified, event dependencies are specified which enforce that always either feed or eluent are being pumped through the column.

```{figure} ./figures/event_dependencies.png
Events of batch elution process with event dependencies.
```

## Optimize Fractionation Times

After simulation, the {class}`~CADETProcess.simulationResults.SimulationResults` can be analyzed to determine optimal fractionation times using the {mod}`~CADETProcess.fractionation` module.
