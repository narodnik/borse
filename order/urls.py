from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('other/', views.other),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view),
]
