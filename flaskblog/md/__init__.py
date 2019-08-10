"""
Markdown class
"""
from marko import Markdown
from marko.ext.gfm import GFMExtension
from marko.ext.toc import TocExtension
from marko.ext.pangu import PanguExtension
from marko.ext.footnote import FootnoteExtension

from .extensions import FlogExtension

markdown = Markdown(
    extensions=[
        GFMExtension,
        PanguExtension,
        TocExtension,
        FootnoteExtension,
        FlogExtension,
    ]
)
