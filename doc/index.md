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
Yet even imperfect tools can be useful.
The software developed here provides useful tools to simulate the diverse physicochemical effects and operating conditions that govern chromatographic separations.

The early decision to modularize the framework's code was key: by separating functionality and defining clear interfaces, development, testing, and integration become more efficient. (todo: revisit "key")
This modularity also supports incremental improvement, allowing emerging issues or missing features to be addressed without disrupting other software components.

Open-source principles, combined with adaptability to different standards, further strengthen this approach by promoting transparency and collaboration within the scientific community.
In fact, many of the strongest modules emerged from such joint efforts, and I am grateful to all who contributed their expertise and perspective.
Much of this work was made easier by the willingness of others to go the *extra mile*, and their enthusiasm has been a constant source of motivation.

Looking ahead, I hope to continue developing this software.
However, knowing what is *good enough* is an Art in itself, and for now, this thesis represents the current state of my efforts.


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
Die rigorose modellbasierte Auslegung und Optimierung chromatographischer Prozesse ist jedoch anspruchsvoll: Die nichtlineare Dynamik, der periodische Betrieb und die große Anzahl an Freiheitsgraden erschweren die Prozessentwicklung.
Gleichzeitig führt die Vielfalt der Betriebskonzepte, von Batch-Elution Chromatographie bis hin zu kontinuierlichen Mehrkolonnenprozessen, dazu, dass bestehende Werkzeuge entweder auf spezifische Prozesse zugeschnitten oder zu allgemein gehalten sind, um ohne aufwändige benutzerdefinierte Konfiguration eingesetzt werden zu können.

Diese Arbeit stellt ein modulares Framework zur Modellierung und Optimierung chromatographischer Prozesse vor, das als Open-Source-Paket **CADET-Process** implementiert wurde.
Das Framework gliedert Prozesskonfiguration, Simulation, Leistungsbewertung und Optimierung in unabhängige Komponenten.
Es stellt eine flexible Schnittstelle zur Definition komplexer Betriebskonzepte bereit, darunter Ventilschaltpläne, Recyclingkonfigurationen und Mehrkolonnenanordnungen, und ermöglicht die Konfiguration und Lösung von Leistungskennzahlen und Optimierungsaufgaben ohne benutzerdefinierten Integrationsaufwand.
Das Framework wurde nach etablierten Prinzipien des wissenschaftlichen Software-Engineerings entwickelt, um Zuverlässigkeit, Reproduzierbarkeit und langfristige Wartbarkeit zu gewährleisten, und ist inzwischen sowohl im akademischen als auch im industriellen Umfeld als Teil des übergeordneten **CADET**-Ökosystems etabliert.

Das Framework wird anhand experimenteller Daten durch eine Studie zur Parameterschätzung an einem Protein-Reinigungssystem im Labormaßstab mittels Ionenaustauschchromatographie validiert.
Das sterische Massenwirkungsgesetz, Säulentransportphänomene sowie Systemperipherieeffekte einschließlich der Beiträge von Ventilen und Leitungen werden schrittweise charakterisiert und in das Modell integriert, was veranschaulicht, wie Modellkomplexität inkrementell aufgebaut werden kann.
Eine weitere Serie synthetischer Fallstudien demonstriert anschließend die Optimierungsmöglichkeiten des Frameworks anhand von Betriebskonzepten zunehmender Komplexität: Batch-Elution, Closed-Loop- und Steady-State-Recycling, Flip-Flop-Chromatographie sowie Reihenschaltungen von Säulen.
Die Simulationsergebnisse werden gegen analytische Lösungen der Gleichgewichtstheorie validiert, und die Mehrzielsoptimierung deckt nicht-intuitive Betriebsstrategien auf, darunter Serieninjektionen, intermediäre Abfallfraktionen und Peakverschachtelung unter überladenen Bediungungen.
Ein bemerkenswertes Ergebnis ist, dass sich die Batch-Elution als produktivitätsoptimaler Grenzfall komplexerer Recyclingkonfigurationen erweist, ein Resultat, das sich natürlich aus der Optimierungsformulierung ergibt und auf das Potenzial des Frameworks für die Superstrukturoptimierung hinweist, bei der das Betriebskonzept selbst als Entwurfsvariable behandelt wird.

