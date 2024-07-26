from django.shortcuts import redirect, render
from rest_framework import viewsets
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.shortcuts import render, get_object_or_404
from django.db.models import Q


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            return Product.objects.filter(category__slug=category_slug)
        return Product.objects.all()


def product_list(request):
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    
    context = {
        'categories': categories,
        'products': products,
        'current_category': category_slug
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug)
    return render(request, 'products/product_detail.html', {'product': product, 'request': request})

def product_share(request, share_id):
    product = get_object_or_404(Product, share_id=share_id)
    return redirect('product_detail', category_slug=product.category.slug, product_slug=product.slug)