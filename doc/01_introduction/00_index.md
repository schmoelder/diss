(introduction)=
# Introduction

% Relevance of Chromatography
Production processes in chemical, pharmaceutical, and biotechnological industries typically require the separation of products from side products or impurities.
While classical separation processes like distillation, extraction, or filtration are effective in many cases, they face limitations when dealing with components that are physico-chemically very similar, sensitive to harsh conditions, or part of multi-component mixtures.
In particular for such challenging separations, chromatography is a powerful alternative {cite}`Guiochon2006,SchmidtTraub2020,Nicoud2015`.

The term *chromatography* was first used by Russian botanist Michail Tswett in the early 1900s to describe a method he developed for separating and analyzing chlorophyll extracts dissolved in organic solvents.
When passing samples through a column packed with inulin, he observed that the mixture would separate into distinct colored bands which could be collected at the column outlet.
He postulated that the separation is based on the ability of the dissolved components to physically interact with the immobilized inulin particles causing components to migrate through the column at different rates {cite}`Tswett1906`.

However, the nonlinear dependence of retention on solute concentration at high loads, as well as the lack of sophisticated detectors, posed difficulties in understanding and controlling the separation process.
Furthermore, the technique initially suffered from low productivities (the ratio of purified product to the amount of packing material) making its application inefficient and expensive.
For these reasons, chromatography was not widely adopted until almost three decades later when Tswett's work was rediscovered and established as a preparative separation method for a broad spectrum of chemical compounds {cite}`Guiochon2006`.

Since then, both the technique and our understanding of it have evolved steadily.
From the early stages, efforts to improve process performance led to creative process designs.
For example, when the method was scaled up in the 1940s to purify rare earth materials for nuclear research, cascading multi-column operations were introduced to increase throughput.
The buffer composition was also adjusted to minimize the use of expensive chemicals while maintaining effective separation {cite}`Spedding1947`.
In the 1960s, when the oil industry started using chromatography for hydrocarbons, the bigger production scales led to the development of continuous operating concepts like simulated moving bed (SMB) which could operate at much higher productivities than conventional batch-elution processes {cite}`SchmidtTraub2020`.
At the same time, progress in theoretical modeling and numerical simulation deepened the understanding of process dynamics, enabling more precise design and optimization.
Meanwhile, advances in material science made it possible to produce highly selective adsorbents, opening up opportunities in the biopharmaceutical industry, a trend that continues today {cite}`SchmidtTraub2020`.

Today, the technique is widely used, as a broad range of stationary phases can be combined with diverse solvents.
Its applications span from analytical chromatography, primarily used for characterization and quantification, to large-scale preparative purification of bulk chemicals on multi-ton scales
These preparative applications include the separation of petrochemical isomers and sugars, as well as the purification of essential compounds such as amino acids and pharmaceuticals.
In addition, it plays an important role in complex separations in the biopharmaceutical industry, where stringent requirements regarding purity and regulatory compliance must be met {cite}`SchmidtTraub2020`.

% Operating Concepts
Most process-scale chromatographic separations are performed using a single column.
In conventional batch-elution mode, small amounts of the mixture are injected periodically onto the chromatographic column and the mixture components elute as separated peaks from its outlet.
However, as previously mentioned, many advanced operating modes exist that can outperform conventional batch chromatography in terms of productivity, solvent consumption, and recovery yield.
For example, operating concepts like closed-loop recycling {cite}`Bombaugh1969,Heuer1995` or mixed-recycle steady-state recycling (MR-SSR) {cite}`Bailly1982,Sainio2009,Kaspereit2011` incorporate different strategies for the recycling of unresolved fractions from the column outlet back to the inlet with the aim of improving yield, solvent consumption and/or productivity {cite}`Sainio2009`.
If purity requirements are low, bypass streams can be advantageous {cite}`Siitonen2012`.
Moreover, the use of multiple columns gives rise to various concepts ranging from serial or parallel arrangements of columns {cite}`Ziomek2006,GarciaPalacios2009`, over pseudo-continuous processes, up to the many variants of the powerful continuous SMB concept.
More details on such advanced chromatographic operating modes are given in {numref}`chromatographic_principle` and in {cite}`SchmidtTraub2020,Nicoud2015,Rodrigues2015`.

% Challenges in Process Design
The choice of operating concept depends on the specific separation problem, as each approach involves trade-offs between multiple criteria.
Simple systems are cost-effective and adaptable, making them suitable for smaller or more flexible applications. Complex multi-column systems, while requiring higher capital investment, allow for finer control and optimization, often resulting in lower operating costs for large-scale processes.
Additionally, some operating concepts exhibit distinct startup behavior (see {numref}`stationarity`), limiting their practicality to large-scale separation campaigns where initial inefficiencies can be offset {cite}`Rajendran2013`.
Thus, selecting an appropriate operating mode is a critical step in process design.

