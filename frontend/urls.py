from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.searchPage, name='searchPage'),
    path('data/<str:uri>/', views.companyDetail, name='companyDetail'),
]