(modeling_approach)=
# Modeling approach

As shown in {numref}`knauer_pid`, the chromatographic system comprises more than the chromatographic column.
Incorporating the system periphery into the model enhances its accuracy by accounting for time delays and additional dispersion caused by tubings and valves.
Without this detailed modeling, these peripheral effects would be incorrectly attributed to column parameters such as bed porosity or axial dispersion.

The periphery can be modeled using combinations of continuously stirred-tank reactors (CSTRs) or dispersive plug flow reactors (DPFRs) (see {numref}`model_formulation`).

The model shown in {numref}`knauer_model` can be summarized as follows:
- The buffer flasks and pumps are modeled by {class}`~CADETProcess.processModel.Inlet` unit operations to define inlet concentrations and flow rates.
- The mixer is approximated by combining a {class}`~CADETProcess.processModel.Cstr` with a {class}`~CADETProcess.processModel.TubularReactor` to model residence time and backmixing.
- The sample loop is represented by a {class}`~CADETProcess.processModel.TubularReactor` unit operation with its corresponding volume.
- Tubing sections before and after the column, as well as the segment between the UV and conductivity sensors, are modeled using {class}`~CADETProcess.processModel.TubularReactor` unit operations to account for additional residence time, backmixing, and the time difference between conductivity and UV signals.
- The outlet of the post-column tubing is compared with the experimental UV signal.
- The output of the detector tubing is compared with the experimental conductivity signal.

At this stage, neither an isotherm model nor a column transport model have been specified.
These will be discussed later in {numref}`column_parameters` and {numref}`adsorption_parameters`, respectively.


```{figure} ./figures/knauer_model.png
:name: knauer_model

Model of Knauer system.
```
