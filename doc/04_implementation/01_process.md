(process_model)=
# Process model

The starting point of process development is the setup of a {class}`~CADETProcess.processModel.Process` model, which represents the specific chromatographic process at hand.
It is composed of {class}`UnitOperations <CADETProcess.processModel.UnitBaseClass>`, which define the physico-chemical behavior of individual apparatus components.
Multiple unit operations can be connected in a {class}`~CADETProcess.processModel.FlowSheet`, which describes the mass transfer between them.
Time-dependent changes to model parameters, including flow rates and system connectivity, are defined using {class}`Events <CADETProcess.dynamicEvents.Event>`.
The following sections describe each of these building blocks in turn.

(unit_operations)=
## Unit operations

A {class}`UnitOperation <CADETProcess.processModel.UnitBaseClass>` represents the physico-chemical behavior of an apparatus and holds the model parameters.
{numref}`unit_operation` displays a UML class diagram (see {numref}`uml`) illustrating the unit operation's structure and relationships.

```{figure} ./figures/unit_operation.png
:name: unit_operation
:width: 100%

UML diagram of a unit operation.
The `UnitOperationBase` provides a unified interface for all its implementations.
Exemplary, a `LumpedRateModelWithoutPores` is shown that inherits from the base class and in addition specifies the parameter of the model
equations, including their type (e.g. a float for the column length).
Each unit operation also has information about components involved in the system.
Optionally, unit operations can also be associated with binding and reaction models.
Both are defined as abstract interfaces where concrete implementations specify the corresponding parameters (demonstrated here by a `Linear` and `MassActionLaw` class respectively).
For unit operations in which binding models or reactions are not modeled, the `NoBinding` and `NoReaction` classes are used.
```

To ensure consistency across all parts of the process, a {class}`~CADETProcess.processModel.ComponentSystem` must be configured and assigned to all unit operations.
This system defines the components involved in the separation, including their names and optionally physical properties such as charge or molar mass.
Component names are automatically used to generate legends in CADET-Process plot methods.
All unit operations can be associated with {class}`BindingModels <CADETProcess.processModel.BindingBaseClass>` that describe the interaction of components with surfaces or chromatographic stationary phases.
A variety of equilibrium relations are available, including the simple {class}`~CADETProcess.processModel.Linear` adsorption isotherm, the competitive {class}`~CADETProcess.processModel.Langmuir` model, and the {class}`~CADETProcess.processModel.StericMassAction` law (see {numref}`isotherm_models`).
Moreover, {class}`ReactionModels <CADETProcess.processModel.ReactionBaseClass>` can be used to model chemical reactions (see {numref}`reaction_models`).

(flow_sheet)=
## Flow sheet

The connectivity of unit operations is defined in the {class}`~CADETProcess.processModel.FlowSheet` class.
This class provides a directed graph structure that allows for the simple definition of configurations for multi-column or reactor-separator networks, even when they are cyclic.
Furthermore, unit operation models can be used to model tubing and other external volumes.

Every unit operation can have any number of input and output streams, except for {class}`Inlets <CADETProcess.processModel.Inlet>` and {class}`Outlets <CADETProcess.processModel.Outlet>`, which act as system sources and sinks, respectively.
If a unit operation has more than one input, all ingoing streams are mixed before entering the unit.
If a unit operation has multiple outputs, the distribution of those streams needs to be specified (see {numref}`flow_demo`).
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

For a more practical example, typical for batch-elution chromatography, refer to {numref}`batch_elution_flow_sheet_intro`.
Here, the feed and eluent reservoirs can both be modeled as {class}`~CADETProcess.processModel.Inlet` unit operations, which are each connected to a column model unit operation, e.g. a {class}`~CADETProcess.processModel.LumpedRateModelWithPores`.
This unit is then connected to an {class}`~CADETProcess.processModel.Outlet` unit, which represents the material leaving the process for further processing.
Note that it is straightforward to also include internal recycles in the {class}`~CADETProcess.processModel.FlowSheet`, which is important for systems such as MR-SSR (see case study in {numref}`mrssr`).

### A note on flow rates

