---
jupytext:
  formats: md:myst,py:percent
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(recycling_process)=
# Recycling Techniques

The design of preparative chromatography poses major challenges in balancing the interdependence of product purity and yield, as well as the efficiency of the column and its pressure drop.
To improve difficult separations, it may be necessary to increase the column's separation efficiency by using a longer column or reducing the particle size of the stationary phase.
However, using a longer column or a particles can result in an excessively high pressure drop.
To overcome this issue, several recycling techniques exist to effectively improve the separation.
By connecting the column's outlet to its inlet, the separation can pass through the column multiple times, without the need for a longer column or smaller particles, and hence, with a manageable pressure drop.

In the following different recycling concepts are introduced.

(clr_process_process)=
## Closed Loop Recycling Process

In closed-loop recycling (CLR), the stock mixture is pumped over the column several times until the desired purity is achieved.
The general structure of a CLR is shown below.

```{figure} ./figures/clr_flow_sheet.svg
:name: clr_flow_sheet

Flow sheet for closed-loop recycling process.
```

To realize the recycling, the {attr}`~CADETProcess.processModel.FlowSheet.output_state` of the column needs to be modified, leading to the following event structure:

```{figure} ./figures/clr_events.svg
:name: clr_events

Events for closed-loop recycling process.
```

To reduce the number of event times that need to be specified, event dependencies are specified which enforce that always either feed or eluent are being pumped through the column.

Now, the cycle time is set to $10~min$ and the `feed_duration` to $1~min$.

Here, the first plot shows the concentration profile at the column outlet.
It is important to note that since part of this profile is recycled, the concentration profile at the system outlet must be considered (second plot) to evaluate the process performance.

@TODO: Add figures / chromatograms

The disadvantage of the CLR process is an increased dispersion due to multiple passes through the pump and additional piping.

To improve the overall process performance, the CLR process is often combined with peak shaving.
In this process, the initial and final regions of the chromatogram with sufficient purity are "shaved off" during each cycle.
Peak shaving can reduce the number of recycling cycles required, since a decreasing amount of components must be pumped across the column.

```{figure} ./figures/clr_peak_shaving_events.svg
:name: clr_peak_shaving_events

Events for closed-loop recycling process with peak shaving.
```

(ssr_process)=
## Steady-State Recycling Process

In addition to the recycled fraction, fresh feed can also be injected in each cycle, resulting in the formation of a cyclic steady-state.
This process, called closed-loop steady-state recycling (CL-SSR), can achieve higher productivity compared to CLR.
However, due to additional dispersion in the system periphery, maintaining the separation of components generated during the passage of the column is difficult to realize.
Hence, determining the optimal time at which to add new feed is therefore complex.
To overcome this problem, a tank can be inserted in which the recycling fraction and new feed are mixed.
The recycling fraction and new feed are then injected together in a process called mixed-recycle steady-state recycling (MR-SSR).
A schematic flow diagram of the MR-SSR process is shown below.

```{figure} ./figures/mrssr_flow_sheet.svg
:name: mrssr_flow_sheet

Flow sheet for mixed-recycle steady-state recycling process.
```

For this demonstration, consider a two-component system with a Langmuir isotherm.

To realize the recycling, the {attr}`~CADETProcess.processModel.FlowSheet.output_state` of the column needs to be modified.
To reduce the number of event times that need to be specified, event dependencies are specified which enforce that always either feed or eluent are being pumped through the column.

```{figure} ./figures/mrssr_events.svg
:name: mrssr_events

Events for mixed-recycle steady-state recycling process with event dependencies.
```

Now, the cycle time is set to $10~min$ and the `feed_duration` to $1~min$ and the recycling times are specified.

Since the process shows a startup behavior before reaching steady state, multiple cycles need to be simulated.
For this purpose, a {class}`~CADETProcess.stationarity.StationarityEvaluator` is used (see {ref}`stationarity_guide`).

@TODO: show simulation results
