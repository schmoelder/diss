(model_formulation)=
# Formulation of chromatographic process models

In this chapter, an overview of the formulation of chromatographic process models is provided, covering different aspects of the modeling of separation processes.
Models for retention mechanisms are presented, followed by a description of the equations used to describe the phenomena occurring inside the column and how they are coupled to the adsorption models.
Finally, effects that occur outside the column in the periphery of the system are considered.

## Digression: machine learning models

In recent years, machine learning (ML) models have become increasingly popular in the field of chromatography due to their ability to efficiently handle large amounts of data and accurately model complex systems {cite}`Subraveti2022`.
These models are predominantly data-driven; that is, they rely less on a physical understanding of the system and more on approximating and interpolating some measured output as a function of input variables.
Machine learning approaches are particularly valuable in scenarios where underlying mechanisms are not fully understood, or when direct measurement of necessary parameters is difficult.
In addition, machine learning models can be used for surrogate modeling, to create a simplified approximation of a complex, computationally expensive model {cite}`Jaepel2022`.

Despite the advances in machine learning, mechanistic models remain crucial, particularly in training machine learning models for chromatographic applications.
Understanding the design criteria and defining the overall structure of the model are essential steps in optimizing chromatographic processes.
Therefore, in this work, the focus will be solely on mechanistic models.

(isotherm_models)=
## Adsorption isotherms

Different adsorption isotherm models are used to describe the accumulation of molecules on the surface of the stationary phase.
Usually, the loading concentration $q$ is be quantified as a function of the mobile phase concentration $c$.

(linear_model)=
### Linear model

In the simplest model, the loading $q$ is directly proportional to the concentration $c$ in the mobile phase where the equilibrium constant $a$, sometimes also referred to as Henry coefficient, represents the strength of the interaction:

```{math}
:label: linear_equilibrium

q = a \cdot c
```

This linear model assumes that there is an excess of adsorption sites and that the adsorbed molecules do not interact with each other {cite}`SchmidtTraub2020`.
Consequently, this model is typically only valid for low concentrations and surface coverages.
In addition, it assumes instant equilibrium between both phases.
However, in many cases, the kinetics of adsorption and desorption need to be considered.
To describe the dynamics of adsorption and desorption, the following dynamic formulation can be used:

```{math}
:label: linear_kinetic

\frac{\mathrm{d} q}{\mathrm{d} t} = k_a \cdot c - k_d \cdot q,
```

where $k_a$ is the adsorption and $k_d$ the desorption rate constant.
In the limit of very fast rates, this approach reduces to the equilibrium formulation (eq. {eq}`linear_equilibrium`) and the ratio of adsorption and desorption rate becomes the equilibrium constant $a$:

```{math}
:label: linear_kinetic_limit

a = \frac{k_a}{k_d}.
```

(langmuir_model)=
### Langmuir Model

As the concentration in the liquid phase increases, leading to higher loading, the surface of the stationary phase can reach a point of saturation, where it can no longer take up additional molecules.
The Langmuir isotherm model describes this saturation by assuming the formation of a monomolecular layer on the solid surface.
Once the surface is fully covered, no further adsorption occurs.
This can be quantified by the following equation:

```{math}
:label: langmuir_single_equilibrium

q = q_{max} \frac{b \cdot c}{1 + b \cdot c},
```

where $q_{max}$ is the saturation capacity of the resin.

For low concentrations, the Langmuir isotherm reduces to a linear model {cite}`SchmidtTraub2020`:

```{math}
\lim_{c \to 0} q = q_{max} \cdot b \cdot c = a \cdot c.
```

The binding models described previously have considered only the adsorption of a single substance.
However, chromatography is mainly concerned with the adsorption of mixtures of substances.
Therefore, not only competing effects between the molecules of one component but also the competition between molecules of different species must be accounted for:

```{math}
:label: langmuir_multi_equilibrium

q_i = q_{max, i} \frac{b_i \cdot c_i}{1 + \sum_{j}^{n_{comp}} b_j \cdot c_j}.
```

Again, the model can also be reformulated in a kinetic form:

```{math}
:label: langmuir_multi_kinetic

\frac{\mathrm{d} q_i}{\mathrm{d} t} = k_{a, i} \cdot c_{i} \cdot q_{max, i} \left( 1 - \sum_{j=1}^{n_{comp}} \frac{q_j}{q_{max, j}} \right) - k_{d, i} \cdot q_i.
```

(ldf)=
### Digression: linear driving force models

The linear driving force (LDF) approximation is sometimes used as an alternative to the native kinetic form of an isotherm.

In the native approach, the rate of change of the amount of solute adsorbed, $\frac{dq}{dt}$, is an explicit function of the solute concentration $c$ and the amount adsorbed ($q$); for example, in the Langmuir model, $\frac{dq}{dt} = k_a \cdot c (q_{max} - q) - k_d \cdot q$.
In the LDF approximation, the equilibrium concentration $q^*$ is used to calculate the rate of change of the amount of solute adsorbed for a given $c$.
For example, in the Langmuir model, $q^* = \frac{q_m k_{eq} c}{1 + k_{eq} c}$, where $k_{eq} = k_a / k_d$.
The rate of change of the amount of solute adsorbed is then proportional to the difference between the actual amount of solute adsorbed and the amount that would be adsorbed at equilibrium, i.e., $\frac{dq}{dt} = k_{kin}(q^*-q)$.
It is worth noting that the sign of $\frac{dq}{dt}$ causes the resulting flux to act towards equilibrium.
In this approach, the original rate constants $k_a$ and $k_d$ are replaced by the equilibrium constant $k_{eq}$ and a new kinetic constant $k_{kin}$.

Note that not all isotherms have a native representation in terms of explicit functions of solute concentration and amount adsorbed.
For example, the Freundlich model does not follow this form {cite}`Herzog1909`.
In such cases, only LDF approximations exist.
Similarly, LDF versions are not available for all binding models.

### Bi-Langmuir

Another extension of the Langmuir isotherm is the Bi-Langmuir isotherm.
Here, interactions at different centers of the stationary phase are considered without allowing an exchange between the different binding sites $q_{i, j}$ and $q_{i, k}$ $\left( k \neq j \right)$.
Therefore, there are no competitive effects between the different sites.
Originally, the Bi-Langmuir model is limited to two different binding site types but the model can be extended to arbitrary many binding site types {cite}`SchmidtTraub2020`.

```{math}
:label: bi-langmuir_kinetic

\frac{\mathrm{d} q_{i, j}}{\mathrm{d} t} =  k_{a, i}^{(j)} \cdot c_{i} \cdot q_{max, i}^{(j)} \left( 1 - \sum_{k=1}^{n_{comp}} \frac{q_{k, j}}{q_{max, k}^{(j)}}\right) - k_{d, i}^{(j)} q_{i, j}
```

### Steric mass action law

In case of ion exchange chromatography, the adsorption of ionic species is not based on physisorption but on chemisorption which usually involves much stronger interaction forces.
To model this, a stationary phase is considered that carries functional groups that are always loaded with ions {cite}`SchmidtTraub2020`.
These ions can be displaced stoichiometrically by other ions in solution.
For example, in case of a monoprotic-monoprotic cation exchange, cations $A^+$ can exchange place with bound salt cations $S^+$.

```{math}
:label: cation_exchange

\ce{A^+ + R^-S^+ <=>  S^+ + R^-A^+}.
```

Analogously, for an anion exchange resin, negative ions are exchanged:

```{math}
:label: anion_exchange

\ce{A^- + R^+S^- <=>  S^- + R^+A^-}.
```

A characteristic charge $\nu$ is introduced that accounts for the number of binding sites occupied by the molecule.
By convention, the component index for the salt is $i = 0$.
The equilibrium with respect to a reference component $S$ is given by

```{math}
:label: sma_selectivity

K_{i, 0} = \left( \frac{q_i}{c_i} \right)^{\nu_i} \left( \frac{c_0}{q_0} \right)^{\nu_0} \quad i = 1, \dots, N_{comp} - 1,
```

