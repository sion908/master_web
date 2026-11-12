"""記事本文用の任意ディレクティブ。

サイトの配色やヘッダーは替えない。``article-ui`` はページ内の目次だけを出す。
進捗バー、番号バッジ、要点だけの切替は付けない。

.. article-ui::
   :label: ページ内の短い名前

.. lead::

   節の導入。

.. tldr::

   #. 結論

.. cards::
   :cols: 3

   .. block-card:: 見出し

      本文

      .. more:: くわしく

         折りたたみ

.. callout::

   強調したい一段落。次の段落は補足になる。

.. definition:: 大きい一文

   補足。

.. compare::

   .. column:: 左
      :who: 補足ラベル

      項目
         内容

   .. column:: 右
      :who: 補足ラベル
      :hunter:

      項目
         内容

.. principle:: 見出し
   :num: 1
   :line: 一行の要約。 ``**強調**`` も書ける。

   .. more:: くわしく

      本文

.. cycle::

   .. step:: 名前
      :num: 1

      説明

.. notes::

   * 出典

本文中の印は ``:chip:`研究の概要``` と ``:stat:`g = 0.66``` 。
``card`` は sphinx-design が使っているので、こちらは ``block-card`` にした。
"""

from html import escape

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.application import Sphinx


class ablock(nodes.General, nodes.Element):
    pass


class article_ui(ablock):
    pass


class lead_block(ablock):
    pass


class tldr_block(ablock):
    pass


class cards_block(ablock):
    pass


class card_block(ablock):
    pass


class callout_block(ablock):
    pass


class definition_block(ablock):
    pass


class compare_block(ablock):
    pass


class column_block(ablock):
    pass


class principle_block(ablock):
    pass


class more_block(ablock):
    pass


class cycle_block(ablock):
    pass


class step_block(ablock):
    pass


class notes_block(ablock):
    pass


def _inline(directive: Directive, text: str):
    text_nodes, messages = directive.state.inline_text(text, directive.lineno)
    return text_nodes, messages


def _paragraph(directive: Directive, text: str, cls: str):
    paragraph = nodes.paragraph()
    paragraph["classes"].append(cls)
    text_nodes, messages = _inline(directive, text)
    paragraph += text_nodes
    return paragraph, messages


class ArticleUiDirective(Directive):
    optional_arguments = 0
    option_spec = {"label": directives.unchanged}
    has_content = False

    def run(self):
        node = article_ui()
        node["label"] = self.options.get("label", "")
        return [node]


class LeadDirective(Directive):
    has_content = True

    def run(self):
        node = lead_block()
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class TldrDirective(Directive):
    has_content = True

    def run(self):
        node = tldr_block()
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class CardsDirective(Directive):
    has_content = True
    option_spec = {"cols": directives.unchanged}

    def run(self):
        cols = self.options.get("cols", "1")
        if cols not in {"1", "2", "3"}:
            raise self.error("cols は 1、2、3 のいずれかにしてください")
        node = cards_block()
        node["cols"] = cols
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class BlockCardDirective(Directive):
    required_arguments = 1
    final_argument_whitespace = True
    has_content = True

    def run(self):
        node = card_block()
        node["title"] = self.arguments[0]
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class CalloutDirective(Directive):
    has_content = True

    def run(self):
        node = callout_block()
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class DefinitionDirective(Directive):
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True

    def run(self):
        node = definition_block()
        messages = []
        if self.arguments:
            paragraph, messages = _paragraph(
                self, self.arguments[0], "ablock-definition-lead"
            )
            node += paragraph
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node, *messages]


class CompareDirective(Directive):
    has_content = True

    def run(self):
        node = compare_block()
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class ColumnDirective(Directive):
    required_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {
        "who": directives.unchanged,
        "hunter": directives.flag,
    }

    def run(self):
        node = column_block()
        node["title"] = self.arguments[0]
        node["who"] = self.options.get("who", "")
        node["hunter"] = "hunter" in self.options
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class PrincipleDirective(Directive):
    required_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {
        "num": directives.unchanged,
        "line": directives.unchanged,
    }

    def run(self):
        node = principle_block()
        node["title"] = self.arguments[0]
        node["num"] = self.options.get("num", "")
        messages = []
        if "line" in self.options:
            paragraph, messages = _paragraph(self, self.options["line"], "ablock-one-line")
            node += paragraph
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node, *messages]


class MoreDirective(Directive):
    required_arguments = 1
    final_argument_whitespace = True
    has_content = True

    def run(self):
        node = more_block()
        node["summary"] = self.arguments[0]
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class CycleDirective(Directive):
    has_content = True

    def run(self):
        node = cycle_block()
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class StepDirective(Directive):
    required_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {"num": directives.unchanged}

    def run(self):
        node = step_block()
        node["title"] = self.arguments[0]
        node["num"] = self.options.get("num", "")
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class NotesDirective(Directive):
    has_content = True

    def run(self):
        node = notes_block()
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def _chip_role(kind: str):
    classes = ["ablock-chip"]
    if kind:
        classes.append(f"ablock-chip-{kind}")

    def role(name, rawtext, text, lineno, inliner, options=None, content=None):
        return [nodes.inline(text, text, classes=classes)], []

    return role


