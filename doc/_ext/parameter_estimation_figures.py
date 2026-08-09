from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from CADETProcess import plotting


TEXT_WIDTH_IN = 156 / 25.4
THESIS_FIGURE_LAYOUT = "1.5_col"


@dataclass(frozen=True)
class SplitFigurePreset:
    row_height_in: float
    column_width_in: float
    max_width_in: float = TEXT_WIDTH_IN
    layout: str = THESIS_FIGURE_LAYOUT


OBJECTIVE_GRID_PRESET = SplitFigurePreset(
    row_height_in=1.5,
    column_width_in=2.05,
)


def chunked(items: Iterable[int], chunk_size: int) -> Iterable[tuple[int, ...]]:
    chunk = []
    for item in items:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield tuple(chunk)
            chunk = []

    if chunk:
        yield tuple(chunk)


def _format_objective_variable_label(label: str) -> str:
    labels = {
        "tubing_pre_column_length": "length",
        "tubing_post_column_length": "length",
        "tubing_detectors_length": "length",
        "tubing_pre_injection_length": "length",
        "tubing_pre_column_axial_dispersion": "axial dispersion",
        "tubing_post_column_axial_dispersion": "axial dispersion",
        "tubing_detectors_axial_dispersion": "axial dispersion",
        "axial_dispersion": "axial dispersion",
        "mixer_volume": "mixer volume",
        "bed_porosity": "bed porosity",
        "particle_porosity": "particle porosity",
        "film_diffusion": "film diffusion",
        "characteristic_charge": "characteristic charge",
        "adsorption_rate": "adsorption rate",
    }
    return labels.get(label, label.replace("_", " "))


def create_split_objective_figures(
    optimization_results,
    rows_per_figure: int = 2,
    columns_per_figure: int = 2,
    row_height_in: float = OBJECTIVE_GRID_PRESET.row_height_in,
    column_width_in: float = OBJECTIVE_GRID_PRESET.column_width_in,
    max_width_in: float = OBJECTIVE_GRID_PRESET.max_width_in,
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

    figures = []
    axes_full = np.empty((nrows, ncols), dtype=object)
    figure_groups = []
    row_groups = list(chunked(range(nrows), rows_per_figure))
    column_groups = list(chunked(range(ncols), columns_per_figure))

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

        for fig in figures:
            fig.tight_layout()

    return figures, axes_full, figure_groups


def save_split_objective_figures(
    optimization_results,
    output_dir: Path,
    file_stem: str = "objectives",
    rows_per_figure: int = 2,
    columns_per_figure: int = 2,
    **kwargs,
) -> list[Path]:
    """Save split objective figures as thesis-ready artifacts."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

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
