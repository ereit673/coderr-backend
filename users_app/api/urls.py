from django.urls import path

from . import views

urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.CustomAuthToken.as_view(), name='login'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profiles/business/', views.BusinessProfileListView.as_view(),
         name='business_profiles')
]
