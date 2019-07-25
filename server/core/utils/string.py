import re


# https://djangosnippets.org/snippets/585/
# https://gist.github.com/jaytaylor/3660565
def camelcase_to_underscore(string):
    subbed = re.compile(r'(\S)([A-Z][a-z]+)').sub(r'\1_\2', string)
    return re.compile('([a-z0-9])([A-Z])').sub(r'\1_\2', subbed).lower()
