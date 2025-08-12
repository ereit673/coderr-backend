from django.urls import path

from . import views

urlpatterns = [
    path('offers/', views.OfferListCreateView.as_view(), name='offers-list'),
    path('offers/<int:pk>/',
         views.OfferRetrieveUpdateDestroyView.as_view(), name='offers-detail'),
    path('offerdetails/<int:pk>/', views.OfferDetailView.as_view(),
         name='offerdetails-detail'),
    path('orders/', views.OrderListCreateView.as_view(), name='orders-list'),
    path('orders/<int:pk>/', views.OrderUpdateDeleteView.as_view(),
         name='orders-detail'),
    path('order-count/<int:business_user_id>/',
         views.OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/',
         views.OrderCompleteCount.as_view(), name='completed-orders'),
    path('reviews/', views.ReviewListCreateView.as_view(), name='reviews-list'),
    path('reviews/<int:pk>/', views.ReviewUpdateDeleteView.as_view(),
         name='reviews-detail'),
    path('base-info/', views.BaseInfoView.as_view(), name='base-info')
]
