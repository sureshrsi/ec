# store/urls.py
from django.urls import path
from .views import (
    signup, signin, signout, product_list, product_detail, add_to_cart, cart,
    update_cart_quantity, remove_from_cart, add_to_wishlist, wishlist,
    remove_from_wishlist, move_to_cart
)

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('', product_list, name='product_list'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('update-cart-quantity/<int:item_id>/',
         update_cart_quantity, name='update_cart_quantity'),
    path('remove-from-cart/<int:item_id>/',
         remove_from_cart, name='remove_from_cart'),
    path('add-to-wishlist/<slug:slug>/',
         add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', wishlist, name='wishlist'),
    path('remove-from-wishlist/<int:item_id>/',
         remove_from_wishlist, name='remove_from_wishlist'),
    path('move-to-cart/<int:item_id>/', move_to_cart, name='move_to_cart'),
    #     path('checkout/', checkout, name='checkout'),
    #     path('payment-success/', payment_success, name='payment_success'),
]
