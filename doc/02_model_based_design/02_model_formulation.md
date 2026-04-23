(model_formulation)=
# Formulation of chromatographic process models

This chapter provides an overview of the formulation of chromatographic process models, highlighting various aspects of their modeling approaches.
It begins with models for retention mechanisms, followed by a description of the equations used to capture the phenomena occurring within the column and their coupling to adsorption isotherm models.
Moreover, the chapter considers effects that occur outside the column, in the system's periphery.

## Digression: machine learning models

In recent years, machine learning (ML) models have gained increasing popularity in the field of chromatography due to their ability to efficiently handle large datasets and accurately model complex systems {cite}`Subraveti2022`.
These models are predominantly data-driven, meaning they rely less on a physical understanding of the system and instead focus on approximating and interpolating measured outputs as functions of input variables.
Machine learning approaches are particularly valuable in scenarios where the underlying mechanisms are not fully understood or when direct measurement of necessary parameters is challenging.
In addition, ML models can be employed for surrogate modeling, providing simplified approximations of complex, computationally expensive models {cite}`Jaepel2022`.
The modular architecture of CADET-Process naturally supports replacing individual modules with data-driven models.
For example, the simulator could be replaced by a PINN, or surrogate models could be built to map optimization variables to KPIs.
This hybrid approach allows combining mechanistic and data-driven elements.
While machine learning offers powerful tools, mechanistic models remain essential, particularly in cases where they are used to inform or train machine learning models for chromatographic applications.
Understanding the design criteria and defining the overall structure of mechanistic models are critical steps in optimizing chromatographic processes.
As such, this work focuses exclusively on mechanistic models.

(isotherm_models)=
## Adsorption isotherm models

Adsorption isotherm models describe the accumulation of molecules on the surface of a stationary phase.
Typically, the loading concentration $q$ of a component is expressed as a function of its concentration $c$ in the mobile phase.
These models, often referred to as "binding models", provide the mathematical framework for understanding adsorption behavior.

(linear_model)=
### Linear model

The simplest binding model assumes that the loading concentration $q$ of a component is directly proportional to its concentration $c$ in the mobile phase.
This relationship is defined by an equilibrium constant $a$, sometimes referred to as the Henry coefficient, which represents the strength of interaction between the stationary phase and the component:

```{math}
:label: linear_equilibrium

q = a \cdot c
```

This linear model assumes an excess of adsorption sites and no interactions between the adsorbed molecules {cite}`SchmidtTraub2020`.
As a result, the model is typically valid only for low concentrations and surface coverages.
Additionally, it assumes that equilibrium between the stationary and mobile phases is instantaneous.
However, in many practical cases, the kinetics of adsorption and desorption must be considered.
To account for these dynamics, the following kinetic formulation can be applied:

```{math}
:label: linear_kinetic

\frac{\text{d} q}{\text{d} t} = k_a \cdot c - k_d \cdot q,
```

where $k_a$ is the adsorption rate constant and $k_d$ is the desorption rate constant.

In the limit of very fast adsorption and desorption rates, this dynamic approach reduces to the equilibrium formulation (eq. {eq}`linear_equilibrium`).
In this case, the equilibrium constant $a$ is defined as the ratio of the adsorption and desorption rates:

```{math}
:label: linear_kinetic_limit

a = \frac{k_a}{k_d}.
```

(langmuir_model)=
### Langmuir Model

At higher concentrations in the mobile phase, the stationary phase may reach saturation, where it can no longer accommodate additional molecules.
The Langmuir isotherm model accounts for this saturation by assuming that adsorption leads to the formation of a monomolecular layer on the stationary phase surface.
Once the surface is fully occupied, no further adsorption occurs.
This behavior is described by the following equation:

```{math}
:label: langmuir_single_equilibrium

q = q_{\text{max}} \frac{b \cdot c}{1 + b \cdot c},
```

where $q_{\text{max}}$ represents the saturation capacity of the stationary phase, and $b$ is the equilibrium constant for adsorption.

At low concentrations, the Langmuir isotherm simplifies to the linear model {cite}`SchmidtTraub2020`:

