(fundamentals)=
# Model-based design of chromatographic processes

Model-based approaches serve as decision-support tools throughout the process development lifecycle.
They assist in experimental design, quantify costs and risks associated with new process concepts, and enable informed decisions during both development and operation.
In chromatography, nonlinear dynamics and numerous interacting physico-chemical phenomena make purely empirical design costly and time-consuming, motivating the use of mechanistic models.
These are typically formulated as systems of partial differential-algebraic equations (PDAEs), solved either analytically under simplifying assumptions or numerically in the general case.
With the increasing availability of data and computational resources, model-based approaches have become both practical and widely adopted.

Several important steps are required to ensure a model's reliability and accuracy.
First, *model selection* involves choosing a suitable theoretical framework, defining key assumptions, and identifying the relevant model parameters.
The model must then be *verified* to ensure its theoretical soundness and correct implementation through rigorous testing.
This involves checking that the mathematical equations are solved correctly, the software implementation matches the theoretical formulation, and the model behaves as expected when compared to benchmarks and well-defined test cases.
During model *calibration*, parameters are estimated to minimize residuals between model predictions and experimental data (see {numref}`model_calibration`), improving predictive accuracy.
Following successful calibration, the model undergoes *validation* using independent experimental datasets not used during calibration to assess its accuracy and reliability in real-world scenarios.
It is important to note that model development typically follows an iterative design–build–test–learn (DBTL) cycle rather than a linear progression, allowing for continuous refinement through repeated calibration and validation steps.

This chapter reviews the fundamentals underlying these steps.
It begins with the mechanistic principles of retention and transport ({numref}`chromatographic_principle`), followed by mathematical model formulations and their numerical solution ({numref}`model_formulation`, {numref}`model_solution`), and concludes with methods for process performance evaluation and optimization ({numref}`design_formulation`, {numref}`design_solution`).

<!--
Ziel des Kapitels: übersicht über state of the art. Motivation der eigens verwendeten Methoden. EINORDNUNG!

What we need:
- Understanding of chromatographic principles and processes
- Physico-chemical models for binding and transport phenomena
- Numerical methods to solve models
- Metrics for determining process performance
- Algorithms to find optimal process
-->
