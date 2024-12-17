import os
import regex

GPT4O_OPENAI_API_KEY_ENV = 'OPENAI_API_KEY'
GPT4O_AZURE_ENDPOINT_ENV = 'AZURE_ENDPOINT'
GPT4O_MODEL_NAME = os.getenv('MODEL_NAME')
GPT4O_TEMPERATURE = 1e-16
GPT4O_API_TYPE = os.getenv('OPENAI_API_TYPE')
GPT4O_API_VERSION = os.getenv('OPENAI_API_VERSION')
GPT4O_DEPLOYMENT_NAME = os.getenv('DEPLOYMENT_NAME')
GPT4O_TOP_P = 1e-16
GPT4O_SEED = 1234
GPT4O_MODEL_KWARGS = {'top_p': GPT4O_TOP_P, 'seed': GPT4O_SEED}

GPT4O_ITALICS_PATTERN = regex.compile(r'\*(.*?)\*')


######## PROMPTING ########

PROMPT_TEMPLATE_FORMAT = 'jinja2'

PROMPT_TEMPLATE_TITLE = """
{{original_tex}}

Given the statement above, propose a good name for the statement (e.g. 'Pythagorean theorem', 'Ortogonality', etc.). Output nothing else than the name.
"""

PROMPT_TEMPLATE_TEX2HTML = """
Convert this latex code below to normal text that can be shown on a webpage (that uses MathJax).
Still use $...$, $$...$$, \\begin{equation}...\\end{equation} etc. for all equations and expressions.
If needed, put $...$ around latex commands in the text (eg. '\\verb!...!' -> '$\\verb!...!$', '\\texttt{...}' -> '$\\texttt{...}$', '\\emph{...}' -> '$\\emph{...}$')
Otherwise, use HTML tags to format the text as in the latex code.
Do not start the text with 'Theorem 1:', 'Lemma:', 'Proof. ' etc.
Output only the text.

Example:
LATEX CODE:
\\begin{theorem} \\label{thm:pythagorean_theorem}
Let $a$ and $b$ be the side lengths of a right triangle (see Definition~\\ref{def:right_triangle}), and let $c$ be the length of the hypotenuse. Then
\\begin{equation}
a^2 + b^2 = c^2
\\end{equation}
This is called the \\texttt{Pythagorean theorem}.
\\end{theorem}
OUTPUT:
Let $a$ and $b$ be the side lengths of a right triangle (see Definition $\\ref{def:right_triangle}$), and let $c$ be the length of the hypotenuse. Then
\\begin{equation}
a^2 + b^2 = c^2
\\end{equation}
This is called the $\\texttt{Pythagorean theorem}$.

Example:
LATEX CODE:
\\begin{axiom} \\label{axiom:transitivity_ineqs}
For any numbers $a$, $b$, and $c$:
\\begin{enumerate}
    \\item If $a > b$ and $b > c$, then $a > c$.
    \\item If $a < b$ and $b < c$, then $a < c$.
\\end{enumerate}
\\end{axiom}
OUTPUT:
For any numbers $a$, $b$, and $c$:
<ol>
    <li>If $a > b$ and $b > c$, then $a > c$.</li>
    <li>If $a < b$ and $b < c$, then $a < c$.</li>
<ol>

LATEX CODE:
{{original_tex}}
"""

PROMPT_TEMPLATE_MOTIVATION = """
Generate a short motivation of why the mathematical statement (definition/axiom/lemma/theorem/corollary) below is useful and when to use it.
Output a text that can be shown on a webpage (that uses MathJax).
Output only the text.

Example:
STATEMENT:
Let $a$ and $b$ be the side lengths of a right triangle (see Definition $\\ref{def:right_triangle}$), and let $c$ be the length of the hypotenuse. Then
\\begin{equation}
a^2 + b^2 = c^2
\\end{equation}
This is called the $\\texttt{Pythagorean theorem}$.
OUTPUT:
Pythagorean theorem is useful when working with right triangles. If two side lengths are known, it can be used to compute the third side length.

STATEMENT:
{{statement_html}}
"""

PROMPT_TEMPLATE_PROOF_EXPLANATION = """
Generate a short explaination of the different steps in the proof below.
Output a text that can be shown on a webpage (that uses MathJax).
Use <br> to show new lines on the webpage.
Output only the text.

Example:
PROOF:
\\begin{equation*}\n     \\Exp [\\Dm_{kj} \\Dm_{k'j}] = \\sum_{zz'} \\Xm_{kz} \\Xm_{k'z'} \\Exp[\\Wm_{zj}\\Wm_{z'j}] = \\sigma^2 \\sum_{z}\\Xm_{kz}\\Xm_{k'z} = \\frac{1}{d}\\langle \\Xm_k, \\Xm_{k'} \\rangle.\n\\end{equation*}",
OUTPUT:
To understand the proof, let's break it down into several steps:\n<br>\n<br>1. <i></i>Expectation of Product<i></i>: The proof begins by considering the expectation of the product of two elements, \\(\\Dm_{kj}\\) and \\(\\Dm_{k'j}\\). This is expressed as:\n<br>   \\[\n   \\Exp [\\Dm_{kj} \\Dm_{k'j}]\n   \\]\n<br>\n<br>2. <i></i>Substitution with Sum<i></i>: Next, the elements \\(\\Dm_{kj}\\) and \\(\\Dm_{k'j}\\) are substituted with their respective sums involving \\(\\Xm\\) and \\(\\Wm\\):\n<br>   \\[\n   \\sum_{zz'} \\Xm_{kz} \\Xm_{k'z'} \\Exp[\\Wm_{zj}\\Wm_{z'j}]\n   \\]\n<br>\n<br>3. <i></i>Expectation of \\(\\Wm\\) Terms<i></i>: The expectation \\(\\Exp[\\Wm_{zj}\\Wm_{z'j}]\\) is simplified using the property that \\(\\Wm_{zj}\\) and \\(\\Wm_{z'j}\\) are independent and identically distributed with variance \\(\\sigma^2\\). This results in:\n<br>   \\[\n   \\sigma^2 \\sum_{z}\\Xm_{kz}\\Xm_{k'z}\n   \\]\n<br>\n<br>4. <i></i>Inner Product Representation<i></i>: Finally, the sum \\(\\sum_{z}\\Xm_{kz}\\Xm_{k'z}\\) is recognized as the inner product \\(\\langle \\Xm_k, \\Xm_{k'} \\rangle\\), and the factor \\(\\sigma^2\\) is adjusted by the dimension \\(d\\):\n<br>   \\[\n   \\frac{1}{d}\\langle \\Xm_k, \\Xm_{k'} \\rangle\n   \\]\n<br>\n<br>Thus, the proof shows that:\n<br>\\[\n\\Exp [\\Dm_{kj} \\Dm_{k'j}] = \\frac{1}{d}\\langle \\Xm_k, \\Xm_{k'} \\rangle\n\\]

PROOF:
{{proof_html}}
"""