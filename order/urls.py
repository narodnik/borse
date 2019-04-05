from django.urls import path

from . import views

app_name = 'order'
urlpatterns = [
    path('', views.index),
    path('other/', views.other),
    path('logout/', views.logout_view),
]
