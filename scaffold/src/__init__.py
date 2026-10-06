"""scaffold — checkable SymPy notes for papers and textbooks, plus a central knowledge base."""
from .books import BookNotes
from .category import Functor, describe_diagram, morphism_name, to_xypic
from .claims import Claim, Status, sympy_equal
from .kb import Entry, KnowledgeBase, import_notes
from .notes import PaperNotes
from .render import to_markdown

__all__ = ["PaperNotes", "BookNotes", "Claim", "Status", "Functor", "sympy_equal",
           "describe_diagram", "morphism_name", "to_xypic", "to_markdown",
           "KnowledgeBase", "Entry", "import_notes"]
__version__ = "0.1.0"
