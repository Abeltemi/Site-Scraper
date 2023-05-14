from django.shortcuts import render
from .models import Link

import requests
from bs4 import BeautifulSoup

from django.http import HttpResponseRedirect

# Create your views here.
URL = 'http://www.google.com'

def scrape(request):
    
    if request.method == "POST":
        address_name = request.POST.get('site', '')
        response = requests.get(url=address_name)
        if response.status_code == 200:
            html_text = response.text
            soup = BeautifulSoup(html_text, 'html.parser')
            for link in soup.find_all('a'):
                name = link.string
                address = link.get('href')
                Link.objects.create(name=name, address=address)
        else:
            data = Link.objects.all()
            print('error getting data')
        return HttpResponseRedirect('/')
    else:
        data = Link.objects.all()
            
    return render(request, 'scraperapp/result.html', {'data': data})
                
def delete(request):
    Link.objects.all().delete()
    
    return render(request, 'scraperapp/result.html')