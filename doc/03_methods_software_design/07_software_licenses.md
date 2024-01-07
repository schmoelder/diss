(software_licenses)=
# Software licenses

In order to protect and encourage the creation of intellectual goods, intellectual property laws give creators property rights to the works they create.
Internationally, these laws are regulated under the rules of the World Trade Organization's (WTO) Agreement on Trade-Related Aspects of Intellectual Property Rights, which requires WTO members to provide the rights to copyright, patents, and trademarks {cite}`WTO1994`.

*Copyright* automatically attaches to every novel expression of an idea, whether through text, sounds, or imagery, without the need for registration.
The copyright laws grant the exclusive rights to reproduction, modification, and distribution of the work for a certain time.

*Patents*, on the other hand, protect the underlying substance of the idea itself, rather than its specific expression.
Like copyright, it prevents others from copying, selling or advertising the invention, but there is a limited time in which the idea can be protected until it enters the public domain.
However, to get patent protection, the inventor must first apply for and be granted a patent from the responsible patent office.

Finally, a *trademark* is a word, phrase, symbol, or design that identifies and distinguishes the source of the goods of one party from those of others.
It prevents others from using similar marks in a way that would cause confusion about the origin of the goods.
Unlike copyright and patents, trademark rights can be re-registered as long as the marks are actively used {cite}trips.

## Licenses

While computer software is primarily designed to achieve functional goals, there are many different ways in which these instructions can be formulated.
As a result, computer software (in the form of source code or binary executable) is protected by copyright because human creativity is involved.
Although this provides some level of protection for the software, the operations and underlying ideas of the application can also be patented to further safeguard intellectual property.

However, a problem arises when software is published without a license.
Because no permission for use has been granted, the software cannot legally be used until it enters the public domain after the copyright term has passed.
The copyright holder can demand at any point that the software no longer be used and fine those who continue to use it.
Therefore, a proper license should be added to the software as soon as it is shared with others.
These licenses define the permissions and limitations of using and redistributing the software {cite}`Laurent2004`.

Software licenses can be classified into two categories: (1) proprietary licenses and free and (2) open-source software (FOSS) licenses.
In the case of proprietary software, users are typically required to accept an end-user license agreement (EULA) that specifies the terms and conditions for using the software, such as the number of allowed installations.
In contrast, the copyright holders of FOSS grant users the freedom to use, study, modify, and distribute the software.

However, there is some ambiguity in the terms "open source software" and "free software".
"Free software" does not only mean that the software is free of charge.
For example, "freeware" is also free of charge but does not necessarily guarantee access to the source code or permission to share the software.
In this context, "free software" should be interpreted as the freedom in "free speech" (not "free beer").
Later, the term "open source software" was introduced as an alternative term.
However, as previously explained, even published source code cannot be used unless the license explicitly allows it.
Therefore, terms such as FOSS (free and open-source software) and *libre* software are used nowadays to mean the same concept.
FOSS licenses can be divided into two categories: (1) permissive licenses, which allow modification and re-licensing under other licenses, and (2) copyleft licenses, which protect against proprietarization by requiring the use of the same license for derivative works.

The following table gives an overview of the different rights that are granted to users by different types of software licenses.

```{table} Software Licenses
:name: software_licenses_overview


| Rights granted       | Public domain (e.g. CC0) | Permissive license (e.g. MIT) | Copyleft license (e.g. GPL) | Freeware | Proprietary software | Trade secret |
| -------------------- | ------------------------ | ----------------------------- | --------------------------- | -------- | -------------------- | ------------ |
| Copyright retention  | -                        | +                             | +                           | +        | +                    | +            |
| Copying/distribution | +                        | +                             | +                           | Often    | -                    | -            |
| Modification         | +                        | +                             | +                           | -        | -                    | -            |
| Re-licensing         | +                        | +                             | -                           | -        | -                    | -            |

```

On their website, the Open Source Initiative lists more than 100 different software licenses {cite}`opensource`.
The following section discusses some of the most significant licenses.

The *GNU General Public License (GPL)* is the most popular open-source license.
It guarantees end-users the freedom to run, study, share, and modify the software.
Its primary objective is to keep software free, making it a copyleft license.
Any derivative work created must be published under the same license.
This license, specifically *GPLv3* is also used for the release of **CADET-Processs** in the hope that other researchers may find it useful for their work.

The *MIT* license is an example of a more lenient license with very few restrictions.
It requires copyright to be reserved, limits liability, and allows re-licensing under any other license, including proprietary licenses.

The *Creative Commons license (CC)* is frequently used to distribute copyrighted work.
It isn't restricted to any particular type of work and can be used for any creative work, such as texts, music, or videos.
Its modular approach allows for different conditions to be combined.
For instance, the *CC-BY-SA* license necessitates that the original creator be credited, and any changes be distributed under the same terms.
Because some of the conditions are incompatible with other licenses, CC is usually not used for software but can be used for documentation, supplementary material, or scientific publications (such as this one).

## Benefits of open-source software

There are multiple benefits of releasing software under an open-source license.
Firstly, by making software freely available, the general public can benefit from the development work that has already been done.
Secondly, opening up development to the public can encourage the adoption of standards, leading to increased outside contributions to the project and its ecosystem.
Moreover, there is a growing movement advocating for publicly funded software to be made publicly accessible to everyone {cite}`UNESCO2021, Schiltz2007`.
Therefore, releasing software under an open-source license can be a great way to promote collaboration and innovation.

In his book "Understanding Open Source and Free Software Licensing", author Andrew Laurent identifies three primary benefits of open distribution and modification of software {cite}`Laurent2004`.
*Innovation*, as more programmers introduce new ideas to improve a program; *reliability*, as more perspectives lead to the discovery and resolution of more bugs, resulting in better quality code; and *longevity*, as other programmers can continue a project even if the original developer(s) stop contributing.

Another critical aspect, particularly relevant to this work, is the reproducibility of scientific research.
Results cannot be verified by others without access to both the raw data and the libraries and tools required to analyze the data.
And without validation, it's difficult to build further on such results reliably.

Because intellectual property is protected through copyright laws and licenses, and there are tools available that remove many of the technical limitations to publishing software, more scientific software should be made open to everyone.
Sharing knowledge and providing people with access to tools is the most effective ways to promote innovation and collaboration, particularly in a time of global inequality.
