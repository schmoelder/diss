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

- First published by Lukas Thiel in his master thesis
- Here, same raw data but independent analysis / fits
- Goal:
    - validate CADET-Process using real experimental data
    - show how to model system periphery (often neglected)
    - demonstrate parameter estimation features
    - Load-wash-elute process with gradient

## Overview experiment
- System:
    - Knauer System
    - column
    - lysozyme
    - buffers
    - sensors / calibration
- Experiments:
    - characterization experiments
    - gradient methods



## Calibration of Chromatography System

The objective is to calibrate a chromatography system using various experiments to estimate system parameters.
The process involves several key steps:

1. **Void Volume Estimation**: Acetone tracers are used to estimate the void volume of the tubing before and after the column.
2. **Conductivity Measurement**: A salt pulse experiment assesses the influence of the void volume between the conductivity and UV sensors on the conductivity measurement. This measurement compares the salt gradient from simulations to the conductivity signal.
3. **Mixer and Tubing Influence**: A salt step experiment analyzes the influence of the mixer and the tubing before the column valve.
4. **Column Properties**: Specific experiments investigate column properties such as porosity and axial dispersion.
5. **Protein-Specific Parameters**: Additional experiments estimate protein-specific particle porosity and transport parameters, aiding in selecting the appropriate column model.
6. **Binding Parameters**: Experiments are conducted to determine binding parameters, considering factors like pH and salt concentration. These experiments involve linear gradients at various pH levels and column volumes for calibration and validation.
7. **Gradient Method**: The experimental sequence includes loading the sample, washing, linear gradient elution, and final stripping.

## Acid base titration
(see also in parameter_estimation files)

## Conductivity Calibration Curve
(see also in parameter_estimation files)

## Rescaling of the UV Signal
(see also in parameter_estimation files)

## Characterization of system periphery

The objective is to characterize the periphery of a chromatography system by dividing it into individual parts and investigating each using tracer experiments. The system includes pumps, a mixing unit, a sample valve, tubing, a column, a UV detector, and a conductivity sensor.

The procedure involves several steps:

1. **Modular Tubing Configuration**: The system's tubing is modular, allowing for different connections to isolate and study specific parts.
2. **Acetone Pulse Experiments**: Acetone pulses are used to determine the influence of tubing before and after the column by connecting it directly to the UV detector or using a connector.
3. **Salt Pulse and Step Experiments**: A salt pulse experiment measures the void volume between the UV detector and the conductivity sensor. A salt step experiment, gradually increasing the salt concentration, estimates the influence of the static mixer and the tubing before the sample valve.
4. **Data Analysis**: The results from these experiments are compared to simulation data to understand the retention time and dispersion characteristics of the system.

## Estimation of column parameters

## Estimation of the ionic capacity of the resin

## Estimation of adsorption parametesr
