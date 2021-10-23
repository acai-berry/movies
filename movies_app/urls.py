from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('films/', views.film_list),
    path('films/<int:id>/', views.film_detail),
    path('genre/', views.genre_list, name='genre-list'),
    path('genre/<int:id>/', views.genre_detail)
]
