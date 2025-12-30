(rdm)=
# Research data management

In contrast to wet-lab research, computational studies often lack an equivalent to structured lab notebooks.
As a consequence, reproducibility is frequently impaired: the exact code version used is unclear, parameters are insufficiently documented, and results may be recorded while their underlying sources continue to evolve.

The **FAIR principles** (Findable, Accessible, Interoperable, and Reusable) provide widely accepted guidelines for research data management (RDM) and have been adopted as a key requirement by national and international research funding organizations {cite}`Wilkinson2016`.

In modern scientific research, particularly in computational and hybrid experimental–computational workflows, **reproducibility** and **traceability** remain major challenges.
Typical difficulties include:
- **Incomplete provenance**: Results are not reliably linked to the exact code version, configuration, and execution environment that produced them.
- **Increasing workflow complexity**: Chained simulations, recycling of outputs as inputs, and the combination of experimental and simulated data introduce nontrivial dependencies.
- **Scalability under FAIR constraints**: Large datasets and frequent iterations complicate efficient versioning while maintaining FAIR compliance.

Conventional ad-hoc approaches—such as manual documentation, loosely organized scripts, or monolithic repositories—do not scale well and often lead to loss of context or irreproducible results.

To address these challenges, **[CADET-RDM](https://cadet-rdm.readthedocs.io/en/latest/)** was developed in collaboration with Ronald Jäpel {cite}`CADET-RDM_documentation`.
While developed independently, the tool was explicitly designed to support the types of workflows encountered in this thesis.
Accordingly, all case studies presented in this work were managed using **CADET-RDM**.

The system is based on a dual-repository *Git* architecture:
1. **Project repository**: Maintains the evolving codebase (e.g., Python or C++ simulation components) under standard version control.
2. **Output repository**:
   - Collects metadata—such as the current state of the project repository, call arguments, and environment snapshots—in the `main` branch, forming a persistent and self-documenting audit trail.
   - Stores results in **isolated, shallow branches**, each uniquely associated with a specific run identifier.

Key features of CADET-RDM include:
- **FAIR-by-design data handling**: Results are findable via versioned branches, accessible through standard *Git* tools, interoperable with common Python-based data formats, and reusable due to explicit provenance tracking.
- **Platform independence**, allowing seamless integration with existing *Git* hosting solutions.
- ***Git* LFS integration** for efficient storage of large data files (e.g., HDF5 outputs and CSV files).
- **Lightweight versioning**, enabled by shallow branches and *Git*’s native branching model.
- Native support for **chained simulations** and mixed experimental–simulation workflows.
