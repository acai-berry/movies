from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('films', views.FilmViewSet, basename='films')
router.register('genre', views.GenreViewSet)
router.register('carts', views.CartViewSet)

film_router = routers.NestedDefaultRouter(router, 'films', lookup='film')
film_router.register('reviews', views.ReviewViewSet, basename='film-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemsViewSet, basename='cart-items')

urlpatterns = router.urls + film_router.urls + carts_router.urls
