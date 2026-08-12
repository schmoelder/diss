---
jupytext:
  main_language: python
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

(characterization)=
# Model of a typical chromatographic laboratory system

This chapter demonstrates the parameter estimation capabilities of CADET-Process through the systematic characterization of a chromatographic laboratory system for a protein purification process.
The presented study builds upon work first published by Lukas Thiel in his master's thesis {cite}`Thiel2023`.
While utilizing the same raw data, this work presents an independent modeling approach and fitting procedure.
In contrast to Thiel's work, which aimed to model the influence of pH on protein adsorption, the primary goals of this chapter are:

- validating CADET-Process using real experimental data,
- showcasing parameter estimation methods for different types of experiments,
- modeling the system periphery, demonstrating the influence of valves and tubing, which are often neglected in modeling,
- demonstrating a load-wash-elute process with lysozyme using the steric mass-action binding model and a salt gradient.

The process involves several key steps:

- **System periphery**: Acetone and salt tracers are used to estimate the void volume of the injection valve, the tubing before and after the column, as well as the tubing between the detectors.
- **Column properties**: Specific experiments investigate column properties such as porosity and axial dispersion.
- **Protein-specific parameters**: Additional experiments estimate protein-specific particle porosity and transport parameters, aiding in selecting the appropriate column model.
- **Binding parameters**: Experiments are conducted to determine binding parameters, considering factors like pH and salt concentration. These experiments involve linear gradients at various pH levels and column volumes for calibration and validation.

The study repository, including scripts and CADET-RDM provenance for the reported results, is publicly available at: [https://github.com/schmoelder/diss_parameter_estimation](https://github.com/schmoelder/diss_parameter_estimation).
