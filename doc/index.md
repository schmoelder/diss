# A modular framework for modeling and optimizing chromatographic processes

% Create custom role for inserting raw latex
```{role} raw-latex(raw)
:format: latex
```

% Disable page numbers
{raw-latex}`\pagenumbering{gobble}`

% Epigraph
```{raw} latex
\clearpage
\epigraph{\itshape
  And what is good, Phaedrus, \\
  And what is not good---\\
  Need we ask anyone to tell us these things?
}{
  --- Robert M.~Pirsig, \\
  \textit{
    Zen and the Art of Motorcycle Maintenance: \\
    An Inquiry Into Values
  }
}
\clearpage
```

## Preface
All models are wrong, but some are useful.
As a modeling engineer, it is my job to find out what is important: to select an effective model for the problem at hand, test the software that runs it, and validate it against reality.
This work addresses all three: it presents models for chromatographic separation processes, the software to simulate them, and experimental validation against real data.

This is inherently a complex undertaking.
Models are, by definition, approximations, and the software that implements them may contain omissions or undiscovered errors; this work is no exception.
Yet even imperfect tools can be useful: the software developed here provides a practical framework to simulate, evaluate, and optimize the diverse physicochemical effects and operating conditions that govern chromatographic separations.

The early decision to modularize the codebase was the key to making this work possible.
Without clear separation of functionality and well-defined interfaces, developing, testing, and extending a system of this complexity would not have been feasible.
This modularity also enables incremental improvements, allowing issues or missing features to be addressed without disrupting other components.
Open-source principles, combined with adaptability to different standards, further strengthen this approach by promoting transparency and collaboration within the scientific community.
In fact, many of the strongest modules emerged from such joint efforts, and I am grateful to all who contributed their expertise and perspective.
Learning from the enthusiasm of others is an unmatched shortcut to understanding.

Looking ahead, I hope to continue developing this software.
However, knowing what is good enough is an Art in itself, and for now, this thesis represents the current state of my efforts.


{raw-latex}`\clearpage`

## Acknowledgements

There are many people I need to thank, but first and foremost, I want to express my deepest gratitude to my partner, Leila.
Her unconditional support and patience throughout this journey have been invaluable.
No one else had to endure my struggles as much, yet she was always there as a thoughtful listener.
Being outside my field of research, she also provided a great way to test my own understanding: if I could explain complicated issues clearly to her, I knew I had truly grasped them.
Beyond this, she has been a catalyst for my personal growth, helping me find what truly matters in life.

Moreover, I would like to thank Prof. Kaspereit for granting me the freedom to explore research software engineering, a field completely new to me.
Coming from chemical engineering with little prior programming experience, it took longer than expected to understand the challenges and find my place within it, yet I was given the time I needed, and it was never doubted that I would eventually succeed.

My time in Erlangen would not have been the same without my wonderful colleagues and students, too many to name individually.
In particular, I want to highlight José Vargas and Benjamin Reif for their continued friendship, all the insightful discussions and support, as well as all the fun and memorable moments we shared.

When I started my contract in 2020 at Forschungszentrum Jülich, I was under the naive impression that my thesis was "almost finished."
Little did I know that, in fact, it was only about "half time."
Being surrounded by mathematicians and software engineers revealed both how much work remained and inspired me to push further than I could have imagined.
Once again, I was given the freedom to explore and proceed at my own pace.
One of the most rewarding experiences was contributing to the evolution of **CADET** from an academic code to software now used worldwide in both academia and industry.
I am deeply grateful to the entire **ModSim** group, especially Eric von Lieres, Hannah Lanzrath, and Jan Breuer, for their unwavering support.

Finally, I owe my sincere gratitude to Prof. Matthias Franzreb and Juliane Diehm from KIT.
In a time of need, they offered me scientific refuge and a desk free from distractions, allowing me to finally complete what I had started more than ten years ago.

{raw-latex}`\clearpage`

## Published work

Parts of this thesis were and are being published as in peer-reviewed journals, at conferences, in supervised students' theses and in the form of open source software packages.
Any thought, methodology, result, conclusion and direct or indirect contribution to this work is considered as properly cited by the following listing:

