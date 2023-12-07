# A modular framework for modeling and optimizing chromatographic processes

This repository contains (a draft of) my dissertation.
It is written using [JupyterBook](https://jupyterbook.org/intro.html), an open source tool for writing publication-quality content in Markdown including executable code and output.
This allows to directly use the code developed for calculating the case studies and displaying results.

## Build JupyterBook locally

To run and build all examples locally, please ensure that a recent version of [Anaconda Python](https://www.anaconda.com/products/individual) is installed.

### Activate environment

The conda environment is provided as `environment.yml`.
This includes all dependencies required to run the examples and build the JupyterBook.

1. `conda env create -f environment.yml`
2. `conda activate diss`

### Build html

Run the following command in your terminal:

```bash
jb build doc/
```

### Build pdf

```bash
jb build doc/ --builder pdflatex
```
