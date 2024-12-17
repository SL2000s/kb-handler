from typing import Optional

from .base_statement import Statement
from ...utils.tex_processing import (
    proof2explaination
)

class Proof(Statement):
    proof_explaination_html: Optional[str] = None

    def extend_explaination_html(self, overwrite: bool = True):
        if overwrite or self.proof_explaination_html is None:
            self.proof_explaination_html = proof2explaination(
                self.statement_html
            )