```{math}
\lim_{c \to 0} q = q_{\text{max}} \cdot b \cdot c = a \cdot c.
```

The binding models described above focus exclusively on the adsorption of a single substance.
However, chromatography is primarily concerned with the separation of mixtures of substances.
As a result, both the competitive effects among molecules of a single component and the interactions and competition between different species must be accounted for:

```{math}
:label: langmuir_multi_equilibrium

q_i = q_{\text{max}, i} \frac{b_i \cdot c_i}{1 + \sum_{j}^{N_{\text{comp}}} b_j \cdot c_j}.
```

Similarly, the model can be reformulated in a kinetic form:

```{math}
:label: langmuir_multi_kinetic

\frac{\text{d} q_i}{\text{d} t} = k_{a, i} \cdot c_{i} \cdot q_{\text{max}, i} \left( 1 - \sum_{j=1}^{N_{\text{comp}}} \frac{q_j}{q_{\text{max}, j}} \right) - k_{d, i} \cdot q_i.
```

(ldf)=
### Digression: linear driving force models

The linear driving force (LDF) approximation is sometimes used as an alternative to the native kinetic form of an isotherm {cite}`SchmidtTraub2020`.
In the native approach, the rate of change of the amount of solute adsorbed, $\frac{\text{d}q}{\text{d}t}$, is an explicit function of the solute concentration $c$ and the amount adsorbed $q$.
For example, in the Langmuir model:

```{math}
:label: langmuir_native

\frac{dq}{dt} = k_a \cdot c (q_{\text{max}} - q) - k_d \cdot q.
```

In the LDF approximation, the equilibrium concentration $q^*$ is used to calculate the rate of change of the amount of solute adsorbed for a given $c$.
For the Langmuir model, $q^*$ is defined as:

```{math}
:label: langmuir_ldf_q

q^* = \frac{q_{\text{max}} \cdot K_{\text{eq}} \cdot c}{1 + K_{\text{eq}} \cdot c},
```

where $K_{\text{eq}} = \frac{k_a}{k_d}$.

The rate of change of the amount of solute adsorbed is then expressed as:

```{math}
:label: langmuir_ldf_dq_dt

\frac{\text{d}q}{\text{d}t} = k_{\text{kin}} \cdot (q^* - q).
```

Here, the flux is proportional to the difference between the actual amount adsorbed and the equilibrium amount, $q^*$.
It is worth noting that the sign of $\frac{\text{d}q}{\text{d}t}$ ensures the flux acts toward equilibrium.
In this approximation, the original rate constants $k_a$ and $k_d$ are replaced by the equilibrium constant $K_{\text{eq}}$ and a new kinetic constant $k_{\text{kin}}$.
It is important to note that not all isotherms have a native representation in terms of explicit functions of solute concentration and amount adsorbed.
For example, the Freundlich model does not follow this form {cite}`Herzog1909`.
In such cases, only LDF approximations are available.
Similarly, not all binding models have corresponding LDF versions.


### Bi-Langmuir isotherm model

The Bi-Langmuir isotherm is a further extension of the Langmuir model, accounting for interactions at multiple binding sites on the stationary phase.
In this model, different binding sites $m$ are considered, but no exchange occurs between the sites.
As a result, there are no competitive effects between different binding sites.
The original Bi-Langmuir model is typically limited to two types of binding sites.
However, it can be extended to an arbitrary number of binding site types {cite}`SchmidtTraub2020`.
The kinetic formulation of the Bi-Langmuir isotherm is given by:

```{math}
:label: bi-langmuir_kinetic

\frac{\text{d} q_{i}^{m}}{\text{d} t} =  k_{a, i}^{m} \cdot c_{i} \cdot q_{\text{max}, i}^{m} \left( 1 - \sum_{j=1}^{N_{\text{comp}}} \frac{q_{j, m}}{q_{\text{max}, j}^{m}}\right) - k_{d, i}^{m} q_{i, m}
```

