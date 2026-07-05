from django.urls import path
from . import views

urlpatterns = [
    path('pagar/',views.pagar(), name='pagar')
]