# These are some snippets...
## Objectives

For this purpose, a general-purpose tool is required that allows an efficient and flexible handling of the different subtasks in the development of optimal chromatographic processes. The main requirements are:
- Setting up a model for the desired process structure and the specific chromatographic column(s),
- Solving the model equations for simulating the process,
- Determining process performance by evaluating the outgoing streams/chromatograms,
- Performing optimization of continuous variables, timed events, and potentially process structure.


In this work, we present a new modular framework for the efficient modelling, simulation and optimization of advanced chromatographic processes.
The framework decouples the different tasks mentioned above in order to allow for a simple and independent manipulation or exchange of operating concept, modelling depth of the chromatographic column(s), solution of the model equations, performance evaluation, and optimization algorithms.
The developed platform performs these tasks in separate corresponding modules, which can be interchanged with other own or third-party modules.
The platform is implemented in an object-oriented manner in the programming language Python.
The current implementation includes an interface to CADET [20], which is an efficient open source simulator for various chromatographic column models, among them the very detailed general rate model.
Due to this powerful combination, we denote our framework as CADET-Process.
The software is open source and distributed under GPL version 3, and thus freely available to academia and industry.
The code can be obtained from https://github.com/fau-advanced-separations/CADET-Process.

___


ohne Unterkapitel, wenige Seiten

- Hintergrund (prep Chrom, Relevanz, Komplexität)
- Forschungslücke (Software)
- Herausforderungen diesbzgl.
- Zielstellung (grob): Brücke zwischen mechanist. Modellen und Scheduling
- Grobstruktur/-Inhalt der Arbeit (wichtigste Hauptergebnisse)

___


## Principles
> Adsorptive separations have been in use well before the twentieth century. Tswett (1905, 1906), however, was the first who coined the term “Chromatography” in 1903 for the isolation of chlorophyll constituents. Kuhn and Brockmann, in the course of their research recognized the need for more reproducible and also more selective adsorbents, specially tuned for specific separation problems. This recognized demand for reproducible stationary phases led to the development of first materials standardized for adsorption strength and describes the first attempt toward reproducible separations (Unger et al., 2010).

> Liquid Chromatography (LC) was first applied as a purification tool and has thereby been used as a preparative method. It is the only technique that enables to separate and identify both femtomoles of compounds out of complex matrices in life sciences, and also allows the purification and isolation of synthetic industrial products in the ton range. The development of modern LC methodology and the corresponding technologies are based on three main pillars, which have developed over different time scales (Figure 1.1). In the field of preparative and process chromatography the “restart” after the dormant period between the 1930s and the 1960s was not induced by the parallel emergence of analytical HPLC, but from engineering in search of more effective purification technologies. High selectivity of HPLC in combination with the principle to enhance mass transfer by counter current flow significantly increased the performance of preparative chromatography in terms of productivity, eluent consumption, yield, and concentration. The first process of this kind was the Simulated Moving Bed (SMB) chromatography for large-scale separation in the petrochemical area and in food processing. The development of new processes was accompanied by theoretical modeling and process simulation which are a prerequisite for better understanding of transport phenomena and process optimization.

> In the 1980s, highly selective adsorbents were developed for the resolution of racemates into enantiomers. These adsorbents were mainly employed in analytical HPLC (Allenmark, 1992). However, the availability of enantioselective packings in

## Objectives
For this purpose, a general-purpose tool is required that allows an efficient and flexible handling of the different subtasks in the development of optimal chromatographic processes. The main requirements are:
- Setting up a model for the desired process structure and the specific chromatographic column(s),
> 1. An exchange of mass and energy occurs between the single phases. The driving force for these transport processes is a deviation from thermodynamic equilibrium.
> 1. After completion of the exchange procedures, the two phases are characterized by different compositions and can be separated. Result of this phase separation is a partial separation of the initially homogeneous mixture.
