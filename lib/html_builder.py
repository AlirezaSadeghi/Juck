

class HtmlBuilder():

    def __init__(self):
        self._html = u''


    def append(self, html):
        self._html += html
        return html

    def clear(self):
        self._html = u''

    def get_html(self):
        return self._html

    def open_tag_iterative(self, tags, content='',**kwargs):
        tag_list = tags.strip().split(' ')

        val      = ''
        for tag in tag_list:
            if tag in kwargs:
                val += self.open_tag(tag, **kwargs[tag])
            else:
                val += self.open_tag(tag)

        val += content

        for tag in reversed(tag_list):
            val += self.close_tag(tag)

        return val

    def open_tag(self, tag, **kwargs):
        val = u'<' + tag

        for attr, value in kwargs.items():
            attr = 'class' if attr == 'class_' else attr
            val += ' %s="%s" ' %(attr, value)

        val += u'> '
        return val

    def open_single_tag(self, tag, **kwargs):
        val = u'<' + tag

        for attr, value in kwargs.items():
            attr = 'class' if attr == 'class_' else attr
            val += ' %s="%s" ' %(attr, value)

        val += u' /> '
        return val


    def close_tag(self, tag):
        val = u'</' + tag + u'>'
        return val


    def br(self):
        val = ' <br/>'
        return val


    def append_tag(self, tag, html='', **kwargs):
        val = ''
        val += self.open_tag(tag, **kwargs)
        val += self.append(html)
        val += self.close_tag(tag)
        return val


    def create_list(self, items, **kwargs):

        ul_kwargs   = kwargs.get('ul')
        if ul_kwargs:
            val = self.open_tag('ul', **ul_kwargs)
        else:
            val = self.open_tag('ul')


        for item in items:
            li_kwargs   = kwargs.get('li')
            if li_kwargs:
                val += self.open_tag('li', **li_kwargs)
            else:
                val += self.open_tag('li')
            val += item
            val += self.close_tag('li')

        val += self.close_tag('ul')
        return val

    def create_li_list(self, items, **kwargs):
        val = ''

        for item in items:
            val += self.open_tag('li', **kwargs)
            val += item
            val += self.close_tag('li')

        return val

    def select(self, options, **kwargs):
        selected_value = 0
        if 'selected' in kwargs :
            selected_value = kwargs.pop('selected')

        val = self.open_tag('select', **kwargs)

        for i, option in options.items():
            if i == selected_value:
                val += self.open_tag('option', option, value=i, selected='selected')
            else:
                val += self.open_tag('option', option, value=i)

        val += self.close_tag('select')
        return val
