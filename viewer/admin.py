from django.contrib import admin

from viewer.models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra forms for adding images


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]



class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'order_date', 'total_amount', 'status')
    search_fields = ('customer_name', 'customer_email', 'order_id')
    list_filter = ('status', 'order_date')


admin.site.register(ColorOfTrim)
admin.site.register(ColorOfMat)
admin.site.register(Category)
admin.site.register(Subcategory)



admin.site.register(Body)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)

admin.site.register(PaymentMethod)
admin.site.register(ShippingMethod)
admin.site.register(Payment)
admin.site.register(Shipping)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)


