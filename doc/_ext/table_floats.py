"""Render regular Sphinx tables as LaTeX floats."""

from docutils import nodes


def wrap_regular_tables(app, doctree, docname):
    """Wrap non-longtable nodes in standard LaTeX table floats."""
    if app.builder.format != "latex":
        return

    for table in list(doctree.findall(nodes.table)):
        row_count = sum(1 for _ in table.findall(nodes.row))
        if "longtable" in table.get("classes", []) or row_count > 30:
            continue

        parent = table.parent
        index = parent.index(table)
        parent.insert(
            index,
            nodes.raw("", r"\begin{table}[htbp]", format="latex"),
        )
        parent.insert(
            index + 2,
            nodes.raw("", r"\end{table}", format="latex"),
        )


def setup(app):
    app.connect("doctree-resolved", wrap_regular_tables)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