In CADET-Process, the {class}`~CADETProcess.processModel.Inlet` model acts as source unit that "generates" flow.
This flow is then transported to unit operations downstream.
Since fluids in CADET-Process are considered incompressible, all flow entering a unit must also exit from it.
A notable exception is the {class}`~CADETProcess.processModel.Cstr` model, which can have a variable volume.
If the flow rate of a {class}`~CADETProcess.processModel.Cstr` is explicitly specified, the outgoing streams can be decoupled from the ingoing streams, which is useful for modeling holdup tanks.
The volume must not reach zero, as this would render the mass balance equations undefined.
If not specified for a {class}`~CADETProcess.processModel.Cstr`, the unit is treated like all other unit operations models, and the outgoing flow rate equals the incoming flow rate.
This can be useful, e.g., when modeling holdup volumes or valves in the periphery of the chromatographic system.
Since CADET-Process is designed to support internal recycles, the actual flow rates for every unit operation must be resolved before simulation.
This calculation is performed automatically before each simulation, accounting for dynamic changes to flow rates and system connectivity.

(process)=
## Process

The {class}`~CADETProcess.processModel.Process` class is used to define dynamic changes to the unit operation parameters or flow sheet connectivity.
Beyond the flow sheet structure, it also specifies the total duration of one cycle, $\Delta t_{\text{cycle}}$.
Each dynamic change is represented by an {class}`Event <CADETProcess.dynamicEvents.Event>`, which stores the following information:

- `name`: Name of the event.
- `performer`: Object performing the event (e.g., a unit operation)
- `parameter`: Parameter that is changed.
- `state`: Value to which the parameter is changed to at event execution.
- `time`: Time at which the event is executed.

{numref}`events` illustrates the events required to model and simulate a single batch-elution process cycle.

```{figure} ./figures/events.png
:name: events
:width: 100%

Dynamic events of a batch-elution process.
At $t = 0~\text{min}$, the flow of the `Feed` unit operation is set to $60 \text{mL}~\text{min}^{-1}$ on, while the flow of the `Eluent` unit is turned off.
At $t = 1~\text{min}$, the flow of the `Feed` unit operation is turned off, while the flow of the `Eluent` unit is set to $60~\text{mL}~\text{min}^{-1}$.
The simulation ends at $\Delta t_{\text{cycle}}$.
```

When simulating multiple cycles, all event times are interpreted modulo $\Delta t_{\text{cycle}}$, so each event always falls within a single cycle.
If a specified time exceeds the cycle time, it is mapped back into the interval $[0, \Delta t_{\text{cycle}})$ automatically.

### Event Dependencies

To reduce complexity in process configurations within CADET-Process, dependencies between events can be specified.
These dependencies determine the occurrence times of one event based on the timings of other events.
This is particularly useful in process optimization: instead of treating the times of related events as independent variables, only one needs to be optimized while the others are derived from it, reducing the number of free parameters.
A {class}`~CADETProcess.dynamicEvents.Duration` is a special construct that carries no parameter change of its own; it acts as a named time interval between two events, serving as an anchor that other events can depend on.
Because it represents a fixed interval rather than an absolute position, it remains meaningful when the anchor event's time changes, which makes durations well suited as optimization variables.
For simulations spanning multiple cycles, each event's execution time is offset by the cycle number, so that the same sequence of events repeats correctly in every cycle.
Consequently, the execution time $t_{j,n}$ of a dependent event $j$ during the $nth$ cycle is calculated using the following equation:

$$
t_{j,n} = \left( n - 1 \right) \Delta t_{\text{cycle}} + \sum_i^{n_{\text{dep}}} \lambda_i \cdot f_i(t_{\text{dep},i}) ,
$$

where $\Delta t_{\text{cycle}}$ represents the cycle time, $n_{\text{dep}}$ is the number of dependencies of event $j$, $t_{\text{dep},i}$ is the time of dependency $i$, $\lambda_i$ is a linear factor, and $f_i$ is a transform function.

By incorporating event dependencies into the batch-elution process example, the feed is switched on every time the elution buffer is switched off, and vice versa.
If the start time of the injection is set to $t = 0~\text{min}$, only the feed duration and cycle time need to be adjusted, which is particularly useful in process optimization scenarios (see {numref}`event_dependencies`).

```{figure} ./figures/event_dependencies.png
:name: event_dependencies
:width: 100%

Dynamic events in a batch-elution process, with dependent events highlighted in green and durations in blue.
Arrows indicate the dependency of an event's execution time on other events or durations.
In simulations with multiple cycles, the event time also accounts for the cycle time.
```
