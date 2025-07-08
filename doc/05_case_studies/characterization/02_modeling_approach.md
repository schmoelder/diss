(modeling_approach)=
# Modeling approach
In the following, the parameter determination for the chromatography periphery is discussed.
The influence of valves, mixer, and tubing on the chromatogram is incorporated into the model to enable accurate determination of binding behavior parameters.
This approach also simplifies the application of experimental data, requiring only minimal preprocessing beyond UV signal-to-concentration conversion.
Additionally, column properties such as porosity, dispersion, and protein-dependent film diffusion are determined.
The simplification of the steric mass action (SMA) model is presented, and the ion capacity is determined.
Finally, the mixing of high and low salt buffers is analyzed in relation to potential pH changes during linear gradients.

## CADET Process Model
Incorporating the chromatography system periphery into the model enhances the determinability of isotherm parameters.
The influence of periphery components on the chromatogram can be accounted for in the model using approaches introduced in @TODO: update reference
Modeling can be implemented through combinations of single continuously stirred-tank reactors (CSTRs) or dispersed plug flow reactors (DPFRs).
In this work, the chromatography system described in @TODO: update reference is represented by CSTR and DPFR units before and after the column.
A summary of the calibrated process model is presented in {numref}`table` @TODO: Update reference

```{figure} ./figures/knauer_model.png
:name: knauer_model

Model of Knauer system.
```

The optimal modeling approach for tracer experiments is determined based on the sum of squared errors (SSE) between experimental and simulated data.
@TODO: Update reference and 5.3 describe the detailed procedure of the inverse fit method and the resulting parameters in more detail.

The model shown in @TODO: Update reference can be summarized as follows:
- The mixer and sample valve are approximated by a combination of DPFR and CSTR units.
- The tubing before and after the column, as well as the section between the UV sensor and conductivity sensor, are modeled using DPFRs.
- A sample inlet is included after the CSTR to represent the sample introduction via the sample loop at the column valve.
- The DPFRs before and after the column account for tubing effects.
- The outlet of the post-column DPFR is compared to the experimental UV signal.
- The final DPFR accounts for the retention time difference between UV and conductivity signals.
- The output of this final DPFR is used for comparison with the experimental conductivity signal.

Note that the conductivity outlet is not used for parameter estimation but serves solely for verification of salt gradients between experiments and simulations.
The column transport is modeled using the lumped diffusion model, while adsorption isotherms are described by the steric mass action model with pH dependencies.
