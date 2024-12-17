from ..extraction.statements_extraction.statements_extraction import StatementsExtraction

def build_statements(tex: str, paper_id: str = None):
    statements_extraction = StatementsExtraction(tex, paper_id)
    return statements_extraction.statements