from typing import Optional

from .base_provable import Provable


class Corollary(Provable):
    parent_id: Optional[str] = None