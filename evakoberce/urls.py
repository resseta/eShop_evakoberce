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
from django.views.generic import TemplateView

from viewer import views
from viewer.views import home, AccessoriesListView, accessories, add_to_cart, view_cart
from accounts.views import SignUpView, user_logout

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name="home"),

    path('accessories/', AccessoriesListView.as_view(), name="accessories"),
    path('accessories/<pk>/', accessories, name='accesories'),
    path('kontakt/', TemplateView.as_view(template_name="kontakt.html"), name='kontakt'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.subcategory_list, name='subcategory_list'),
    path('subcategories/<int:subcategory_id>/', views.product_list, name='product_list'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart_empty/', views.cart_empty_view, name='cart_empty'),

    path('error/', views.error_view, name='error_view'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.success_view, name='success'),

    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/logout/', user_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