where $k_{a, i}^{m}$ and $k_{d, i}^{m}$ are the adsorption and desorption rate constants, and $q_{\text{max}, i}^{m}$ is the maximum loading capacity of the $m$-th binding site.


### Steric mass action law

In ion exchange chromatography, the adsorption of ionic species is not based on physisorption but rather on chemisorption, which typically involves much stronger interaction forces.
To model this process, the stationary phase is assumed to carry functional groups that are always loaded with ions {cite}`SchmidtTraub2020`.
These ions can be displaced stoichiometrically by other ions in solution.

For instance, in the case of a monoprotic-monoprotic cation exchange, cations $A^+$ can replace bound salt cations $S^+$:

```{math}
:label: cation_exchange

\ce{A^+ + R^-S^+ <=>  S^+ + R^-A^+}.
```

Similarly, for an anion exchange resin, negative ions are exchanged:

```{math}
:label: anion_exchange

\ce{A^- + R^+S^- <=>  S^- + R^+A^-}.
```

A characteristic charge $\nu$ is introduced to account for the number of binding sites occupied by the molecule.
By convention, the component index for the salt is defined as $i = 0$.

The equilibrium with respect to a reference component $S$ is expressed as:

```{math}
:label: sma_selectivity

K_{i, 0} = \left( \frac{q_i}{c_i} \right)^{\nu_i} \left( \frac{c_0}{q_0} \right)^{\nu_0} \quad i = 1, \dots, N_{\text{comp}} - 1,
```

where $c_0$ and $q_0$ denote the concentrations of the reference component in the liquid and solid phases of the beads, respectively.
The reference component is typically a simple ionic species, but in principle, any molecule can be chosen.
Due to the stronger interaction forces in chemisorption, electroneutrality must be considered to determine the concentration of the bound reference component:

```{math}
:label: sma_electroneutrality

q_0 = \Lambda - \sum_{j=1}^{N_{\text{comp}} - 1} \nu_j q_j,
```

where $\Lambda$ is the total ionic capacity of the resin.
Steric effects also play an important role, especially for large molecules like proteins.
Due to their shape, some binding sites may be shielded from other molecules, effectively reducing the number of free binding sites $\bar{q}_0$.

This can be accounted for by modifying the selectivity expression:

```{math}
:label: sma_selectivity_steric

K_{i, 0} = \left( \frac{q_i}{c_i} \right)^{\nu_i} \left( \frac{c_0}{\bar{q}_0} \right)^{\nu_0} \quad i = 1, \dots, N_{\text{comp}} - 1,
```

To model steric shielding, a steric shielding factor $\sigma$ is introduced {cite}`Brooks1992`:

```{math}
:label: sma_free_sites

\bar{q}_0 = q_0 - \sum_{j=1}^{N_{\text{comp}} - 1} \sigma_j q_j = \Lambda - \sum_{j=1}^{N_{\text{comp}} - 1} \left( \nu_j + \sigma_j \right) q_j
```

The complete Steric Mass Action (SMA) model, which incorporates both kinetics and equilibrium, is then given as:

```{math}
:label: sma_isotherm

\frac{\text{d} q_i}{\text{d} t} = k_{a, i} c_{i} \bar{q}_0^{\nu_i} - k_{d, i}\cdot q_i\cdot c_{0}^{\nu_i}
```

where $k_{a, i}$ and $k_{d, i}$ are the adsorption and desorption rate constants.


(reaction_models)=
## Reaction models

Similarly to binding models, multiple chemical reaction models exist.
In this work, only the mass action law reaction model is considered.

The mass action law is a fundamental principle in chemical reaction kinetics that states that the rate of a chemical reaction is proportional to the product of the concentrations of its reactants.
This model is suitable for most reactions, though it is important to note that the model uses the concentrations of reactants and products to directly calculate reaction fluxes.
As a result, the model assumes dilute solutions and a well-stirred reaction vessel to ensure homogeneity.
The net flux for component $i$ is expressed as:

