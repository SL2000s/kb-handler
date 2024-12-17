import os
import warnings

from ..data_models.paper_database import PaperDatabase


def load_paper_database(path: str = None):
    if path and os.path.exists(path):
        with open(path, 'r') as file:
            paper_database = PaperDatabase.model_validate_json(file.read())
    else:
        if path:
            warnings.warn(f'Could not load a paper database from {path}. Returning empty database.')
        paper_database = PaperDatabase(db_path=path)
    return paper_database


def create_paper_database(path: str = None, extraction_dir: str = '/tmp/paper_extraction'):
    paper_database = PaperDatabase(db_path=path, extraction_dir=extraction_dir)
    return paper_database