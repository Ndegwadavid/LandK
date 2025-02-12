"""
URL configuration for landk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import product_list, product_detail, product_share



urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('products.urls')),
    path('api/', include('products.urls')),
    path('products/', product_list, name='product_list'),
    path('share/<str:share_id>/', product_share, name='product_share'),
    path('<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),
    path('orders/', include('orders.urls')),  # Add this line

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)