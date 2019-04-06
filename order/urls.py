from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view),
    path('register/', views.register, name='register'),
    path('orderbook/<str:base_code>/<str:quote_code>/',
        views.orderbook, name='orderbook'),
]
