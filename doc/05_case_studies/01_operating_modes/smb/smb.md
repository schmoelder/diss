---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
execution:
  timeout: 300

---

(smb_process)=
# Simulated moving bed

For many applications, the use of multiple columns can improve process performance when compared with conventional batch elution processes.
Next to the well known simulated moving bed (**SMB**) many other operating modes exist which extend the use of multiple columns, e.g. **Varicol**, or **PowerFeed** processes and gradient operations {cite}`SchmidtTraub2020`.

In all of the aforementioned processes, multiple chromatographic columns are mounted to a rotating column carousel and a central multiport switching valve distributes in- and outgoing streams to and from the columns.
After a given time, the column positions are moved to the next position in the carousel.
In this process, the columns pass through different zones which serve different purposes.

For example, in a classical SMB, four zones are present (see {ref}`Figure below <smb_system>`)

- Zone I: Elution of the strongly adsorbing component
- Zone II: Elution of the weakly adsorbing component
- Zone III: Adsorption of the strongly adsorbing component
- Zone IV : Adsorption of the weakly adsorbing component

Moreover, four in- and outlets are connected to the zones:

- Feed: Inlet containing the components to be separated
- Eluent: Inlet with elution buffer
- Extract: Outlet containing the strongly adsorbing component
- Raffinate: Outlet containing the weakly adsorbing component

To facilitate the configuration of complex SMB, carousel, or other multi column systems systems, a {class}`~CADETProcess.modelBuilder.CarouselBuilder` was implemented in **CADET-Process**
It allows a straight-forward configuration of the zones and returns a fully configured {class}`~CADETProcess.processModel.Process` object including all internal connections, as well as switching events.

Here are some of the features:

- Any number of inlets and outlets or other peripheral units.
- Any number of zones
- Any number of columns per zone.
- Different column connectivity within the zones:
  - Serial
  - Parallel
- Different connectivity between zones:
  - Directly connected zones
  - Skip zones
  - Mix and split in- and outgoing streams
  - Allow for different flow direction in every zone.
- Any number of side streams

## SMB Process

To demonstrate the tool, consider a standard SMB process.

```{figure} ./figures/smb_flow_sheet.svg
:name: smb_system

Standard SMB system
```

Before configuring the zones, the binding and column models are configured.
The column is later used as a template for all columns in the system.

Now, the {class}`Inlets <CADETProcess.processModel.Inlet>` and {class}`Outlets <CADETProcess.processModel.Outlet>` of the system are configured:

To allow more complicated systems, **CADET-Process** provides two options for configuring zones, a {class}`~CADETProcess.modelBuilder.SerialZone` and a {class}`~CADETProcess.modelBuilder.ParallelZone`.
For both, the number of columns in the zone needs to be specified.
Since here all the zones only consist of one column, either can be used.

The {class}`~CADETProcess.modelBuilder.CarouselBuilder` can now be used like a regular {class}`~CADETProcess.processModel.FlowSheet` where the zones are conceptually used like other {class}`UnitOperations <CADETProcess.processModel.UnitOperations>`.
After initializing the {class}`~CADETProcess.modelBuilder.CarouselBuilder`, the column template is assigned and all units and zones are added.

Now, the connections are added to the builder.
To define split streams, the `output_state` is used which sets the ratio between outgoing streams of a unit operation in the flow sheet.

Now, the switch time is assigned to the builder which determines after how much time a column is switched to the next position.
By calling the {meth}`~CADETProcess.modelBuilder.CarouselBuilder.build_process` method, a regular {class}`~CADETProcess.processModel.Process` object is constructed which can be simulated just as usual using **CADET**.
It contains the assembled flow sheet with all columns, as well as the events required for simulation.

Since multi column systems often exhibit a transient startup behavior, it might be useful to simulate multiple cycles until cyclic stationarity is reached (see {ref}`stationarity_guide`).
Because this simulation is computationally expensive, only a few simulations are run for the documentation.
Please run this simulation locally to see the full results.

The results can now be plotted.
For example, this is how the concentration profiles of the raffinate and extract outlets are plotted:

It is important to note that for the purpose of simplifying the implementation, each `Zone` internally has an inlet and an outlet which are modelled using a {class}`~CADETProcess.processModel.Cstr` with a very small volume.
The concentration of these in and outlets can also be plotted.
These units get a `_inlet` and `_outlet` suffix.
For example, this is the concentration of the inlet of zone III:
