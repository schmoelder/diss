(design_solution)=
# Solution of chromatographic design problems

The design of preparative chromatographic processes involves numerous degrees of freedom that can be manipulated to optimize performance.
These include continuous variables such as column geometry, injection volume, concentration, and flow rates, as well as discrete decisions such as selecting the operating mode or flow sheet connectivity.
Addressing these challenges systematically requires a combination of methods: shortcut methods provide rapid design guidance based on simplified or analytical problem formulations, parameter sampling supports exploration of the design space and sensitivity analysis, and optimization algorithms enable systematic identification of optimal operating conditions.
Importantly, these methods are not limited to process design but apply equally to model calibration and parameter estimation, as introduced in {numref}`model_calibration`.
The following sections introduce the most relevant approaches used in this work.

(shortcut_methods)=
## Shortcut methods

Shortcut methods refer to techniques for the design and optimization of processes that are based on heuristics and simplifying assumptions {cite}`Nicoud2015`.
By exploiting simplified problem formulations or analytical results, they avoid the need for full numerical simulations, making them particularly useful as a first step in process design or as a source of initial estimates for subsequent optimization.
Examples include the use of empirical equations or pre-determined values to estimate key parameters, statistical or machine learning techniques to model process behavior, and optimization algorithms to efficiently identify the best solutions.

One notable shortcut method is the application of equilibrium theory.
Although it assumes the absence of kinetic limitations, which may not hold for certain scenarios, such as the separation of larger molecules, it serves as a foundational concept in several design methods.
Equilibrium theory provides inherent boundaries for process design, making it a valuable starting point {cite}`SchmidtTraub2020`.
This approach is particularly useful in the design and operation of SMB processes.
The central idea is to determine an operating region for dimensionless flow rate ratios where a complete separation of a two-component mixture is achievable in a (theoretical) true moving bed (TMB) process.
For linear isotherms, this operating region takes the shape of a triangle and is commonly referred to as the *triangle theory*.
Originally developed for linear isotherms, this theory has since been extended to other isotherm models, such as the Langmuir isotherm {cite}`Mazzotti2006`.

Equilibrium theory also finds application in the design of MR-SSR processes (see {numref}`mrssr`).
In this context, it is used to predict the breakthrough of components and determine the optimal times to switch recycling valves and fractionation intervals {cite}`Kaspereit2005,Kaspereit2011`.
For instance, Siitonen et al. generalized established design methods for various single- and multi-column processes by applying equilibrium theory.
Their approach allowed for the direct prediction of multiple dimensionless operating parameters required to achieve the complete separation of a binary feed mixture, using the Langmuir isotherm {cite}`Siitonen2015`.

Depending on the desired level of precision, the parameters obtained through shortcut methods can either be directly applied in process design or serve as initial estimates for more detailed optimization.
However, these methods have inherent limitations due to their simplifying assumptions and the specific operating modes they address.
They can become restrictive when dealing with multi-component mixtures, advanced operating concepts, or highly complex problem scenarios.
In such cases, optimization algorithms are often employed to overcome these challenges and refine the process design.

(parameter_sampling)=
## Parameter sampling

Parameter sampling is a common approach used in the design of chromatographic processes.
It involves creating a grid of possible parameter values and evaluating the process performance for each combination.
However, as the number of parameters increases, the number of parameter combinations grows exponentially, a phenomenon known as the curse of dimensionality.
To address this challenge, several advanced sampling techniques have been developed to efficiently explore the parameter space.
One such technique is advanced polytope sampling, which employs methods like *Markov Chain Monte Carlo (MCMC)* and *Hit-and-Run*.

*MCMC* generates a sequence of samples from a probability distribution and is particularly effective for exploring complex parameter spaces where traditional methods may struggle to locate the global optimum {cite}`Smith1984`.
*Hit-and-Run*, on the other hand, generates samples by taking a random step in a random direction and constraining the sample to remain within the boundaries of the parameter space {cite}`Jadebeck2020`.
Both methods effectively reduce the number of samples required to accurately represent the parameter space, improving both the efficiency and accuracy of the sampling process.

Despite these advantages, finding the global optimum remains a challenge, and a large number of evaluations may still be required.
In such cases, optimization algorithms like gradient descent and genetic algorithms are often more effective for locating the global optimum.
These algorithms iteratively explore the parameter space and can converge on optimal solutions more quickly and efficiently than sampling-based methods.
However, advanced sampling techniques are still valuable for efficiently initializing these optimization algorithms by providing a representative starting point for parameter exploration.

Parameter sampling also supports the development of surrogate and error models, which characterize process sensitivity to variability in operating conditions.
For example, a Design of Experiments (DoE) approach systematically varies process parameters and measures their effect on performance metrics.
The resulting data can be used to build statistical models that predict process performance and quantify prediction uncertainty.
More representative sampling of the parameter space reduces the risk of bias in these models.

(optimization_algorithms)=
## Optimization

Optimization is the systematic search for decision variable values $x$ that minimize or maximize one or more objective functions $f(x)$, subject to constraints on the feasible region.
As discussed above, it provides a unified framework for tasks ranging from model calibration to process design.
Optimization problems can be classified based on the type of variables, constraints, and objectives involved.
Some common classes include:

