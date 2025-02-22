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
    path("contact/", views.contact, name='contact'),

    path("send-free-guide/", views.send_free_guide, name="send_free_guide"),

    
]