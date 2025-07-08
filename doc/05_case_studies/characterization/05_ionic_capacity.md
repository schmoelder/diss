(ionic_capacity)=
# Estimation of the ionic capacity of the resin

To determine the ionic capacity of the resin, a titration experiment is conducted.
In this experiment, the column is first flushed with water, followed by equilibration with $20~CV$ of acetic acid at $pH 3$.
During equilibration, the acetic acid exchanges counter-ions with $n_{\text{H}^+}$ protons.
Next, the column is flushed with water for 10 CV to remove loosely bound acetic acid.
Finally, the resin is titrated with a NaOH solution.
The NaOH concentration is determined via pH measurement, and the NaOH volume is calculated from the increase in conductivity over time.
The amount of exchanged sodium ions, $n_{\text{Na}^+}$, is then determined using the NaOH volume and concentration:

$$
n_{\text{Na}^+} = V_{\text{NaOH}} \cdot c_{\text{NaOH}}
$$

The total ionic capacity is calculated by dividing the exchanged sodium ions by the solid volume of the resin:

$$
\Lambda = \frac{n_{\text{Na}^+}}{V_c \cdot (1 - \varepsilon_{\text{total}})}
$$

The total porosity, $\varepsilon_{\text{total}}$, is determined using the column porosity $\varepsilon_c$and the particle porosity $\varepsilon_p$, which are estimated from tracer experiments used for model calibration.
It is given as the sum of the interstitial volume $V_{\text{int}}$ and pore volume $V_{\text{pore}}$, divided by the column volume $V_C$:

$$
\varepsilon_{\text{total}} = \frac{V_{\text{int}} + V_{\text{pore}}}{V_C} = \varepsilon_c + (1 - \varepsilon_c) \cdot \varepsilon_p
$$
