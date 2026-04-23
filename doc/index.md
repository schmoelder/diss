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

To know whether a process is good, we model it.
To trust the model, we validate it against reality.
And to rely on the software that runs it, we test it systematically.
This work addresses all three, and aims to be transparent about where each falls short: some components remain unfinished, and others may exhibit issues I have not yet considered.
Nevertheless, the software developed in this work provides robust and effective approximations of *some* aspects of reality, particularly in modeling and simulating the diverse physicochemical effects and operational conditions that govern separation processes in chromatographic columns.

To achieve this, the early decision to modularize the framework's code proved crucial.
By separating functionality and defining clear interfaces, development, testing, and integration of interconnected logic became more efficient.
This modularity also supports incremental improvements: emerging issues or missing features can be addressed without disrupting other parts of the system.

Open-source principles, combined with adaptability to different standards, further strengthen this approach by promoting transparency within the broader scientific community.
In fact, many of the strongest modules emerged from joint efforts, and I am grateful to those who contributed their expertise and perspective.
Much could be taken for granted because others were willing to go the *extra mile*.
The enthusiasm of others has been a constant source of motivation.

Looking ahead, I hope to continue developing this software.
However, knowing where to *stop* is an Art in itself, and for now, this thesis represents the current state of my efforts.

{raw-latex}`\clearpage`

## Acknowledgements

There are many people I need to thank, but first and foremost, I want to express my deepest gratitude to my partner, Leila.
Her unconditional support and patience throughout this journey have been invaluable.
No one else had to endure my struggles as much, yet she was always there as a thoughtful listener.
Being outside my field of research, she provided a great way to test my own understanding: if I could explain complicated issues clearly to her, I knew I had truly grasped them.
Beyond this, she has been a catalyst for my personal growth, helping me find what truly matters in life.

Moreover, I would like to thank Prof. Kaspereit for granting me the freedom to explore a field that was completely new to me.
It took longer than expected to understand the subject and find my place within it, yet I was given the time I needed, and it was never doubted that I would eventually succeed.

My time in Erlangen would not have been the same without my wonderful colleagues and students, too many to name individually.
In particular, I want to highlight José Vargas and Benjamin Reif for their continued friendship, all the insightful discussions and support, as well as the fun and memorable moments we shared.

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
{raw-latex}`\pagenumbering{arabic}`
