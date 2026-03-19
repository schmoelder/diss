(process_model)=
# Process model

The starting point of process development is the setup of a {class}`~CADETProcess.processModel.Process` (see {numref}`Figure %s <framework_overview>`) model, i.e., the specific configuration of the chromatographic process.
This is realized using {class}`UnitOperations <CADETProcess.processModel.UnitBaseClass>` as building blocks.
Multiple {class}`UnitOperations <CADETProcess.processModel.UnitBaseClass>` can be connected in a {class}`~CADETProcess.processModel.FlowSheet`, which describes the mass transfer between the individual units.
Finally, dynamic {class}`Events <CADETProcess.dynamicEvents.Event>` can be defined to model dynamic changes of model parameters, including flow rates and system connectivity.
In this chapter, an overview about the different components of the {class}`~CADETProcess.processModel.Process` is given.

(unit_operations)=
## Unit operations

A {class}`UnitOperation <CADETProcess.processModel.UnitBaseClass>` represents the physico-chemical behavior of an apparatus and holds the model parameters.
{numref}`unit_operation` displays a UML (Unified Modeling Language) diagram illustrating the unit operation's structure and relationships.
A UML diagram is a visual representation that depicts the structure, relationships, and interactions of components or objects in a system using standardized symbols and notations {cite}`Rumbaugh2010`.

```{figure} ./figures/unit_operation.png
:name: unit_operation

UML diagram of a unit operation.
The `UnitOperationBase` provides a unified interface for all its implementations.
Exemplary, a `LumpedRateModelWithoutPores` is shown that inherits from the base class and in addition specifies the parameter of the model
equations, including their type (e.g. a float for the column length).
Each unit operation also has information about components involved in the system.
Optionally, unit operations can also be associated with binding and reaction models.
Both are defined as abstract interfaces where concrete implementations specify the corresponding parameters (demonstrated here by a `Linear` and `MassActionLaw` class respectively).
For unit operations in which binding models or reactions are not modeled, the `NoBinding` and `NoReaction` classes are used.
```

To ensure that all parts of the process have the same number of components, a {class}`~CADETProcess.processModel.ComponentSystem` needs to be configured and added to all unit operations.
These components can also be named, which later automatically adds legends to the plot methods of CADET-Process.
All unit operations can be associated with {class}`BindingModels <CADETProcess.processModel.BindingBaseClass>` that describe the interaction of components with surfaces or chromatographic stationary phases.
For this purpose, a variety of equilibrium relations can be selected.
These include the simple {class}`~CADETProcess.processModel.Linear` adsorption isotherm, competitive forms of the {class}`~CADETProcess.processModel.Langmuir` and the {class}`~CADETProcess.processModel.BiLangmuir` models, as well as the competitive {class}`~CADETProcess.processModel.StericMassAction` law.
Moreover, {class}`ReactionModels <CADETProcess.processModel.ReactionBaseClass>` can be used to model chemical reactions.

(flow_sheet)=
## Flow sheet

The connectivity of unit operations is defined in the {class}`~CADETProcess.processModel.FlowSheet` class.
This class provides a directed graph structure that allows for the simple definition of configurations for multi-column or reactor-separator networks, even when they are cyclic.
Furthermore, unit operation models can be used to model tubing and other external volumes.

Every unit operation can have any number of input and output streams except for {class}`Inlets <CADETProcess.processModel.Inlet>`, which represent streams entering the system, and {class}`Outlets <CADETProcess.processModel.Outlet>`, which represent those exiting.
If a unit operation has more than one input, all ingoing streams are mixed before entering the unit.
If a unit operation has multiple outputs, the distribution of those streams needs to be specified (see {numref}`Fig. %s <flow_demo>`).
In the following, this distribution will be denoted as `output_state`.

```{figure} ./figures/flow_demo.png
---
width: 60%
name: flow_demo
---

Flow sheet with multiple inlets and outlet.
Streams entering a unit operation are mixed.
For streams exiting a unit operation, the percent ratio to each of its destinations must be specified.
```

For a more practical example, typical for batch-elution chromatography, refer to {numref}`Fig. %s <batch_elution_flow_sheet_intro>`.
Here, the feed and eluent reservoirs can both be modeled as {class}`~CADETProcess.processModel.Inlet` unit operations, which are each connected to a column model unit operation, e.g. a {class}`~CADETProcess.processModel.LumpedRateModelWithPores`.
This unit is then connected to an {class}`~CADETProcess.processModel.Outlet` unit, which represents the material leaving the process for further processing.
Note that it is straightforward to also include internal recycles in the {class}`~CADETProcess.processModel.FlowSheet`, which is important for systems such as SSR or SMB processes (see example in {numref}`Section %s <ssr>`).

