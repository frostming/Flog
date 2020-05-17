"""
Markdown class
"""
from marko import Markdown
from marko.ext.toc import Toc

from .extensions import Flog

toc_ext = Toc(
    '<div class="list-group">',
    '</div>',
    '<a class="list-group-item" href="#{slug}">{text}</a>'
)
markdown = Markdown(extensions=["gfm", "pangu", toc_ext, "footnote", "codehilite", Flog])
