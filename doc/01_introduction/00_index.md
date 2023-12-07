# Introduction

% Relevance of Chromatography
Production processes in chemical, pharmaceutical, or biotechnological industries typically require the separation of products from side products or impurities.
While classical separation processes like distillation, extraction, or filtration are effective in many cases, they have limitations when dealing with components that are physico-chemically very similar, sensitive to harsh conditions, or part of multi-component mixtures.
In particular for such challenging separations, chromatography is a powerful alternative {cite}`Guiochon2006,SchmidtTraub2020,Nicoud2015`.

The term *chromatography* was first used by Russian botanist Michail Tswett in the early 1900s to describe a method he developed for separating and analyzing chlorophyll extracts dissolved in organic solvents.
When passing samples through a column packed with inulin, he observed that the mixture would separate into distinct colored bands which could be collected at the column outlet.
He postulated that the separation is based on the ability of the dissolved components to physically interact with the immobilized inulin particles causing it to be retained longer on the column {cite}`Tswett1906`.

However, the nonlinear effects inherent to the interactions, as well as the lack of modern detectors posed a difficulty in understanding and controlling the separation process.
Furthermore, the technique initially suffered from low productivities — the ratio of purified product to the amount of packing material required — which made its application very expensive.
For these reasons, chromatography was not widely adapted until almost three decades later when Tswett's works were rediscovered and established as a preparative separation method for a broad spectrum of chemical compounds {cite}`Guiochon2006`.

Since then, the technique and our understanding thereof have continuously been evolved and extended.
Already early on, efforts to improve the process performance led to creative solutions in the process design.
For example, when the method was applied on a large scale to purify rare earth materials required for nuclear research in the 1940s, cascading multi-column operations were considered to improve throughput.
Furthermore, the buffer composition was taken into account to minimize the use of expensive chemicals while still ensuring a suitable pH for the separation {cite}`Spedding1947`.
In the 1970s, when the oil industry started using chromatography for hydrocarbons, the bigger production scales led to the development of continuous operating concepts like simulated moving bed (SMB) which could operate at much higher productivities than conventional batch elution processes.
This was accompanied by theoretical modeling and advancements in numerical process simulation which are a prerequisite for better understanding the transport phenomena and for rigorous process optimization.
Simultaneously, the advancements in material sciences meant that highly selective adsorbents could be manufactured which opened the doors to applications in the biopharmaceutical industry, a trend which continues to this day {cite}`SchmidtTraub2020`.

Today, the technique is widely used, as many different adsorbents can be combined with a broad range of solvents.
It has applications in performing complex separations in the biopharmaceutical industry, where there are stringent purity requirements and regulatory compliance, including Good Manufacturing Practice (GMP).
Additionally, the technique is employed in the purification of basic chemicals on a multi-ton scale.
This includes the preparative separation of petrochemical isomers and sugars, as well as the purification of essential chemicals such as amino acids and pharmaceuticals {cite}`SchmidtTraub2020`..

% Operating Concepts
Most chromatographic separations are performed using a single column.
In conventional elution mode, small amounts of the mixture are injected periodically onto the chromatographic column and the mixture components elute as separated peaks from its outlet.
However, as previously hinted at, many advanced operating modes exist that can outperform conventional batch chromatography in terms of productivity, solvent consumption, and recovery yield.

For example, operating concepts like closed-loop recycling {cite}`Bombaugh1969,Heuer1995` or steady-state recycling (SSR) {cite}`Bailly1982,Sainio2009,Kaspereit2011` incorporate different strategies for the recycling of unresolved fractions from the column outlet back to the inlet with the aim of improving yield, solvent consumption and/or productivity {cite}`Sainio2009`.
If purity requirements are limited, bypass streams can be advantageous {cite}`Siitonen2012`.
Moreover, the use of multiple columns gives rise to various concepts ranging from clever series or parallel arrangements of multiple batch columns {cite}`Ziomek2006,GarciaPalacios2009`, over pseudo-continuous processes, up to the many variants of the powerful continuous simulated moving bed (SMB) concept.
More details on such advanced chromatographic operating modes are given in {numref}`chapter %s <chromtographic_principle>` and in {cite}`SchmidtTraub2020,Nicoud2015,Rodrigues2015`.

% Challenges in Process Design
Depending on the separation problem at hand, different operating concepts are better suited than others and the process selection usually involves a trade-off between multiple criteria.
Small and simple systems are usually cheaper and more versatile than large multi-column systems which involve high capital investments.
On the other hand, bigger, more complicated systems are often more robust in their operation and can lead to lower production costs compared to single column processes.
Another factor to consider is the distinctive startup behaviour of some operating concepts (see {numref}`chapter %s <stationarity_guide>`) making them only viable for large separation campaigns where these losses can be absorbed {cite}`Rajendran2013`.
This is to show that the selection of an appropriate operating mode is an important step in the design of the process.

% Model based design
Due to the rapid development of computational methods as well as the low costs of running simulations compared to laboratory experiments, the driving force for the development of new advanced chromatographic processes is increasingly based on mathematical modeling and optimization tools.
While there are still many physico-chemical phenomena which are challenging to describe, there is generally a high level of confidence in the modeling of the dynamics of chromatographic processes. Nowadays many wet lab experiments are only performed to calibrate these models {cite}`Rajendran2013`.

