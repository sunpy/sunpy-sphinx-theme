"""
This provides a card extension for the website.
"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.application import Sphinx

__all__ = ["Card", "_Card", "depart_card_node", "visit_card_node"]


class _Card(nodes.General, nodes.Element):
    pass


def visit_card_node(self, node) -> None:
    """
    Prepare the card node for rendering.
    """
    title = node.get("title", "")
    key = title or node["github"]
    key = key.lower().replace(" ", "-")
    title = f"<h4>{title}</h4>" if len(title) > 0 else ""
    col_extra_class = "column-half" if title else ""
    img_src = node.get("img_name")
    # If there is no "img_name" given, we fallback to using the github avatar
    # if a user handle is provided. If so, the image provided is actually the sunpy icon
    if img_src == "sunpy_icon.svg" and node.get("github") is not None:
        img_src = f"https://github.com/{node['github']}.png"
    body = f"""<div class="column {col_extra_class}">
                {title}
                <div class="card">
                <img class="dark-light" src="{img_src}" alt="{node["name"]}">
                <p>{node["name"]}</p>
                <p><button type="button" class="btn btn-sunpy btn-sunpy1 stretched-link" data-bs-toggle="modal" data-bs-target="#{key}">More Info</button></p>
                <div class="modal fade" id="{key}" tabindex=-1>
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h4 class="modal-title center">{node["name"]}</h4>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
    """
    self.body.append(body)


def depart_card_node(self, node) -> None:
    """
    Finalize the card node after rendering.
    """
    body = f"""
                                <p>Affiliation: <a href="{node["aff_link"]}">{node["aff_name"]}</a></p>
                                <p>GitHub: <a href="https://github.com/{node["github"]}">{node["github"]}</a></p>
                                <p>Start Date: {node["date"]}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div></div>"""
    self.body.append(body)


class Card(Directive):
    """
    A custom directive for a card.
    """

    has_content = True
    required_arguments = 1
    optional_arguments = 6
    option_spec = {  # NOQA: RUF012
        "img_name": directives.unchanged,
        "title": directives.unchanged,
        "github": directives.unchanged,
        "aff_name": directives.unchanged,
        "aff_link": directives.unchanged,
        "date": directives.unchanged,
        "desc": directives.unchanged,
    }

    def run(self):
        """
        Run the directive.
        """
        title = self.options.get("title") if "title" in self.options else ""
        img_name = self.options.get("img_name") if "img_name" in self.options else "sunpy_icon.svg"
        github = self.options.get("github") if "github" in self.options else ""
        aff_name = self.options.get("aff_name") if "aff_name" in self.options else ""
        aff_link = self.options.get("aff_link") if "aff_link" in self.options else ""
        date = self.options.get("date") if "date" in self.options else ""
        desc = self.options.get("desc") if "desc" in self.options else "N/A"
        name = " ".join(self.arguments)
        out = _Card(
            name=name,
            img_name=img_name,
            title=title,
            github=github,
            aff_name=aff_name,
            aff_link=aff_link,
            date=date,
            desc=desc,
        )
        self.state.nested_parse(self.content, 0, out)
        return [out]


def setup(app: Sphinx):
    app.add_css_file("sunpy_cards.css", priority=600)
    app.add_directive("custom-card", Card)
    app.add_node(_Card, html=(visit_card_node, depart_card_node))
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
