import regex

from ...data_models.statements.axiom import Axiom
from ...data_models.statements.base_corable import Corable
from ...data_models.statements.base_provable import Provable
from ...data_models.statements.corollary import Corollary
from ...data_models.statements.definition import Definition
from ...data_models.statements.lemma import Lemma
from ...data_models.statements.proof import Proof
from ...data_models.statements.statements import Statements
from ...data_models.statements.theorem import Theorem
from ...utils.tex_processing import remove_tex_comments, expand_tex_restatables

from ...config.config import (
    DEFINITION,
    AXIOM,
    LEMMA,
    THEOREM,
    COROLLARY,
    PROOF
)

STATEMENTS_PATTERNS_UNCOMPILED = {
    THEOREM: [r'\\begin\{theorem\}.*?\\end\{theorem\}'],
    LEMMA: [r'\\begin\{lemma\}.*?\\end\{lemma\}'],
    DEFINITION: [r'\\begin\{definition\}.*?\\end\{definition\}'],
    COROLLARY: [r'\\begin\{corollary\}.*?\\end\{corollary\}'],
    AXIOM: [r'\\begin\{axiom\}.*?\\end\{axiom\}'],
    PROOF: [r'\\begin\{proof\}.*?\\end\{proof\}']
}

statements_patterns = {}
for statement_type, statement_patterns in STATEMENTS_PATTERNS_UNCOMPILED.items():
    compiled_patterns = [regex.compile(pattern, regex.DOTALL) for pattern in statement_patterns]
    statements_patterns[statement_type] = compiled_patterns


class StatementsExtraction():
    class ExtractedStatement():
        def __init__(self, statement_type, statement_tex, index):
            self.statement_type = statement_type
            self.statement_tex = statement_tex
            self.index = index
            # self.end_index = self.index + len(statement) - 1

    def __init__(self, tex, paper_id: str = None):
        self.preprocessed_tex = self._preprocess_tex(tex)
        self.paper_id = paper_id
        self.statements = self._extract_statements()
    
    def _preprocess_tex(self, tex):
        tex = remove_tex_comments(tex)
        tex = expand_tex_restatables(tex)
        return tex

    def _extract_statements(self):
        statements = Statements()
        extracted_statements = self._sorted_extracted_statements()
        last_provable = None
        last_corable = None
        for extracted_statement in extracted_statements:
            statement_type = extracted_statement.statement_type
            statement_tex = extracted_statement.statement_tex
            statement = self._create_statement_object(statement_type, statement_tex)
            if statement_type == COROLLARY and last_corable:
                last_corable.corollary_ids.append(statement.statement_id)
                statement.parent_id = last_corable.statement_id
            if statement_type == PROOF and last_provable:
                last_provable.proof = statement
            if statement_type != PROOF:
                statements.add_statement(statement)
            if issubclass(type(statement), Provable):
                last_provable = statement
            if issubclass(type(statement), Corable):
                last_corable = statement
        return statements

    def _sorted_extracted_statements(self):
        extracted_statements = []
        for statement_type, statement_patterns in statements_patterns.items():
            for pattern in statement_patterns:
                for match in pattern.finditer(self.preprocessed_tex):
                    extracted_statement = self.ExtractedStatement(statement_type, match.group(), match.start())
                    extracted_statements.append(extracted_statement)
        extracted_statements.sort(key=lambda x: x.index)
        return extracted_statements

    def _create_statement_object(self, statement_type, statement_tex):
        if statement_type == DEFINITION:
            child_class = Definition
        elif statement_type == AXIOM:
            child_class = Axiom
        elif statement_type == LEMMA:
            child_class = Lemma
        elif statement_type == THEOREM:
            child_class = Theorem
        elif statement_type == COROLLARY:
            child_class = Corollary
        else:
            child_class = Proof
        return child_class(
            paper_id=self.paper_id,
            statement_original_tex=statement_tex,
            statement_type=statement_type,
        )