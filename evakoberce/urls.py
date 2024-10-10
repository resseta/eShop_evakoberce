"""
URL configuration for evakoberce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from viewer import views
from viewer.views import home, AccessoriesListView, accessories

urlpatterns = [
    path('admin/', admin.site.urls),


    path('home/', views.category_list, name='category_list'),
    path('home/<str:category_name>/', views.subcategory_list, name='subcategory_list'),
    path('home/<str:category_name>/<str:subcategory_name>/', views.subsubcategory_list, name='subsubcategory_list'),
    path('home/<str:category_name>/<str:subcategory_name>/<str:subsubcategory_name>/', views.product_list,
         name='product_list'),
    path('home/<str:category_name>/<str:subcategory_name>/<str:subsubcategory_name>/<str:product_name>/',
         views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('create_order/', views.create_order, name='create_order'),
    path('success/', views.success_view, name='success'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)