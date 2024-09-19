from django.shortcuts import render
from django.views.generic import ListView

from viewer.models import CarMat


# Create your views here.

def home(request):
    return render(request, "home.html")


# class CarMat(ListView):
#     template_name = "carmat.html"
#     model = CarMat
#     context_object_name = 'carmat'