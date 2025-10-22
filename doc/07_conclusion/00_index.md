(conclusion)=
# Conclusion

The development and optimal design of advanced chromatographic processes is challenging due to their distinct nonlinear dynamics, periodic operation, and a multitude of design variables.
A software platform was developed that greatly simplifies this by decoupling the main design tasks into interchangeable modules for process modeling, simulation, product fractionation, and process optimization.
This enables flexible and fast adjustment of process and column configurations, chromatographic interaction mechanisms, and design goals or constraints.
The software was implemented using the programming language Python and includes an interface to the open-source simulation tool *CADET*, a fast and accurate numerical solver for chromatographic processes.
This makes the program, denoted as **CADET-Process**, directly applicable to developing advanced processes for demanding applications in, for example, the separation of biomolecules, nanoparticles, and the like, where complex interaction mechanisms and various dispersive effects need to be considered.

The `FlowSheet` of the chromatographic systems could be described by connecting `UnitOperations` in a directed graph which represents the material flow between them.
The dynamic behavior typical for chromatography, especially for advanced operating modes, was modeling by defining events that change the state of the system at given times.
The introduction of dependencies of the event times reduces the complexity of modeling advanced operating concepts.
Features, such as the assertion of cyclic stationarity, as well as the automatic determination of optimal fractionation times proved crucial for an efficient implementation of the simulation module and provide standalone functionality that can also be used outside the framework.

Several case studies for the optimization of binary and ternary separations were performed on single- and multicolumn systems with and without recycling.
It was shown how the choice of optimization variables and product ranking can lead to different optimal process designs.
Although the main purpose of the case studies was to introduce and demonstrate the applicability of the framework, the results feature  optimal designs of new operating strategies, like batch chromatography with optimal cycle-to-cycle overlap and waste fractions, as well as interlocked peaks for separation problems with strongly binding components.

% Outlook
Various extensions of the software can be envisaged, some of them are already in progress.

- Other unit operations
- compartment modeling
- integrated processes

Furthermore, the normalization of optimization variables with different orders of magnitude can greatly improve the performance of the optimization, as can other, more complex parameter transforms.

The presented framework is a fully-featured toolbox for modeling and optimizing chromatographic processes which is the base for more systematic and targeted development of novel chromatographic processes.

More operating concepts, optimization variables, and objective functions can easily be implemented.
The framework's modular approach in general enables a straightforward exchange of process models, numeric solvers, and optimizers for future extension of the software.