```{math}
:label: mass_action

\begin{aligned}
 f_{\text{react},i}\left(c\right) &= \sum_{j=0}^{N_{\text{react}}-1} s_{i,j} \varphi_j\left(c\right), \\
 \varphi_j(c) &= k_{\text{fwd},j} \prod_{\ell=0}^{N_{\text{comp}}-1} \left(c_{\ell}\right)^{e_{\text{fwd},\ell,j}} - k_{\text{bwd},j} \prod_{\ell=0}^{N_{\text{comp}}-1} \left(c_{\ell}\right)^{e_{\text{bwd},\ell,j}},
\end{aligned}
```

Here, subscript $i$ denotes the component of interest, $j$ the reaction, and $\ell$ is a summation index over all components:

- $s_{i,j}$ are the stoichiometric coefficients of component $i$ in reaction $j$, which are negative for reactants and positive for products.
- $\varphi_j(c)$ is the net flux of reaction $j$.
- $k_{\text{fwd},j}$ and $k_{\text{bwd},j}$ are the forward and backward rate constants, respectively.
- $e_{\text{fwd},\ell,j}$ and $e_{\text{bwd},\ell,j}$ are the reaction orders for the forward and backward reactions, respectively.
The exponents $e_{\text{fwd},\ell,j}$ and $e_{\text{bwd},\ell,j}$ are derived from the stoichiometric coefficients using the following rules:

```{math}
:label: mal_exponents

\begin{aligned}
 e_{\text{fwd},\ell,j} &= \max(0, -s_{\ell,j}), \\
 e_{\text{bwd},\ell,j} &= \max(0, s_{\ell,j}).
\end{aligned}
```

(column_models)=
## Chromatographic column models

During the chromatographic process, components are transported through the column by convection and experience dispersion due to inhomogeneities in the packing and molecular diffusion.
The equilibrium thermodynamics, adsorption kinetics, and, where applicable, chemical reaction models, also need to be incorporated into the chromatographic column model {cite}`Guiochon2006`.

Dynamic column models are typically based on differential mass balances within a control volume of the fluid mobile phase and the stationary phase {cite}`SchmidtTraub2020`.
This results in a system of partial differential equations (PDEs), which are usually solved using numerical methods.
However, some simplified models allow for analytical solutions (see {numref}`model_solution`).

To simplify the modeling process, various assumptions are often made:

- The fluid density and viscosity are assumed to be constant, implying no significant changes in fluid properties as it flows through the column.
- The interstitial volume, fluid flow, and component distribution are assumed to be homogeneous across the column cross-section.
- Convection inside the particles is neglected, and transport within the particles is assumed to be governed solely by diffusion.

(plug_flow_model)=
### Plug flow reactor

The plug flow reactor (PFR) model is the simplest approach for describing fluid dynamics in a column.
In this model, the column is treated as an empty tubular reactor, where a mixture is introduced at one end and flows through the column as a "plug" without axial mixing.
Although the PFR model is not directly applicable to modeling chromatographic processes, it serves as a useful starting point for developing more detailed column models.
Moreover, the PFR model can be used to describe tubing in chromatographic systems, which is important for accurately modeling the non-idealities of real processes.

Mass transport in the mobile phase due to convection is governed by the volumetric flow rate $Q$ applied at the column inlet:

```{math}
:label: convection_pfr

\dot{m}_{conv, i} = Q \cdot c_i \quad \text{with} \quad Q = A_c \cdot u,
```

where $u$ is the mobile phase velocity, and $A_c$ is the column's cross-sectional area.

The differential mass balance for component $i$ in the mobile phase is given by

```{math}
:label: mass_balance_pfr

\frac{\partial c_i}{\partial t} = - u \cdot \frac{\partial c_i}{\partial z}.
```

where $z$ is the axial coordinate along the column.

The initial conditions for the concentration and the loading specify their values at time $t = 0$.
At the column inlet and outlet, Danckwerts boundary conditions are typically applied {cite}`Danckwerts1953`:

```{math}
:label: danckwerts_in_pfr

u \cdot c_{in,i}(t) = u \cdot c_i(t,0) \quad \forall t > 0,
```

```{math}
:label: danckwerts_out_pfr

\frac{\partial c_i}{\partial z}(t, L_c) = 0 \quad \forall t > 0,
```

