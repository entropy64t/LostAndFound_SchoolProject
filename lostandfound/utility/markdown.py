import bleach
from markdown_it import MarkdownIt

md = MarkdownIt()

ALLOWED_TAGS = [
    "p",
    "br",
    "strong",
    "em",
    "del",
    "h1",
    "h2",
    "h3",
    "ul",
    "ol",
    "li",
    "blockquote",
    "code",
    "pre",
    "a",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
}


def parse_markdown(text: str) -> str:
    html = md.render(text)

    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=["http", "https", "mailto"],
    )
