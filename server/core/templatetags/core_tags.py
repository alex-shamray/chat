from urllib.parse import urlparse, urlunparse

from django import template
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import QueryDict
from django.template.base import Node
from django.template.defaulttags import url
from django.utils.translation import ugettext as _

register = template.Library()


@register.simple_tag(name='range')
def _range(stop, *args):
    start, step = None, None
    if args:
        if len(args) == 2:
            start, step = map(int, args)
        elif len(args) == 1:
            start = int(args[0])
    args = filter(None, (start, stop, step))
    if not stop:
        return []
    return range(*args)


class PageRangeNode(template.Node):
    def __init__(self, nodelist, page_obj_var):
        self.nodelist = nodelist
        self.page_obj_var = page_obj_var

    def _render_node(self, context, page):
        context.push()
        context['page'] = page
        rendered = self.nodelist.render(context)
        context.pop()
        return rendered

    def render(self, context):
        page_obj = self.page_obj_var.resolve(context)
        index = page_obj.number
        max_index = len(page_obj.paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = list(page_obj.paginator.page_range)[start_index:end_index]
        bits = [self._render_node(context, page) for page in page_range]
        return ''.join(bits)


class URLWithRedirectNode(Node):
    def __init__(self, url_node):
        self.url_node = url_node

    def render(self, context):
        url = self.url_node.render(context)
        next = context.request.get_full_path()
        redirect_field_name = REDIRECT_FIELD_NAME

        url_parts = list(urlparse(url))
        if redirect_field_name:
            querystring = QueryDict(url_parts[4], mutable=True)
            querystring[redirect_field_name] = next
            url_parts[4] = querystring.urlencode(safe='/')

        return urlunparse(url_parts)


@register.tag(name='pagerange')
def page_range(parser, token):
    """
    Iterates over the pages, and renders the contained block for each page.

    Usage:
            <ul>
                {% pagerange page_obj %}
                    {% if page_obj.number == page %}
                        <li><a href="?page={{ page }}" class="btn btn-default">{{ page }}</a></li>
                    {% else %}
                        <li><a href="?page={{ page }}" class="btn">{{ page }}</a></li>
                    {% endif %}
                {% endpagerange %}
            </ul>
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(_('%s tag requires a Page object') % bits[0])

    page_obj_var = template.Variable(bits[1])

    nodelist = parser.parse(('endpagerange',))
    parser.delete_first_token()

    return PageRangeNode(nodelist, page_obj_var)


@register.tag
def url_with_redirect(parser, token):
    return URLWithRedirectNode(url(parser, token))
