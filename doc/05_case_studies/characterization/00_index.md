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
# Characterization of a "real" system

The characterization of chromatographic systems is a critical step in ensuring the accuracy and reliability of experimental data.
This chapter builds upon the foundational work first published by Lukas Thiel in his master thesis {cite}`Thiel2023`.
While utilizing the same raw data, this study presents an independent analysis and fitting process.
In contrast to Thiel's work, which primarily aimed to model the influence of pH on protein adsorption, the primary goals of this chapter are:
- Validation of **CADET-Process** using real experimental data
- Modeling of system periphery, demonstrating the influence of valves and tubings which are often neglected in modeling
- Showcasing parameter estimation approaches and algorithms for different problems
- Demonstrating a Load-Wash-Elute process with a salt gradient, another common yet complex procedure in chromatography

The objective is to calibrate a chromatography system using various experiments to estimate system parameters.
The process involves several key steps:

1. **Void Volume Estimation**: Acetone tracers are used to estimate the void volume of the tubing before and after the column.
2. **Conductivity Measurement**: A salt pulse experiment assesses the influence of the void volume between the conductivity and UV sensors on the conductivity measurement. This measurement compares the salt gradient from simulations to the conductivity signal.
3. **Mixer and Tubing Influence**: A salt step experiment analyzes the influence of the mixer and the tubing before the column valve.
4. **Column Properties**: Specific experiments investigate column properties such as porosity and axial dispersion.
5. **Protein-Specific Parameters**: Additional experiments estimate protein-specific particle porosity and transport parameters, aiding in selecting the appropriate column model.
6. **Binding Parameters**: Experiments are conducted to determine binding parameters, considering factors like pH and salt concentration. These experiments involve linear gradients at various pH levels and column volumes for calibration and validation.
7. **Gradient Method**: The experimental sequence includes loading the sample, washing, linear gradient elution, and final stripping.
