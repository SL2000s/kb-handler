from pydantic import Field
from typing import List

from kb_handler.paper_extraction.data_models.statements.base_statement import Statement


class Corable(Statement):
    corollary_ids: List[str] = Field(default_factory=list)