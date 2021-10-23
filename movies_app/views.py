from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Film, Genre, Order_Item
from .serializers import FilmSerializer, GenreSerializer

class FilmViewSet(ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

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

    # def delete(self, request, pk):
    #     genre = get_object_or_404(Genre.objects.annotate(
    #         films_count=Count('films')), pk=pk)
    #     if genre.films.count() > 0:
    #         return Response({'error': 'Genre cannot be deleted because it has associated films'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     genre.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)



   

