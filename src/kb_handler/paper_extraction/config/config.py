import os


PKG_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DOTENV_PATH = os.path.join(PKG_ROOT, '.env')

# ARXIV_EXTRACT_DIR = os.path.join(ROOT, 'data', 'tmp', 'arxiv_tex_extractions')

DEFINITION = 'definition'
AXIOM = 'axiom'
LEMMA = 'lemma'
THEOREM = 'theorem'
COROLLARY = 'corollary'
PROOF = 'proof'

STATEMENT_TYPES_METADATA = {
    DEFINITION: {
        'singular': 'definition',
        'plural': 'definitions',
        'capitalized_singular': 'Definition',
        'capitalized_plural': 'Definitions',
    },
    AXIOM: {
        'singular': 'axiom',
        'plural': 'axioms',
        'capitalized_singular': 'Axiom',
        'capitalized_plural': 'Axioms',
    },
    LEMMA: {
        'singular': 'lemma',
        'plural': 'lemmas',
        'capitalized_singular': 'Lemma',
        'capitalized_plural': 'Lemmas',
    },
    THEOREM: {
        'singular': 'theorem',
        'plural': 'theorems',
        'capitalized_singular': 'Theorem',
        'capitalized_plural': 'Theorems',
    },
    COROLLARY: {
        'singular': 'corollary',
        'plural': 'corollaries',
        'capitalized_singular': 'Corollary',
        'capitalized_plural': 'Corollaries',
    },
}

PAPERS_INDEX_URL = 'library/papers/index.html'
# STATEMENT_LIBRARY_URL = 'library/index.html'
PAPER_URL_TEMPLATE = 'library/papers/{paper_id}/index.html'
STATEMENT_TYPE_URL_TEMPLATE = 'library/{statement_type_plural}/index.html'
STATEMENT_URL_TEMPLATE = 'library/{statement_type_plural}/{library_name}/index.html'
STATEMENT_TYPE_URLS = {
    statement_type: STATEMENT_TYPE_URL_TEMPLATE.format(
        statement_type_plural=type_metadata['plural']
    )
    for statement_type, type_metadata in STATEMENT_TYPES_METADATA.items()
}

ITALICS_RE_SUBSTITUTION_PATTERN = r'<i>\1</i>'

STATEMENT_TYPE_HTML_TEMPLATE_PATHS = {
    DEFINITION: 'statement.html.jinja',
    AXIOM: 'statement.html.jinja',
    LEMMA: 'provable.html.jinja',
    THEOREM: 'provable.html.jinja',
    COROLLARY: 'provable.html.jinja',
}