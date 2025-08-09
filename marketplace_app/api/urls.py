from django.urls import path

from . import views

urlpatterns = [
    path('offers/', views.OfferListCreateView.as_view(), name='offer-list'),
]