where $c_0$ and $q_0$ denote the reference component concentrations in the liquid and solid phase of the beads, respectively.
Usually, the reference component is a simple ionic component.
However, in general any molecule can be used as a reference.

Due to the larger interaction strength, electroneutrality needs to be considered to determine the concentration of the bound reference component.

```{math}
:label: sma_electroneutrality

q_0 = \Lambda - \sum_{j=1}^{N_{comp} - 1} \nu_j q_j,
```

where $\Lambda$ is the total ionic capacity of the resin.

Steric effects can also play an important role, especially for large molecules such as proteins.
Due to the their shape, some binding sites may be shielded from other molecules, which effectively reduces the number of free binding sites $\bar{q}_0$.

```{math}
:label: sma_selectivity_steric

K_{i, 0} = \left( \frac{q_i}{c_i} \right)^{\nu_i} \left( \frac{c_0}{\bar{q}_0} \right)^{\nu_0} \quad i = 1, \dots, N_{comp} - 1,
```

To account for this shielding, a steric shielding factor $\sigma$ is introduced {cite}`Brooks1992`:

```{math}
:label: sma_free_sites

\bar{q}_0 = q_0 - \sum_{j=1}^{N_{comp} - 1} \sigma_j q_j = \Lambda - \sum_{j=1}^{N_{comp} - 1} \left( \nu_j + \sigma_j \right) q_j
```

Finally, the complete steric mass action law model (SMA) reads as follows:

```{math}
:label: sma_isotherm

\frac{\mathrm{d} q_i}{\mathrm{d} t} = k_{a, i} c_{i} \bar{q}_0^{\nu_i} - k_{d, i}\cdot q_i\cdot c_{0}^{\nu_i}
```

(reaction_models)=
## Reaction models

Similarly to the binding models, multiple reaction models exist.
For this work only the mass action law reaction is considered.

The mass action law is a fundamental principle in chemical kinetics that states that the speed of a chemical reaction is proportional to the product of the concentrations of its reactants.
The model is suitable for most reactions; however, it is important to note that the concentrations are directly used for calculating the fluxes.
Hence, the model only holds for dilute solutions under the assumption of a well-stirred reaction vessel.

The net flux for component $i$ is given by

```{math}
:label: mass_action

\begin{aligned}
 f_{\mathrm{react},i}\left(c\right) &= \sum_{j=0}^{N_{\mathrm{react}}-1} s_{i,j} \varphi_j\left(c\right), \\
 \varphi_j(c) &= k_{\mathrm{fwd},j} \prod_{\ell=0}^{N_{\mathrm{comp}}-1} \left(c_{\ell}\right)^{e_{\mathrm{fwd},\ell,j}} - k_{\mathrm{bwd},j} \prod_{\ell=0}^{N_{\mathrm{comp}}-1} \left(c_{\ell}\right)^{e_{\mathrm{bwd},\ell,j}},
\end{aligned}
```

where $s_{i,j}$ are the stoichiometric coefficients of component $i$ in reaction $j$, $\varphi_j(c)$ is the net flux of reaction $j$, and $k_{\mathrm{fwd},j}$ and $k_{\mathrm{bwd},j}$ are the rate constants.
The exponents $e_{\mathrm{fwd},\ell,j}$ and $e_{\mathrm{bwd},\ell,j}$ are usually derived by the order of the reaction, that is,

```{math}
\begin{aligned}
 e_{\mathrm{fwd},\ell,j} &= \max(0, -s_{\ell,j}), \\
 e_{\mathrm{bwd},\ell,j} &= \max(0, s_{\ell,j}).
\end{aligned}
```

(column_models)=
## Column models

During the chromatographic process, components are transported through the column via convection, and experience dispersion due to inhomogeneities in the packing and molecular diffusion.
The previously discussed equilibrium thermodynamics and adsorption kinetics also need to be included in the column model {cite}`Guiochon2006`.

Dynamic column models are typically based on the differential mass balances of a control element in the fluid mobile phase and the stationary phase {cite}`SchmidtTraub2020`.
To solve these equations, numerical integration of the partial differential equations (PDEs) is required, although some reduced models have analytical solutions (see {numref}`section %s<model_solution>`).

