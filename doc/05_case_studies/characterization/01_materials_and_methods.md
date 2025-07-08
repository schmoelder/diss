(materials_and_methods)=
# Materials and methods

All experiments were conducted by Lukas Thiel at the laboratory of Institute of Fluid Process Engineering at RWTH Aachen.
The chromatography system used in this thesis is a Knauer system. @TODO: Which model?
{numref}`knauer_pid` shows the process and instrumentation diagram of the Knauer chromatography system used in this work.
The system consists of two buffer flasks with different ion concentrations.
Each buffer is connected to a pump via tubing.
Both pumps are further connected to a static mixer.
The valve is equipped with a $50~mL$ sample loop to inject a well-defined amount of sample into the system.
The valve is connected to a SP Sepharose High Performance column.
The column is a strong cation exchanger with an $SO_3^{-}$ functional group and a column volume (CV) of $4.7~mL$.
The average particle size, $d50v$, is provided by the manufacturer Cytiva as $34~μm$, with an ionic capacity between $0.15$ and $0.2~mM~H^{+}$.
The column outlet is connected to a multi-UV sensor.
The UV signal at $280~m$ is used for tracer and protein detection.
The outlet of the UV sensor is connected to a conductivity sensor.
The outflow of the system is captured in a storage tank.
A computer is connected to the system with the software *PurityChrom 5* to operate the system, capture, process, and view the measured data.

```{figure} ./figures/knauer_pid.png
:name: knauer_pid

P&ID of Knauer system.
```

Acetone and Blue Dextran 2000 kDa were used as tracers in this thesis, along with Lysozyme from chicken egg white with a molar weight of $14.3~kDa$.
The buffers consist of a low salt buffer with $20~mM$ sodium acetate ($C_2H_3NaO_2$), whereas the high salt buffer consists of $20~mM$ sodium acetate and additional $1~M$ sodium chloride ($NaCl$).
Both buffers are adjusted with hydrochloric acid ($HCl$) of $4~M$ and sodium hydroxide ($NaOH$) of $1~M$ to the desired pH.
Furthermore, acetic acid with a $pH$ of $3$ is used in this thesis for resin titration.
The manufacturer of the material can be found in {numref}`materials`.

```{table} Materials used in characterization experiments
:name: materials
:align: center

| Material          | Manufacturer            | Purity/ Concentration |
| ----------------- | ----------------------- | --------------------- |
| Acetic Acid       | Merck KGaA              | ≥ 99.7 %              |
| Acetone           | Carl Roth GmbH & Co. KG | ≥ 99.5 %              |
| Blue Dextran      | Merck KGaA              |                       |
| Hydrochloric Acid | Carl Roth GmbH & Co. KG | 4 M ± 0.2 %           |
| Lysozyme          | Carl Roth GmbH & Co. KG | ≥ 90 %                |
| Sodium Acetate    | Merck KGaA              | ≥ 99 %                |
| Sodium Chloride   | Carl Roth GmbH & Co. KG | ≥ 99 %                |
| Sodium Hydroxide  | Carl Roth GmbH & Co. KG | 1 M ± 0.2 %           |
```

## Conductivity Calibration Curve

A conductivity detector is integrated into the chromatographic system to monitor salt concentration in real time during chromatography experiments.
Conductivity $\kappa$ describes a solution's ability to conduct electricity and is defined as

$$
\kappa = \frac{l}{A \cdot R},
$$

where $A$ is the conductor’s cross-sectional area, $l$ is its length, and $R$ is the resistance.
Conductivity is measured in siemens per meter ($S \cdot \text{m}^{-1}$), where $[S] = [\Omega^{-1}] = [A/V]$ @TODO: cite.
Higher ion density increases conductivity @TODO: cite.

To quantify the relationship between salt concentration and conductivity, a calibration curve is recorded by measuring the conductivity of solutions with varying salt concentrations at a constant pH of 5.
Conductivity values are recorded over one minute at predefined salt concentrations (20 mM, 270 mM, 570 mM, 770 mM, and 1020 mM).
Since the relationship between salt concentration and conductivity is nonlinear, a quadratic function is fitted to the measured data using the least squares method.
This function is then used to determine salt concentration from conductivity in subsequent analyses.


## Rescaling of the UV Signal

To compare simulations with experimental data, the UV signal must also be converted into concentration values.
A calibration curve can be generated for different protein concentrations, and a trendline can be used for interpolation.
For this work, however, the UV signal is rescaled using the mass balance.
For each experiment, a known amount of protein is injected into the column.
The UV signal is then rescaled so that its integral matches the inserted protein amount.
To define the peak's start and endpoint for integration, start and stop times are set.
Baseline correction is also applied by adjusting the UV signal to zero if necessary.

(experiments)=
## Experiments
@TODO: Add description of pulse injection / gradient / breakthrough etc.