Here, $c_{in,i}(t)$ is the inlet concentration of component $i$, and $L_c$ is the length of the column.

(dispersive_plug_flow_model)=
### Dispersive plug flow reactor

Due to non-idealities, axial dispersion often plays a significant role in the fluid dynamics of real chromatographic systems.
The dispersion is the result from several factors, such as uneven fluid distribution, wall effects, and molecular diffusion.
To account for this, axial dispersion can be incorporated into the model equations.
This phenomenon is described analogously to Fick's laws of diffusion {cite}`SchmidtTraub2020`:

```{math}
:label: axial_dispersion

\frac{\partial c_i}{\partial t} = D_{ax,i} \cdot \frac{\partial^2 c_i}{\partial z^2}
```

where $D_{ax,i}$ is the axial dispersion coefficient, which reflects the deviations from ideal plug flow due to column packing quality.
Incorporating axial dispersion modifies the mass balance equation of the PFR model, leading to the dispersive plug flow reactor (DPFR) model:

```{math}
:label: mass_balance_dpfr

\frac{\partial c_i}{\partial t} = -u \cdot \frac{\partial c_i}{\partial z} + D_{ax,i} \frac{\partial^2 c_i}{\partial z^2}.
```

The boundary conditions for this model are:

```{math}
:label: danckwerts_in_dpfr

u \cdot c_{in,i}(t) = u \cdot c_i(t,0) - D_{ax,i} \frac{\partial c_i}{\partial z}(t, 0) \quad \forall t > 0.
```

To account for chemical reactions within the (D)PFR, an additional term describing reaction kinetics is included in the mass balance equation (see {numref}`reaction_models`):

```{math}
:label: mass_balance_dpfr_reaction

\frac{\partial c_i}{\partial t} = -u \cdot \frac{\partial c_i}{\partial z} + D_{ax,i} \frac{\partial^2 c_i}{\partial t^2} + f_{react}(c),
```

where $f_{\text{react},i}(c)$ represents the reaction flux for component $i$.

(equilibrium_model)=
### Equilibrium model

To model a chromatographic column, it is necessary to consider the stationary phase, typically a packed bed of porous spherical particles.
The particles in the bed reduce the effective cross-sectional area available for convection in the column:

```{math}
:label: convection_em

\dot{m}_{conv, i} = Q \cdot c_i \quad \text{with} \quad Q = \varepsilon \cdot A \cdot u ,
```

where $\varepsilon$ is the total porosity of the packed bed, $u$ is the mobile phase velocity, and $A$ is the column's cross-sectional area.
Solutes can diffuse from the interstitial volume between particles into the pores of the particles, where intraparticle diffusion and adsorption onto particle surfaces occur.
The differing interactions of solutes with the stationary phase lead to their separation.

The simplest chromatographic model is the equilibrium model (EM), which assumes:

- No mass transfer limitations into the pores.
- Instantaneous transport and diffusion inside the pores.
- Rapid equilibrium between the mobile phase and the stationary phase.

Under these assumptions, the liquid phase concentration within the particle pores is identical to the bulk liquid phase concentration, and the concentration in the solid phase is uniform (i.e., independent of the radial position inside the particle).

The differential mass balance for component $i$ is expressed as:

```{math}
:label: mass_balance_em

\frac{\partial c_i}{\partial t} + F \cdot \frac{\partial q_i}{\partial t} = -u \cdot \frac{\partial c_i}{\partial z},
```

where:

- $c_i$ is the concentration of component $i$ in the mobile phase,
- $q_i$ is the concentration in the stationary phase, and
- $F = \frac{1 - \varepsilon}{\varepsilon}$ is the phase ratio.
The relationship between $c$ and $q$ is defined by the adsorption isotherm (see {numref}`isotherm_models`):

```{math}
:label: implicit_adsorption

0 = f_{\text{ads}} \left( c, q \right).
```

(lumped_rate_model_without_pores)=
### Lumped rate model without pores

