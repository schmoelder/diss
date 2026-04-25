(software_licenses)=
# Software licenses

To protect and incentivize the creation of intellectual goods, intellectual property laws grant creators exclusive rights to their work.
At the international level, these rights are governed by agreements such as the World Trade Organization's (WTO) Agreement on Trade-Related Aspects of Intellectual Property Rights (TRIPS), which requires member states to provide legal protection for copyrights, patents, and trademarks {cite}`trips_agreement`.

*Copyright* automatically applies to original expressions of ideas, including text, images, and software code, without requiring formal registration.
It grants the exclusive right to reproduce, modify, and distribute the work for a limited period of time.

*Patents*, in contrast, protect inventions and functional ideas rather than their specific expression.
They prevent others from making, using, or selling the invention for a limited duration, after which it enters the public domain.
Patent protection must be actively applied for and granted by the relevant authority.

A *trademark* is a word, phrase, symbol, or design that identifies and distinguishes the origin of goods or services.
It protects against confusingly similar uses by others and can be maintained indefinitely, provided it remains in active use.

## Licenses

Although software is developed to fulfill functional requirements, its implementation is shaped by numerous design decisions, resulting in a concrete expression that is protected by copyright.
Both source code and compiled binaries therefore fall under copyright law, while specific technical solutions may additionally be protected by patents.

A practical issue arises when software is distributed without an explicit license.
In this case, all rights remain reserved by default, and others are not legally permitted to use, modify, or redistribute the software.
This restriction applies even if the source code is publicly accessible.
To avoid this ambiguity, a license should be provided whenever software is shared, explicitly defining the permitted uses and limitations {cite}`Laurent2004`.

Software licenses can broadly be classified into two categories: proprietary licenses and free and open-source software (FOSS) licenses.
Proprietary software is typically distributed under an end-user license agreement (EULA), which restricts usage, modification, and redistribution.
In contrast, FOSS licenses grant users the freedom to use, study, modify, and share the software.

The terminology in this domain is often ambiguous.
The term "free software" refers to freedom rather than price, in the sense of "free speech" rather than "free beer".
By contrast, "freeware" denotes software that is available at no cost but does not necessarily grant access to the source code or rights to modify and redistribute it.
The term "open-source software" was introduced to emphasize accessibility of the source code and collaborative development.
Importantly, publicly visible source code remains fully protected by copyright unless an explicit license grants usage rights.

FOSS licenses can be further divided into permissive and copyleft licenses.
Permissive licenses allow modification and redistribution under different licensing terms, including proprietary ones.
Copyleft licenses, by contrast, require that derivative works be distributed under the same license, thereby preserving openness.
The following table summarizes the rights associated with common licensing models.

```{table} Software Licenses
:name: software_licenses_overview

| Rights granted       | Public domain (e.g. CC0) | Permissive license (e.g. MIT) | Copyleft license (e.g. GPL) | Freeware | Proprietary software | Trade secret |
| -------------------- | ------------------------ | ----------------------------- | --------------------------- | -------- | -------------------- | ------------ |
| Copyright retention  | -                        | +                             | +                           | +        | +                    | +            |
| Copying/distribution | +                        | +                             | +                           | Often    | -                    | -            |
| Modification         | +                        | +                             | +                           | -        | -                    | -            |
| Re-licensing         | +                        | +                             | -                           | -        | -                    | -            |
```

The Open Source Initiative lists more than 100 approved licenses {cite}`OpenSourceInitiative`.
The following highlights several widely used examples.

The *GNU General Public License (GPL)* is one of the most widely used open-source licenses.
It guarantees the rights to use, study, modify, and redistribute software and enforces these freedoms through its copyleft provision, requiring derivative works to be licensed under the same terms.
CADET-Process is released under GPLv3 to ensure that improvements remain openly accessible.

The *MIT license* represents a permissive alternative with minimal restrictions.
It allows redistribution and re-licensing, including incorporation into proprietary software, while requiring attribution and limiting liability.

The *Creative Commons (CC)* licenses are commonly used for non-software content such as text, figures, and multimedia.
They offer a modular framework in which conditions such as attribution and share-alike requirements can be combined.
Due to compatibility issues and their focus on creative works, CC licenses are generally not recommended for software but are widely used for documentation and scientific publications (such as this one).

## Benefits of open-source software

Laurent identifies three primary benefits of open-source distribution: innovation, reliability, and longevity {cite}`Laurent2004`.
Open development fosters innovation by enabling contributions from a diverse community.
It improves reliability, as broader scrutiny increases the likelihood of identifying and resolving defects.
It also supports longevity, since projects can be maintained and extended beyond their original developers.

Open-source development further promotes community engagement.
Users can report issues and propose improvements through public platforms (see {numref}`version_control`), and exchange workflows and best practices via the CADET community forum (https://forum.cadet-web.de), which is complemented by an annual workshop and monthly office hours.

There is also a growing movement advocating that publicly funded research software should be openly accessible {cite}`unesco_open_science, Schiltz2007`.
Open availability is a prerequisite for reproducibility, as scientific results cannot be independently verified without access to the underlying tools and data.
Releasing CADET-Process as open-source software therefore reflects a commitment to transparency and reproducibility.
The following chapter extends this perspective to research data management.
