from django_filters.rest_framework import (
    BaseInFilter, CharFilter, FilterSet,
    RangeFilter
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Movie


class PaginationMovie(PageNumberPagination):
    page_size = 1
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'count': self.page.paginator.count,
            'results': data
        })


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFilterInFilter(BaseInFilter, CharFilter):
    pass


class MovieFilter(FilterSet):
    """Movie filter

    """
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    year = RangeFilter()

    class Meta:
        model = Movie
        fields = ['genres', 'year']
