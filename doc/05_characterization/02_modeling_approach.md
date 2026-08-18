(modeling_approach)=
# Modeling approach

As shown in {numref}`knauer_pid`, the chromatographic system comprises more than the chromatographic column.
Incorporating the system periphery into the model enhances its accuracy by accounting for time delays and additional dispersion caused by tubing and valves.
Without this inclusion, the peripheral effects would be incorrectly attributed to column parameters such as bed porosity or axial dispersion.
The periphery can be modeled using combinations of CSTRs or DPFRs (see {numref}`model_formulation`).
The model shown in {numref}`knauer_model` can be summarized as follows:

- The buffer flasks are modeled by {class}`~CADETProcess.processModel.Inlet` unit operations to define inlet concentrations profiles and provide flow rates.
- The mixer and pump head are approximated by combining a {class}`~CADETProcess.processModel.Cstr` with a {class}`~CADETProcess.processModel.TubularReactor` to model residence time and backmixing.
- The sample loop is represented by a {class}`~CADETProcess.processModel.TubularReactor` unit operation with its corresponding volume.
- Tubing sections before and after the column, as well as the segment between the UV and conductivity sensors, are modeled using {class}`~CADETProcess.processModel.TubularReactor` unit operations to account for additional residence time, backmixing, and the time difference between conductivity and UV signals.
- The outlets of the post-column tubing and the detector tubing serve as model measurement points, corresponding to the UV and conductivity sensors in the physical system, respectively.

At this stage, neither an isotherm model nor a column transport model have been specified.
These will be discussed later in {numref}`column_parameters` and {numref}`adsorption_parameters`, respectively.

```{figure} ./figures/knauer_model.png
:name: knauer_model
:width: 100%

Model of Knauer system.
```

To streamline the setup of the system model, a custom {class}`~CADETProcess.processModel.FlowSheet` subclass was implemented for this work that automatically configures and connects the unit operations, with arguments for specifying the sample loop volume and any units bypassed during periphery characterization.
Several custom {class}`~CADETProcess.processModel.Process` subclasses were also implemented to configure pulse injection, breakthrough curve, and gradient elution experiments, along with utilities to convert raw Knauer data into {class}`~CADETProcess.reference.ReferenceIO` objects.

For each experiment, a {class}`~CADETProcess.comparison.Comparator` was set up using the {class}`~CADETProcess.comparison.NRMSE` metric (see {numref}`comparison`), and its output was used as the objective in an {class}`~CADETProcess.optimization.OptimizationProblem` with the corresponding parameters as optimization variables (see {numref}`optimization`).
All optimization problems were solved using the {class}`U-NSGA-3 <CADETProcess.optimization.U_NSGA3>` optimizer.
