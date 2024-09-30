from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from graphviz.backend import View

from viewer.models import Accessories, Category, Subcategory, Product


# Create your views here.


def home(request):
    return render(request, "home.html")


class AccessoriesListView(ListView):
    template_name = "accessories.html"
    model = Accessories
    context_object_name = 'accessories'


def accessories(request, pk):
    if Accessories.objects.filter(id=pk).exists():
        accessories_ = Accessories.objects.get(id=pk)
        context = {'accessories': accessories_}
        return render(request, "accessories.html", context)
    return redirect('accessories')


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()
    return render(request, 'subcategory_list.html', {'category': category, 'subcategories': subcategories})


def product_list(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    products = subcategory.products.all()
    return render(request, 'product_list.html', {'subcategory': subcategory, 'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})