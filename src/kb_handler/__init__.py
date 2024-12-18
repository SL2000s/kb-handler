from typing import Dict

from kb_handler.paper_extraction.builders.paper_builder import build_arxiv_paper
from kb_handler.paper_extraction.builders.paper_knowledgebase_builder import (
    create_paper_knowledgebase as create_kb,
    load_paper_knowledgebase as load_kb,
)
from kb_handler.paper_extraction.data_models.paper_knowledgebase import PaperKnowledgebase


def save_kb(kb: PaperKnowledgebase, path: str=None):
    kb.save(path)


def merge_paper(kb: PaperKnowledgebase, paper: Dict):
    kb.add_dict_papers(paper)