- Linear programming (LP): Finding the optimal solution to a linear objective function subject to linear equality and inequality constraints.
- Quadratic programming (QP): Finding the optimal solution to a quadratic objective function subject to linear equality and inequality constraints.
- Constrained optimization programming (COP): Solving an objective function subject to one or more constraints on the variables.
- Nonlinear programming (NLP): Finding the optimal solution to a nonlinear objective function subject to nonlinear equality and inequality constraints.
- Integer linear programming (ILP): Finding the optimal solution to an objective function where variables are constrained to be integers, with linear constraints.
- Mixed integer linear programming (MIP): Finding the optimal solution to an objective function where some or all variables are constrained to be integers, with linear constraints.
- Mixed integer nonlinear programming (MINLP): Finding the optimal solution to an objective function where some or all variables are constrained to be integers, with linear or nonlinear constraints
- Multi-objective optimization (MOO): Solving multiple conflicting objective functions simultaneously, typically requiring trade-offs between competing goals.

The choice of optimization algorithm depends on the specific class of problem being addressed, as well as the desired trade-off between solution quality and computational efficiency.
Optimization algorithms can generally be categorized into deterministic and stochastic solvers.
Deterministic solvers follow predefined search patterns and do not rely on randomness, ensuring repeatable results.
Stochastic solvers incorporate randomness into their search procedure; for example, genetic algorithms simulate biological evolution through mutation, crossover, and selection.
Although results may vary between runs, reproducible outcomes can be ensured by fixing the random seed, which is important for scientific reproducibility.
Different solvers excel depending on the problem characteristics.
Gradient-based solvers, for example, can efficiently find local optima but may struggle with flat objective functions or non-convex landscapes.
On the other hand, derivative-free solvers, while often better at handling non-convex functions, generally require significantly more computational effort.
Gradient-based NLP solvers, such as interior-point methods {cite}`Kawajiri2006`, sequential programming {cite}`Arkell2018`, and simplex algorithms {cite}`GarciaPalacios2009`, have been widely used for process optimization.
Additionally, derivative-free approaches, including genetic algorithms {cite}`Heinonen2014,Schmoelder2020` and Gaussian process regression {cite}`Freier2018,Jaepel2022`, have proven effective for complex, non-convex problems.
For optimization problems involving both continuous and discrete variables, MINLP has been successfully applied.
Methods such as extended cutting plane algorithms {cite}`Emet2008`, outer approximation {cite}`Kaspereit2012`, and evolutionary algorithms {cite}`GarciaPalacios2011` have been employed to address challenges related to structural decision variables and general process optimization.
In the following sections, the specific algorithms used in this work will be presented.

(cobyla)=
### Constrained optimization by linear approximation

The constrained optimization by linear approximation algorithm (*COBYLA*) is a method designed for constrained problems where the derivative of the objective function is unknown {cite}`Powell1994`.
At each iteration, the algorithm constructs linear approximations of the objective function and all constraints, solves the resulting linear subproblem to obtain a new candidate solution, and then evaluates the candidate against the original nonlinear functions to update the approximation.
If no improvement is achieved, the step size is reduced; the algorithm terminates once the step size falls below a prescribed tolerance.

*COBYLA* requires no gradient information, making it straightforward to apply to black-box objective functions such as those arising from chromatographic simulations.
It exhibits reliable convergence for problems with a moderate number of variables and moderately nonlinear behavior.
However, its computational cost increases significantly for high-dimensional problems, and, like most local optimization methods, it does not guarantee global optimality.
In the present work, it is therefore applied only to subproblems for which these characteristics are acceptable, while more demanding optimization tasks are treated with alternative approaches.
These characteristics make COBYLA particularly well-suited for automatically determining fractionation times, which are required to evaluate key performance indicators (see {numref}`kpi`).


(genetic_algorithm)=
### Genetic Algorithms

Genetic algorithms (GAs) are optimization routines inspired by the principles of natural evolution.
In a GA, an initial population of candidate solutions is generated, and each candidate is evaluated based on one or more objective functions.
The fittest candidates are selected to reproduce, creating successive generations through crossover and mutation, until a satisfactory solution is found.

One key advantage of GAs is their inherent parallelizability; since each candidate solution can be evaluated independently, the evaluation process can be distributed across multiple processors or computers, significantly accelerating the optimization.
Another key advantage is their insensitivity to initial values: unlike gradient-based methods, GAs evaluate a population of diverse candidate solutions, making them robust and less dependent on starting points.
While GAs are effective optimization tools, they do not guarantee finding the global optimum and can be sensitive to parameter settings, such as population size, mutation rate, and crossover rate.
There are several variations of GAs, including *NSGA-II*, *NSGA-III*, and *SPEA2*, each offering specific features and strengths.
In this work, the *U-NSGA-III* algorithm is employed for multi-objective optimization due to its robustness and performance on problems with multiple objectives {cite}`Jain2014`.

---

With the theoretical foundations for model-based design of chromatographic processes established, the following chapter introduces the software engineering principles that informed the development of CADET-Process.
