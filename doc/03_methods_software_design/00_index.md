(methods_software_design)=
# Development methods for scientific software

In recent decades, the use of software has become an integral part of many scientific endeavors.
In addition to solving computational problems such as numerical simulations, software is also employed to plan experiments, control laboratory equipment, and analyze data sets.

However, scientists often develop their own software despite not being trained programmers and being primarily self-taught.
This can lead to a lack of awareness of techniques and practices that exist to improve the quality of code {cite}`Hannay2009`.
Without proper design, the resulting code may be difficult to extend and maintain, leading to conflicting versions of the software and poorly reproducible datasets.
To ensure reliability and reproducibility, software should therefore be built, validated, and used as carefully as other laboratory equipment {cite}`Wilson2014`.

This chapter introduces the software development methods and best practices that were applied in the design and implementation of CADET-Process, the framework described in this work.
The focus is on practices that promote three key qualities: *reliability*, ensuring the software behaves correctly and predictably; *sustainability*, enabling the codebase to be maintained, extended, and reused over time; and *reproducibility*, ensuring that results obtained with the software can be independently verified by others.
Concretely, programming principles, object-oriented design, documentation, and testing are discussed, along with version control, CI/CD pipelines, software licensing, and research data management.
