from django_filters.rest_framework import (
    BaseInFilter, CharFilter, FilterSet,
    RangeFilter
)

from .models import Movie


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
