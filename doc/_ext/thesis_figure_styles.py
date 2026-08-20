"""Shared physical dimensions for generated thesis figures."""

MM_PER_INCH = 25.4

TEXT_WIDTH_IN = 156 / MM_PER_INCH
THESIS_FIGURE_LAYOUT = "1.5_col"

OBJECTIVE_MARKER_SIZE = 4.0
OBJECTIVE_COLUMN_WIDTH_IN = 2.05
OBJECTIVE_ROW_HEIGHT_IN = 1.5
SINGLE_OBJECTIVE_ROW_HEIGHT_IN = 1.8
CHARACTERIZATION_SINGLE_OBJECTIVE_WIDTH_IN = 92 / MM_PER_INCH
#: Calibrated (not derived from a page dimension) so a single-row objective
#: panel's rendered aspect ratio matches a row of a multi-row objective grid;
#: see the figure sizing guideline in PROJECT.md.
CHARACTERIZATION_SINGLE_OBJECTIVE_HEIGHT_IN = 1.9

CHROMATOGRAM_HEIGHT_IN = 55 / MM_PER_INCH
CHROMATOGRAM_MIN_WIDTH_IN = 90 / MM_PER_INCH
CHROMATOGRAM_COLUMN_WIDTH_IN = 2.05
#: Same as SPARSE_CHROMATOGRAM_COLUMN_WIDTH_IN: two-column Pareto-edge
#: chromatogram grids left visible horizontal margin at 2.05in/col, and
#: matching the sparse-chromatogram width keeps every "two column
#: chromatogram figure" in chapter 6 the same size.
MOO_CHROMATOGRAM_COLUMN_WIDTH_IN = 2.8
SPARSE_CHROMATOGRAM_COLUMN_WIDTH_IN = 2.8

COMPARISON_WIDTH_IN = 100 / MM_PER_INCH
WIDE_COMPARISON_WIDTH_IN = 130 / MM_PER_INCH
