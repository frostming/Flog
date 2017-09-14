import re
from slugify import slugify
from mistune_contrib import toc
from mistune import escape, escape_link
from mistune import BlockLexer, Renderer


class FlogBlockLexer(BlockLexer):
    IMAGE_RE = re.compile(
        r'[ ]*(!\[([^\[\]]+)?\]\(([^)]+)\))'
        r'([ ]+(!\[([^\[\]]+)?\]\(([^)]+)\)))*$', re.M
    )

    TAG_RE = re.compile(
        r'^\{%\s?([^%\n\s]+)\s([^%\n]+?)\s?%}(?:(.*?)(\{%\s?end\1\s?%\}))?',
        re.DOTALL
    )

    def __init__(self, *args, **kwargs):
        super(FlogBlockLexer, self).__init__(*args, **kwargs)
        self.install_extensions()

    def install_extensions(self):
        self.rules.image_block = self.IMAGE_RE
        self.rules.tag_plugin = self.TAG_RE
        self.default_rules.insert(5, 'image_block')
        # self.default_rules.insert(1, 'tag_plugin')

    def parse_image_block(self, m):
        text = m.group()
        self.tokens.append({
            'type': 'image_block',
            'text': text
        })

    def parse_tag_plugin(self, m):
        plugin = m.group(1)
        args = m.group(2).strip().split()
        body = m.group(3)
        endtag = m.group(4)
        self.tokens.append({
            'type': 'tag_plugin',
            'plugin': plugin,
            'args': args,
            'body': body,
            'endtag': endtag
        })


class FlogRenderer(toc.TocMixin, Renderer):
    IMG_RE = re.compile(r'<figure.*?>.+?</figure>')

    def __init__(self, *args, **kwargs):
        super(FlogRenderer, self).__init__(*args, **kwargs)
        self.reset_toc()
        self.plugins = {}

    def register_tag_plugin(name=None):
        def wrapper(func):
            if name is None:
                name = func.__name__
            self.plugins[name] = func
            return func

    def header(self, text, level, raw=None):
        link = slugify(text)
        rv = '<h%d id="%s">%s</h%d>\n' % (
            level, link, text, level
        )
        self.toc_tree.append((link, text, level, raw))
        self.toc_count += 1
        return rv

    def image(self, src, title, text):
        src = escape_link(src)
        text = escape(text, quote=True)
        rv = ['<figure>']
        rv.append('<img data-original="%s" src="%s" alt="%s">'
                  % (src, src, text))
        if title:
            rv.append('<figcaption>%s</figcaption>' % title)
        rv.append('</figure>')
        return ''.join(rv)

    def block_image(self, images):
        rv = ['<div class="photo">']
        if len(self.IMG_RE.findall(images)) > 1:
            images = '<div class="photo-set d-lg-flex">%s</div>' % images
        rv.append(images)
        rv.append('</div>')
        return '\n'.join(rv)

    def tag_plugin(self, md, plugin, args, body, endtag):
        plugin_func = self.plugins[plugin]
        if endtag is None:
            return plugin_func(md, args)
        return plugin_func(md, args, body)

    def footnotes(self, text):
        html = '<div class="footnotes">\n<ol>%s</ol>\n</div>\n'
        return html % (text,)

    def _iter_toc(self, level):
        first_level = None
        last_level = None
        if not self.toc_tree:
            return

        yield '<div class="list-group" id="table-of-content">\n'

        for toc in self.toc_tree:
            index, text, l, raw = toc

            if l > level:
                # ignore this level
                continue

            if first_level is None:
                # based on first level
                first_level = l
                last_level = l
                yield '<a class="list-group-item" href="#%s">%s</a>\n' \
                    % (index, text)
            elif last_level == l:
                yield '<a class="list-group-item" href="#%s">%s</a>\n' \
                    % (index, text)
            elif last_level == l - 1:
                last_level = l
                yield '<div class="list-group">\n<a class="list-group-item"'\
                    ' href="#%s">%s</a>\n' % (index, text)
            elif last_level > l:
                # close indention
                while last_level > l:
                    yield '</div>\n'
                    last_level -= 1
                yield '<a class="list-group-item" href="#%s">%s</a>\n' \
                    % (index, text)

        # close tags
        while last_level > first_level:
            yield '</div>\n'
            last_level -= 1

        yield '</div>\n'
