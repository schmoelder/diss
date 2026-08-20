from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from CADETProcess import plotting
from thesis_figure_styles import (
    CHARACTERIZATION_SINGLE_OBJECTIVE_HEIGHT_IN,
    CHARACTERIZATION_SINGLE_OBJECTIVE_WIDTH_IN,
    CHROMATOGRAM_HEIGHT_IN,
    COMPARISON_WIDTH_IN,
    OBJECTIVE_COLUMN_WIDTH_IN,
    OBJECTIVE_MARKER_SIZE,
    OBJECTIVE_ROW_HEIGHT_IN,
    SINGLE_OBJECTIVE_ROW_HEIGHT_IN,
    TEXT_WIDTH_IN,
    THESIS_FIGURE_LAYOUT,
    WIDE_COMPARISON_WIDTH_IN,
)


@dataclass(frozen=True)
class SplitFigurePreset:
    row_height_in: float
    column_width_in: float
    max_width_in: float = TEXT_WIDTH_IN
    layout: str = THESIS_FIGURE_LAYOUT


#: Columns use the same width as the chapter 6 objective grids so that figures
#: with the same number of columns are the same size across both chapters.
#: Spanning the full text block instead left the two-column figures visibly
#: stretched next to their chapter 6 counterparts.
OBJECTIVE_COLUMNS_PER_FIGURE = 3
OBJECTIVE_GRID_PRESET = SplitFigurePreset(
    row_height_in=OBJECTIVE_ROW_HEIGHT_IN,
    column_width_in=OBJECTIVE_COLUMN_WIDTH_IN,
)
SINGLE_OBJECTIVE_GRID_PRESET = SplitFigurePreset(
    row_height_in=CHARACTERIZATION_SINGLE_OBJECTIVE_HEIGHT_IN,
    column_width_in=OBJECTIVE_COLUMN_WIDTH_IN,
)


#: Width for comparison figures that carry several twin axes plus an in-plot
#: legend. The legend needs room relative to the text, and the font size is
#: fixed in points, so widening the figure is what buys that room.
def resize_comparison_figure(
    fig: plt.Figure,
    width_in: float = COMPARISON_WIDTH_IN,
    height_in: float = CHROMATOGRAM_HEIGHT_IN,
) -> plt.Figure:
    fig.set_size_inches(width_in, height_in)
    fig.tight_layout()
    return fig


#: Resize figure for objective-related comparison plots (e.g., meta score plots)
#: to match the objective grid preset panel dimensions.
#: Uses the same column/row dimensions as OBJECTIVE_GRID_PRESET for consistency.
def resize_objective_comparison_figure(
    fig: plt.Figure,
    ncols: int = 1,
    nrows: int = 1,
    row_height_in: float = OBJECTIVE_ROW_HEIGHT_IN,
) -> plt.Figure:
    width_in = ncols * OBJECTIVE_COLUMN_WIDTH_IN
    if nrows == 1:
        # CHARACTERIZATION_SINGLE_OBJECTIVE_HEIGHT_IN is calibrated to match a
        # multi-row grid using the *default* OBJECTIVE_ROW_HEIGHT_IN (see
        # thesis_figure_styles.py); scale it if the figure being matched
        # against uses a different row height (e.g. shrunk to fit a page).
        height_in = SINGLE_OBJECTIVE_GRID_PRESET.row_height_in * (
            row_height_in / OBJECTIVE_ROW_HEIGHT_IN
        )
    else:
        height_in = nrows * row_height_in
    fig.set_size_inches(width_in, height_in)
    fig.tight_layout()
    return fig


def _set_scatter_marker_size(axes: np.ndarray, marker_size: float) -> None:
    for ax in axes.flatten():
        for collection in ax.collections:
            if hasattr(collection, "set_sizes"):
                collection.set_sizes([marker_size])


def balanced_chunks(items: Iterable[int], max_chunk_size: int) -> Iterable[tuple[int, ...]]:
    items = list(items)
    n_items = len(items)
    n_chunks = int(np.ceil(n_items / max_chunk_size))
    chunk_size = n_items // n_chunks
    n_larger_chunks = n_items % n_chunks

    start = 0
    for i_chunk in range(n_chunks):
        stop = start + chunk_size
        if i_chunk < n_larger_chunks:
            stop += 1
        yield tuple(items[start:stop])
        start = stop


