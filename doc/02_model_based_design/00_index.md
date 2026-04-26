(fundamentals)=
# Model-based design of chromatographic processes

Model-based approaches serve as decision-support tools throughout the process development lifecycle.
They assist in experimental design, quantify costs and risks associated with new process concepts, and enable informed decisions during both development and operation.
In chromatography, nonlinear dynamics and numerous interacting physico-chemical phenomena make purely empirical design costly and time-consuming, motivating the use of mechanistic models.
These are typically formulated as systems of partial differential-algebraic equations (PDAEs), solved either analytically under simplifying assumptions or numerically in the general case.
With the increasing availability of data and computational resources, model-based approaches have become both practical and widely adopted.

Several steps are required to ensure the reliability and accuracy of a model.
The process begins with *model selection*, which involves choosing a suitable theoretical framework, defining key assumptions, and identifying the relevant model parameters.
Subsequently, the model is *verified* to ensure its theoretical soundness and correct implementation through rigorous testing.
This includes confirming that the mathematical equations are solved correctly, that the software implementation matches the theoretical formulation, and that the model behaves as expected when compared to benchmarks and well-defined test cases.
In the *calibration* step, parameters are estimated by minimizing residuals between model predictions and experimental data (see {numref}`model_calibration`), thereby improving predictive accuracy.
The calibrated model is then *validated* using independent experimental datasets to assess its predictive capability under real-world conditions.
Rather than following a strictly linear sequence, model development is typically embedded in an iterative design–build–test–learn (DBTL) cycle, allowing for continuous refinement through repeated calibration and validation.
Within this cycle, many tasks, including parameter estimation, experimental design, and process optimization, can be expressed as optimization problems, as they involve the systematic adjustment of decision variables to achieve a desired objective (see {numref}`design_solution`).

<!--
Ziel des Kapitels: übersicht über state of the art. Motivation der eigens verwendeten Methoden. EINORDNUNG!

What we need:
- Understanding of chromatographic principles and processes
- Physico-chemical models for binding and transport phenomena
- Numerical methods to solve models
- Metrics for determining process performance
- Algorithms to find optimal process
-->
