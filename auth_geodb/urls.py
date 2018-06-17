from django.urls import path
from auth_geodb import views

urlpatterns = [
    path('', views.auth_login, name="auth_login"),
    path('logout', views.auth_logout, name="auth_logout"),
]
