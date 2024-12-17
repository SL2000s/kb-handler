import os
import warnings

from ..data_models.paper_knowledgebase import PaperKnowledgebase


def load_paper_knowledgebase(path: str = None):
    if path and os.path.exists(path):
        with open(path, 'r') as file:
            paper_knowledgebase = PaperKnowledgebase.model_validate_json(file.read())
    else:
        if path:
            warnings.warn(f'Could not load a paper knowledgebase from {path}. Returning empty knowledgebase.')
        paper_knowledgebase = PaperKnowledgebase(kb_path=path)
    return paper_knowledgebase


def create_paper_knowledgebase(path: str = None, extraction_dir: str = '/tmp/paper_extraction'):
    paper_knowledgebase = PaperKnowledgebase(kb_path=path, extraction_dir=extraction_dir)
    return paper_knowledgebase