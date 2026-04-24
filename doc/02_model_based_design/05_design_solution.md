(design_solution)=
# Solution of chromatographic design problems

The design of preparative chromatographic processes is a complex task, involving numerous degrees of freedom that can be manipulated to optimize performance.
These include continuous variables, such as column length and diameter, injection volume, concentration, and flow rate, as well as dynamic changes to the connectivity the flow sheet.
Additionally, structural decisions - such as selecting the optimal operating concept or mode - can also be subject to optimization.
This makes it possible to determine the operating conditions and the overall process structure simultaneously, ensuring that the design aligns with the specific requirements of the separation problem.
Overall, the design process requires a systematic approach to carefully evaluate all variables and identify the optimal combination of parameters to achieve the desired separation performance.
In this chapter, multiple approaches for addressing these challenges are discussed.

(shortcut_methods)=
## Shortcut methods

Shortcut methods refer to techniques for the design and optimization of processes that are based on heuristics and simplifying assumptions {cite}`Nicoud2015`.
These methods aim to simplify and accelerate the design process by reducing the time and computational resources required.
Examples include the use of empirical equations or pre-determined values to estimate key parameters, statistical or machine learning techniques to model process behavior, and optimization algorithms to efficiently identify the best solutions.

One notable shortcut method is the application of equilibrium theory.
Although it assumes the absence of kinetic limitations - which may not hold for certain scenarios, such as the separation of larger molecules - it serves as a foundational concept in several design methods.
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

Beyond process design, parameter sampling plays a critical role in the development of error models, which are essential for the successful implementation and operation of chromatographic processes.
Error models are used to predict process performance under varying operating conditions, identify potential sources of variability, and highlight opportunities for improvement.
Sampling techniques are particularly useful for generating data to develop and validate these error models.
For example, a Design of Experiments (DoE) approach systematically varies process parameters and measures their impact on performance metrics.
The resulting data can then be used to build statistical models that predict process performance and evaluate the uncertainty of these predictions.
By employing advanced sampling methods, the collected data becomes more representative of the parameter space, reducing the risk of bias or non-representativeness in error models.

(optimization_algorithms)=
## Optimization algorithms

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

The choice of optimization algorithm and solution method depends on the specific class of problem being addressed, as well as the desired trade-off between solution quality and computational efficiency.

Optimization algorithms can generally be categorized into deterministic and stochastic solvers.
Deterministic solvers follow predefined search patterns and do not rely on randomness, ensuring repeatable results.
Stochastic solvers, such as genetic algorithms, incorporate randomness, e.g. by simulating biological evolution.
These algorithms adapt populations through mutations, crossover of genetic information, and selection, where better-performing solutions survive while inferior ones are eliminated.

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
This algorithm approximates both the objective function and constraints with linear problems.
Then, the linear problem is solved which results in a new candidate solution.
This candidate is then evaluated against the original objective and constraint functions to gather new information, which is used to refine the linear approximation.
If the solution cannot be improved, the step size is reduced, further refining the search.
The algorithm terminates once the step size becomes sufficiently small.

While *COBYLA* supports nonlinear constraints, it can be computationally expensive for problems with a large number of variables or constraints due to the high number of function evaluations required.
Additionally, since the method relies on linear approximations, it may not provide highly accurate results for problems with strongly nonlinear behavior.
Moreover, like many optimization algorithms, *COBYLA* does not guarantee global optimality and may become trapped in local optima.


(genetic_algorithm)=
### Genetic Algorithms

Genetic algorithms (GAs) are optimization algorithms inspired by the principles of natural evolution.
In a GA, an initial population of candidate solutions is generated, and each candidate is evaluated based on one or more objective functions.
The fittest candidates are then selected to reproduce, creating the next generation through processes such as crossover and mutation.
This cycle of selection, reproduction, and mutation is repeated over several generations until a satisfactory solution is found.
There are several variations of GAs, including *NSGA2*, *NSGA3*, and *SPEA2*, each offering specific features and strengths.
One key advantage of GAs is their inherent parallelizability; since each candidate solution can be evaluated independently, the evaluation process can be distributed across multiple processors or computers, significantly accelerating the optimization.
Another key advantage is their insensitivity to initial values: unlike gradient-based methods, GAs evaluate a population of diverse candidate solutions, making them robust and less dependent on starting points.
While GAs are effective optimization tools, they do not guarantee finding the global optimum and can be sensitive to parameter settings, such as population size, mutation rate, and crossover rate.
For this work, a modified *NSGA3* is used due to its strong support for multi-objective optimization problems {cite}`Jain2014`.
