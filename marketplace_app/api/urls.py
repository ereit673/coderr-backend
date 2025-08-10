from django.urls import path

from . import views

urlpatterns = [
    path('offers/', views.OfferListCreateView.as_view(), name='offers-list'),
    # path('offers/<int:pk>/', views.OfferDetailView.as_view(), name='offers-detail'),


]
