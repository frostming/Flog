"""
Markdown class
"""
from marko import Markdown
from marko.ext.gfm import GFMExtension
from marko.ext.toc import TocExtension
from marko.ext.pangu import PanguExtension
from marko.ext.footnote import FootnoteDef

from .extensions import FlogExtension

markdown = Markdown(extensions=[
    FlogExtension,
    TocExtension,
    PanguExtension,
    FootnoteDef,
    GFMExtension
])
