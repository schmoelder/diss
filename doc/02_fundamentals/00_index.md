(fundamentals)=
# Model-based design of chromatographic processes

The complex and nonlinear behavior of chromatographic systems makes empirical design of such processes difficult and time-consuming.
To address this challenge and optimize the performance of chromatographic processes, mathematical models and numerical simulations are increasingly being used to characterize the behavior of these systems and to identify optimal operating conditions.
Models provide a framework for a deeper understanding of the underlying mechanisms of chromatography and have become more prevalent in recent years due to unprecedented availability of data and compute resources.

These models are key in testing hypotheses to verify and refine the understanding of chromatographic processes and their dominanting effects.
They are also instrumental in the design and selection of experiments, which maximizes the information gained from each experiment.
Moreover, models play a crucial role in evaluating the feasibility and value propositions of new potential processes.
They provide quantifiable information on the costs and risks associated with various scenarios, aiding in well-informed decision-making.
Furthermore, models are used for robustness analysis, uncertainty quantification, and real-time process control, ensuring safe and reliable operations.

Several important steps are required to ensure a model's reliability and accuracy.
First, a suitable model must be developed that is capable of addressing the problem at hand.
This development phase often involves selecting an appropriate theoretical framework, defining key assumptions, and determining model parameters.
Once developed, the model must be *verified* to ensure its theoretical soundness and its ability to represent the real-world system accurately.
The verification process typically involves comparing model predictions to experimental data and refining parameters as needed to improve alignment.
Subsequently, the software implementation of the model must undergo rigorous testing.
This step ensures that the software is free of errors and that its operations are consistent with the mathematical formulation of the model.

The process of model *validation* then involves comparing the model's predictions with experimental data or benchmarks.
This is essential for assessing its accuracy and reliability in simulating real-world scenarios.
Following this, the model undergoes *calibration* of its parameters, a critical step for aligning the model with experimental data or other relevant sources of information, thereby enhancing its predictive accuracy.

It is important to note that the development of new models is typically not a linear process but an iterative one.
The model is continually refined and improved through repeated cycles of design, building, testing, and learning (DBTL) from the results.
This iterative approach ensures that the model evolves and adapts to provide the most accurate and reliable outcomes possible.

In this context, developing an accurate model for chromatographic processes requires a thorough understanding of their mechanistic principles.
Aspects such as retention mechanisms and transport phenomena are particularly important, as discussed in {numref}`section %s <chromtographic_principle>`.
Typically, chromatographic processes are mathematically described using partial differential equations, which are first parametrized to represent the specific system under study and then solved numerically.
For a more in-depth discussion on the modeling approach and the numerical solutions to these equations, refer to sections {numref}`%s <model_formulation>` and {numref}`%s <model_solution>`.

The primary focus of this work is to investigate various operating modes of chromatography and conduct a comprehensive comparison of their performance.
For this analysis, it is assumed that the models being used have already undergone verification, validation, and calibrated.
These models then enable the determination of a range of metrics to evaluate the performance of specific chromatographic process scenarios, as detailed in {numref}`section %s <design_formulation>`.
Subsequently, different optimization algorithms can be applied to identify optimal operating conditions by maximizing the defined performance metrics.
A more detailed discussion of these optimization techniques can be found in {numref}`section %s <design_solution>`.

<!--
Ziel des Kapitels: übersicht über state of the art. Motivation der eigens verwendeten Methoden. EINORDNUNG!

What we need:
- Understanding of chromatographic principles and processes
- Physico-chemical models for binding and transport phenomena
- Numerical methods to solve models
- Metrics for determining process performance
- Algorithms to find optimal process
-->
