from django.shortcuts import render, redirect

import requests

# Create your views here.

API_URL = "http://localhost:8000/api"

def homepage(request):
    return render(request, 'home_page.html')

def searchpage(request):
    search = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    params = {
        "q": search,
        "page": page
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    response = requests.get(f'{API_URL}/search/', params=params, headers=headers)
    context = {'api_data': response.json()['data'], 'pagination': response.json()['pagination'], 'range': range(1, response.json()['pagination']['last_page']+1), 'search': search}
    
    return render(request, 'search_page.html', context)

def companyDetail(request, uri):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    response = requests.get(f'{API_URL}/data/{uri}', headers=headers)
    context = {'api_data': response.json()}

    return render(request, 'company_detail.html', context)
