(conclusion)=
# Conclusion

This work presents a modular framework for the systematic modeling, simulation, and optimization of chromatographic processes, covering both standard and advanced operating modes.
The framework separates process configuration, simulation, performance evaluation, and optimization into independent components that can be developed, tested, and exchanged without structural changes to the rest of the system.
The resulting open-source package, CADET-Process, has since been adopted in both academic and industrial settings.
Its utility was demonstrated through two complementary case studies, each exercising a different aspect of this design.

The characterization study demonstrated that the framework accurately reproduces the behavior of a real laboratory system, from system periphery effects through column transport to protein adsorption under a salt gradient.
A progressive parameter estimation procedure, working from dead volume and dispersion through to binding parameters, proved effective and practically applicable to a typical ion-exchange purification setup.

The operating modes study showed that the same framework, without modification, can optimize processes of substantially greater structural complexity.
Multi-objective optimization consistently identified non-intuitive operating strategies, including stacked injections, intermediate waste fractions, and peak interlocking under overloaded conditions.
A notable emergent finding is that batch elution recovers as the productivity-optimal limiting case of more complex recycling configurations.
This behavior was not enforced by the optimization formulation but arose naturally from the decision variable structure, pointing to the framework's suitability for superstructure optimization, where the operating mode itself is a design variable.

Throughout this work, best practices in scientific software engineering, including version control, unit testing, and structured documentation, were applied to ensure reproducibility and long-term maintainability of the codebase.

Several extensions of **CADET-Process** are envisaged, some of which are already under active development.
These include the integration of additional unit operations, compartment-based modeling approaches, and fully integrated process models extending the framework beyond chromatography.
For example, bioreactors incorporating cell growth and enzymatic reactions could be modeled in combination with compartment models derived from computational fluid dynamics, allowing simultaneous capture of mixing effects and kinetic reactions {cite}`Li2026`.
Other unit operations, such as filtration and membrane separations, present distinct modeling challenges, including pressure-driven transport and highly concentrated systems where concentration polarization and the volume of particulate substances must be explicitly accounted for.

This development aligns with ongoing improvements in CADET-Core, particularly regarding model equations and numerical solution methods.
Several design decisions previously implemented in CADET-Process, such as a more modular interface structure, explicit event ordering, and pre-processing of flow rates, will be migrated into CADET-Core to benefit the broader ecosystem.

Future research will also explore surrogate modeling techniques to characterize relationships between high-dimensional input parameters and process performance metrics, enabling more efficient optimization and conditional design studies.
The framework is equally well suited for computationally demanding tasks such as MCMC simulations for rigorous uncertainty quantification {cite}`Heymann2023`.
