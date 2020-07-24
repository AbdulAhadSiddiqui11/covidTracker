from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
import requests
import urllib.parse
from django.views.decorators.csrf import csrf_exempt

import json

from . import getdata, maps


def index(request): 
    world_map_dict = world_map()

    context = dict(**world_map_dict)

    return render(request, template_name='stats.html', context=context)

def report(request):
    df = getdata.daily_report(date_string=None)
    df = df[['Confirmed', 'Deaths', 'Recovered']].sum()
    death_rate = f'{(df.Deaths / df.Confirmed)*100:.02f}%'

    data = {
        'num_confirmed': int(df.Confirmed),
        'num_recovered': int(df.Recovered),
        'num_deaths': int(df.Deaths),
        'death_rate': death_rate
    }

    data = json.dumps(data)

    return HttpResponse(data, content_type='application/json')


def trends(request):
    df = getdata.percentage_trends()

    data = {
        'confirmed_trend': int(round(df.Confirmed)),
        'deaths_trend': int(round(df.Deaths)),
        'recovered_trend': int(round(df.Recovered)),
        'death_rate_trend': float(df.Death_rate)
    }

    data = json.dumps(data)

    return HttpResponse(data, content_type='application/json')


def global_cases(request):
    df = getdata.global_cases()
    return HttpResponse(df.to_json(orient='records'), content_type='application/json')


def world_map():
    plot_div = maps.world_map()
    return {'world_map': plot_div}


def realtime_growth(request):
    import pandas as pd
    df = getdata.realtime_growth();

    df.index = pd.to_datetime(df.index)
    df.index = df.index.strftime('%Y-%m-%d')

    return HttpResponse(df.to_json(orient='columns'), content_type='application/json')


def daily_growth(request):
    df_confirmed = getdata.daily_confirmed()[["date", "World"]]
    df_deaths = getdata.daily_deaths()[["date", "World"]]

    df_confirmed = df_confirmed.set_index("date")
    df_deaths = df_deaths.set_index("date")

    json_string = '{' + \
        '"confirmed": ' + df_confirmed.to_json(orient='columns') + ',' + \
        '"deaths": ' + df_deaths.to_json(orient='columns') + \
    '}'

    return HttpResponse(json_string, content_type='application/json')

@csrf_exempt
def getHospitals(request):
    print('inside gethospitals')
    isolation=[
        "Gandhi General Hospital",
        "Government Chest and General Hospital",
        "Fever Hospital",
        "MGM Hospital",
        "RIMS",
        "District Hospital",
        "Government General Hospital",
        "Care Hospital",
        "Continental Hospital",
        "Apollo Hospital",
        "Thumbay Hospital",
        "Virinchi Hospital",
        "Star Hospital",
        "Yashoda Hospital",
        "KIMS Hospital",
        "Sunshine Hospital",
        "Omega Hospital",
        "Prathima Hospital",
        "Star Hospitals",
        ]
    if request.method == 'POST':
        #print("in IF")
        print(request.POST)
        data = json.loads(request.body.decode('utf-8'))
        address = str(data['loc'])
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
        #print('Sending request 1')
        response = requests.get(url,headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}, params={})
        #print('got a response')
        response = response.json()
        URL = "https://discover.search.hereapi.com/v1/discover"
        latitude =  str(response[0]["lat"])
        longitude = str(response[0]["lon"])
        api_key = 'tu4m3GFeH7ze3oQDsOBqMpRk3-yFx7XyapfV92Yw-uo' # Acquire from developer.here.com
        query = 'hospitals'
        limit = 10
        PARAMS = {
                    'apikey':api_key,
                    'q':query,
                    'limit': limit,
                    'at':'{},{}'.format(latitude,longitude)
                } 

        # sending get request and saving the response as response object 
        #print('Sending request 2')
        r = requests.get(url = URL, params = PARAMS) 
        data = r.json()
        result=[]
        isoltion_center=[]
        hospital=[]
        #print('got a response 2')
        for i in range(limit):
            title=data['items'][i]['title']
            res=hospitalFive_address =  data['items'][i]['address']['label']
            if title in isolation:
                isoltion_center.append(res)
            else:	
                hospital.append(res)
        result=[isoltion_center,hospital]
        #print(result)
        return HttpResponse(json.dumps({'hospitals':result}), content_type='application/json')