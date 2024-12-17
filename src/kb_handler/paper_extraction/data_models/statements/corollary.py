from typing import Optional

from kb_handler.paper_extraction.data_models.statements.base_provable import Provable


class Corollary(Provable):
    parent_id: Optional[str] = None