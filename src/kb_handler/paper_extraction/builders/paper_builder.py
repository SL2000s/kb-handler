from typing import Dict

from ..extraction.tex_extraction.arxiv_extraction import ArxivExtraction
from ..extraction.tex_extraction.base_extraction import BaseExtraction
from ..data_models.paper import Paper
from ..data_models.statements.statements import Statements


def extraction2paper(extraction: BaseExtraction):
    paper = Paper(
        title=extraction.get_title(),
        authors=extraction.get_authors(),
        year=extraction.get_year(),
        source_url=extraction.get_paper_url(),
        bibtex=extraction.get_bibtex(),
        original_tex=extraction.get_tex(),
    )
    return paper


def dict_extraction2paper(extraction: Dict):
    paper = Paper(
        title=extraction.get('title'),
        authors=extraction.get('authors'),
        year=extraction.get('year'),
        source_url=extraction.get('paper_url'),
        bibtex=extraction.get('bibtex'),
        original_tex=extraction.get('tex'),
        processed_original_tex=extraction.get('processed_tex'),
        statements=Statements.model_validate(extraction.get('statements', {}))
    )
    return paper


def build_arxiv_paper(arxiv_id: str, extraction_dir: str):
    arxiv_extraction = ArxivExtraction(arxiv_id, extraction_dir)
    return extraction2paper(arxiv_extraction)


if __name__ == '__main__':
    arxiv_id = '2006.04710'
    arxiv_paper = build_arxiv_paper(arxiv_id, '/tmp/arxiv_extractions')
    print(arxiv_paper.statements.model_dump_json(indent=4))