from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from viewer.models import CarMat, Brand, Accessories


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
        context['carmats'] = carmat
        context['accessories'] = accessories
        return context


def carmat(request, pk):
    if CarMat.objects.filter(id=pk).exists():
        carmat_ = CarMat.objects.get(id=pk)
        context = {'carmat': carmat_}
        return render(request, "carmats.html", context)
    return redirect('carmats')


class AccessoriesListView(ListView):
    template_name = ("accessories.html")
    model = Accessories
    context_object_name = 'accessories'


def accessories(request, pk):
    if Accessories.objects.filter(id=pk).exists():
        accessories_ = Accessories.objects.get(id=pk)
        context = {'accessories': accessories_}
        return render(request, "accessories.html", context)
    return redirect('accessories')



