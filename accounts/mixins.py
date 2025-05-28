from rest_framework.pagination import PageNumberPagination
from rest_framework.settings import api_settings

class PaginationHandlerMixin:
    pagination_class = PageNumberPagination

    def paginate_queryset(self, queryset, request, view=None):
        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        page = paginator.paginate_queryset(queryset, request, view=view)
        return paginator, page