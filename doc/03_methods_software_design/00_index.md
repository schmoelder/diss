(methods_software_design)=
# Development methods for scientific software

In recent decades, the use of software has become an integral part of many scientific endeavors.
In addition to solving computational problems such as numerical simulations, software is also employed to plan experiments, control laboratory equipment, and analyze data sets.

However, scientists often develop their own software despite not being trained programmers and being primarily self-taught.
This can lead to a lack of awareness of techniques and practices that exist to improve the quality of code {cite}`Hannay2009`.
Without proper design, the resulting code may be difficult to extend and maintain, leading to conflicting versions of the software and poorly reproducible datasets.
But, to ensure reliability and reproducibility, software should also be built, validated, and used as carefully as other laboratory equipment {cite}`Wilson2014`.

This chapter provides an overview of modern approaches, best practices, and tools that can aid in designing sustainable scientific software.
Examples will be given to demonstrate the benefits of version control, documentation, and testing, and how these practices can be integrated into development CI/CD pipelines.
Additionally, the important topics of copyright and licensing will be touched upon.
