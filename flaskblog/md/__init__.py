"""
Markdown class
"""
from marko import Markdown

from .extensions import Flog

markdown = Markdown(extensions=["gfm", "pangu", "toc", "footnote", "codehilite", Flog])