The model-based design and optimization of chromatographic separations is, however, not trivial.
This is due to the periodic operation and the distinct non-linear dynamics of chromatographic processes, as well as the many degrees of freedom involved.
For some of the operating modes, there exist simple shortcut methods that deliver rough initial design estimates (see e.g. {cite}`Siitonen2011` for batch chromatography, {cite}`Sainio2009,Kaspereit2011` for SSR systems, {cite}`Mazzotti2006` for SMB processes, or {cite}`Siitonen2015` for a common treatment).
But these models often include many simplifications.
Hence, rigorous process development often requires more detailed models and optimization schemes.
Here, it should be considered that multiple chromatographic interactions mechanisms can be exploited, like adsorption, ionic interactions, binding to specific ligands, or size exclusion, to name only a few.
Depending on the given system, further physical phenomena like axial dispersion, film and pore diffusion may have to be accounted for.
Consequently, there exists a variety of different modeling approaches in chromatography (see {numref}`chapter %s<model_formulation>`) as well as numerical solvers (see {numref}`chapter %s<model_solution>`).
Apart from that, also a variety of optimization approaches have been proposed for designing chromatographic processes.
An overview is given in sections {numref}`%s <design_formulation>` and {numref}`%s <design_solution>` and in {cite}`Kawajiri2020`.

When additionally considering the many advanced operating modes mentioned above, this gives rise to an unmanageable number of specific process models and optimization schemes that may have to be implemented when seeking for an optimal process for a given separation task.

% Tool requirements
Against this background, a general-purpose tool is needed that allows an efficient and flexible handling of the different subtasks in the development of optimal chromatographic processes.
The main requirements are:

- Setting up a model for the desired process structure and the specific chromatographic column(s),
- Solving the model equations for simulating the process,
- Determining process performance by evaluating the outgoing streams/chromatograms,
- Performing optimization of continuous variables, timed events, and potentially process structure.

% Existing tools
There are several commercial programs available which provide parts of the aforementioned required functionalities, like Aspen Chromatography {cite}`aspen`, GoSilico (formally known as ChromX) by Cytiva {cite}`gosilico`, and Ypso-Ionic (formally known as as ChromWorks) by YpsoFacto {cite}`ypsoionic`.
Most of these programs are aimed at experimentalists and allow users to carry out simulations of simple processes without requiring programming expertise.
In contrast, there exist many highly application specific programs in academia which were developed to examine individual research qjuestions.
However, neither provide the flexibility and customizability required for the *ab initio* development of novel process concepts.
A notable exception here is *CADET* by the Forschungszentrum Jülich {cite}`Leweke2018`.
It offers a diverse family of different binding, reaction, and unit operation models which can be used to simulate a large range of separation processes.
Moreover, multiple unit operations can be connected in a network which generally also allows modeling complicated process configurations.
However, the software is primarily a numerical solver for the partial differential equations.
This makes the definition of advanced operating concepts not only laborious but also limits the direct use of *CADET* for process optimization without another layer of abstraction for the definition of dynamic processes.

% Approach
In this context, a new modular framework for the efficient modeling, simulation and optimization of advanced chromatographic processes was developed for this work.
The framework decouples the different tasks mentioned above in order to allow for a simple and independent manipulation and exchange of operating concept, modeling depth of the chromatographic column(s), solution of the model equations, performance evaluation, and optimization algorithms.
These tasks are performed in separate modules which can be interchanged with other custom or third-party modules.

The platform is implemented in an object-oriented manner in the programming language Python.
The current implementation includes an interface to *CADET* as the main solver of the framework but it is generally possible to also use other solvers.
Due to this powerful combination, the framework developed for this work was named *CADET-Process*.
The software is open source and distributed under GPL version 3, and thus freely available to academia and industry.
The code can be obtained from <https://github.com/fau-advanced-separations/CADET-Process>.

At this point, it is important to note that not only chromatography has developed over the last decades, but also best practices for sustainable scientific software development have been established.
Without the application of these modern standards of software design, reliability and reproducibility of the code cannot be ensured which is particularly important in a scientific context.
Since process engineers are usually not trained in this field, a chapter of this work is dedicated to the introduction of important techniques such as version control, unit testing, and software documentation (see {numref}`chapter %s <methods_software_design>`).

% Demonstrations
To demonstrate the flexibility of the framework, several case studies are performed.

First, a simple batch elution process is optimized, introducing the general setup.
This case explores various scenarios, including single-objective and multi-objective optimization studies.
Next, a more complex steady-state recycling process is studied, inspired by the work of Kaspereit et al {cite}`Kaspereit2011`.
Initially, the framework reproduces the first results through a parametric study.
Subsequently, these findings are compared with optimization results to demonstrate the effectiveness of the optimizer in locating global optima.
Furthermore, the optimization scenarios are expanded to offer increased flexibility in process design.

Finally, an optimization study is conducted to optimize buffer components, aiming to linearize a pH gradient within a system involving a complex set of interconnected reactions. This case study illustrates the framework's capacity to handle intricate and interrelated factors in process optimization.
