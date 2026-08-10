from collections.abc import Iterable
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker

from CADETProcess import plotting
from operating_modes.post_processing import (
    format_mm_ss,
    get_variables,
    metrics,
    plot_moo_chromatograms,
)


TEXT_WIDTH_IN = 156 / 25.4
OBJECTIVE_MARKER_SIZE = 4.0
OBJECTIVE_UNIT_NOTE = "Objective and KPI units follow the corresponding result table."
THESIS_FIGURE_LAYOUT = "1.5_col"


@dataclass(frozen=True)
class SplitFigurePreset:
    row_height_in: float
    column_width_in: float
    min_width_in: float = 3.0
    max_width_in: float = TEXT_WIDTH_IN
    layout: str = THESIS_FIGURE_LAYOUT


OBJECTIVE_GRID_PRESET = SplitFigurePreset(
    row_height_in=1.5,
    column_width_in=2.05,
)
SOO_OBJECTIVE_GRID_PRESET = SplitFigurePreset(
    row_height_in=1.8,
    column_width_in=2.05,
)
MOO_CHROMATOGRAM_GRID_PRESET = SplitFigurePreset(
    row_height_in=1.45,
    column_width_in=2.05,
)
CHROMATOGRAM_PANEL_PRESET = SplitFigurePreset(
    row_height_in=2.35,
    column_width_in=2.05,
)


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


def _create_split_axes(
    nrows: int,
    ncols: int,
    rows_per_figure: int,
    columns_per_figure: int,
    row_height_in: float,
    column_width_in: float,
    min_width_in: float = 3.0,
    max_width_in: float = TEXT_WIDTH_IN,
    layout: str = THESIS_FIGURE_LAYOUT,
) -> tuple[list[plt.Figure], np.ndarray, list[tuple[tuple[int, ...], tuple[int, ...]]]]:
    figures = []
    row_groups = list(balanced_chunks(range(nrows), rows_per_figure))
    column_groups = list(balanced_chunks(range(ncols), columns_per_figure))
    figure_groups = []
    axes_full = np.empty((nrows, ncols), dtype=object)

    for row_group in row_groups:
        for column_group in column_groups:
            width_in = min(
                max_width_in,
                max(min_width_in, column_width_in * len(column_group)),
            )
            fig, axes = plotting.setup_figure(
                layout=layout,
                nrows=len(row_group),
                ncols=len(column_group),
                figsize=(width_in, row_height_in * len(row_group)),
                squeeze=False,
            )
            figures.append(fig)
            figure_groups.append((row_group, column_group))

            for local_row, global_row in enumerate(row_group):
                for local_col, global_col in enumerate(column_group):
                    axes_full[global_row, global_col] = axes[local_row, local_col]

    return figures, axes_full, figure_groups


def create_figure_directives(
    glue_name: str,
    figure_name: str,
    caption: str,
    figure_groups: list[tuple[tuple[int, ...], tuple[int, ...]]],
    scale: str = "100%",
    row_label: str = "rows",
    column_label: str = "decision variables",
) -> str:
    directives = []
    include_part_note = len(figure_groups) > 1
    if column_label == "decision variables":
        caption = f"{caption} {OBJECTIVE_UNIT_NOTE}"

    for i, (row_group, column_group) in enumerate(figure_groups, start=1):
        if i == 1:
            name = figure_name
        else:
            name = f"{figure_name}_{i}"

        if include_part_note:
            first_row = row_group[0] + 1
            last_row = row_group[-1] + 1
            first_col = column_group[0] + 1
            last_col = column_group[-1] + 1
            caption_text = (
                f"{caption} Panels {row_label} {first_row}--{last_row}, "
                f"{column_label} {first_col}--{last_col}."
            )
        else:
            caption_text = caption

        directives.append(
            "\n".join(
                [
                    f"```{{glue:figure}} {glue_name}_{i}",
                    f":name: {name}",
                    f":scale: {scale}",
                    "",
                    caption_text,
                    "```",
                ]
            )
        )

    return "\n\n".join(directives)


def resize_chromatogram_figure(
    fig: plt.Figure,
    ncols: int = 1,
    row_height_in: float = CHROMATOGRAM_PANEL_PRESET.row_height_in,
    column_width_in: float = CHROMATOGRAM_PANEL_PRESET.column_width_in,
    min_width_in: float = CHROMATOGRAM_PANEL_PRESET.min_width_in,
    max_width_in: float = CHROMATOGRAM_PANEL_PRESET.max_width_in,
) -> plt.Figure:
    width_in = min(
        max_width_in,
        max(min_width_in, column_width_in * ncols),
    )
    fig.set_size_inches(width_in, row_height_in)
    fig.tight_layout()
    return fig