While the idealized equilibrium model is a useful tool for understanding chromatographic phenomena, it does not account for peak broadening effects or mass transfer limitations, which are critical in real systems.
For instance, peak broadening may result from axial dispersion, diffusion, or slow adsorption kinetics.
These effects are especially important for large molecules like proteins, whose diffusion rates are much slower than those of smaller molecules {cite}`Guiochon2006`.

In lumped rate models, these non-idealities are accounted for by "lumping" them into one or more kinetic parameters.
To account for peak broadening effects, axial dispersion is included, leading to the equilibrium-dispersive model (EDM):

```{math}
:label: mass_balance_edm

\frac{\partial c_i}{\partial t} + F \cdot \frac{\partial q_i}{\partial t} = -u \cdot \frac{\partial c_i}{\partial z} + D_{ax,i} \frac{\partial^2 c_i}{\partial z^2}
```

Conversely, the Thomas model considers finite adsorption rates as discussed in {numref}`isotherm_models`, but neglects dispersion effects {cite}`Thomas1944`:

```{math}
:label: mass_balance_thomas

\frac{\partial c_i}{\partial t} + F \cdot \frac{\partial q_i}{\partial t} = -u \cdot \frac{\partial c_i}{\partial z} ,
```

with

```{math}
:label: dynamic_adsorption_thomas

\frac{\partial q_i}{\partial t} = f_{\text{ads}}\left( c, q \right) .
```

These models, collectively referred to as transport models, form the basis for describing chromatographic processes under non-ideal conditions.
To simplify model naming and establish a unified framework, consistent with the nomenclature of CADET, this family of models will be referred to as the lumped rate model without pores (LRM).
This framework allows for independent specification of dispersion and adsorption dynamics:

- The equilibrium model corresponds to the LRM with $D_{ax} = 0$ and rapid equilibrium.
- The transport-dispersive model (TDM) corresponds to the LRM with dynamic binding ($f_{\text{ads}}$) and $D_{ax} > 0$.


(lumped_rate_model_with_pores)=
### Lumped rate model with pores

To account for additional transport-limiting effects, the volume of the particle pores can be considered by introducing the particle porosity, $\varepsilon^p$.
This creates a separate reference volume within the particles where the solute concentration, $c_i^p$, can differ from the bulk liquid phase concentration, $c_i^b$, where convection occurs.
The interstitial porosity $\varepsilon^b$ represents the void volume between the particles in the packed bed.
The total porosity, $\varepsilon^t$, is given by:

```{math}
:label: total_porosity

\varepsilon^t = \varepsilon^b + \left( 1 - \varepsilon^b \right) \varepsilon^p
```

where the term $\left( 1 - \varepsilon^b \right) \varepsilon^p$ accounts for the volume of the pores inside the particles.

The stationary phase particles are surrounded by a stagnant boundary layer, whose thickness depends on the properties of the mobile phase and the flow rate.
A thicker boundary layer slows down mass transport and increases band broadening, while a thinner layer allows for faster mass transfer and improves separation efficiency.
To model this, a film diffusion term accounts for transport through the stagnant film around the particles.
The flux through this boundary layer depends on the specific surface area, $a_s$, of the particles in a finite volume element, which is expressed as:

```{math}
:label: specific_particle_surface

a_s = \frac{\text{d} A}{\text{d} V} = \frac{3}{r^p} \cdot (1 - \varepsilon^b),
```

where $r^p$ is the particle radius.
The transport from the bulk phase (denoted by the superscript $b$) to the pore phase (denoted by the superscript $p$) is then given by:

```{math}
:label: film_diffusion

\frac{\partial c^p_i}{\partial t} = F \cdot \frac{3}{\varepsilon^p r^p} \cdot k_{f,i} \left(c^b_i - c_i^p \right)
```

where $k_{f,i}$ is the film mass transfer coefficient.

The lumped rate model with pores (LRMP) combines these considerations into the following mass balance equations for component $i$ in the bulk phase and the pore phase:

