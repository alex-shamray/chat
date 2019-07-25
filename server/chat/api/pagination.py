from rest_framework import pagination


class CursorPagination(pagination.CursorPagination):
    page_size = 20
    ordering = '-date_created'