def _format_variable_axis(ax, variable_info):
    ax.set_xlabel(f"${variable_info['symbol']}~/~{variable_info['unit']}$")
    if variable_info.get("format_mm_ss"):
        ax.xaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, _: rf"${format_mm_ss(x)}$")
        )
    else:
        ax.xaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, _: f"{x * variable_info['factor']:.4g}")
        )


def _prune_redundant_axis_labels(
    axes: np.ndarray,
    figure_groups: list[tuple[tuple[int, ...], tuple[int, ...]]],
) -> None:
    for row_group, column_group in figure_groups:
        bottom_visible_rows = {}
        for global_col in column_group:
            visible_rows = [
                global_row
                for global_row in row_group
                if axes[global_row, global_col].axison
            ]
            if visible_rows:
                bottom_visible_rows[global_col] = visible_rows[-1]

        for global_row in row_group:
            for global_col in column_group:
                ax = axes[global_row, global_col]
                if global_row != bottom_visible_rows.get(global_col):
                    ax.set_xlabel("")
                    ax.tick_params(labelbottom=False)
                if global_col != column_group[0]:
                    ax.set_ylabel("")
                    ax.tick_params(labelleft=False)


def _label_bottom_x_axes(
    axes: np.ndarray,
    figure_groups: list[tuple[tuple[int, ...], tuple[int, ...]]],
) -> None:
    xlabels = [ax.get_xlabel() for ax in axes.flatten() if ax.get_xlabel()]
    if not xlabels:
        return

    xlabel = xlabels[0]
    for row_group, column_group in figure_groups:
        for global_col in column_group:
            visible_rows = [
                global_row
                for global_row in row_group
                if axes[global_row, global_col].axison
            ]
            if visible_rows:
                ax = axes[visible_rows[-1], global_col]
                ax.set_xlabel(xlabel)


def _set_scatter_marker_size(axes: np.ndarray, marker_size: float) -> None:
    for ax in axes.flatten():
        for collection in ax.collections:
            if hasattr(collection, "set_sizes"):
                collection.set_sizes([marker_size])


def _n_x(optimization_results) -> int:
    return optimization_results.x.shape[1]


def _n_f(optimization_results) -> int:
    return optimization_results.f.shape[1]


def _n_m(optimization_results) -> int:
    meta_scores = optimization_results.m
    if meta_scores is None:
        return 0

    return meta_scores.shape[1]


def plot_soo_objective_figures(
    case,
    optimization_results,
    columns_per_figure: int = 3,
    rows_per_figure: int | None = None,
    row_height_in: float = SOO_OBJECTIVE_GRID_PRESET.row_height_in,
    column_width_in: float = SOO_OBJECTIVE_GRID_PRESET.column_width_in,
    marker_size: float = OBJECTIVE_MARKER_SIZE,
) -> tuple[
    list[plt.Figure],
    np.ndarray,
    list[tuple[tuple[int, ...], tuple[int, ...]]],
]:
    operating_mode = case.options.process_options.operating_mode
    variables = get_variables(
        operating_mode,
        case.options.optimization_options.include_cycle_time,
    )

    ncols = _n_x(optimization_results)
    nrows = _n_f(optimization_results) + _n_m(optimization_results)
    if rows_per_figure is None:
        rows_per_figure = nrows

    with plotting.mpl_style_context(OBJECTIVE_GRID_PRESET.layout):
        figures, axes, figure_groups = _create_split_axes(
            nrows,
            ncols,
            rows_per_figure,
            columns_per_figure,
            row_height_in,
            column_width_in,
            SOO_OBJECTIVE_GRID_PRESET.min_width_in,
            SOO_OBJECTIVE_GRID_PRESET.max_width_in,
            SOO_OBJECTIVE_GRID_PRESET.layout,
        )
        optimization_results.plot_objectives(
            autoscale=False,
            ax=axes,
            tight_layout=False,
        )
        _set_scatter_marker_size(axes, marker_size)

        variable_infos = list(variables.values())[:ncols]
        for i_var, variable_info in enumerate(variable_infos):
            ax = axes[0, i_var]
            _format_variable_axis(ax, variable_info)
            ax.set_ylabel(f"${metrics['meta']['symbol']}$")
            ax.yaxis.set_major_formatter(
                ticker.FuncFormatter(
                    lambda y, _: f"{y * metrics['meta']['factor']:.4g}"
                )
            )

        _prune_redundant_axis_labels(axes, figure_groups)

        for fig in figures:
            fig.tight_layout()

    return figures, axes, figure_groups


