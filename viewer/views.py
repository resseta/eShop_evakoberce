from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from graphviz.backend import View

from viewer.models import CarMat, Brand, Accessories, ModelName


# Create your views here.


def home(request):
    return render(request, "home.html")


# class CarMatsListView(ListView):
#     template_name = "carmats.html"
#     model = CarMat
#     context_object_name = 'carmats'
#
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         brands = Brand.objects.all
#         context['brands'] = brands
#         context['accessories'] = accessories
#         context['carmats'] = CarMat.objects.all()
#         return context


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        models = ModelName.objects.all
        context['models'] = models
        context['brands'] = Brand.objects.all()
        context['accessories'] = accessories
        return context

def brand(request, pk):
    if Brand.objects.filter(id=pk).exists():
        brand = Brand.objects.get(id=pk)
        context = {'brand': brand}
        request.session['brand'] = brand.id
        return redirect('models')
    return redirect('brands')


class ModelsListView(ListView):
    template_name = "models.html"
    model = ModelName
    context_object_name = 'models'

    def get_queryset(self):
        brand_id = self.request.session['brand']
        brand = Brand.objects.get(id=brand_id)
        models = ModelName.objects.filter(brand_name=brand)
        return models


def model(request, pk):
    if ModelName.objects.filter(id=pk).exists():
        model_ = ModelName.objects.get(id=pk)
        context = {'model': model_}
        request.session['model'] = model_.id
        return redirect("carmats")
    return redirect('models')


class CarMatsListView(ListView):
    template_name = "carmat.html"
    model = CarMat
    context_object_name = 'carmats'

    def get_queryset(self):
        model_id = self.request.session['model']
        model = ModelName.objects.get(id=model_id)
        carmats = CarMat.objects.filter(model_name=model)
        return carmats


def carmat(request, pk):
    if CarMat.objects.filter(id=pk).exists():
        carmat_ = CarMat.objects.get(id=pk)
        context = {'carmat': carmat_}
        return render(request, "carmats.html", context)
    return redirect('carmats')

