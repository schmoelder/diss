# A modular framework for modeling and optimizing chromatographic processes

% Creates a custom role for inserting raw latex
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
\pagenumbering{arabic}
```
