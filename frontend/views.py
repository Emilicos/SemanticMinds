from django.shortcuts import render, redirect

import requests

# Create your views here.

API_URL = "http://localhost:9999/api"

def searchPage(request):
    return render(request, 'home_page.html')

def companyDetail(request, uri):
    
    return render(request, 'company_detail.html')
