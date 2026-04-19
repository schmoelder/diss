(introduction)=
# Introduction

% Relevance of Chromatography
Production processes in chemical, pharmaceutical, and biotechnological industries typically require the separation of products from side products or impurities.
While classical separation processes like distillation, extraction, or filtration are effective in many cases, they face limitations when dealing with components that are physico-chemically very similar, sensitive to harsh conditions, or part of multi-component mixtures.
In particular for such challenging separations, chromatography is a powerful alternative {cite}`Guiochon2006,SchmidtTraub2020,Nicoud2015`.

The term *chromatography* was first used by Russian botanist Michail Tswett in the early 1900s to describe a method he developed for separating and analyzing chlorophyll extracts dissolved in organic solvents.
When passing samples through a column packed with inulin, he observed that the mixture would separate into distinct colored bands which could be collected at the column outlet.
He postulated that the separation is based on the ability of the dissolved components to physically interact with the immobilized inulin particles causing them to be retained longer on the column {cite}`Tswett1906`.

However, the nonlinear effects inherent to these interactions, as well as the lack of sophisticated detectors posed difficulties in understanding and controlling the separation process.
Furthermore, the technique initially suffered from low productivities — the ratio of purified product to the amount of packing material required — which made its application very inefficient and expensive.
For these reasons, chromatography was not widely adopted until almost three decades later when Tswett's work was rediscovered and established as a preparative separation method for a broad spectrum of chemical compounds {cite}`Guiochon2006`.

Since then, the technique and our understanding of it have continuously evolved and expanded.
Already early on, efforts to improve the process performance led to creative solutions in the process design.
For example, when the method was applied on a large scale to purify rare earth materials required for nuclear research in the 1940s, cascading multi-column operations were considered to improve throughput.
Furthermore, the buffer composition was taken into account to minimize the use of expensive chemicals while still ensuring a suitable pH for the separation {cite}`Spedding1947`.
In the 1960s, when the oil industry started using chromatography for hydrocarbons, the bigger production scales led to the development of continuous operating concepts like simulated moving bed (SMB) which could operate at much higher productivities than conventional batch-elution processes {cite}`SchmidtTraub2020`.
This was accompanied by theoretical modeling and advancements in numerical process simulation which are a prerequisite for better understanding the inherent complex process dynamics and for rigorous process design and optimization.
Simultaneously, the advancements in material sciences meant that highly selective adsorbents could be manufactured which opened the doors to applications in the biopharmaceutical industry, a trend which continues to this day {cite}`SchmidtTraub2020`.

Today, the technique is widely used, as many different adsorbents can be combined with a broad range of solvents.
It is employed in the purification of basic bulk chemicals on a multi-ton scale.
This includes the preparative separation of petrochemical isomers and sugars, as well as the purification of essential chemicals such as amino acids and pharmaceuticals {cite}`SchmidtTraub2020`.
In addition, it has many applications in performing complex separations in the biopharmaceutical industry, where there are stringent requirements regarding purity and regulatory compliance.

% Operating Concepts
Most process-scale chromatographic separations are performed using a single column.
In conventional elution mode, small amounts of the mixture are injected periodically onto the chromatographic column and the mixture components elute as separated peaks from its outlet.
However, as previously mentioned, many advanced operating modes exist that can outperform conventional batch chromatography in terms of productivity, solvent consumption, and recovery yield.

For example, operating concepts like closed-loop recycling {cite}`Bombaugh1969,Heuer1995` or steady-state recycling (SSR) {cite}`Bailly1982,Sainio2009,Kaspereit2011` incorporate different strategies for the recycling of unresolved fractions from the column outlet back to the inlet with the aim of improving yield, solvent consumption and/or productivity {cite}`Sainio2009`.
If purity requirements are low, bypass streams can be advantageous {cite}`Siitonen2012`.
Moreover, the use of multiple columns gives rise to various concepts ranging from serial or parallel arrangements of columns {cite}`Ziomek2006,GarciaPalacios2009`, over pseudo-continuous processes, up to the many variants of the powerful continuous SMB concept.
More details on such advanced chromatographic operating modes are given in {numref}`chromatographic_principle` and in {cite}`SchmidtTraub2020,Nicoud2015,Rodrigues2015`.

% Challenges in Process Design
Depending on the separation problem at hand, different operating concepts are better suited than others and the process selection usually involves a trade-off between multiple criteria.
Simple systems are less expensive and more adaptable than complex multi-column systems which involve high capital investments.
On the other hand, bigger, more complicated systems are often more robust in their operation and can lead to lower operating costs compared to single column processes.
Another factor to consider is the distinctive startup behavior of some operating concepts (see {numref}`stationarity`) making them only viable for large separation campaigns where these losses can be absorbed {cite}`Rajendran2013`.
This is to show that the selection of an appropriate operating mode is an important step in the design of the process.

% Model-based design
Due to the rapid development of computational methods as well as the low costs of running simulations compared to laboratory experiments, the driving force for the development of new advanced chromatographic processes is increasingly based on mathematical modeling and optimization tools.
While there are still many physico-chemical phenomena which are challenging to describe, there is generally a high level of confidence in the modeling of the dynamics of chromatographic processes.
Nowadays many wet lab experiments are only performed to calibrate these models {cite}`Rajendran2013`.

