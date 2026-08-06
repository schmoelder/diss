"""Place the bibliography in front of the appendix in the LaTeX build.

``sphinx_jupyterbook_latex`` unconditionally moves every bibliography to the very
end of the assembled document (``LatexRootDocPostTransforms``, priority 700), so
the bibliography ends up behind the appendix no matter how ``_toc.yml`` is
ordered.  This extension registers a post-transform that runs afterwards and
moves the bibliography back in front of the appendix.

If the appendix is renamed, adjust :data:`APPENDIX_DOCNAME`.  Should the upstream
extension ever stop relocating bibliographies, this transform becomes a no-op
rather than a breakage.
"""

from typing import Any, Optional

from docutils import nodes
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.builders.latex.nodes import thebibliography
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util import logging

logger = logging.getLogger(__name__)

APPENDIX_DOCNAME = "99_appendix/00_index"
"""Document that the bibliography has to be placed in front of."""


def findall(node: nodes.Element):
    """Return the node's iteration method (``findall`` replaces ``traverse`` in docutils 0.18)."""
    return getattr(node, "findall", node.traverse)


def is_root_document(document: nodes.document, app: Sphinx) -> bool:
    """Check whether a document is the root document, based on its source path."""
    return app.project.path2doc(document["source"]) == app.config.master_doc


class BibliographyBeforeAppendix(SphinxPostTransform):
    """Move the bibliography in front of the appendix.

    Runs after ``LatexRootDocPostTransforms`` (priority 700), which is what
    appends the bibliography to the end of the document in the first place.
    """

    formats = ("latex",)
    default_priority = 750

    def run(self, **kwargs: Any) -> None:
        # Only the assembled root document holds every chapter; the individual
        # per-file doctrees have nothing to reorder.
        if not is_root_document(self.document, self.app):
            return

        bibliographies = list(findall(self.document)(thebibliography))
        if not bibliographies:
            return

        appendix = self._find_appendix()
        if appendix is None:
            logger.warning(
                "no document %r found, leaving the bibliography at the end of "
                "the document",
                APPENDIX_DOCNAME,
            )
            return

        for bibliography in bibliographies:
            bibliography.parent.remove(bibliography)

        # The index is resolved after the removals, so it accounts for any
        # bibliography that used to sit in the same parent.
        parent = appendix.parent
        parent.insert(parent.index(appendix), bibliographies)

    def _find_appendix(self) -> Optional[addnodes.start_of_file]:
        """Return the node that starts the appendix, or None if it is absent."""
        for node in findall(self.document)(addnodes.start_of_file):
            if node["docname"] == APPENDIX_DOCNAME:
                return node
        return None


def setup(app: Sphinx) -> dict:
    app.add_post_transform(BibliographyBeforeAppendix)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
