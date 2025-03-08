from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name='index'),
    path("about/", views.about, name='about'),
    path("bookings/", views.bookings, name='booking'),
    path("readings/", views.readings, name='readings'),
    path("business/", views.business, name='business'),
    path("guidanceplan/", views.guidanceplan, name='guidanceplan'),
    path("shop/", views.shop, name='shop'),
    path("testshop/", views.testshop, name='testshop'),
    path("contact/", views.contact, name='contact'),

    path("send-free-guide/", views.send_free_guide, name="send_free_guide"),
     path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),

    path('paypal/create-order/<int:product_id>/', views.create_paypal_order, name='create_paypal_order'),
    path('paypal/capture-order/', views.capture_paypal_order, name='capture_paypal_order'),
    

    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),

    path("remove-from-cart/", views.remove_from_cart, name="remove_from_cart"),
    path('create-paypal-cart-order/', views.create_paypal_cart_order, name='create_paypal_cart_order'),

]