from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from viewer.models import CarMat, Brand


# Create your views here.


def home(request):
    return render(request, "home.html")


class CarMatsListView(ListView):
    tamplate_name = "carmats.html"
    model = CarMat
    context_object_name = 'carmats'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        brands = Brand.objacts.all
        context = ['carmats']
        context = ['accessories']


def carmat(request, pk):
    pass
