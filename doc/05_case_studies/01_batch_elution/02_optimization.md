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

(batch_elution_example)=

# Optimization of Batch Elution Process

By selecting appropriate operating conditions, such as injected amount and flow rate, an efficient operating scenario can be achieved in which the stationary phase is utilized very efficiently.
The highest product recovery is achieved by "baseline separation," where the component peaks of the same injection do not overlap when leaving the column.
Moreover, by minimizing the time between two injections, productivity can be improved.
By allowing for waste fractions collected between product fractions or between peaks of consecutive injections, productivity and eluent consumption may be further improved at the cost of lower recovery.

These operating conditions can be adjusted using model based design.
For this purpose, an {class}`~CADETProcess.optimization.OptimizationProblem` is set up where to maximize process performance.
This can be achieved by combining multiple parameters into a single objective (see {ref}`batch_elution_optimization_single`) or by setting up a multi-objective problem (see {ref}`batch_elution_optimization_multi`).

## Single Objective Optimziation

```{figure} ./results_single/results_batch_elution_single/figures/objectives.png
:name: batch_elution_single_objectives

Objective space; each dot represents an evaluation.
```

## Multi-Objective optimization with equal ranking

```{figure} ./results_multi_ranked/results_batch_elution_multi_ranked/figures/objectives.png
:name: batch_elution_multi_ranked_objectives

Objective space; each dot represents an evaluation.
```

```{figure} ./results_multi_ranked/results_batch_elution_multi_ranked/figures/pareto.png
:name: batch_elution_multi_ranked_pareto

Pareto front
```

## Multi-Objective optimization

```{figure} ./results_multi/results_batch_elution_multi/figures/objectives.png
:name: batch_elution_multi_objectives

Objective space; each dot represents an evaluation.
```

```{figure} ./results_multi/results_batch_elution_multi/figures/pareto.png
:name: batch_elution_multi_pareto

Pareto Front
```
