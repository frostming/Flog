from mistune import Markdown
from .extensions import FlogRenderer, FlogBlockLexer


renderer = FlogRenderer()
from . import plugins   # noqa


class FlogMarkdown(Markdown):
    def output_image_block(self):
        text = self.token['text']
        return self.renderer.block_image(self.inline(text))

    def output_tag_plugin(self):
        self.token.pop('type')
        return self.renderer.tag_plugin(self, **self.token)


md = FlogMarkdown(renderer=renderer, block=FlogBlockLexer())