The model-based design and optimization of chromatographic separations is, however, not trivial.
This is due to the periodic operation and the distinct non-linear dynamics of chromatographic processes, as well as the many degrees of freedom involved such as column dimensions, valve switching times, or operating conditions.
For some of the operating modes, there exist simple shortcut methods that deliver rough initial design estimates (see e.g. {cite}`Siitonen2011` for batch chromatography, {cite}`Sainio2009,Kaspereit2011` for SSR systems, {cite}`Mazzotti2006` for SMB processes, or {cite}`Siitonen2015` for a common treatment), but these models often include many simplifications.
For example, they might only work for certain binding models, neglect mass-transfer, or only cover single column operation.
However, in many practical cases, a wide range of binding interaction mechanisms are relevant, including adsorption, ionic interactions, binding to specific ligands, or size exclusion.
Furthermore, physical phenomena like axial dispersion, film diffusion, or pore diffusion often play a significant role and must be accounted for.
As a result, rigorous process development often necessitates the utilization of more detailed models and advanced optimization schemes.
Consequently, there exists a variety of different models in chromatography (see {numref}`model_formulation`) as well as different numerical solvers (see {numref}`model_solution`).
A variety of optimization approaches has also been proposed for the design of certain chromatographic processes.
An overview is given in sections {numref}`%s <design_formulation>` and {numref}`%s <design_solution>` and in {cite}`Kawajiri2020`.

% Tool requirements
Considering the many advanced operating modes mentioned above, this complexity gives rise to an overwhelming number of specific process models and optimization schemes that may have to be implemented when seeking for an optimal process for a given separation task.
Against this background, a general-purpose tool is needed that allows an efficient and flexible handling of the different tasks in the development of optimal chromatographic processes.
The main tasks are:

- Setting up a model for the chromatographic system and the desired process structure,
- Solving the model equations for simulating the process,
- Determining process performance by evaluating the outgoing streams/chromatograms,
- Performing optimization of continuous variables, timed events, and potentially the process structure.

% Existing tools
Several commercial programs are available which provide parts of the aforementioned required functionalities, like Aspen Chromatography {cite}`aspen`, GoSilico (formally known as ChromX) by Cytiva {cite}`GoSilico`, and Ypso-Proxima (formally known as as ChromWorks) by YpsoFacto {cite}`ypso-proxima`.
Most of these programs are aimed at experimentalists and allow users to carry out simulations of simple processes without requiring programming expertise.
In contrast, there exist many highly application-specific programs in academia which were developed to examine individual research questions.
However, neither provide the flexibility and customizability required for the *ab initio* development of novel process concepts.
A notable exception here is **CADET** by the Forschungszentrum Jülich {cite}`Leweke2018,Leweke2025`.
It offers a diverse family of different binding, reaction, and unit operation models which can be used to simulate a large range of separation processes.
Moreover, multiple unit operations can be connected in a network which generally also allows modeling complicated process configurations.
However, the software is primarily a numerical solver for the partial differential equations.
This makes the definition of advanced operating concepts not only laborious but also limits the direct use of CADET for process optimization without another layer of abstraction for the definition of dynamic processes.

While these current tools provide useful functionality, they have limitations for advanced chromatographic process design.
Existing commercial software lacks flexibility for complex process configurations, and academic tools often require specialized programming knowledge.
No available framework systematically separates the key components: process setup, simulation, performance evaluation, and optimization.
This makes it difficult to compare different operating modes or exchange individual components without extensive reimplementation.

% Approach
To address these limitations, a modular framework for the efficient modeling, simulation and optimization of advanced chromatographic processes was developed for this work.
The framework implements a modular architecture where process configuration, simulation, evaluation, and optimization exist as independent components that can be developed, tested, and exchanged separately.
This design enables flexible combination of physico-chemical models, numerical solvers, process configurations, and optimization algorithms.

The software is implemented in an object-oriented paradigm in the programming language **Python**.
It provides an interface to **CADET-Core**, which serves as the primary solver within the framework; however, the architecture is sufficiently flexible to accommodate alternative solvers.
This tight integration motivated the designation of the framework as **CADET-Process**.
The code is open source and distributed under *GPL* version 3, making it freely accessible to both academic and industrial users.
The repository is publicly available at [https://github.com/fau-advanced-separations/CADET-Process](https://github.com/fau-advanced-separations/CADET-Process).

Best practices for sustainable scientific software development have been applied throughout this work to ensure reliability and reproducibility of the code.
Without the application of these modern standards of software design, reliability and reproducibility of the code cannot be ensured which is particularly important in a scientific context.
Since process engineers are usually not trained in this field, a chapter of this work is dedicated to the introduction of important techniques such as version control, unit testing, and software documentation (see {numref}`methods_software_design`).

% Demonstrations
To demonstrate the flexibility of the framework, several case studies are presented in this work.
First, a model of a typical chromatographic laboratory system is developed, focusing on a protein purification step.
The objectives here are to:
- showcase parameter estimation methods for different problems,
- validate CADET-Process using experimental data,
- incorporate system periphery, including the influence of valves and tubing, which are often neglected in modeling,
- demonstrate a load–wash–elute process for lysozyme using the steric mass-action binding model with a salt gradient, representing a common yet complex chromatographic procedure.

Next, the optimization of advanced operating concepts is investigated through a set of synthetic case studies.
These studies assume known model parameters and focus on preparative separations of binary and ternary mixtures.
Operating modes of increasing complexity are examined, including batch-elution, recycling strategies, flip-flop chromatography, and serial column configurations.
For validation, process simulations are compared with equilibrium theory solutions.
Single- and multi-objective optimization are used to optimize feed durations, valve switching and cycle times, and column geometry, aiming to maximize productivity and yield while minimizing solvent consumption.