Durch diese Entwicklungen etabliert sich CADET-Process als umfassendes Open-Source-Framework für die Auslegung und Optimierung chromatographischer Prozesse, das der wissenschaftlichen Gemeinschaft frei zur Verfügung steht und Fortschritte in akademischer Forschung und industrieller Anwendung ermöglicht.

{raw-latex}`\clearpage`

## Abstract

Chromatography is a widely used separation technique in the chemical, pharmaceutical, and biotechnological industries.
Rigorous model-based design and optimization of chromatographic processes is, however, challenging: the nonlinear dynamics, periodic operation, and large number of degrees of freedom make process development difficult.
At the same time, the diversity of operating concepts, from batch-elution to multi-column continuous processes, means that existing tools are either tailored to specific processes or too general-purpose to apply without extensive custom configuration.

This thesis presents a modular framework for modeling and optimizing chromatographic processes, implemented as the open-source package **CADET-Process**.
The framework separates process configuration, simulation, performance evaluation, and optimization into independent components.
It provides a flexible interface for defining complex operating concepts such as valve switching schemes, recycling configurations, and multi-column setups, and allows key performance indicators and optimization problems to be configured and solved without custom integration code.
The framework is developed following established research software engineering practices to ensure reliability, reproducibility, and long-term maintainability, and has since been adopted in both academic and industrial settings as part of the broader **CADET** ecosystem.

The framework is validated against experimental data through a parameter estimation study of a laboratory-scale protein purification system using ion-exchange chromatography.
Steric mass-action binding kinetics, column transport phenomena, and system periphery effects including valve and tubing contributions are characterized and incorporated into the model progressively, illustrating how model complexity can be built up incrementally.
A complementary series of synthetic case studies then demonstrates the framework's optimization capabilities across operating modes of increasing complexity: batch-elution, closed-loop and steady-state recycling, flip-flop chromatography, and serial column configurations.
Simulation results are validated against analytical equilibrium theory solutions, and multi-objective optimization reveals non-intuitive operating strategies including stacked injections, intermediate waste fractions, and peak interlocking under overloaded conditions.
A notable finding is that batch elution emerges as the productivity-optimal limiting case of more complex recycling configurations, a result that arises naturally from the optimization formulation and points to the framework's potential for superstructure optimization, where the operating mode itself is a design variable.

Through these developments CADET-Process establishes itself as a comprehensive open-source framework for chromatographic process design and optimization, freely available to the scientific community and enabling advances in both academic research and industrial applications.

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
BDF
    Backward differentiation formula

CC
    Creative Commons

CG
    Continuous Galerking method

CI/CD
    Continuous integration/Continuous deployment

CLR
    Closed-loop recycling

COBYLA
    Constrained optimization by linear approximation algorithm

COP
    Constrained optimization programming

CSTR
    Continuous stirred tank reactor model

CV
    Column volume

DAE
    Differential-algebraic equation

DBTL cycle
    Design, build, test, learn cycle

DG
    Discontinuous Galerking method

DoE
    Design of experiments

DOF
    Degrees of freedom

DRY
    Don't repeat yourself

ET
    Equilibrium theory

EM
    Equilibrium model

EDM
    Equilibrium-dispersive model

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

GRM
    General rate model

GPL
    GNU General Public License

ILP
    Integer linear programming

KISS
    Keep it simple, stupid

LC
    Liquid chromatography

LDF
    Linear driving force

LFS
    Large file system

LP
    Linear programming

LRM
    Lumped rate model without pores

LRMP
    Lumped rate model with pores

KPI
    Key performance indicator

SMB
    Simulated moving bed

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

ODE
    Ordinary differential equation

OOP
    Object-oriented programming

(D)PFR
    (Dispersive) Plug flow reactor

