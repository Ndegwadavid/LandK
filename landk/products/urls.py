from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='product')

urlpatterns = [
    path('products/<slug:category_slug>/', ProductViewSet.as_view({'get': 'list'}), name='category_products'),
] + router.urls