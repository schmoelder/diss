(design_solution)=
# Solution of chromatographic design problems

The design of preparative chromatographic processes presents significant challenges due to the many degrees of freedom that can be manipulated to optimize their performance.
In addition to continuous variables such as column length and diameter, injection concentration, and flow rate, there are also dynamic changes to the flow sheet that must be timed and optimized.
Structural decisions can also be subject to optimization to determine the optimal operating concept and conditions for a given separation simultaneously.
Overall, the design process requires careful consideration of all of these variables and the identification of the optimal combination of parameters to achieve the desired separation performance.

In this chapter, multiple approaches are discussed to solve these problems.

## Shortcut methods

Shortcut methods in the design of chromatographic processes refer to techniques that can help reduce the time and resources required to design and optimize such processes.
These methods often rely on simplifying assumptions or heuristics to make the design process more efficient.
Examples of shortcut methods include using empirical equations or pre-determined values to estimate key parameters, using statistical or machine learning techniques to model the behavior of the process, and using optimization algorithms to find the best solution.

@todo:
Beispiele:

- Kaspereit {cite}`Kaspereit2005`
- Triangle theory {cite}`Mazzotti2006`
- Unified design {cite}`Siitonen2015`

## Parameter sampling

Parameter sampling is a common method used in the design of chromatographic processes.
It involves creating a grid of possible parameter values and evaluating the performance of the process for each combination of values.
However, as the number of parameters increases, the number of combinations of values grows exponentially, making it difficult to evaluate all possible combinations.
This phenomenon is known as the *curse of dimensionality*.

Several advanced sampling techniques have been developed to overcome the challenges associated with parameter sampling.
One such method is advanced polytope sampling, which employs techniques such as *Markov Chain Monte Carlo (MCMC)* and *Hit-and-Run* to more efficiently sample the parameter space.
*MCMC* is a popular sampling method that involves generating a sequence of samples from a probability distribution.
It can be used to explore complex parameter spaces, where traditional methods may struggle to find the global optimum solution {cite}`Smith1984`.
*Hit-and-Run* is another sampling method that generates samples by taking a random step in a random direction and then constraining the sample to lie within the boundaries of the parameter space {cite}`Jadebeck2020`.
Both of these methods can be effective in reducing the number of samples required to accurately represent the parameter space and can improve the efficiency and accuracy of the design process.

Despite the benefits of these advanced sampling techniques, finding the global optimum solution can still be a challenge, and a large number of evaluations may be required.
As a result, other optimization algorithms, such as gradient descent and genetic algorithms, may be more effective at finding the global optimum solution.
These methods use iterative optimization techniques to systematically explore the parameter space and can often converge on the optimal solution more quickly and efficiently than sampling-based methods.
Nevertheless, advanced sampling techniques can be useful for an efficient exploration of the parameter to initialize other optimization algorithms.

Moreover, sampling techniques are important tools for developing error models, which are critical for the successful implementation and operation of chromatographic processes.
Error models predict process performance under different operating conditions and help identify potential sources of variability and opportunities for process improvement.
Sampling methods are used to generate data for error model development and validation.
For example, a Design of Experiments (DoE) approach can systematically vary process parameters and measure their impact on performance metrics.
The resulting data can then be used to develop statistical models to predict process performance and evaluate the uncertainty associated with these predictions.
The use of advanced sampling methods can ensure that the collected data is representative of the parameter space and reduce the risk of bias or non-representativeness in error models.

## Optimization algorithms

Optimization problems can be classified based on the type of variables, constraints, and objectives involved.
Some common classes include:

- Linear programming: Finding the optimal solution to a linear objective function subject to linear equality and inequality constraints.
- Quadratic programming: Finding the optimal solution to a quadratic objective function subject to linear equality and inequality constraints.
- Nonlinear programming: Finding the optimal solution to a nonlinear objective function subject to nonlinear equality and inequality constraints.
- Integer programming: Finding the optimal solution to an objective function subject to linear or nonlinear equality and inequality constraints, where some or all of the variables are required to be integers.
- Constrained optimization: Finding the optimal solution to an objective function subject to one or more constraints on the variables.
- Multi-objective optimization: Finding the optimal solutions to multiple conflicting objective functions, often by trade-off or compromise.

