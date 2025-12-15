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
