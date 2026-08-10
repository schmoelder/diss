(conclusion)=
# Conclusion

This work presents a modular framework for the systematic modeling, simulation, and optimization of chromatographic processes, covering both standard and advanced operating modes.
By separating process configuration, simulation, performance evaluation, and optimization into independent components, the framework allows each part to be developed, tested, and replaced without structural changes to the rest of the system.
The resulting open-source package, CADET-Process, has since been adopted in both academic and industrial settings; its development followed best practices in scientific software engineering, including version control, unit testing, and structured documentation, to ensure long-term reproducibility and maintainability.

Two complementary case studies validated this design from different angles.
The first case study validated the framework against experimental data for a typical ion-exchange laboratory system.
The system was modeled using a stepwise refinement approach, starting from dead volume characterization and column transport and extending to protein adsorption under a salt gradient, with estimated parameters in good agreement with literature values.
Beyond validation, the multi-objective formulation revealed that individual gradient experiments yield distinct optimal parameters that do not coincide with the combined optimum obtained through scalar aggregation, an inconsistency that would remain hidden under scalar aggregation.

The study on operating modes took a different approach, using synthetic parameters to investigate process optimization across a range of advanced configurations, with analytical equilibrium theory solutions used for validation.
Multi-objective optimization consistently revealed non-intuitive operating strategies, including stacked injections, intermediate waste fractions, and peak interlocking under overloaded conditions.
A notable finding of this analysis is that batch elution emerges as the productivity-optimal limiting case of more complex recycling configurations.
This result was not imposed by the optimization formulation but arises naturally from the structure of the decision variables.
It highlights the framework’s suitability for superstructure optimization, where the operating mode itself becomes a design variable rather than a fixed choice.

Looking ahead, several extensions are envisaged, some of which are already under active development.
Extending the set of unit operations will broaden the framework beyond chromatography to more general separation and reaction systems.
Filtration and membrane separations introduce additional challenges related to pressure-driven transport and concentration polarization.
Bioreactors incorporating cell growth and enzymatic reactions could be coupled with compartment models derived from computational fluid dynamics, capturing mixing effects and reaction kinetics simultaneously {cite}`Li2026`.
In parallel, design elements developed within CADET-Process, such as a more modular interface structure, explicit event ordering, and pre-processing of flow rates, are being migrated into CADET-Core to strengthen the broader ecosystem.

These extensions raise the computational cost on two sides.
An integrated process with more unit operations and coupled physics is considerably more expensive to simulate than a single column.
At the same time, a larger design space takes more simulations to explore.
Evaluating every candidate design directly therefore stops being affordable, and methodological advances are needed alongside the models themselves.
Surrogate models address the first side by replacing the simulation with an approximation trained on its outputs.
Because they predict performance metrics directly instead of resolving the underlying concentration profiles, conditional design studies over high-dimensional parameter spaces become tractable.
Bayesian optimization addresses the second side, selecting each new simulation for the information it adds rather than sampling the space uniformly.

Cheaper evaluation also opens up analyses that are out of reach today.
Rigorous uncertainty quantification by sampling-based methods such as MCMC requires very many model evaluations, which currently restricts it to comparatively cheap models, and a fast surrogate removes that restriction {cite}`Heymann2023`.
All of these methods act on the evaluation of a process rather than on its formulation, so the separation of process configuration, evaluation, and optimization is what allows them to be added without changing the process models.

Making such methods available in routine practice is a separate task from developing them.
Model-based control for real-time optimization is the most demanding of the directions ahead, while graphical user interfaces, teaching material, and deployment templates determine how widely the framework can be adopted.

The preface opened with a familiar provocation: all models are wrong, but some are useful.
The results presented here make that statement operational rather than rhetorical.
Careful validation provides confidence in where such models are useful in practice.
Multi-objective analysis then reveals where compressing discrepant observations into a single scalar objective can obscure structure rather than resolve it.
The framework developed in this work provides a transparent, modular approach to model, validate, and rely upon simulation software for chromatographic process development, offering a tool to better understand whether a process is *good*, and where it falls short.
