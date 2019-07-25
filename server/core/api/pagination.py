"""
Pagination serializers determine the structure of the output that should
be used for paginated responses.
"""
from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    """
    A simple page number based style that supports page numbers as
    query parameters. For example:

    http://api.example.org/accounts/?page=4
    http://api.example.org/accounts/?page=4&page_size=100
    """
    # Client can control the page size using this query parameter.
    page_size_query_param = 'page_size'

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = 1000
