from django.urls import path
from . import views

urlpatterns = [
    path('', views.searchPage, name='searchPage'),
    path('company/<str:uri>/', views.companyDetail, name='companyDetail'),
]