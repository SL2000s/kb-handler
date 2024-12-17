import os
import warnings

from pydantic import BaseModel, Field
from typing import Dict, List, Optional

from ..builders.paper_builder import build_arxiv_paper, dict_extraction2paper
from ..data_models.paper import Paper
from ..data_models.statements.base_provable import Provable
from ..utils.tex_processing import statement2title
from ..utils.utils import sanitize_filename

from ..config.config import (
    STATEMENT_TYPES_METADATA,
    PAPER_URL_TEMPLATE,
    STATEMENT_URL_TEMPLATE,
)


class PaperDatabase(BaseModel):
    db_path: Optional[str] = None
    papers: List[Paper] = Field(default_factory=list)
    extraction_dir: Optional[str] = '/tmp/paper_extraction'
    pages_root: Optional[str] = None

    # def __init__(self, **data):
    #     super().__init__(**data)

    def paperid2paper(self, paper_id: str):
        for paper in self.papers:
            if paper.paper_id == paper_id:
                return paper
        return None

    def statementid2statement(self, statement_id: str):
        for statement in self.all_statements():
            if statement.statement_id == statement_id:
                return statement
        return None

    def paper_source_url2paper(self, url: str):
        for paper in self.papers:
            if paper.source_url == url:
                return paper
        return None

    def arxiv_id2paper(self, arxiv_id: str):
        for paper in self.papers:
            if arxiv_id in paper.source_url:
                return paper
        return None

    def add_dict_papers(self, papers: Dict[str, Dict]):
        for paper_dict in papers.values():
            if not self.paper_source_url2paper(paper_dict['paper_url']):
                self.papers.append(dict_extraction2paper(paper_dict))

    def add_arxiv_paper(self, arxiv_id: str):
        if not self.arxiv_id2paper(arxiv_id):
            self.papers.append(
                build_arxiv_paper(
                    arxiv_id,
                    os.path.join(self.extraction_dir, 'arxiv_tex_extractions')
                )
            )
        else:
            warnings.warn(f'Arxiv paper {arxiv_id} already in database. Skipping it.')

    def add_arxiv_papers(self, arxiv_ids: List[str]):
        for arxiv_id in arxiv_ids:
            self.add_arxiv_paper(arxiv_id)

    def extend(self, overwrite: bool = True):
        self.extend_statement_nrs(overwrite)
        self.extend_label2statementids(overwrite)
        self.extend_statement_titles(overwrite)
        self.extend_html_fields(overwrite)

    def extend_statement_nrs(self, overwrite: bool = True):
        for statement_type, type_meta_data in STATEMENT_TYPES_METADATA.items():
            nr = 0 if overwrite else self.highest_library_nr(statement_type)
            for statement in self.type_statements(statement_type):
                if overwrite or not statement.library_nr:
                    nr += 1
                    statement.library_nr = nr
                    lib_name = f'{type_meta_data["capitalized_singular"]} {nr}'
                    statement.library_name = lib_name

    def extend_label2statementids(self, overwrite: bool = True):
        for paper in self.papers:
            paper.extend_label2statementid(overwrite)

    def extend_statement_titles(self, overwrite: bool = True):
        for statement in self.all_statements():
            if overwrite or statement.title is None:
                title = statement2title(statement.statement_original_tex)
                statement.title = title

    def extend_html_fields(self, overwrite: bool = True):
        self.extend_urls(overwrite)
        self.extend_mathjax_macros(overwrite)
        self.extend_mathjax_environments(overwrite)
        self.extend_html_statements(overwrite)
        self.extend_motivation_htmls(overwrite)
        self.extend_proof_explaination_htmls(overwrite)

    def extend_urls(self, overwrite: bool = True):
        self.extend_paper_urls(overwrite)
        self.extend_statement_urls(overwrite)

    def extend_paper_urls(self, overwrite: bool = True):
        for paper in self.papers:
            if overwrite or not paper.html_url:
                url_paper_id = sanitize_filename(paper.title or paper.paper_id)
                paper.html_url = PAPER_URL_TEMPLATE.format(paper_id=url_paper_id)

    def extend_statement_urls(self, overwrite: bool = True):
        for statement in self.all_statements():
            if overwrite or statement.html_url is None:
                statement_type = statement.statement_type
                type_metadata = STATEMENT_TYPES_METADATA[statement_type]
                statement_type_plural = type_metadata['plural']
                url_statement_id = sanitize_filename(
                    statement.library_name or statement.statement_id
                )
                html_url_unsanitized = STATEMENT_URL_TEMPLATE.format(
                    statement_type_plural=statement_type_plural,
                    library_name = url_statement_id,
                )
                statement.html_url = html_url_unsanitized

    def extend_mathjax_macros(self, overwrite: bool = True):
        for paper in self.papers:
            paper.extend_mathjax_macros(overwrite)

    def extend_mathjax_environments(self, overwrite: bool = True):
        for paper in self.papers:
            paper.extend_mathjax_environments(overwrite)

    def extend_html_statements(self, overwrite: bool = True):
        for statement in self.all_statements_and_proofs():
            statement.extend_statement_html(overwrite)
        self.extend_html_refs()

    def extend_motivation_htmls(self, overwrite: bool = True):
        for statement in self.all_statements():
            statement.extend_motivation_html(overwrite)

    def extend_proof_explaination_htmls(self, overwrite: bool = True):
        for proof in self.all_proofs():
            proof.extend_explaination_html(overwrite)    

    def extend_html_refs(self):
        for paper in self.papers:
            paper.extend_statements_html_refs(self.pages_root)

    def highest_library_nr(self, statement_type: str):
        highest = 0
        for statement in self.type_statements(statement_type):
            if statement.library_nr:
                highest = max(highest, statement.library_nr)
        return highest

    def all_statements_and_proofs(self):
        for statement in self.all_statements():
            yield statement
        for proof in self.all_proofs():
            yield proof

    def all_proofs(self):
        for statement in self.all_statements():
            if issubclass(type(statement), Provable):
                if statement.proof:
                    yield statement.proof

    def all_statements(self):
        for statement_type in STATEMENT_TYPES_METADATA:
            for statement in self.type_statements(statement_type):
                yield statement

    def type2statements(self):
        type2statements = {}
        for statement_type in STATEMENT_TYPES_METADATA:
            type_statements = list(self.type_statements(statement_type))
            type2statements[statement_type] = type_statements
        return type2statements

    def type_statements(self, statement_type):
        for paper in self.papers:
            for statement in paper.type_statements(statement_type):
                yield statement

    def statements_objects(self):
        for paper in self.papers:
            yield paper.statements

    def save(self, path: str = None):
        path = path or self.db_path
        if path:
            json_str = self.model_dump_json(indent=4)
            with open(path, 'w') as json_file:
                json_file.write(json_str)
        else:
            warnings.warn(f"Could not save database at path '{path}'!")
        return path