"""
Markdown class
"""
from marko import Markdown

from .extensions import FlogParser, FlogRenderer

markdown = Markdown(FlogParser, FlogRenderer)