To simplify the modeling problem, various assumptions are typically made, which make it easier to develop and solve mathematical models for chromatographic processes.
These include the assumption of constant fluid density and viscosity, which implies that the properties of the fluid do not change as it passes through the column.
Moreover, the interstitial volume, fluid flow, and component distribution are assumed to be homogeneous over the column cross-section.
Hence, differences in these properties across the column are neglected, which simplifies the modeling process.
Additionally, it is often assumed that there is no convection inside the particles and that transport processes within the particles are entirely governed by diffusion.

(plug_flow_model)=
### Plug flow reactor

The plug flow reactor (PFR) is the simplest model used to describe the fluid dynamics in a column.
This model represents an empty tubular reactor where a mixture is introduced at one end and flows through the reactor as a plug with no mixing along the axial direction.
Although the PFR cannot be used to model a chromatographic process directly, it is a useful starting point for developing other column models.
The PFR model can also be used to model tubing in a system.

The mass transport in the mobile phase due to convection is a function of the volumetric flow rate $Q$ applied to the column inlet.

```{math}
:label: convection_pfr

\dot{m}_{conv, i} = Q \cdot c_i \quad \text{with} \quad Q = A \cdot u,
```

with interstitial velocity $u$, and cross-sectional area $A$.
The differential mass balance for component $i$ in the mobile phase is given by

```{math}
:label: mass_balance_pfr

\frac{\partial c_i}{\partial t} = - u \cdot \frac{\partial c_i}{\partial z}.
```

The initial conditions for the concentration and the loading specify their values at time $t = 0$.
For the column inlet and outlet, Danckwerts boundary conditions are often applied {cite}`Danckwerts1953`.

```{math}
:label: danckwerts_in_pfr

u \cdot c_{in,i}(t) = u \cdot c_i(t,0) \quad \forall t > 0,
```

```{math}
:label: danckwerts_out_pfr
\frac{\partial c_i}{\partial z}(t, L) = 0 \quad \forall t > 0,
```

Due to non-idealities, axial dispersion plays a significant role in the overall fluid dynamics of real systems.
This dispersion is the result of various factors, including uneven fluid distribution, wall effects, and molecular diffusion.
To account for this effect, axial dispersion can be incorporated in the model equations.
The phenomenon can be described in analogy to Fick's laws of diffusion {cite}`SchmidtTraub2020`:

```{math}
:label: axial_dispersion

\frac{\partial c_i}{\partial t} = D_{ax,i} \cdot \frac{\partial^2 c_i}{\partial z^2}
```

The axial dispersion coefficient $D_{ax,i}$ accounts for the deviations from ideal plug flow due to the quality of the column packing.
Inclusion of axial dispersion modifies the mass balance equation in a PFR model, and is described by

```{math}
:label: mass_balance_dpfr

\frac{\partial c_i}{\partial t} = -u \cdot \frac{\partial c_i}{\partial z} + D_{ax,i} \frac{\partial^2 c_i}{\partial z^2},
```

with the following boundary conditions:

```{math}
:label: danckwerts_in_dpfr

u \cdot c_{in,i}(t) = u \cdot c_i(t,0) - D_{ax,i} \frac{\partial c_i}{\partial z}(t, 0) \quad \forall t > 0.
```

This model is commonly known as dispersive plug flow reactor (DPFR).

To account for chemical reactions in the (D)PFR, an additional term reflecting the reaction kinetics must be considered in the mass balance equation (see {numref}`reaction_models`):

```{math}
:label: mass_balance_dpfr_reaction

\frac{\partial c_i}{\partial t} = -u \cdot \frac{\partial c_i}{\partial z} + D_{ax,i} \frac{\partial^2 c_i}{\partial t^2} + f_{reac}(c).
```

(lumped_rate_model_without_pores)=
### Equilibrium model

To model a chromatographic column, it is necessary to consider the stationary phase, which typically consists of a packed bed made of porous spherical particles.
The particles in the bed effectively reduce the cross-sectional area of the column in which convection occurs.