def _format_objective_variable_label(label: str) -> str:
    labels = {
        "tubing_pre_column_length": "length",
        "tubing_post_column_length": "length",
        "tubing_detectors_length": "length",
        "tubing_pre_injection_length": "length",
        "tubing_pre_column_axial_dispersion": "axial dispersion",
        "tubing_post_column_axial_dispersion": "axial dispersion",
        "tubing_detectors_axial_dispersion": "axial dispersion",
        "axial_dispersion": r"$D_{ax}~/~\text{m}^{2}\,\text{s}^{-1}$",
        "mixer_volume": "mixer volume",
        "bed_porosity": "bed porosity",
        "particle_porosity": r"$\varepsilon^p~/~-$",
        "film_diffusion": r"$k_f~/~\text{m}\,\text{s}^{-1}$",
        "characteristic_charge": r"$\nu~/~-$",
        "adsorption_rate": r"$K_{\text{eq}}~/~\text{m}_\text{l}^3\,\text{m}_\text{s}^{-3}$",
    }
    return labels.get(label, label.replace("_", " "))


def create_split_objective_figures(
    optimization_results,
    rows_per_figure: int = 4,
    columns_per_figure: int = OBJECTIVE_COLUMNS_PER_FIGURE,
    row_height_in: float | None = None,
    column_width_in: float | None = None,
    max_width_in: float = OBJECTIVE_GRID_PRESET.max_width_in,
    marker_size: float = OBJECTIVE_MARKER_SIZE,
) -> tuple[
    list[plt.Figure],
    np.ndarray,
    list[tuple[tuple[int, ...], tuple[int, ...]]],
]:
    """Plot objective values on split axes using CADET-Process plotting."""
    nrows = optimization_results.f.shape[1]
    if optimization_results.m is not None:
        nrows += optimization_results.m.shape[1]
    ncols = optimization_results.x.shape[1]
    if row_height_in is None:
        if nrows == 1:
            row_height_in = SINGLE_OBJECTIVE_GRID_PRESET.row_height_in
        else:
            row_height_in = OBJECTIVE_GRID_PRESET.row_height_in
    if column_width_in is None:
        if nrows == 1:
            column_width_in = SINGLE_OBJECTIVE_GRID_PRESET.column_width_in
        else:
            column_width_in = OBJECTIVE_GRID_PRESET.column_width_in

    figures = []
    axes_full = np.empty((nrows, ncols), dtype=object)
    figure_groups = []
    row_groups = list(balanced_chunks(range(nrows), rows_per_figure))
    column_groups = list(balanced_chunks(range(ncols), columns_per_figure))

    with plotting.mpl_style_context(OBJECTIVE_GRID_PRESET.layout):
        for row_group in row_groups:
            for column_group in column_groups:
                fig_width = min(max_width_in, column_width_in * len(column_group))
                fig, axes = plotting.setup_figure(
                    layout=OBJECTIVE_GRID_PRESET.layout,
                    nrows=len(row_group),
                    ncols=len(column_group),
                    figsize=(fig_width, row_height_in * len(row_group)),
                    squeeze=False,
                )
                figures.append(fig)
                figure_groups.append((row_group, column_group))

                for local_row, global_row in enumerate(row_group):
                    for local_col, global_col in enumerate(column_group):
                        axes_full[global_row, global_col] = axes[local_row, local_col]

        optimization_results.plot_objectives(
            ax=axes_full,
            tight_layout=False,
        )
        _set_scatter_marker_size(axes_full, marker_size)

        for row_group, column_group in figure_groups:
            for global_row in row_group:
                for global_col in column_group:
                    ax = axes_full[global_row, global_col]
                    if global_row != row_group[-1]:
                        ax.set_xlabel("")
                        ax.tick_params(labelbottom=False)
                    else:
                        ax.set_xlabel(
                            _format_objective_variable_label(ax.get_xlabel())
                        )
                    if global_col != column_group[0]:
                        ax.set_ylabel("")
                        ax.tick_params(labelleft=False)

        for fig in figures:
            fig.tight_layout()

    return figures, axes_full, figure_groups


def save_split_objective_figures(
    optimization_results,
    output_dir: Path,
    file_stem: str = "objectives",
    rows_per_figure: int = 4,
    columns_per_figure: int = OBJECTIVE_COLUMNS_PER_FIGURE,
    **kwargs,
) -> list[Path]:
    """Save split objective figures as thesis-ready artifacts."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stale_paths = [output_dir / f"{file_stem}.png"]
    stale_paths.extend(
        path
        for path in output_dir.glob(f"{file_stem}_*.png")
        if path.stem.removeprefix(f"{file_stem}_").isdigit()
    )
    for path in stale_paths:
        if path.exists():
            path.unlink()

    figures, _, _ = create_split_objective_figures(
        optimization_results,
        rows_per_figure=rows_per_figure,
        columns_per_figure=columns_per_figure,
        **kwargs,
    )

    output_paths = []
    for i_fig, fig in enumerate(figures):
        suffix = "" if i_fig == 0 else f"_{i_fig + 1}"
        output_path = output_dir / f"{file_stem}{suffix}.png"
        fig.savefig(output_path, dpi=300)
        plt.close(fig)
        output_paths.append(output_path)

    return output_paths
