import regex

from langchain.prompts.prompt import PromptTemplate

from ..config.config import ITALICS_RE_SUBSTITUTION_PATTERN
from ..config.llm_config import (
    PROMPT_TEMPLATE_FORMAT,
    PROMPT_TEMPLATE_TITLE,
    PROMPT_TEMPLATE_TEX2HTML,
    PROMPT_TEMPLATE_MOTIVATION,
    PROMPT_TEMPLATE_PROOF_EXPLANATION,
    GPT4O_ITALICS_PATTERN,
)
from ..utils.openai import llm_quest


LATEX_STATEMENT_TEMPLATE = """\\begin{{{statement_type}}}[{title}]
{content}
\\end{{{statement_type}}}"""

LATEX_COMMENT_PATTERN = regex.compile(r'%.*?$', regex.MULTILINE)
LATEX_RESTABLE_PATTERN = regex.compile(r'(\\begin\{restatable\}\[(.*?)\]\{(.*?)\}\{(.*?)\}(.*?)\\end\{restatable\})', regex.DOTALL)

MACRO_PATTERNS_TO_MATHJAX = [  # list of (compile_regex, template strings where rendered by *[regex groups] (NOTE: \ are replaced by \\ later))
    (regex.compile(r'\\DeclareMathOperator\*?\{\\(\w+)\}\{(\w+)\}'), '{}: "\\operatorname{{{}}}"'),
    (regex.compile(r'\\newcommand\{\\(\w+)\}\{(([^{}]*(\{(?:[^{}]|(?2))*\})*)*)\}'), '{}: "{}"'),
    (regex.compile(r'\\newcommand\\(\w+)\{(([^{}]*(\{(?:[^{}]|(?2))*\})*)*)\}'), '{}: "{}"'),
    (regex.compile(r'\\newcommand\{\\(\w+)\}\[1\]\{(([^{}]*(\{(?:[^{}]|(?2))*\})*)*)\}'), '{}: ["{}", 1]'),  # TODO: don't hardcode numbers
    (regex.compile(r'\\newcommand\{\\(\w+)\}\[2\]\{(([^{}]*(\{(?:[^{}]|(?2))*\})*)*)\}'), '{}: ["{}", 2]'),  # TODO: don't hardcode numbers
    (regex.compile(r'\\newcommand\{\\(\w+)\}\[3\]\{(([^{}]*(\{(?:[^{}]|(?2))*\})*)*)\}'), '{}: ["{}", 3]'),  # TODO: don't hardcode numbers
    (regex.compile(r'\\def\s*\\(\w+)\{(([^{}]*(\{(?:[^{}]|(?2))*\})*)*)\}'), '{}: "{}"')
]

PROMPT_TEMPLATE_TITLE = PromptTemplate.from_template(
    PROMPT_TEMPLATE_TITLE,
    template_format=PROMPT_TEMPLATE_FORMAT
)
PROMPT_TEMPLATE_HTMLTEX = PromptTemplate.from_template(
    PROMPT_TEMPLATE_TEX2HTML,
    template_format=PROMPT_TEMPLATE_FORMAT
)
PROMPT_TEMPLATE_MOTIVATION = PromptTemplate.from_template(
    PROMPT_TEMPLATE_MOTIVATION,
    template_format=PROMPT_TEMPLATE_FORMAT
)
PROMPT_TEMPLATE_PROOF_EXPLANATION = PromptTemplate.from_template(
    PROMPT_TEMPLATE_PROOF_EXPLANATION,
    template_format=PROMPT_TEMPLATE_FORMAT
)


def process_tex_extraction(tex: str):
    tex = remove_tex_comments(tex)
    tex = expand_tex_restatables(tex)
    # tex = tex.replace('cref', 'ref').replace('Cref', 'cref')  # keep this info for inter-link
    return tex


def remove_tex_comments(tex: str):
    return LATEX_COMMENT_PATTERN.sub('', tex)


def expand_tex_restatables(tex):
    matches = LATEX_RESTABLE_PATTERN.findall(tex)
    for match in matches:
        full_match, title, statement_type, restatable_id, content = match
        tex_statement = LATEX_STATEMENT_TEMPLATE.format(
            statement_type=statement_type,
            title=title,
            content=content
        )
        tex = tex.replace(full_match, '')
        tex = tex.replace(f'\\{restatable_id}*', tex_statement)
    return tex


def mathjax_macros(tex: str):
    mathjax_macros_ = [   # extra (hardcoded) macros
        'emph: ["\\\\textit{#1}", 1]',
        'bm: ["\\\\boldsymbol{\\\\mathbf{#1}}", 1]',
        'mathds: ["\\\\mathbf{#1}", 1]',
        'textsl: ["\\\\textit{#1}", 1]',
        'vspace: ["", 1]',
        'xspace: ""',
    ]
    for pattern, sub_template in MACRO_PATTERNS_TO_MATHJAX:
        matches = pattern.findall(tex)
        for match in matches:
            mathjax_macros_.append(sub_template.format(*match).replace('\\', '\\\\').replace('\n', ''))
    return mathjax_macros_


def mathjax_environments(tex: str):
    mathjax_environments_ = [
        'subequations: ["{", "}"]',
    ]
    return mathjax_environments_


def statement2title(tex: str):
    title = llm_quest(
        PROMPT_TEMPLATE_TITLE,
        original_tex=tex
    )
    return title


def _post_process_llm_ans_tex2html(html: str):
    html = GPT4O_ITALICS_PATTERN.sub(ITALICS_RE_SUBSTITUTION_PATTERN, html)
    return html


def tex2html(tex: str):
    html = llm_quest(
        PROMPT_TEMPLATE_HTMLTEX,
        original_tex=tex,
    )
    html = _post_process_llm_ans_tex2html(html)
    return html


def statement2motivation(statement_html: str):
    html = llm_quest(
        PROMPT_TEMPLATE_MOTIVATION,
        statement_html=statement_html
    )
    html = _post_process_llm_ans_tex2html(html)
    return html


def proof2explaination(proof_html: str):
    html = llm_quest(
        PROMPT_TEMPLATE_PROOF_EXPLANATION,
        proof_html=proof_html
    )
    html = _post_process_llm_ans_tex2html(html)
    return html