from abc import ABC
from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4

from ...utils.tex_processing import (
    statement2motivation,
    tex2html,
)

class Statement(BaseModel, ABC):
    statement_id: str = Field(default_factory=lambda: str(uuid4()))
    paper_id: Optional[str] = None
    library_nr: Optional[int] = None
    library_name: Optional[str] = None
    title: Optional[str] = None
    statement_original_tex: Optional[str] = None
    statement_html: Optional[str] = None
    statement_type: str = None
    statement_motivation_html: Optional[str] = None
    html_url: Optional[str] = None

    def extend_statement_html(self, overwrite: bool = True):
        if overwrite or self.statement_html is None:
            html = tex2html(self.statement_original_tex)
            self.statement_html = html

    def extend_motivation_html(self, overwrite: bool = True):
        if overwrite or self.statement_motivation_html is None:
            self.statement_motivation_html = statement2motivation(
                self.statement_html
            )