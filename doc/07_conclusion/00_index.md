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

As model scope and dimensionality increase, methodological advances become increasingly important.
Surrogate modeling techniques are used to characterize the relationship between high-dimensional process parameters and performance metrics, enabling conditional design studies.
Building on these surrogates, Bayesian optimization provides a sample-efficient approach for process design by balancing exploration and exploitation of the parameter space, while computationally intensive methods such as MCMC enable rigorous uncertainty quantification {cite}`Heymann2023`.
Translating these methods into practical workflows motivates further development for practical applications.
This includes model-based control strategies for real-time optimization, graphical user interfaces to improve accessibility, teaching materials for educational use, and templates for industrial deployment.

The preface opened with a familiar provocation: all models are wrong, but some are useful.
The results presented here make that statement operational rather than rhetorical.
Careful validation provides confidence in where such models are useful in practice.
Multi-objective analysis then reveals where compressing discrepant observations into a single scalar objective can obscure structure rather than resolve it.
The framework developed in this work provides a transparent, modular approach to model, validate, and rely upon simulation software for chromatographic process development, offering a tool to better understand whether a process is *good*, and where it falls short.
