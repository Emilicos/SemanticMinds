from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('search/', views.searchpage, name='searchPage'),
    path('data/<str:uri>/', views.companyDetail, name='companyDetail'),
]