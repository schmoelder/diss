# A modular framework for modeling and optimizing chromatographic processes

% Create custom role for inserting raw latex
```{role} raw-latex(raw)
:format: latex
```

% Disable page numbers
```{raw} latex
\pagenumbering{gobble}
```

% Epigraph
```{raw} latex
\clearpage
\epigraph{\itshape
  And what is good, Phaedrus, And what is not good ---\\
  Need we ask anyone to tell us these things?
}{
  ---Robert M. Pirsig, \\
  \textit{
    Zen and the Art of Motorcycle Maintenance: \\
    An Inquiry Into Values
  }
}
\clearpage
```

## Preface

As a modeling engineer, I am constantly aware that arbitrary precision can be achieved, but often at a cost that is not justified.
This work is no exception.
Instead, I aim to be transparent about the limitations of the presented framework: some components remain unfinished, and others may exhibit issues I have not yet considered.
There is always more to learn and improve, and some challenges may remain unaddressed.
Despite these limitations, the software developed in this work provides robust and effective approximations of *some* aspects of reality, particularly in modeling and simulating the diverse physicochemical effects and operational conditions that govern separation processes in chromatographic columns.

To achieve this, the early decision to modularize the framework's code proved crucial.
By separating functionality and defining clear interfaces, development, testing, and integration of interconnected logic became more efficient.
This modularity also supports incremental improvements: emerging issues or missing features can be addressed without disrupting other parts of the system.

Open-source principles, combined with adaptability to different standards, further strengthen this approach by promoting transparency within the broader scientific community.
In fact, many of the strongest modules emerged from joint efforts, and I am grateful to those who contributed their expertise and perspective.
Much could be taken for granted because others were willing to go the *extra mile*.
Learning from the enthusiasm of others is an unmatched shortcut to understanding.

Looking ahead, I hope to continue developing this software.
However, knowing where to *stop* is an art in itself, and for now, this thesis represents the current state of my efforts.

{raw-latex}`\clearpage`

## Acknowledgements

There are many people I need to thank, but first and foremost, I want to express my deepest gratitude to my partner, Leila.
Her unconditional support and patience throughout this journey have been invaluable.
No one else had to endure my struggles as much, yet she was always there as a thoughtful listener.
Being outside my field of research, she provided a great way to test my own understanding: if I could explain complicated issues clearly to her, I knew I had truly grasped them.
Beyond this, she was a catalyst for personal growth, guiding me to discover what truly matters to me in life.

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

Last but not least, I owe my sincere gratitude to Prof. Matthias Franzreb and Juliane Diehm from KIT.
In a time of need, they offered me scientific refuge and a desk free from distractions, allowing me to finally complete what I had started ten years ago.

{raw-latex}`\clearpage`

## Published work

Parts of this thesis were and are being published as in peer-reviewed journals, at conferences, in supervised students' theses and in the form of open source software packages.
Any thought, methodology, result, conclusion and direct or indirect contribution to this work is considered as properly cited by the following listing:

**Articles:**
- Dienstbier et al.
- Schmölder et al.
- Breuer et al., (DG)
- Leweke et al., (JOSS)
- @TODO: what else?

**Conference and symposium talks:**
- SPICA Wien
- SPICA Darmstadt
- ProcessNet Köln
- Prep? (not really part of this thesis)

**Conference posters:**
- ProcessNet Aachen: Schmölder et al.

**Code repositories and software packages**:
- CADET-Process
- CADET-Core
- CADET-RDM

**Datasets**:
- Characterization @TODO
- Batch Elution @TODO

**Supervised and co-supervised student projects**:
- Johanna Ullrich
- Fabian Popp
- Stefan Wolf
- Felix Derleth
- Simon Cortelezzi
- Carola Schlumberger
- Eliane Tauber
- Jana Dienstbier
- Jan Breuer
- Lukas Thiel
- Daniel Klaus
- Florian Hülsmann

{raw-latex}`\clearpage`

## Zusammenfassung

Dies und das hab ich gemacht.

{raw-latex}`\clearpage`

## Abstract

This and that I did.

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
