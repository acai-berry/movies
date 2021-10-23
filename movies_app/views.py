from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film, Genre
from .serializers import FilmSerializer, GenreSerializer



# from movies_app.models import Genre, Film


# Create your views here.
# def test(request):
#     data = Film.objects.all()
#     films = {'films': data}
#     return render(request, 'index.html', films)

@api_view(['GET', 'POST'])
def film_list(request):
    if request.method == 'GET':
        queryset = Film.objects.select_related('genre').all()
        serializer = FilmSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FilmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

       

@api_view(['GET', 'PUT', 'DELETE'])
def film_detail(request, id):
    film = get_object_or_404(Film, pk=id)
    if request.method == 'GET':
        serializer = FilmSerializer(film)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = FilmSerializer(film, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if film.orderitems.count() > 0:
            return Response({'error': 'Film cannot be deleted because it is associated with orderitem.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def genre_list(request):
    if request.method == 'GET':
        queryset = Genre.objects.annotate(films_count=Count('films')).all()
        serializer = GenreSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GenreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def genre_detail(request, id):
    genre = get_object_or_404(Genre.objects.annotate(
            films_count=Count('films')), pk=id)
    if request.method == 'GET':
        serializer = GenreSerializer(genre)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GenreSerializer(genre, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if genre.films.count() > 0:
            return Response({'error': 'Genre cannot be deleted because it has associated films'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)