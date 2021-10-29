from django.core.paginator import Page
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from movies_app.pagination import DefaultPagination
from .filters import FilmFilter
from .models import Film, Genre, OrderItem, Review, Cart, CartItem
from .serializers import AddCartItemSerializer, CartSerializer, FilmSerializer, GenreSerializer, ReviewSerializer, CartItemSerializer
from movies_app import serializers

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
        if Order_Item.objects.filter(film_id=kwargs['pk']).count() > 0:
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


class CartViewSet(CreateModelMixin, 
                    GenericViewSet, 
                    RetrieveModelMixin, 
                    DestroyModelMixin):
    queryset = Cart.objects.prefetch_related('items__film').all()
    serializer_class = CartSerializer


class CartItemsViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects \
                .filter(cart_id=self.kwargs['cart_pk']) \
                .select_related('film')


