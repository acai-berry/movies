from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from pprint import pprint


router = DefaultRouter()
router.register('films', views.FilmViewSet)
router.register('genre', views.GenreViewSet)


# URLConf
urlpatterns = router.urls
