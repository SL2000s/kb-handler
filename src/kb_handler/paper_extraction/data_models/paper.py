import os
import regex
import urllib

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from uuid import uuid4

from kb_handler.paper_extraction.builders.statements_builder import build_statements
from kb_handler.paper_extraction.config.config import STATEMENT_TYPES_METADATA
from kb_handler.paper_extraction.data_models.statements.base_provable import Provable
from kb_handler.paper_extraction.data_models.statements.statements import Statements
from kb_handler.paper_extraction.utils.tex_processing import process_tex_extraction, mathjax_macros, mathjax_environments


TEX_LABEL_PATTERN = regex.compile(r'\\label\{([^{}]+)\}')
TEX_REF_PATTERN = regex.compile(r'(\$\\ref\{([^{}]+)\}\$)')
TEX_CREF_PATTERN = regex.compile(r'(\$\\cref\{([^{}]+)\}\$)')
TEX_CCREF_PATTERN = regex.compile(r'(\$\\Cref\{([^{}]+)\}\$)')
STATEMENT_INTERLINK_TEMPLATE = '<a href="{url}">{text}</a>'


def add_root(path, root):  # TODO: look over how paths are constructed -- should not store absolute paths
    if not path:
        return path
    path = os.path.join(root or '', path)
    return path


class Paper(BaseModel):
    paper_id: str = Field(default_factory=lambda: str(uuid4()))
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    year: Optional[int] = None
    source_url: Optional[str] = None
    html_url: Optional[str] = None
    bibtex: Optional[str] = None
    original_tex: Optional[str] = None
    processed_original_tex: Optional[str] = None
    statements: Optional[Statements] = None
    mathjax_macros: Optional[List] = None
    mathjax_environments: Optional[List] = None
    label2statementid: Optional[Dict[str, str]] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.processed_original_tex is None:
            self.processed_original_tex = process_tex_extraction(self.original_tex)
        if self.statements is None:
            self.statements = build_statements(self.original_tex, self.paper_id)

    def statementid2statement(self, statement_id: str):
        for statement in self.statements.all_statements():
            if statement.statement_id == statement_id:
                return statement
        return None

    def type_statements(self, statement_type: str):
        field_str = STATEMENT_TYPES_METADATA[statement_type]['plural']
        for statement in getattr(self.statements, field_str, []):
            yield statement

    def extend_label2statementid(self, overwrite: bool = True):
        if overwrite or self.label2statementid is None:
            label2statementid = {}
            for statement in self.statements.all_statements():
                tex = statement.statement_original_tex
                if issubclass(type(statement), Provable):
                    if statement.proof:
                        tex += statement.proof.statement_original_tex
                matches = TEX_LABEL_PATTERN.findall(tex)
                for match in matches:  # assumes first match is the label for the statement  # TODO: check this comment
                    label2statementid[match] = statement.statement_id
            self.label2statementid = label2statementid

    def extend_statements_html_refs(self, pages_root):
        if self.label2statementid is None:
            self.extend_label2statementid(True)
        for statement in self.statements.all_statements_and_proofs():
            self._extend_statement_html_refs(statement, pages_root)
    
    def _extend_statement_html_refs(self, statement, pages_root):
        statement_html = statement.statement_html

        matches = TEX_REF_PATTERN.findall(statement_html)
        for sub_match, label_match in matches:
            if label_match in self.label2statementid:
                ref_statement_id = self.label2statementid[label_match]
                ref_statement = self.statementid2statement(ref_statement_id)
                if ref_statement.statement_id != statement.statement_id:
                    ref_url = ref_statement.html_url
                    statement_html = statement_html.replace(
                        sub_match,
                        STATEMENT_INTERLINK_TEMPLATE.format(
                            url=f'{add_root(ref_url, pages_root)}#{urllib.parse.quote_plus(label_match)}',
                            text=ref_statement.library_name
                        )
                    )
        # TODO: merge this loop with loop above
        matches = TEX_CREF_PATTERN.findall(statement_html) + TEX_CCREF_PATTERN.findall(statement_html)
        for sub_match, label_match in matches:
            if label_match in self.label2statementid:
                ref_statement_id = self.label2statementid[label_match]
                ref_statement = self.statementid2statement(ref_statement_id)
                if ref_statement.statement_id != statement.statement_id:
                    ref_url = ref_statement.html_url
                    statement_html = statement_html.replace(
                        sub_match,
                        STATEMENT_INTERLINK_TEMPLATE.format(
                            url=f'{add_root(ref_url, pages_root)}#{urllib.parse.quote_plus(label_match)}',
                            text=ref_statement.library_name
                        )
                    )
            else:
                statement_html = statement_html.replace(
                    sub_match,
                    f'\\ref{{{label_match}}}'
                )

        statement.statement_html = statement_html

    def extend_mathjax_macros(self, overwrite: bool = True):
        if overwrite or self.mathjax_macros is None:
            macros = mathjax_macros(self.processed_original_tex)
            self.mathjax_macros = macros

    def extend_mathjax_environments(self, overwrite: bool = True):
        if overwrite or self.mathjax_environments is None:
            environments = mathjax_environments(self.processed_original_tex)
            self.mathjax_environments = environments