```{math}
:label: convection_em

\dot{m}_{conv, i} = Q \cdot c_i \quad \text{with} \quad Q = \varepsilon \cdot A \cdot u ,
```

where $\varepsilon$ denotes the total porosity of the packed bed.

Solutes can diffuse from the interstitial volume between the particles into the particle pores, where they can undergo additional intraparticle diffusion before adsorbing onto the particle surfaces.
The differing interactions of these molecules with the surface ultimately lead to the separation of the molecules.

The simplest chromatography model is the equilibrium model (EM), which assumes no mass transfer limitation into the pore and fast transport and diffusion inside the pores.
Consequently, liquid phase concentrations within particle pores are identical to those in the bulk liquid phase, and the concentrations of the liquid and solid phases within the adsorbent particles are constant and independent of radial position of the particle.

To model the adsorption process, rapid equilibrium between the mobile phase and the stationary phase is assumed.
The differential mass balance equation for component $i$ is given by

```{math}
:label: mass_balance_em

\frac{\partial c_i}{\partial t} + F \cdot \frac{\partial q_i}{\partial t} = -u \cdot \frac{\partial c_i}{\partial z},
```

where $q_i$ is the solid phase concentration of component $i$, and $F = \left( 1 - \varepsilon \right) / \varepsilon$ is the phase ratio.
The solid phase concentration $q$ is related to the mobile phase concentration through the adsorption isotherm (see {numref}`isotherm_models`), with

```{math}
0 = f_{ads} \left( c, q \right).
```

### Lumped rate model without pores

While the rather ideal equilibrium model provides a powerful tool to understand important phenomena that take place during chromatographic separations, peak broadening effects and mass transfer limitations often play a significant role in in real systems.
These effects are particularly important to consider for large molecules, such as proteins, since their molecular diffusion rates are inversely related to their size {cite}`Guiochon2006`.
Thus, larger molecules tend to diffuse much more slowly than smaller ones.
In lumped rate models, these effects are "lumped" into one or more kinetic parameters.

To account for peak broadening effects, axial dispersion can be considered, analogous to the PFR.
This leads to a formulation commonly known as the equilibrium-dispersive model (EDM):

```{math}
:label: mass_balance_edm

\frac{\partial c_i}{\partial t} + F \cdot \frac{\partial q_i}{\partial t} = -u \cdot \frac{\partial c_i}{\partial z} + D_{ax,i} \frac{\partial^2 c_i}{\partial z^2}
```

Conversely, the Thomas model considers finite adsorption rates as discussed in {numref}`isotherm_models`, but does not take dispersion into account {cite}`Thomas1944`:

```{math}
:label: mass_balance_thomas

\frac{\partial c_i}{\partial t} + F \cdot \frac{\partial q_i}{\partial t} = -u \cdot \frac{\partial c_i}{\partial z} ,
```

with

```{math}
\frac{\partial q_i}{\partial t} = f_{ads}\left( c, q \right) .
```

These models are sometimes also referred to as transport models.

In this work, to simplify the naming of models and create a unified framework, the term "lumped rate model without pores" (LRM) is used for this family of models.
This allows for an independent specification of dispersion and adsorption dynamics.
For example, the equilibrium model corresponds to the LRM with $D_{ax} = 0$ and rapid equilibrium.
The transport-dispersive model corresponds to the LRM with dynamic binding and $D_{ax} \gt 0$.

Furthermore, as with the PFR, reactions can also be considered for the LRM.
In this case, the solid phase needs to be accounted for as well:

```{math}
:label: mass_balance_lrm_reaction

\frac{\partial c_i}{\partial t} + F \cdot \frac{\partial q}{\partial t} = -u \cdot \frac{\partial c_i}{\partial z} + D_{ax, i} \frac{\partial^2 c_i}{\partial z^2} + f_{reac}(c, q) + F \cdot f_{reac, s}(c, q)
```

### Lumped rate model with pores

