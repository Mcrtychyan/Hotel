from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('create/<slug:room_slug>/', views.create_reservation, name='create'),
    path('payment/<int:reservation_id>/', views.payment_view, name='payment'),
    path('my/', views.my_reservations, name='my_reservations'),
    path('cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel'),
]