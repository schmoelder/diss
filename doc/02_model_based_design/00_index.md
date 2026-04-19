(fundamentals)=
# Model-based design of chromatographic processes

The complex and nonlinear behavior of chromatographic systems makes empirical design of such processes difficult and time-consuming.
To address this challenge and optimize the performance of chromatographic processes, mathematical models and numerical simulations are increasingly being used to characterize the behavior of these systems and to identify optimal operating conditions.
Models provide a framework for a deeper understanding of the underlying mechanisms of chromatography and have become more prevalent in recent years due to unprecedented availability of data and compute resources.

These models are key in testing hypotheses to verify and refine the understanding of chromatographic processes and their dominating effects.
They are also instrumental in the design and selection of experiments, which maximizes the information gained from each experiment.
Moreover, models play a crucial role in evaluating the feasibility and value propositions of new potential processes.
They provide quantifiable information on the costs and risks associated with various scenarios, aiding in well-informed decision-making.
Furthermore, models are used for robustness analysis, uncertainty quantification, and real-time process control, ensuring safe and reliable operations.

Several important steps are required to ensure a model's reliability and accuracy.
First, a suitable model must be developed that is capable of addressing the problem at hand.
This development phase often involves selecting an appropriate theoretical framework, defining key assumptions, and identifying model parameters.

The model must then be *verified* to ensure its theoretical soundness and correct implementation through rigorous testing.
This involves checking that the mathematical equations are solved correctly, the software implementation matches the theoretical formulation, and the model behaves as expected when compared to benchmarks and well-defined test cases.

During model *calibration*, parameters are systematically adjusted to optimize alignment with experimental data, thereby enhancing predictive accuracy.
Following successful calibration, the model undergoes *validation* using independent experimental datasets not used during calibration to rigorously assess its accuracy and reliability in real-world scenarios.
It is important to note that model development typically follows an iterative DBTL cycle (design, build, test, learn) rather than a linear progression, allowing for continuous refinement through repeated cycles of calibration and validation.

Consequently, developing accurate models for chromatographic processes requires a thorough understanding of their mechanistic principles.
Aspects such as retention mechanisms and transport phenomena are particularly important, as discussed in {numref}`chromatographic_principle`.
Typically, chromatographic processes are mathematically described using partial differential equations, which are first parametrized to represent the specific system under study and then solved numerically.
For a more in-depth discussion on the modeling approach and the numerical solutions to these equations, refer to sections {numref}`model_formulation` and {numref}`model_solution`.

The primary focus of this work is to validate the CADET-Process framework for modeling and optimizing chromatographic processes.
This validation includes parameter estimation and model calibration against experimental data, as demonstrated in {numref}`characterization`.
The validated framework then enables the investigation of various operating modes and a comprehensive comparison of their performance.
These models enable the determination of a range of metrics to evaluate the performance of specific chromatographic process scenarios, as detailed in {numref}`design_formulation`.
Subsequently, different optimization algorithms can be applied to identify optimal operating conditions by maximizing the defined performance metrics.
A more detailed discussion of these optimization techniques can be found in {numref}`design_solution`.

<!--
Ziel des Kapitels: übersicht über state of the art. Motivation der eigens verwendeten Methoden. EINORDNUNG!

What we need:
- Understanding of chromatographic principles and processes
- Physico-chemical models for binding and transport phenomena
- Numerical methods to solve models
- Metrics for determining process performance
- Algorithms to find optimal process
-->
