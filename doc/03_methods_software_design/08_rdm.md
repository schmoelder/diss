(rdm)=
# Research data management

In contrast to wet-lab research, computational studies often lack an equivalent to structured lab notebooks, making it difficult to trace results back to the exact code, parameters, and execution environment that produced them.
Reproducibility is compromised when code versions are not tracked, configurations are insufficiently documented, or results are recorded while their underlying sources continue to evolve.
The **FAIR principles** (Findable, Accessible, Interoperable, and Reusable) provide widely adopted guidelines for research data management (RDM) and are increasingly required by national and international funding organizations {cite}`Wilkinson2016`.

Ensuring FAIR compliance in practice introduces several challenges, particularly in computational workflows:
- **Incomplete provenance**: Results are not reliably linked to the exact code version, configuration, and execution environment that produced them.
- **Increasing workflow complexity**: Chained simulations, reuse of outputs as inputs, and the integration of experimental and simulated data create nontrivial dependencies.
- **Scalability under FAIR constraints**: Large datasets and frequent iterations complicate efficient versioning while maintaining traceability.

To address these challenges, the CADET-RDM framework was developed in collaboration with Ronald Jäpel in parallel with this work, specifically targeting the types of workflows considered here {cite}`CADET-RDM_documentation`.
All case studies presented in this thesis were managed using CADET-RDM.
The system is based on a dual-repository *Git* architecture.
A **project repository** maintains the evolving codebase under standard version control.
An **output repository** operates in parallel: its `main` branch records metadata such as the corresponding project state, execution parameters, and environment information, forming a persistent audit trail, while results are stored in isolated, shallow branches associated with individual runs.

This design makes FAIR compliance an inherent property of the workflow rather than an additional requirement.
Results are findable through versioned branches, accessible via standard *Git* tools, interoperable through common Python-based data formats, and reusable due to explicit provenance tracking.
Large outputs such as HDF5 simulation data and CSV files are handled efficiently using *Git* LFS, keeping storage requirements manageable as datasets grow.
Native support for chained simulations further enables end-to-end traceability of complex workflows.
Within this work, CADET-RDM provides the infrastructure required to systematically link simulations, parameter studies, and optimization results to their exact computational context, ensuring that all reported results remain reproducible and fully traceable.

The practices introduced throughout this chapter, from modular design and automated testing to version control and reproducible data management, provide the foundation for what follows: the implementation of CADET-Process, a framework that translates the chromatographic models from {numref}`fundamentals` into a flexible, well-tested, and reproducible computational tool.
