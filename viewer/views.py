from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from viewer.models import CarMat


# Create your views here.

def home(request):
    return render(request, "home.html")
    # return HttpResponse('<ul>'
    #                     '<li>Autokoberce</li>'
    #                     '</ul>'
    #                     )
