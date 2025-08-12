from django.urls import path

from reviews_app.api import views

urlpatterns = [
    path('reviews/', views.ReviewListCreateView.as_view(), name='reviews-list'),
    path('reviews/<int:pk>/', views.ReviewUpdateDeleteView.as_view(),
         name='reviews-detail'),
    path('base-info/', views.BaseInfoView.as_view(), name='base-info')
]
