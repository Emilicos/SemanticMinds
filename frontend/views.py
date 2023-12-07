from django.shortcuts import render, redirect

import requests

# Create your views here.

API_URL = "http://localhost:8000/api"

def homepage(request):
    return render(request, 'home_page.html')

def searchpage(request):
    search = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    limit = 10
    offset = (int(page) - 1) * limit

    params = {
        "q": search,
        "page": page
    }
    
    response = requests.get(f'{API_URL}/search/', params=params)
    context = {'api_data': response.json()}

    print(context.get('api_data'))
    
    return render(request, 'search_page.html', context)

def companyDetail(request, uri):
    response = requests.get(f'{API_URL}/data/{uri}')
    context = {'api_data': response.json()}

    return render(request, 'company_detail.html', context)