```{math}
:label: mass_balance_lrmp

\frac{\partial c^b_i}{\partial t} = -u \cdot \frac{\partial c^b_i}{\partial z} + D_{ax,i} \frac{\partial^2 c^b_i}{\partial z^2} - F \cdot \frac{3}{r^p} \cdot k_{f,i} \left(c^b_i - c^p_i \right) + f_{\text{react}}(c^b) , \\
\frac{\partial c^p_i}{\partial t} + \frac{1 - \varepsilon^p}{\varepsilon^p} \cdot \frac{\partial q}{\partial t} = \frac{3}{\varepsilon^p r^p} \cdot k_{f,i} \left(c^b_i - c^p_i \right) + f^p_{\text{react}}(c^p, q) + \frac{1 - \varepsilon^p}{\varepsilon^p} f^s_{\text{react}}(c^p, q).
```

where:

- $f_{\text{react}}(c^b)$ represents reaction kinetics in the bulk phase,
- $f_{\text{react}}^p(c^p, q)$ represents reactions in the pore phase, and
- $f_{\text{react}}^s(c^p, q)$ represents reactions on the particle surface.
The adsorption process in this model can be described in either a quasi-stationary or dynamic form:

```{math}
:label: adsorption_dynamics

\begin{aligned}
    \text{quasi-stationary: } \quad 0 &= f_{\text{ads}} \left( c^p, q \right), \\
    \text{dynamic: } \quad \frac{\partial q_i}{\partial t} &= f_{\text{ads}} \left( c^p, q \right) + f^s_{\text{react}}(c^p, q).
\end{aligned}
```

Here:

- $f_{\text{ads}}(c^p, q)$ is the adsorption isotherm model equation (describing binding dynamics),
- $f_{\text{react}}^s(c^p, q)$ accounts for surface reactions on the stationary phase.

(hdr)=
### High definition models

The general rate model (GRM) is often regarded as the most comprehensive chromatography model.
It accounts for both intraparticle and surface diffusion.
Although the GRM is not utilized in this work, readers are encouraged to refer to {cite:t}`Guiochon2006` and {cite:t}`SchmidtTraub2020` for a detailed description.
It is worth noting that even more sophisticated models than the GRM exist.
For example, {cite:t}`Leweke2018` consider advanced features such as various particle geometries, polydisperse particle properties (e.g., particle size and adsorption isotherms), and pore accessibility factors.
To better understand and optimize chromatography processes, 2D column models have been proposed.
These models enable the simulation of radial variations in column properties, such as porosity, velocity, or dispersion coefficients {cite}`Puettmann2014,Qamar2017`.
Furthermore, 3D models provide deeper insights into flow, transport, and adsorption processes by capturing the effects of geometrical inhomogeneities on column performance.
These models allow the incorporation of more complex geometries and offer higher accuracy in simulating column performance {cite}`Rao2023`.

Data generated from high definition simulations can serve as a source of ground truth for identifying and calibrating reduced-order models.
This is particularly valuable when certain parameters, such as dispersion coefficients, cannot be directly measured.
Instead, these parameters can be inferred by analyzing simulation results.
Once calibrated, reduced-order models can then be derived to optimize process design and enhance computational efficiency.
This is especially important because fully spatially resolved simulations, while accurate, are computationally expensive and often impractical for routine optimization tasks.

(cstr)=
### Continuous stirred tank reactor model (CSTR)

In addition to chromatographic columns and (D)PFRs, the continuous stirred tank reactor model is another fundamental building block in unit operation networks, often used to model system void volume or holdup tanks.
Its mass balance is given by

```{math}
:label: mass_balance_cstr

\frac{\text{d}}{\text{d}t} (V c_i) = Q_{\text{in}} c_{\text{in},i} - Q_{\text{out}} c_i,
```

where $Q_{\text{in}}$ and $Q_{\text{out}}$ denote the inlet and outlet volumetric flow rates,

Note, in contrast to other unit operations, the volume of the CSTR can vary over time.
The change of the tank volume is given by

```{math}
:label: volume_balance_cstr

\frac{\text{d}V^{\ell}}{\text{d}t}= Q_{\text{in}} - Q_{\text{out}}.
