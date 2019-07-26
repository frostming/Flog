import re
from marko import block, HTMLRenderer


class PhotoSet(block.BlockElement):
    pattern = re.compile(
        r' {,3}(!\[([^\[\]\n]+)?\]\(([^)\n]+)\))'
        r'( {,3}(!\[([^\[\]\n]+)?\]\(([^)\n]+)\)))*[^\n\S]*$\n?', re.M
    )
    inline_children = True

    def __init__(self, match):
        self.children = match.group()

    @classmethod
    def match(cls, source):
        return source.expect_re(cls.pattern)

    @classmethod
    def parse(self, source):
        rv = source.match
        source.consume()
        return rv


class FlogRendererMixin:
    def render_image(self, element):
        result = super().render_image(element)
        result = result.replace(
            '<img', '<img data-original="{}"'.format(self.escape_url(element.dest))
        )
        caption = '<figcaption>{}</figcaption>'.format(element.title) if element.title else ''
        return '<figure>{}{}</figure>'.format(result, caption)

    def render_photo_set(self, element):
        return '<div class="photo-set d-lg-flex">\n{}</div>\n'.format(
            self.render_children(element)
        )

    def render_fenced_code(self, element):
        rv = [
            '<div class="block-code">\n'
            '<div class="code-head clearfix">{}<span class="copy-code"'
            ' title="Copy code"></span></div>\n'
            .format((element.lang or '').title()),
            super().render_fenced_code(element),
            '</div>\n'
        ]
        return ''.join(rv)

    def _open_heading_group(self):
        return '<div class="list-group">\n'

    def _close_heading_group(self):
        return '</div>\n'

    def _render_toc_item(self, slug, text):
        return '<a class="list-group-item" href="#{}">{}</a>\n'.format(
            slug, re.sub(r"<.+?>", "", text)
        )

    def render_toc(self, maxlevel=3):
        return super().render_toc(maxlevel).replace(
            '<div class="list-group">',
            '<div class="list-group" id="table-of-content">', 1
        )

    def render_html_block(self, element):
        # Disable tag filter, use the original render function
        return HTMLRenderer.render_html_block(self, element)


class FlogExtension:
    elements = [PhotoSet]
    renderer_mixins = [FlogRendererMixin]
