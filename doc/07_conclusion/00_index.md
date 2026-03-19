(conclusion)=
# Conclusion

The presented work enables systematic modeling, simulation, and optimization of both standard and advanced chromatographic operating modes through its modular architecture.
The modular design, where components like process configuration and performance evaluation operate independently, enabled both the parameter estimation and real-world validation in {numref}`chapter %s <characterization>` and the exploration of advanced operating modes in {numref}`chapter %s <operating_modes>`.
While the primary objective of this thesis was to introduce the modular architecture of CADET-Process, {numref}`chapter %s <characterization>` demonstrates its parameter estimation capabilities through a real-world laboratory system validation. Meanwhile, {numref}`chapter %s <operating_modes>` explores advanced operating modes while validating results against analytical equilibrium theory solutions. Together, these chapters showcase both practical application and theoretical validation.

First, the framework enabled accurate parameter estimation for typical laboratory-scale chromatographic systems, highlighting its utility in model calibration and validation.
Second, it was applied to optimize advanced operating concepts, such as batch chromatography with cycle-to-cycle overlap and interlocked peak operation, revealing highly efficient and non-intuitive process designs.
The optimized operating strategies further demonstrate novel process concepts, including waste fraction management and the handling of strongly binding components.
These results emphasize the potential of model-based optimization to systematically identify process designs that are both efficient and otherwise non-obvious.

In addition, this work demonstrates best practices in research software engineering, illustrating how modularity enables extensibility and reproducibility in complex scientific software while maintaining computational efficiency and numerical robustness.
CADET-Process serves as a fully featured toolbox for modeling and optimizing chromatographic processes, providing a solid foundation for the systematic development of novel operating strategies.
Its modular architecture allows the straightforward exchange of process models, numerical solvers, and optimization algorithms, facilitating future extensions with minimal structural changes.
This flexibility supports the implementation of new operating concepts, optimization variables, and objective functions as research and industrial needs evolve.

Several extensions of **CADET-Process** are envisaged, some of which are already under active development.
These include the integration of additional unit operations, compartment-based modeling approaches, and fully integrated process models, extending the framework beyond chromatography and enabling its application across a wider range of chemical and biological processes.
For example, bioreactors incorporating cell growth and enzymatic reactions could be modeled in combination with compartment models derived from computational fluid dynamics, allowing simultaneous capture of mixing effects and kinetic reactions {cite}`Li2026`.
Other unit operations, such as filtration and membrane separations, present distinct modeling challenges, including pressure-driven transport and highly concentrated systems, where concentration polarization and the volume of particulate substances must be explicitly accounted for.

This development aligns with ongoing improvements in CADET-Core, particularly regarding model equations and numerical solution methods.
On the CADET-Process side, further enhancements can be achieved through advanced pre- and post-processing strategies.
In addition, several "lessons learned" previously implemented in CADET-Process, such as a more modular interface structure, explicit event ordering, and pre-processing of flow rates, will be migrated and integrated into the CADET-Core package.

Finally, future research will explore surrogate modeling techniques to better understand the relationships between high-dimensional input parameters and relevant output metrics.
These models will enable more efficient optimization studies, including conditional optimization.
The framework is also well suited for computationally demanding tasks, such as MCMC simulations for rigorous uncertainty quantification {cite}`Heymann2023`.
Together, these extensions will enable more comprehensive, efficient, and insightful studies of complex biological and chemical processes.