To account for further transport limiting effects, the volume of the particle pores can be considered by introducing a particle porosity, $\varepsilon_p$.
This creates a separate reference volume inside the particles where concentration can differ from the bulk phase, where convection occurs.
$\varepsilon_c$ now represents the void between the particles of the packed bed and the total porosity, $\varepsilon_t$, is given by:

```{math}
:label: total_porosity

\varepsilon_t = \varepsilon_c + \left( 1 - \varepsilon_c \right) \varepsilon_p
```

The particles of the stationary phase are surrounded by a stagnant boundary layer.
The thickness of this film depends on the properties of the mobile phase and the flow rate at which the mobile phase passes through the column.
Generally, a thicker boundary layer results in slower mass transport and increased band broadening, while a thinner layer allows for quicker mass transport and better separation efficiency.
A film diffusion term accounts for transport through the stagnant film around the particles.
The flux depends on the specific surface area, $a_s$, of the particle in a finite volume element, given by:

```{math}
:label: specific_particle_surface

a_s = \frac{\mathrm{d} A}{\mathrm{d} V} = \frac{3}{r_p} \cdot (1 - \varepsilon_c),
```

where $r_p$ is the particle radius.
Consequently, the transport from the bulk phase (now denoted with superscript index $b$) to the pore phase ($c_i^p$) is given by

```{math}
\frac{\partial c^p_i}{\partial t} = F \cdot \frac{3}{\varepsilon_p r_p} \cdot k_{f,i} \left(c^b_i - c_i^p \right)
```

The mass balance for component $i$ is given by

```{math}
:label: mass_balance_lrmp

\frac{\partial c^b_i}{\partial t} = -u \cdot \frac{\partial c^b_i}{\partial z} + D_{ax,i} \frac{\partial^2 c^b_i}{\partial z^2} - F \cdot \frac{3}{r_p} \cdot k_{f,i} \left(c^b_i - c^p_i \right) + f_{reac}(c^b) , \\
\frac{\partial c^p_i}{\partial t} + \frac{1 - \varepsilon_p}{\varepsilon_p} \cdot \frac{\partial q}{\partial t} = \frac{3}{\varepsilon_p r_p} \cdot k_{f,i} \left(c^b_i - c^p_i \right) + f^p_{reac}(c^p, q) + \frac{1 - \varepsilon_p}{\varepsilon_p} f^s_{reac}(c^p, q) .
```

with:

```{math}
:label: adsorption_dynamics

\begin{aligned}
    \text{quasi-stationary: } \quad 0 &= f_{ads} \left( c^p, q \right), \\
    \text{dynamic: } \quad \frac{\partial q_i}{\partial t} &= f_{ads} \left( c^p, q \right) + f^s_{reac}(c^p, q) .
\end{aligned}
```

This model is known as lumped rate model with pores.

### High definition models

The general rate model (GRM) is often regarded as the most comprehensive chromatography model.
It takes into account both intraparticle and surface diffusion.
Although this model is not utilized in this work, readers can refer to {cite:t}`Guiochon2006,SchmidtTraub2020` for a complete description.
However, it is important to note that there are even more sophisticated models than the GRM.

For instance, {cite:t}`Leweke2018` consider various particle geometries, polydisperse particle properties (e.g., particle size or binding model), and pore accessibility factors.
To accurately understand and optimize chromatography processes, 2D column models have also been proposed which enable modeling of radial changes in column properties such as porosity, velocity, or dispersion coefficients {cite}`Puettmann2014,Qamar2017`.
Moreover, 3D models provide valuable insight into the flow, transport, and adsorption processes.
They can be used to quantify the effects of geometrical inhomogeneities on column performance.
This approach allows for the incorporation of more complex geometries and provides higher accuracy in the simulation of column performance {cite}`Rao2023`.

The data obtained from these simulations can also be used as a source of ground truth to identify and calibrate appropriate reduced-order models.
The use of high definition models is therefor particularly relevant when parameters cannot be directly measured, such as dispersion coefficients.
Instead, these parameters can be determined by analyzing the simulation data.
The reduced-order models can then be applied to optimize process design and achieve computational efficiency, which is not feasible with fully spatially resolved simulations.
