from decimal import Decimal
from django.db.models import fields
from rest_framework import serializers
from movies_app import models
from movies_app.models import Film, Genre, Review

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'title', 'films_count']
    
    films_count = serializers.IntegerField(read_only=True)
   

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'title', 'slug', 'description', 'price', 'price_with_tax', 'genre']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, film: Film):
        return film.price * Decimal(1.1)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        film_id = self.context['film_id']
        return Review.objects.create(film_id = film_id, **validated_data)
        