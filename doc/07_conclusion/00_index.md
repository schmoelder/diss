(conclusion)=
# Conclusion

This work presents a modular framework for the systematic modeling, simulation, and optimization of chromatographic processes, covering both standard and advanced operating modes.
By separating process configuration, simulation, performance evaluation, and optimization into independent components, the framework allows each part to be developed, tested, and exchanged without structural changes to the rest of the system.
The resulting open-source package, CADET-Process, has since been adopted in both academic and industrial settings; its development followed best practices in scientific software engineering, including version control, unit testing, and structured documentation, to ensure long-term reproducibility and maintainability.

Two complementary case studies were used to validate this design from different angles.
The characterization study confirmed that the framework accurately reproduces the behavior of a real laboratory system, capturing system periphery effects, column transport, and protein adsorption under a salt gradient within a single integrated model.
A progressive parameter estimation procedure, working from dead volume and dispersion through to binding parameters, proved effective for a typical ion-exchange purification setup and illustrated the value of building model complexity incrementally rather than fitting all parameters simultaneously.

The study on operating modes followed a complementary approach, employing synthetic parameters and analytical solutions based on equilibrium theory to investigate process optimization across a range of advanced configurations.
Multi-objective optimization consistently revealed non-intuitive operating strategies, including stacked injections, intermediate waste fractions, and peak interlocking under overloaded conditions.
More generally, batch elution emerged as the productivity-optimal limiting case of more complex recycling configurations.
Notably, this behavior was not imposed by the optimization formulation but arose naturally from the structure of the decision variables.
This observation highlights the framework’s suitability for superstructure optimization, in which the operating mode itself is treated as a design variable rather than a fixed choice.

Looking ahead, several extensions are envisaged, some of which are already under active development.
On the modeling side, the integration of additional unit operations, compartment-based approaches, and fully integrated process models will extend the framework beyond chromatography to a wider class of separation and reaction processes.
Bioreactors incorporating cell growth and enzymatic reactions, for example, could be coupled with compartment models derived from computational fluid dynamics, capturing mixing effects and reaction kinetics simultaneously {cite}`Li2026`; other unit operations such as filtration and membrane separations introduce further challenges around pressure-driven transport and concentration polarization.
In parallel, several design decisions developed within CADET-Process, including a more modular interface structure, explicit event ordering, and pre-processing of flow rates, will be migrated into CADET-Core to benefit the broader ecosystem.
On the methods side, future work will explore surrogate modeling techniques to characterize the relationship between high-dimensional process parameters and performance metrics, enabling more efficient optimization and conditional design studies, as well as computationally demanding approaches such as MCMC simulations for rigorous uncertainty quantification {cite}`Heymann2023`.
