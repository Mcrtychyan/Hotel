from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.contacts_view, name='contacts'),
    path('send/', views.send_message, name='send_message'),
]