RDM
    Research data management

RK
    Runge-Kutta

RSE
    Research software engineering

QP
    Quadratic programming

SFC
    Supercritical fluid chromatography

SMA
    Steric mass action law

SOO
    Single-objective optimization

SSE
    Sum squared errors

SUPG
    Streamline-upwind Petrov-Galerkin stabilization

PD(A)E
    Partial differential (algebraic) equation

PEP
    Python Enhancement Proposal

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

**Symbols**

| Symbol                             | Description                                                 | Unit                                           |
|:---------------------------------- |:----------------------------------------------------------- |:---------------------------------------------- |
| $a$                                | Henry coefficient (linear isotherm)                         |                                                |
| $a_s$                              | Specific particle surface area                              | $\text{m}^{-1}$                                |
| $A_c$                              | Column cross-sectional area                                 | $\text{m}^{2}$                                 |
| $b$                                | Equilibrium constant (Langmuir isotherm)                    | $\text{m}^{3}\,\text{mol}^{-1}$                |
| $c$                                | Mobile phase concentration                                  | $\text{mol}\,\text{m}^{-3}$                    |
| $C_{i,\text{total}}$               | Total separation cost for component $i$                     | $\text{€}\,\text{kg}^{-1}$                     |
| $C_{\text{operating}}$             | Operating cost (overhead, wages, maintenance)               | $\text{€}\,\text{kg}^{-1}$                     |
| $C_{\text{depreciation}}$          | Depreciation cost                                           | $\text{€}\,\text{kg}^{-1}$                     |
| $C_{i,\text{ads}}$                 | Adsorbent cost for component $i$                            | $\text{€}\,\text{kg}^{-1}$                     |
| $C_{i,\text{el}}$                  | Eluent cost for component $i$                               | $\text{€}\,\text{kg}^{-1}$                     |
| $C_{i,\text{feed}}$                | Feed cost for component $i$                                 | $\text{€}\,\text{kg}^{-1}$                     |
| $D_{ax}$                           | Axial dispersion coefficient                                | $\text{m}^{2}\,\text{s}^{-1}$                  |
| $e_{\text{fwd}/\text{bwd},\ell,j}$ | Reaction order of component $\ell$ in reaction $j$          |                                                |
| $EC_i$                             | Specific eluent consumption for component $i$               | $\text{m}^{3}\,\text{kg}^{-1}$                 |
| $F$                                | Phase ratio $(1 - \varepsilon) / \varepsilon$               |                                                |
| $f_{\text{ads}}(c, q)$             | Adsorption isotherm function                                |                                                |
| $p_{\text{ads}}$                   | Adsorbent price                                             | $\text{€}\,\text{m}^{-3}$                      |
| $p_{\text{el}}$                    | Eluent price                                                | $\text{€}\,\text{m}^{-3}$                      |
| $p_{\text{feed}}$                  | Feed price                                                  | $\text{€}\,\text{m}^{-3}$                      |
| $\mathcal{F}(c_j, c_{j+1})$        | Numerical flux function (finite volume)                     |                                                |
| $f_{\text{react},i}$               | Reaction flux for component $i$                             | $\text{mol}\,\text{m}^{-3}\,\text{s}^{-1}$     |
| $k_a$                              | Adsorption rate constant                                    | $\text{m}^{3}\,\text{mol}^{-1}\,\text{s}^{-1}$ |
| $k_d$                              | Desorption rate constant                                    | $\text{s}^{-1}$                                |
| $K_{\text{eq}}$                    | Equilibrium constant (LDF)                                  | $\text{m}^{3}\,\text{mol}^{-1}$                |
| $k_f$                              | Film mass transfer coefficient                              | $\text{m}\,\text{s}^{-1}$                      |
| $k_{\text{kin}}$                   | Kinetic rate constant (LDF approximation)                   | $\text{s}^{-1}$                                |
| $K_{i,0}$                          | Selectivity coefficient (SMA)                               |                                                |
| $L_c$                              | Column length                                               | $\text{m}$                                     |
| $m_i$                              | Amount of component $i$ collected                           | $\text{mol}$                                   |
| $m_{\text{feed},i}$                | Amount of component $i$ in the feed                         | $\text{mol}$                                   |
| $\dot{m}_{i,\text{annual}}$        | Annual production rate of component $i$                     | $\text{kg}\,\text{yr}^{-1}$                    |
| $N_{\text{chrom}}$                 | Number of chromatograms                                     |                                                |
| $N_{\text{comp}}$                  | Number of components                                        |                                                |
| $N_{\text{frac},k}^i$              | Number of fractions for component $i$ in chromatogram $k$   |                                                |
| $N_{\text{react}}$                 | Number of reactions                                         |                                                |
| $PR_i$                             | Specific productivity of component $i$                      | $\text{kg}\,\text{m}^{-3}\,\text{s}^{-1}$      |
| $PU_i$                             | Product purity of component $i$                             | $\%$                                           |
| $q$                                | Stationary phase loading                                    | $\text{mol}\,\text{m}^{-3}$                    |
| $q^*$                              | Equilibrium loading concentration (LDF)                     | $\text{mol}\,\text{m}^{-3}$                    |
| $q_{\text{max}}$                   | Maximum loading capacity                                    | $\text{mol}\,\text{m}^{-3}$                    |
| $Q$                                | Volumetric flow rate                                        | $\text{m}^{3}\,\text{s}^{-1}$                  |
| $r^p$                              | Particle radius                                             | $\text{m}$                                     |
| $s_{i,j}$                          | Stoichiometric coefficient of component $i$ in reaction $j$ |                                                |
| $t$                                | Time                                                        | $\text{s}$                                     |
| $t_{\text{start/end},j}$           | Start / end time of fraction $j$                            | $\text{s}$                                     |
| $u$                                | Interstitial mobile phase velocity                          | $\text{m}\,\text{s}^{-1}$                      |
| $V$                                | Volume                                                      | $\text{m}^{3}$                                 |
| $V_{\text{solid}}$                 | Volume of stationary phase                                  | $\text{m}^{3}$                                 |
| $V_{\text{solvent}}$               | Solvent volume consumed per cycle                           | $\text{m}^{3}$                                 |
| $w$                                | Weighting factor                                            |                                                |
| $Y_i$                              | Recovery yield of component $i$                             | $\%$                                           |
| $z$                                | Axial coordinate                                            | $\text{m}$                                     |
| $\Delta t_{\text{cycle}}$          | Cycle duration                                              | $\text{s}$                                     |
| $\Delta t_{\text{life}}$           | Adsorbent lifetime                                          | $\text{s}$                                     |
| $\varepsilon$                      | Porosity                                                    |                                                |
| $\varphi_j$                        | Net flux of reaction $j$                                    | $\text{mol}\,\text{m}^{-3}\,\text{s}^{-1}$     |
| $\Lambda$                          | Ionic capacity of the resin (SMA)                           | $\text{mol}\,\text{m}^{-3}$                    |
| $\nu$                              | Characteristic charge (SMA)                                 |                                                |
| $\sigma$                           | Steric shielding factor (SMA)                               |                                                |

{raw-latex}`\clearpage`

**Subscripts and superscripts**

| Symbol                          | Description               |
|:------------------------------- |:------------------------- |
| $b$                             | Bulk (interstitial) phase |
| $i, j, \ell$                    | Component index           |
| $p$                             | Particle pore phase       |
| $k$                             | Chromatogram index        |
| $m$                             | Binding site index        |
| $\text{in}$, $\text{out}$       | Inlet, outlet             |
| $\text{chrom}$                  | Chromatogram              |
| $\text{comp}$                   | Component                 |
| $\text{feeds}, \text{solvents}$ | Feed, solvent inlets      |
| $\text{frac}$                   | Fraction                  |
| $\text{react}$                  | Reaction                  |


{raw-latex}`\clearpage`
{raw-latex}`\pagenumbering{arabic}`