def plot_moo_objective_figures(
    case,
    optimization_results,
    columns_per_figure: int = 4,
    rows_per_figure: int = 5,
    row_height_in: float = OBJECTIVE_GRID_PRESET.row_height_in,
    column_width_in: float = OBJECTIVE_GRID_PRESET.column_width_in,
    marker_size: float = OBJECTIVE_MARKER_SIZE,
) -> tuple[
    list[plt.Figure],
    np.ndarray,
    list[tuple[tuple[int, ...], tuple[int, ...]]],
]:
    optimization_problem = optimization_results.optimization_problem
    operating_mode = case.options.process_options.operating_mode
    variables = get_variables(
        operating_mode,
        case.options.optimization_options.include_cycle_time,
    )

    n_comp = optimization_problem.evaluation_objects[0].n_comp
    n_metrics = int(optimization_problem.n_objectives / n_comp)
    ncols = _n_x(optimization_results)
    nrows = _n_f(optimization_results) + _n_m(optimization_results)

    with plotting.mpl_style_context(OBJECTIVE_GRID_PRESET.layout):
        figures, axes, figure_groups = _create_split_axes(
            nrows,
            ncols,
            rows_per_figure,
            columns_per_figure,
            row_height_in,
            column_width_in,
            OBJECTIVE_GRID_PRESET.min_width_in,
            OBJECTIVE_GRID_PRESET.max_width_in,
            OBJECTIVE_GRID_PRESET.layout,
        )
        optimization_results.plot_objectives(
            autoscale=False,
            ax=axes,
            tight_layout=False,
        )
        _set_scatter_marker_size(axes, marker_size)

        for i_metric, (metric_name, metric_info) in enumerate(metrics.items()):
            if metric_name == "purity":
                break
            for i_comp in range(n_comp):
                variable_infos = list(variables.values())[:ncols]
                for i_var, variable_info in enumerate(variable_infos):
                    ax = axes[n_comp * i_metric + i_comp, i_var]
                    _format_variable_axis(ax, variable_info)
                    ax.set_ylabel(
                        f"${metric_info['symbol']}_{{{i_comp}}}$"
                    )
                    ax.yaxis.set_major_formatter(
                        ticker.FuncFormatter(
                            lambda y, _: f"{y * metric_info['factor']:.4g}"
                        )
                    )
                if metric_name == "meta":
                    break

        _prune_redundant_axis_labels(axes, figure_groups)

        for fig in figures:
            fig.tight_layout()

    return figures, axes, figure_groups


def plot_moo_chromatogram_figures(
    case,
    optimization_results,
    simulation_results,
    fractionators,
    columns_per_figure: int | None = None,
    rows_per_figure: int = 5,
    row_height_in: float = MOO_CHROMATOGRAM_GRID_PRESET.row_height_in,
    column_width_in: float = MOO_CHROMATOGRAM_GRID_PRESET.column_width_in,
    set_global_limits: bool = True,
) -> tuple[
    list[plt.Figure],
    np.ndarray,
    list[tuple[tuple[int, ...], tuple[int, ...]]],
]:
    optimization_problem = optimization_results.optimization_problem
    objective = case.options.optimization_options.objective

    n_comp = optimization_problem.evaluation_objects[0].n_comp
    n_metrics = int(optimization_problem.n_objectives / n_comp)
    n_edge_points = n_metrics * n_comp
    n_chrom = len(simulation_results[0].chromatograms)

    if n_chrom == 1:
        nrows = n_metrics + 1
        ncols = n_comp
    else:
        nrows = n_comp * n_metrics + 1
        ncols = n_chrom

    if columns_per_figure is None:
        columns_per_figure = ncols

    simulation_results_array = np.asarray(
        simulation_results[:n_edge_points],
        dtype=object,
    ).reshape(n_metrics, n_comp)
    fractionators_array = np.asarray(
        fractionators[:n_edge_points],
        dtype=object,
    ).reshape(n_metrics, n_comp)
    frac_meta = fractionators[-1]

    with plotting.mpl_style_context(MOO_CHROMATOGRAM_GRID_PRESET.layout):
        figures, axes, figure_groups = _create_split_axes(
            nrows,
            ncols,
            rows_per_figure,
            columns_per_figure,
            row_height_in,
            column_width_in,
            MOO_CHROMATOGRAM_GRID_PRESET.min_width_in,
            MOO_CHROMATOGRAM_GRID_PRESET.max_width_in,
            MOO_CHROMATOGRAM_GRID_PRESET.layout,
        )
        plot_moo_chromatograms(
            optimization_problem,
            objective,
            simulation_results_array,
            fractionators_array,
            frac_meta,
            ax=axes,
            set_global_limits=set_global_limits,
        )
        handles = []
        labels = []
        for ax in axes.flatten():
            legend = ax.get_legend()
            if legend is None:
                continue
            if not handles:
                handles, labels = ax.get_legend_handles_labels()
            legend.remove()

        _label_bottom_x_axes(axes, figure_groups)
        _prune_redundant_axis_labels(axes, figure_groups)

        for fig in figures:
            if handles:
                fig.legend(
                    handles,
                    labels,
                    loc="upper center",
                    ncols=len(labels),
                    frameon=False,
                )
            fig.tight_layout(rect=(0, 0, 1, 0.95))

    return figures, axes, figure_groups
