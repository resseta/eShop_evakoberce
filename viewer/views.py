from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from graphviz.backend import View

from viewer.models import CarMat, Brand, Accessories, ModelName


# Create your views here.


def home(request):
    return render(request, "home.html")


class CarMatsListView(ListView):
    template_name = "carmats.html"
    model = CarMat
    context_object_name = 'carmats'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        brands = Brand.objects.all
        context['brands'] = brands
        context['carmats'] = carmat
        context['accessories'] = accessories
        return context


def carmat(request, pk):
    if CarMat.objects.filter(id=pk).exists():
        carmat_ = CarMat.objects.get(id=pk)
        context = {'carmat': carmat_}
        return render(request, "carmat.html", context)
    return redirect('carmats')


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


class BrandsListView(ListView):
    template_name = "brands.html"
    model = Brand
    context_object_name = 'brands'

    def brand(request, pk):
        if Brand.objects.filter(id=pk).exists():
            brand_ = Brand.objects.get(id=pk)
            context = {'brand': brand_}
            return render(request, "brands.html", context)
        return redirect('brands')


class ModelsListView(ListView):
    template_name = "models.html"
    model = ModelName
    context_object_name = 'models'


def model(request, pk):
    if ModelName.objects.filter(id=pk).exists():
        model_ = ModelName.objects.get(id=pk)
        context = {'model': model_}
        return render(request, "models.html", context)
    return redirect('models')

