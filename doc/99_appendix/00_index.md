```{raw} latex
% Change page style for style for Appendix
\titleformat{\chapter}[display]
    {\normalfont\huge\bfseries\titlerule\vspace{0.25cm}}
    {}
    {0pt}
    {}
    [\vspace{0.25cm}\titlerule]

\appendix

% Sphinx builds the float counters from \arabic{chapter} (sphinxlatexnumfig.sty),
% which stays numeric after \appendix switches \thechapter to letters.
% Rebuild them from \thechapter so appendix floats number A.1, not 1.1.
\renewcommand{\thefigure}{\thechapter.\arabic{figure}}
\renewcommand{\thetable}{\thechapter.\arabic{table}}
\renewcommand{\theequation}{\thechapter.\arabic{equation}}
\renewcommand{\theliteralblock}{\thechapter.\arabic{literalblock}}
```

# Appendix
