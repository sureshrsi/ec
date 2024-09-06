from django.contrib import admin
from .models import Product, Category, CartItem, WishlistItem, Order

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(WishlistItem)
admin.site.register(Order)
