from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
import requests # for making standard html requests
from bs4 import BeautifulSoup # magical tool for parsing html data
import json # for parsing data



def index(request):
    url='https://www.google.com/search?q=good+news+coronavirus&rlz=1C1CHBD_enIN903IN903&source=lnms&tbm=nws&sa=X&ved=2ahUKEwj904fqz9TqAhVQyjgGHZ-wDjUQ_AUoAXoECAwQAw&biw=1366&bih=625'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    tags = soup.find_all('div', attrs={'class':'BNeawe vvjwJb AP7Wnd'})
    news = []
    for tag in tags:
        news.append(tag.get_text())
    return render(request, "index.html", {'news':news[1:], 'headline':news[0]})

def stats(request):
    return render(request, "stats.html")

def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        template = loader.get_template('pages/' + load_template)
        return HttpResponse(template.render(context, request))

    except:
        template = loader.get_template( 'pages/error-404.html' )
        return HttpResponse(template.render(context, request))