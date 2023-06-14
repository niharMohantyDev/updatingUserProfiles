from django.urls import path
from profiles import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomAuthToken.as_view(), name='login'),
    path('update/', views.update, name='update'),
    path('logout/', views.logout, name='logout'),
]