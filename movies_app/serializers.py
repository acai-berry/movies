from decimal import Decimal
from django.db.models import fields
from rest_framework import serializers
from movies_app import models
from movies_app.models import Cart, CartItem, Film, Genre, Review

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


class SimpleFilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'title', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    film = SimpleFilmSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'film']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart):
        return sum([item.film.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    film_id = serializers.IntegerField()

    def validate_film_id(self, value):
        if not Film.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No film with given ID was found.')
        return value


    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        film_id = self.validated_data['film_id']
        
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, film_id=film_id)
            self.instance = cart_item
            raise serializers.ValidationError('Film is already in the cart!')
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'film_id']
