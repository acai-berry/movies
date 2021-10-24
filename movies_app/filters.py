from django_filters.rest_framework import FilterSet
from .models import Film

class FilmFilter(FilterSet):
    class Meta:
        model = Film
        fields = {
            'genre_id': ['exact'],
            'price': ['gt', 'lt']
        }