### A note on flow rates

In CADET-Process, the {class}`~CADETProcess.processModel.Inlet` model acts as source unit that "generates" flow.
This flow is then transported to subsequent unit operations downstream.
Since all fluids in CADET-Process are considered incompressible, all flow entering a unit must also exit from it.
A notable exception is the {class}`~CADETProcess.processModel.Cstr` model which can have a variable volume.
Consequently, if the flow rate of a {class}`~CADETProcess.processModel.Cstr` is explicitly specified, the outgoing streams can be decoupled from the ingoing streams.
This can be useful, e.g., to model holdup tanks.
However, it is important that the volume of a {class}`~CADETProcess.processModel.Cstr` never becomes $0$ or CADET will raise an `Exception`.
If not specified for a {class}`~CADETProcess.processModel.Cstr`, the unit is treated like all other unit operations models, and the outgoing flow rate equals the incoming flow rate.
This can be useful, e.g., when modeling valves.

Since internal recycles are also possible in CADET-Process, the actual flow rates for every unit operation need to be determined before simulation.
This calculation is performed automatically for all time sections before running a simulation while accounting for dynamic changes of flow rates and output states.

(process)=
## Process

The {class}`~CADETProcess.processModel.Process` class is used to define dynamic changes to the unit operation parameters or flow sheet connectivity.
For this purpose, an {class}`Event <CADETProcess.dynamicEvents.Event>` class is introduced which stores the information of those changes:

- `name`: Name of the event.
- `performer`: Object performing the event (e.g., a unit operation)
- `parameter`: Parameter that is changed.
- `state`: Value to which the parameter is changed to at event execution.
- `time`: Time at which the event is executed.

{numref}`events` illustrates the events required to model and simulate a batch-elution process.
In addition to setting event times, it is also necessary to establish the overall duration of the process.
As CADET-Process is designed to simulate cyclic processes as well, where the same sequence of events is repeated multiple times, this interval is referred to as the cycle time $\Delta t_{\text{cycle}}$ (see {numref}`stationarity`).

```{figure} ./figures/events.png
:name: events

Dynamic events of a batch-elution process.
At $t = 0~min$, the flow of the `Feed` unit operation is turned on, while the flow of the `Eluent` unit is turned off.
At $t = 1~min$, the flow of the `Feed` unit operation is turned off, while the flow of the `Eluent` unit is turned on.
```

### Event Dependencies

To reduce complexity in process configurations within CADET-Process, dependencies between events can be specified.
These dependencies determine the occurrence times of one event based on the timings of other events.
This method is particularly advantageous for advanced processes as it reduces the degrees of freedom and improves usability.
Additionally, a {class}`~CADETProcess.dynamicEvents.Duration` can be defined to denote the time interval between two events.
For simulations encompassing more than one cycle, the event time for all events, including independent ones, also accounts for the cycle time.
Consequently, the execution time $t_{j,n}$ of a dependent event $j$ during the $nth$ cycle is calculated using the following equation:

$$
t_{j,n} = \left( n - 1 \right) \Delta t_{\text{cycle}} + \sum_i^{n_{\text{dep}}} \lambda_i \cdot f_i(t_{\text{dep},i}) ,
$$

where $\Delta t_{\text{cycle}}$ represents the cycle time, $n_{\text{dep}}$ is the number of dependencies of event $j$, $t_{\text{dep},i}$ is the time of dependency $i$, $\lambda_i$ is a linear factor, and $f_i$ is a transform function.

By incorporating event dependencies into the batch-elution process example, the feed is switched on every time the elution buffer is switched off, and vice versa.
If the start time of the injection is set to $t = 0~\text{min}$, only the feed duration and cycle time need to be adjusted, which is particularly useful in process optimization scenarios (see {numref}`event_dependencies`).

```{figure} ./figures/event_dependencies.png
:name: event_dependencies

Dynamic events in a batch-elution process, with dependent events highlighted in green and durations in blue.
Arrows indicate the dependency of an event's execution time on other events or durations.
In simulations with multiple cycles, the event time also accounts for the cycle time.
```
