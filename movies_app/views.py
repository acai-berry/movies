from django.core.paginator import Page
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from movies_app.pagination import DefaultPagination
from .filters import FilmFilter
from .models import Film, Genre, Order_Item, Review
from .serializers import FilmSerializer, GenreSerializer, ReviewSerializer

class FilmViewSet(ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FilmFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if Order_Item.objects.filter(film_id=kwargs['pk']).count() >0:
            return Response({'error': 'Film cannot be deleted because it is associated with orderitem.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)



class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.annotate(films_count=Count('films')).all()
    serializer_class = GenreSerializer

    def destroy(self, request, *args, **kwargs):
        if Film.objects.filter(genre_id=kwargs['pk']).count() >0:
            return Response({'error': 'Genre cannot be deleted because it has associated films'}, 
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(film_id=self.kwargs['film_pk'])

    def get_serializer_context(self):
        return {'film_id': self.kwargs['film_pk']}


   