def stat_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    return [nodes.inline(text, text, classes=["ablock-stat"])], []


def visit_article_ui(self, node):
    label = escape(node.get("label") or "目次")
    self.body.append(
        '<nav class="ablock ablock-ui" aria-label="この記事の目次">'
        f'<span class="ablock-ui-label">{label}</span>'
        "</nav>"
    )


def depart_article_ui(self, node):
    return


def visit_lead(self, node):
    self.body.append('<div class="ablock ablock-lead">')


def depart_lead(self, node):
    self.body.append("</div>")


def visit_tldr(self, node):
    self.body.append('<div class="ablock ablock-tldr">')


def depart_tldr(self, node):
    self.body.append("</div>")


def visit_cards(self, node):
    cols = escape(node.get("cols") or "1")
    self.body.append(f'<div class="ablock ablock-cards ablock-cards-{cols}">')


def depart_cards(self, node):
    self.body.append("</div>")


def visit_card(self, node):
    title = escape(node.get("title") or "")
    self.body.append(
        f'<article class="ablock ablock-card"><h3 class="ablock-card-title">{title}</h3>'
    )


def depart_card(self, node):
    self.body.append("</article>")


def visit_callout(self, node):
    self.body.append('<div class="ablock ablock-callout">')


def depart_callout(self, node):
    self.body.append("</div>")


def visit_definition(self, node):
    self.body.append('<div class="ablock ablock-definition">')


def depart_definition(self, node):
    self.body.append("</div>")


def visit_compare(self, node):
    self.body.append('<div class="ablock ablock-compare">')


def depart_compare(self, node):
    self.body.append("</div>")


def visit_column(self, node):
    hunter = " ablock-col-hunter" if node.get("hunter") else ""
    title = escape(node.get("title") or "")
    who = escape(node.get("who") or "")
    who_html = f' <span class="ablock-who">{who}</span>' if who else ""
    self.body.append(f'<div class="ablock-col{hunter}"><h3>{title}{who_html}</h3>')


def depart_column(self, node):
    self.body.append("</div>")


def visit_principle(self, node):
    num = escape(node.get("num") or "")
    title = escape(node.get("title") or "")
    num_html = (
        f'<span class="ablock-principle-num" aria-hidden="true">{num}</span>' if num else ""
    )
    self.body.append(
        '<article class="ablock ablock-principle">'
        f'<div class="ablock-principle-head">{num_html}<div><h3>{title}</h3>'
    )


def depart_principle(self, node):
    self.body.append("</div></div></article>")


def visit_more(self, node):
    summary = escape(node.get("summary") or "")
    self.body.append(
        f'<details class="ablock ablock-more"><summary>{summary}</summary>'
        '<div class="ablock-more-body">'
    )


def depart_more(self, node):
    self.body.append("</div></details>")


def visit_cycle(self, node):
    self.body.append('<div class="ablock ablock-cycle">')


def depart_cycle(self, node):
    self.body.append("</div>")


def visit_step(self, node):
    num = escape(node.get("num") or "")
    title = escape(node.get("title") or "")
    num_html = f'<span class="ablock-step-num" aria-hidden="true">{num}</span>' if num else ""
    self.body.append(
        f'<div class="ablock-step">{num_html}<div><h3>{title}</h3>'
    )


def depart_step(self, node):
    self.body.append("</div></div>")


def visit_notes(self, node):
    self.body.append('<div class="ablock ablock-notes">')


def depart_notes(self, node):
    self.body.append("</div>")


def setup(app: Sphinx):
    nodes_and_visitors = [
        (article_ui, visit_article_ui, depart_article_ui),
        (lead_block, visit_lead, depart_lead),
        (tldr_block, visit_tldr, depart_tldr),
        (cards_block, visit_cards, depart_cards),
        (card_block, visit_card, depart_card),
        (callout_block, visit_callout, depart_callout),
        (definition_block, visit_definition, depart_definition),
        (compare_block, visit_compare, depart_compare),
        (column_block, visit_column, depart_column),
        (principle_block, visit_principle, depart_principle),
        (more_block, visit_more, depart_more),
        (cycle_block, visit_cycle, depart_cycle),
        (step_block, visit_step, depart_step),
        (notes_block, visit_notes, depart_notes),
    ]
    for node_cls, visit, depart in nodes_and_visitors:
        app.add_node(node_cls, html=(visit, depart))

    app.add_directive("article-ui", ArticleUiDirective)
    app.add_directive("lead", LeadDirective)
    app.add_directive("tldr", TldrDirective)
    app.add_directive("cards", CardsDirective)
    app.add_directive("block-card", BlockCardDirective)
    app.add_directive("callout", CalloutDirective)
    app.add_directive("definition", DefinitionDirective)
    app.add_directive("compare", CompareDirective)
    app.add_directive("column", ColumnDirective)
    app.add_directive("principle", PrincipleDirective)
    app.add_directive("more", MoreDirective)
    app.add_directive("cycle", CycleDirective)
    app.add_directive("step", StepDirective)
    app.add_directive("notes", NotesDirective)

    app.add_role("chip", _chip_role("research"))
    app.add_role("stat", stat_role)

    app.add_css_file("article_blocks.css")
    app.add_js_file("article_blocks.js", loading_method="defer")

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