% Model-based design
The rapid development of computational methods, together with the lower cost of simulations compared to laboratory experiments, has shifted the driving force for advancing chromatographic processes toward mathematical modeling and optimization tools.
While some physico-chemical phenomena remain challenging to describe, there is generally high confidence in modeling the dynamics of chromatographic processes.
Today, many wet-lab experiments are conducted primarily for model calibration and validation {cite}`Rajendran2013`.
Despite this progress, model-based design and optimization of chromatographic processes remain non-trivial.
This complexity arises from periodic operation, strongly nonlinear dynamics, and a large number of degrees of freedom, such as column dimensions, valve switching times, and operating conditions.
For certain operating modes, simplified shortcut methods provide useful initial design estimates (e.g., {cite}`Siitonen2011` for batch chromatography, {cite}`Sainio2009,Kaspereit2011` for MR-SSR systems, {cite}`Mazzotti2006` for SMB processes, and {cite}`Siitonen2015` for a unified treatment).
These methods typically rely on simplifying assumptions, such as restricted binding models, neglected mass transfer effects, or single-column operation.
In practical applications, however, a wide range of binding mechanisms, including adsorption, ionic interactions, ligand binding, and size exclusion, may be relevant.
Additional transport phenomena, such as axial dispersion, film diffusion, and pore diffusion, further influence system behavior and must be accounted for.
As a result, rigorous process development generally requires detailed mechanistic models combined with systematic optimization methods for both model calibration and process design.
Consequently, chromatographic processes are described using a variety of model formulations (see {numref}`model_formulation`) and numerical solution strategies (see {numref}`model_solution`), together with diverse optimization approaches for process design.
An overview is provided in Sections {numref}`%s <design_formulation>` and {numref}`%s <design_solution>`, as well as in {cite}`Kawajiri2020`.

% Tool requirements
Developing an optimal chromatographic process requires two complementary workflows: systematic calibration of model parameters against experimental data, and optimization of the process configuration and operating conditions.
The complexity of advanced operating modes makes both workflows non-trivial, as each requires specific process models, evaluation pipelines, and optimization schemes.
Against this background, a general-purpose tool is required that enables efficient and flexible handling of the full range of tasks involved.
The main tasks include:

- setting up a model for the chromatographic system and the desired process structure,
- simulating the process by solving the model equations,
- evaluating simulation results against performance criteria or experimental reference data, and
- optimizing process variables, covering both model calibration and process design.

% Existing tools
Several commercial programs are available which provide parts of the aforementioned required functionalities, like Aspen Chromatography {cite}`aspen`, GoSilico (formerly known as ChromX) by Cytiva {cite}`GoSilico`, and Ypso-Proxima (formerly known as ChromWorks) by YpsoFacto {cite}`ypso-proxima`.
Most of these programs are aimed at experimentalists and allow users to carry out simulations of simple processes without requiring programming expertise.
In contrast, there exist many highly application-specific programs in academia which were developed to examine individual research questions.
However, neither provides the flexibility and customizability required for the *ab initio* development of novel process concepts.
A notable exception here is **CADET** by the Forschungszentrum Jülich {cite}`Leweke2018,Leweke2025`
Its numerical simulation engine **CADET-Core** offers a diverse family of binding, reaction, and unit operation models for simulating a large range of separation processes.
Multiple unit operations can be connected in a network, generally allowing even complex process configurations to be represented.
Yet CADET-Core is primarily a numerical solver for the partial differential equations, and defining advanced operating concepts requires an additional abstraction layer.
Moreover, it provides no dedicated tools for process evaluation, parameter estimation, or optimization.

% Approach
To address these limitations, a modular framework for the efficient modeling, simulation, parameter estimation, and optimization of chromatographic processes was developed for this work.
The framework implements a modular architecture where process configuration, simulation, evaluation, and optimization exist as independent components that can be developed, tested, and exchanged separately.
This design enables flexible combination of physico-chemical models, numerical solvers, process configurations, and optimization algorithms.
The software is implemented in an object-oriented paradigm in the programming language **Python**.
It provides an interface to **CADET-Core**, which serves as the primary solver within the framework; however, the architecture is sufficiently flexible to accommodate alternative solvers.
This tight integration motivated the designation of the framework as **CADET-Process**.
The code is open source and distributed under *GPL* version 3, making it freely accessible to both academic and industrial users.
The repository is publicly available at [https://github.com/fau-advanced-separations/CADET-Process](https://github.com/fau-advanced-separations/CADET-Process).

Best practices for sustainable scientific software development have been applied throughout this work, as reliability and reproducibility are of particular importance in a scientific context where results must be verifiable by others.
Since process engineers are usually not trained in this field, a chapter of this work is dedicated to the introduction of important techniques such as version control, unit testing, and software documentation (see {numref}`methods_software_design`).

% Demonstrations
To demonstrate the flexibility of the framework, several case studies are presented in this work.
First, the parameter estimation capabilities of CADET-Process are demonstrated through the systematic characterization of a typical chromatographic laboratory system for a protein purification step.
The study covers several experiment types and progressively builds up a full process model, incorporating system periphery effects such as valves and tubing that are often neglected, and culminating in a load-wash-elute process for lysozyme using the steric mass-action binding model with a salt gradient.

Next, the optimization of advanced operating concepts is investigated through a set of synthetic case studies.
These studies assume known model parameters and focus on preparative separations of binary and ternary mixtures.
Operating modes of increasing complexity are examined, including batch-elution, recycling strategies, flip-flop chromatography, and serial column configurations.
For validation, process simulations are compared with equilibrium theory solutions.
Single- and multi-objective optimization are used to optimize feed durations, valve switching and cycle times, and column geometry, aiming to maximize productivity and yield while minimizing solvent consumption.