```{bibliography} ./references.bib
:list: bullet
:style: unsrt
:filter: false

Dienstbier2020
Schmoelder2020
Breuer2023
Leweke2025
Li2026
```

**Conference and symposium talks:**

```{bibliography} ./references.bib
:list: bullet
:style: unsrt
:filter: false

Schmoelder2016
Schmoelder2017
Schmoelder2018Talk
Schmoelder2019
Schmoelder2021
Hassan2022
Breuer2024
```

**Conference posters:**

```{bibliography} ./references.bib
:list: bullet
:style: unsrt
:filter: false

Schmoelder2018Poster
Schmoelder2020ProcessNet
Schmoelder2022
Li2024
Schmoelder2024
```

{raw-latex}`\clearpage`

**Code repositories and software packages**:
- **CADET-Process:** [https://github.com/fau-advanced-separations/CADET-Process](https://github.com/fau-advanced-separations/CADET-Process)
- **CADET-Core:** [https://github.com/cadet/CADET-Core](https://github.com/cadet/CADET-Core)
- **CADET-Python:** [https://github.com/cadet/CADET-Python](https://github.com/cadet/CADET-Python)
- **CADET-RDM:** [https://github.com/cadet/CADET-RDM](https://github.com/cadet/CADET-RDM)

**Datasets**:
- This thesis: [https://github.com/schmoelder/diss](https://github.com/schmoelder/diss)
- Model of a typical chromatographic laboratory system: [https://github.com/schmoelder/diss_parameter_estimation](https://github.com/schmoelder/diss_parameter_estimation)
- Optimization of advanced operating concepts: [https://github.com/schmoelder/diss_operating_modes](https://github.com/schmoelder/diss_operating_modes)

**Supervised and co-supervised student projects**:

```{bibliography} ./references.bib
:list: bullet
:style: unsrt
:filter: false

Ullrich2017
Wolf2017
Popp2017
Derleth2017
Schlumberger2018
Cortelezzi2018
Dienstbier2019
Tauber2019
Breuer2022
Thiel2023
Christiansen2022
Klauß2024a
Klauß2024b
Hülsmann2025
```

{raw-latex}`\clearpage`

## Zusammenfassung

Chromatographie ist ein weit verbreitetes Trennverfahren in der chemischen, pharmazeutischen und biotechnologischen Industrie.
Die rigorose, modellbasierte Auslegung und Optimierung chromatographischer Prozesse ist jedoch anspruchsvoll: Nichtlineare Dynamik, periodischer Betrieb und eine große Anzahl an Freiheitsgraden erschweren die Prozessentwicklung.
Gleichzeitig führt die Vielfalt der Betriebskonzepte, von Batch-Elution-Chromatographie bis hin zu kontinuierlichen Mehrsäulenprozessen, dazu, dass bestehende Werkzeuge entweder stark prozessspezifisch oder zu generisch sind, um ohne umfangreiche benutzerdefinierte Anpassungen eingesetzt werden zu können.

Diese Arbeit präsentiert ein modulares Framework zur Modellierung und Optimierung chromatographischer Prozesse, implementiert als Open-Source-Softwarepaket **CADET-Process**.
Das Framework trennt Prozesskonfiguration, Simulation, Auswertung und Optimierung in unabhängige Module.
Es stellt eine flexible Schnittstelle zur Definition komplexer Betriebskonzepte bereit, einschließlich Recyclingkonfigurationen und Mehrsäulenanordnungen, und ermöglicht die Formulierung von Prozessoptimierungsproblemen anhand entsprechender Leistungskennzahlen mit minimalem zusätzlichen Implementierungsaufwand.
Die Entwicklung folgt etablierten Prinzipien des wissenschaftlichen Software-Engineerings und zielt auf Zuverlässigkeit, Reproduzierbarkeit und langfristige Wartbarkeit ab.
Das Framework ist Teil der **CADET**-Softwarefamilie und sowohl im akademischen als auch im industriellen Umfeld etabliert.

Die Validierung erfolgt anhand experimenteller Daten in einer Parameterschätzstudie an einem Ionenaustauschchromatographiesystem im Labormaßstab.
Dabei werden eine sterische Massenwirkungsgesetz-Isotherme, Säulentransportphänomene sowie Systemperipherieeffekte, einschließlich Leitungen und Ventilen, schrittweise charakterisiert und in das Modell integriert.

Eine zusätzliche Serie synthetischer Fallstudien demonstriert die Optimierungsmöglichkeiten des Frameworks für verschiedene Betriebskonzepte, darunter Batch-Elution, Closed-Loop- und stationäres Recycling, Flip-Flop-Chromatographie sowie Säulenschaltungen in Reihe.
Die Simulationsergebnisse werden gegen analytische Lösungen der Gleichgewichtstheorie validiert.
Die Mehrzieloptimierung identifiziert dabei nicht-intuitive Betriebsstrategien, einschließlich Serieninjektionen, intermediärer Abfallfraktionen und Peakverschachtelung unter überladenen Bedingungen.
Ein bemerkenswertes Ergebnis ist, dass sich die Batch-Elution als produktivitätsoptimaler Grenzfall komplexerer Recyclingkonfigurationen ergibt.
Dieses Resultat wurde nicht *a priori* vorgegeben, sondern ergibt sich natürlich aus der Struktur der Entscheidungsvariablen, und unterstreicht das Potenzial des Frameworks für die Superstrukturoptimierung, bei der das Betriebskonzept selbst als Entwurfsvariable behandelt wird.

Durch diese Entwicklungen etabliert sich CADET-Process als umfassendes Open-Source-Framework zur Auslegung und Optimierung chromatographischer Prozesse, das der wissenschaftlichen Gemeinschaft frei zur Verfügung steht und sowohl akademische Forschung als auch industrielle Anwendungen unterstützt.

{raw-latex}`\clearpage`

## Abstract

Chromatography is a widely used separation technique in the chemical, pharmaceutical, and biotechnology industries.
However, rigorous model-based design and optimization of chromatographic processes remain challenging: nonlinear dynamics, periodic operation, and a large number of degrees of freedom complicate process development.
At the same time, the diversity of operating concepts, ranging from batch elution chromatography to continuous multi-column processes, leads to existing tools being either highly process-specific or too generic to be applied without extensive user-defined adaptations.

This work presents a modular framework for the modeling and optimization of chromatographic processes, implemented as the open-source software package **CADET-Process**.
The framework separates process configuration, simulation, evaluation, and optimization into clearly defined modules.
It provides a flexible interface for defining complex operating concepts, including recycling configurations and multi-column arrangements, and enables the formulation of process optimization problems based on appropriate performance metrics with minimal additional implementation effort.
The development follows established principles of scientific software engineering and aims to ensure reliability, reproducibility, and long-term maintainability.
The framework is part of the **CADET** software family and is used in both academic and industrial contexts.

The framework is validated using experimental data in a parameter estimation study on a laboratory-scale ion-exchange chromatography system.
A steric mass action law isotherm, column transport phenomena, and system peripheral effects, including tubing and valves, are progressively characterized and incorporated into the model.

An additional series of synthetic case studies demonstrates the optimization capabilities of the framework for various operating concepts, including batch elution, closed-loop and steady-state recycling, flip-flop chromatography, and column trains.
Simulation results are validated against analytical solutions from equilibrium theory.
Multi-objective optimization reveals non-intuitive operating strategies, including serial injections, intermediate waste fractions, and peak interlocking under overloaded conditions.
A notable finding is that batch elution emerges as the productivity-optimal limiting case of more complex recycling configurations.
This result was not imposed *a priori* but arose naturally from the structure of the decision variables, highlighting the potential of the framework for superstructure optimization, in which the operating concept itself is treated as a design variable.

Overall, CADET-Process establishes itself as a comprehensive open-source framework for the design and optimization of chromatographic processes, freely available to the scientific community and supporting both academic research and industrial applications.

{raw-latex}`\clearpage`

% ToC

```{raw} latex
\pagenumbering{roman}
\tableofcontents
```

{raw-latex}`\clearpage`
{raw-latex}`\section*{Abbreviations}`
{raw-latex}`\phantomsection\addcontentsline{toc}{chapter}{Abbreviations}`

```{glossary}
API
    Application programming interface

BDF
    Backward differentiation formula

CC
    Creative Commons

CG
    Continuous Galerkin method

CI/CD
    Continuous integration/Continuous deployment

CLR
    Closed-loop recycling

COBYLA
    Constrained optimization by linear approximation algorithm

COP
    Constrained optimization problem

CSTR
    Continuous stirred tank reactor model

CV
    Column volume

DAE
    Differential-algebraic equation

DBTL
    Design, build, test, learn cycle

DG
    Discontinuous Galerkin method

DoE
    Design of experiments

DOF
    Degrees of freedom

DRY
    Don't repeat yourself

EDM
    Equilibrium-dispersive model

EM
    Equilibrium model

ET
    Equilibrium theory

EULA
    End-user license agreement

FAIR
    Findable, Accessible, Interoperable, Reusable

FDM
    Finite difference method

FEM
    Finite elements method

FIRST
    Fast, independent, repeatable, self-validating, timely

FOSS
    Free and open-source

FVM
    Finite volume method

GA
    Genetic algorithm

GC
    Gas chromatography

GPL
    GNU General Public License

GRM
    General rate model

ILP
    Integer linear programming

KISS
    Keep it simple, stupid

KPI
    Key performance indicator

LC
    Liquid chromatography

LDF
    Linear driving force

LFS
    Large file storage

LP
    Linear programming

LRM
    Lumped rate model without pores

LRMP
    Lumped rate model with pores

MCMC
    Markov Chain Monte Carlo

MIP
    Mixed-integer linear programming

MINLP
    Mixed-integer nonlinear programming

ML
    Machine learning

MOO
    Multi-objective optimization

MR-SSR
    Mixed-recycle steady-state recycling

NLP
    Nonlinear programming

NRMSE
    Normalized root mean square error

NSGA-II/III
    Nondominated-sorting genetic algorithms (II/III)

ODE
    Ordinary differential equation

OOP
    Object-oriented programming

P&ID
    Process and instrumentation diagram

PD(A)E
    Partial differential (algebraic) equation

PEP
    Python Enhancement Proposal

(D)PFR
    (Dispersive) Plug flow reactor

PR
    Pull request

PyPI
    Python Package Index

QP
    Quadratic programming

RDM
    Research data management

RK
    Runge-Kutta

RSE
    Research software engineering

SFC
    Supercritical fluid chromatography

SMA
    Steric mass action law

SMB
    Simulated moving bed

SOO
    Single-objective optimization

SSE
    Sum squared errors

SUPG
    Streamline-upwind Petrov-Galerkin stabilization

TB
    True moving bed

TDD
    Test-driven development

TDM
    Transport-dispersive model

TRIPS
    Trade-Related Aspects of Intellectual Property Rights

UML
    Unified Modeling Language

VCS
    Version control system

WENO
    Weighted essentially non-oscillatory
```

{raw-latex}`\clearpage`
{raw-latex}`\section*{List of Symbols}`
{raw-latex}`\phantomsection\addcontentsline{toc}{chapter}{List of Symbols}`
```{raw} latex
\let\origthetable\thetable
\let\origtablename\tablename
\renewcommand{\thetable}{}
\renewcommand{\tablename}{}
\makeatletter
\@ifundefined{tablecontinued}{}{%
  \let\origTableContinued\tablecontinued
  \renewcommand{\tablecontinued}[1]{continued from previous page}}
\makeatother
```

**Symbols**

| Symbol                             | Description                                                 | Unit                                           |
| :--------------------------------- | :---------------------------------------------------------- | :--------------------------------------------- |
| $a$                                | Henry coefficient                                           |                                                |
| $a_s$                              | Specific particle surface area                              | $\text{m}^{-1}$                                |
| $A^p$                              | Particle surface area                                       | $\text{m}^{2}$                                 |
| $A_c$                              | Column cross-sectional area                                 | $\text{m}^{2}$                                 |
| $b$                                | Langmuir adsorption equilibrium constant                    | $\text{m}^{3}\,\text{mol}^{-1}$                |
| $c$                                | Molar concentration                                         | $\text{mol}\,\text{m}^{-3}$                    |
| $c^l$                              | Liquid phase concentration (local to stationary phase)      | $\text{mol}\,\text{m}^{-3}$                    |
| $c^s$                              | Stationary phase concentration                              | $\text{mol}\,\text{m}^{-3}$                    |
| $c^s_{\text{max}}$                 | Maximum stationary phase capacity                           | $\text{mol}\,\text{m}^{-3}$                    |
| $\bar{c}^s_0$                      | Free counter-ion sites (SMA)                                | $\text{mol}\,\text{m}^{-3}$                    |
| $C_{i,\text{ads}}$                 | Adsorbent cost for component $i$                            | $\text{€}\,\text{mol}^{-1}$                    |
| $C_{i,\text{eluent}}$              | Eluent cost for component $i$                               | $\text{€}\,\text{mol}^{-1}$                    |
| $C_{i,\text{feed}}$                | Feed cost for component $i$                                 | $\text{€}\,\text{mol}^{-1}$                    |
| $C_{i,\text{total}}$               | Total separation cost for component $i$                     | $\text{€}\,\text{mol}^{-1}$                    |
| $C_{\text{depreciation}}$          | Depreciation cost                                           | $\text{€}\,\text{mol}^{-1}$                    |
| $C_{\text{operating}}$             | Operating cost (overhead, wages, maintenance)               | $\text{€}\,\text{mol}^{-1}$                    |
| $D_{ax}$                           | Axial dispersion coefficient                                | $\text{m}^{2}\,\text{s}^{-1}$                  |
| $e_{\text{fwd}/\text{bwd},\ell,r}$ | Reaction order of component $\ell$ in reaction $r$          |                                                |
| $EC_i$                             | Specific eluent consumption for component $i$               | $\text{m}^{3}\,\text{mol}^{-1}$                |
| $F$                                | Phase ratio                                                 |                                                |
| $f_{\text{ads}}$                   | Adsorption isotherm function                                |                                                |
| $\mathcal{F}$                      | Numerical flux function (finite volume)                     |                                                |
| $f_{\text{react},i}$               | Reaction flux for component $i$                             | $\text{mol}\,\text{m}^{-3}\,\text{s}^{-1}$     |
| $k_a$                              | Adsorption rate constant                                    | $\text{m}^{3}\,\text{mol}^{-1}\,\text{s}^{-1}$ |
| $k_d$                              | Desorption rate constant                                    | $\text{s}^{-1}$                                |
| $k_f$                              | Film mass transfer coefficient                              | $\text{m}\,\text{s}^{-1}$                      |
| $K_{\text{eq}}$                    | Equilibrium constant                                        | $\text{m}^{3}\,\text{mol}^{-1}$                |
| $K_{i,0}$                          | Selectivity coefficient (SMA)                               |                                                |
| $L_c$                              | Column length                                               | $\text{m}$                                     |
| $n_i$                              | Amount of component $i$ collected                           | $\text{mol}$                                   |
| $n_{\text{feed},i}$                | Amount of component $i$ in the feed                         | $\text{mol}$                                   |
| $\dot{n}_{i,\text{annual}}$        | Annual production rate of component $i$                     | $\text{mol}\,\text{yr}^{-1}$                   |
| $N_{\text{chrom}}$                 | Number of chromatograms                                     |                                                |
| $N_{\text{comp}}$                  | Number of components                                        |                                                |
| $N_{\text{eluents}}$               | Number of eluent inlets                                     |                                                |
| $N_{\text{feeds}}$                 | Number of feed inlets                                       |                                                |
| $N_{\text{frac},k}^i$              | Number of fractions for component $i$ in chromatogram $k$   |                                                |
| $N_{\text{react}}$                 | Number of reactions                                         |                                                |
| $N_z$                              | Number of spatial grid cells                                |                                                |
| $p_{\text{ads/eluent/feed}}$       | Adsorbent / eluent / feed price                             | $\text{€}\,\text{m}^{-3}$                      |
| $PR_i$                             | Specific productivity of component $i$                      | $\text{mol}\,\text{m}^{-3}\,\text{s}^{-1}$     |
| $PU_i$                             | Product purity of component $i$                             | $\%$                                           |
| $Q$                                | Volumetric flow rate                                        | $\text{m}^{3}\,\text{s}^{-1}$                  |
| $r^p$                              | Particle radius                                             | $\text{m}$                                     |
| $s_{i,r}$                          | Stoichiometric coefficient of component $i$ in reaction $r$ |                                                |
| $t$                                | Time                                                        | $\text{s}$                                     |
| $t_{0,t}$                          | Column dead time                                            | $\text{s}$                                     |
| $t_{\text{R},i}$                   | Retention time of component $i$                             | $\text{s}$                                     |
| $t_{\text{start/end},f}$           | Start / end time of fraction $f$                            | $\text{s}$                                     |
| $u$                                | Interstitial mobile phase velocity                          | $\text{m}\,\text{s}^{-1}$                      |
| $V$                                | Volume                                                      | $\text{m}^{3}$                                 |
| $V^s$                              | Volume of stationary phase                                  | $\text{m}^{3}$                                 |
| $V_{\text{eluent}}$                | Eluent volume consumed per cycle                            | $\text{m}^{3}$                                 |
| $w$                                | Propagation velocity of a concentration front               | $\text{m}\,\text{s}^{-1}$                      |
| $x$                                | Vector of optimization variables                            |                                                |
| $\omega$                           | Weighting factor                                            |                                                |
| $Y_i$                              | Recovery yield of component $i$                             | $\%$                                           |
| $z$                                | Axial coordinate                                            | $\text{m}$                                     |
| $\Delta t_{\text{cycle}}$          | Cycle duration                                              | $\text{s}$                                     |
| $\Delta t_{\text{life}}$           | Adsorbent lifetime                                          | $\text{s}$                                     |
| $\Delta z$                         | Spatial grid spacing                                        | $\text{m}$                                     |
| $\varepsilon$                      | Porosity (superscript indicates phase)                      |                                                |
| $\varepsilon^t$                    | Total porosity                                              |                                                |
| $\varphi_r$                        | Net flux of reaction $r$                                    | $\text{mol}\,\text{m}^{-3}\,\text{s}^{-1}$     |
| $\Lambda$                          | Ionic capacity of the resin (SMA)                           | $\text{mol}\,\text{m}^{-3}$                    |
| $\nu$                              | Characteristic charge (SMA)                                 |                                                |
| $\sigma$                           | Steric shielding factor (SMA)                               |                                                |

{raw-latex}`\clearpage`

**Superscripts**

| Symbol      | Description                                              |
| :---------- | :------------------------------------------------------- |
| $(\cdot)^b$ | Bulk (interstitial) phase                                |
| $(\cdot)^l$ | Liquid phase (local to stationary phase: $c^b$ or $c^p$) |
| $(\cdot)^m$ | Binding site index                                       |
| $(\cdot)^p$ | Particle pore phase                                      |
| $(\cdot)^s$ | Stationary phase                                         |

**Subscripts**

| Symbol                                           | Description               |
| :----------------------------------------------- | :------------------------ |
| $(\cdot)_{\text{chrom}}$                         | Chromatogram              |
| $(\cdot)_{\text{comp}}$                          | Component                 |
| $(\cdot)_{\text{feed}}, (\cdot)_{\text{eluent}}$ | Feed, eluent inlets       |
| $(\cdot)_{f}$                                    | Fraction index            |
| $(\cdot)_{\text{frac}}$                          | Fraction                  |
| $(\cdot)_{i}, (\cdot)_{j}, (\cdot)_{\ell}$       | Component index           |
| $(\cdot)_{r}$                                    | Reaction index            |
| $(\cdot)_{\text{in}}, (\cdot)_{\text{out}}$      | Inlet, outlet             |
| $(\cdot)_{k}$                                    | Chromatogram index        |
| $(\cdot)_{n}$                                    | Spatial grid / cell index |
| $(\cdot)_{\text{react}}$                         | Reaction                  |


```{raw} latex
\let\thetable\origthetable
\let\tablename\origtablename
\makeatletter
\@ifundefined{origTableContinued}{}{%
  \let\tablecontinued\origTableContinued}
\makeatother
```
{raw-latex}`\clearpage`
{raw-latex}`\pagenumbering{arabic}`
