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
    
]