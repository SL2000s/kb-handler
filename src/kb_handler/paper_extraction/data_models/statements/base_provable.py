from typing import Optional

from .base_statement import Statement
from .proof import Proof


class Provable(Statement):
    proof: Optional[Proof] = None