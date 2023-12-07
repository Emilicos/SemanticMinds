from django.shortcuts import render, redirect

import requests

# Create your views here.

API_URL = "http://localhost:8000/api"

def searchPage(request):
    return render(request, 'home_page.html')

def companyDetail(request, uri):
    response = requests.get(f'{API_URL}/data/{uri}')
    context = {'api_data': response.json()}

    return render(request, 'company_detail.html', context)
