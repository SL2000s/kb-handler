from pydantic import BaseModel, Field
from typing import List

from kb_handler.paper_extraction.data_models.statements.axiom import Axiom
from kb_handler.paper_extraction.data_models.statements.base_provable import Provable
from kb_handler.paper_extraction.data_models.statements.base_statement import Statement
from kb_handler.paper_extraction.data_models.statements.corollary import Corollary
from kb_handler.paper_extraction.data_models.statements.definition import Definition
from kb_handler.paper_extraction.data_models.statements.lemma import Lemma
from kb_handler.paper_extraction.data_models.statements.theorem import Theorem

from kb_handler.paper_extraction.config.config import (
    DEFINITION,
    AXIOM,
    LEMMA,
    THEOREM,
    COROLLARY,
)

class Statements(BaseModel):
    definitions: List[Definition] = Field(default_factory=list)
    axioms: List[Axiom] = Field(default_factory=list)
    lemmas: List[Lemma] = Field(default_factory=list)
    theorems: List[Theorem] = Field(default_factory=list)
    corollaries: List[Corollary] = Field(default_factory=list)

    def add_statement(self, statement: Statement):
        if statement.statement_type == DEFINITION:
            self.definitions.append(statement)
        if statement.statement_type == AXIOM:
            self.axioms.append(statement)
        if statement.statement_type == LEMMA:
            self.lemmas.append(statement)
        if statement.statement_type == THEOREM:
            self.theorems.append(statement)
        if statement.statement_type == COROLLARY:
            self.corollaries.append(statement)

    def all_statements(self):
        for statement in self.definitions + self.axioms + \
                self.lemmas + self.theorems + self.corollaries:
            yield statement

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

    def type2statements(self):  # TODO: implement if needed
        pass