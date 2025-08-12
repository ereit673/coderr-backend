from django.urls import path

from . import views

urlpatterns = [
    path('orders/', views.OrderListCreateView.as_view(), name='orders-list'),
    path('orders/<int:pk>/', views.OrderUpdateDeleteView.as_view(),
         name='orders-detail'),
    path('order-count/<int:business_user_id>/',
         views.OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/',
         views.OrderCompleteCount.as_view(), name='completed-orders'),
]