The choice of optimization algorithm and solution method depends on the specific class of problem being solved and the desired trade-off between solution quality and computational efficiency.

There are two general approaches to solving optimization problems: deterministic and stochastic solvers.
Deterministic solvers use predefined search patterns without applying guesses or random steps.
Stochastic solvers, such as genetic algorithms, are based on biological evolution, where a population adapts indirectly to the environment and changes within.
Adaptation depends on mutations of genes, crossover of genetic information.
During selection, the best adapted individuals survive, while the least adapted part of the population is extincted.

Different solvers will outperform others depending on the problem at hand.
Some of the derivative-based solvers can guarantee finding local but not necessarily global optima.
Moreover, they may be insensitive to the change of variables due to a flat objective function.
On the other hand, derivative-free solvers can often handle non-convex functions better but require significantly more computational power.

Gradient-based nonlinear programming (NLP) solvers, such as interior-point algorithms {cite}`Kawajiri2006`, sequential programming {cite}`Arkell2018`, or simplex {cite}`GarciaPalacios2009`, as well as derivative-free approaches like genetic algorithms {cite}`Heinonen2014,Schmoelder2020` and Gaussian process regression {cite}`Freier2018,Jaepel2022`, have been used successfully for optimal process design.
Additionally, mixed-integer nonlinear programming (MINLP) has been applied to general process optimization using extended cutting plane algorithms {cite}`Emet2008`, as well as for structural decision variables using outer approximation {cite}`Kaspereit2012`, and evolutionary algorithms {cite}`GarciaPalacios2011`.

In the following, the algorithms used in this work will be presented.

## Constrained optimization by linear approximation

The constrained optimization by linear approximation algorithm (COBYLA) is a method for constrained problems where the derivative of the objective function is unknown {cite}`Powell1994`.
To solve the optimization problem, the actual objective function and constraints are approximated with linear problems.
Then, the linear problem is solved which results in a new candidate.
By evaluating the original problem with the candidate, new information about the objectives and constraints is gained, which is used to improve the approximation.
The step size is reduced if the solution cannot be improved, which further refines the solution.
The algorithm terminates if the step size becomes sufficiently small.

During an iteration, an approximating linear programming problem is solved to obtain a candidate for the optimal solution.
The candidate solution is evaluated using the original objective and constraint functions, yielding a new data point in the optimization space.
This information is used to improve the approximating linear programming problem used for the next iteration of the algorithm.
When the solution cannot be improved anymore, the step size is reduced, refining the search.
Finally, the step size becomes sufficiently small, the algorithm terminates.

While COBYLA supports nonlinear constraints, it requires a large number of function evaluations, particularly for problems with a large number of variables or constraints.
This can make it computationally expensive and slow for complex problems.
Additionally, since the algorithm approximates the objective function and constraints using linear problems, it may not provide the most accurate results for non-linear problems.
Moreover, COBYLA does not guarantee global optimality, and can sometimes get stuck in local optima.

### Genetic Algorithms

Genetic algorithms (GA) are a type of optimization algorithm that are inspired by the process of natural evolution.
In a GA, an initial population of candidate solutions is created, and each candidate solution is evaluated based on one or more objectives.
The fittest members of the population are then selected to reproduce and create the next generation of candidates.
This process of selection, reproduction, and mutation is repeated over several generations until a satisfactory solution is found.
One of the advantages of GAs is their parallelizability; since each candidate solution can be evaluated independently, the evaluation process can be easily distributed across multiple processors or computers, leading to faster and more efficient optimization.
There are several variations of GAs, including *NSGA2*, *NSGA3*, and *SPEA2*, each with their own specific features and strengths.
For this work, a modified *NSGA3* {cite}`Jain2014` is used since it has good support multi-objective problems.
Although GAs can be very powerful, they are not guaranteed to find the global optimum and can be sensitive to parameter settings.
