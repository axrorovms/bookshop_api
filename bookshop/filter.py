from django_filters import filters
from django_filters.rest_framework import FilterSet

from bookshop.models import Book


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class Booksfilter(FilterSet):
    category = CharFilterInFilter(field_name='category__id', lookup_expr='in')
    year = filters.RangeFilter()

    class Meta:
        model = Book
        fields = ['category__name', 'year', 'author__name']

