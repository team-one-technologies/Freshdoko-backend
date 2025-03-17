# cart/urls.py
from django.urls import path
from .views import  add_to_cart,get_cart ,product_in_cart,get_cart_stat,update_quantity,delete_cartitem ,initiate_khalti_payment ,khalti_payment_callback,initiate_payoneer_payment,payoneer_payment_callback ,create_order

urlpatterns = [
    path('get-cart/',get_cart, name='view_cart'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('product-in-cart',product_in_cart,name='cart_product'),
    path('get_cart_stat',get_cart_stat,name="cart_status"),
    path('update_quantity/',update_quantity,name="update_quantity"),
    path('delete_cartitem/',delete_cartitem,name="delete_cartitem"),
    path("khalti_initiate_payment/",initiate_khalti_payment,name="intiate_payment"),
    path("khalti_payment-callback/", khalti_payment_callback, name="khalti_payment_callback"),
    path('initiate-payoneer-payment/', initiate_payoneer_payment, name='initiate_payoneer_payment'),
    path('payoneer-payment-callback/', payoneer_payment_callback, name='payoneer_payment_callback'),
    path('create-order/', create_order, name='create_order'),
]


