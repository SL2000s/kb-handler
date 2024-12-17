from typing import Optional

from kb_handler.paper_extraction.data_models.statements.base_statement import Statement
from kb_handler.paper_extraction.data_models.statements.proof import Proof


class Provable(Statement):
    proof: Optional[Proof] = None