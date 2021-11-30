from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib import messages
from .models import Sensorset, Data
from .utils import get_plot
from datetime import datetime
from statistics import fmean, stdev

import requests
import json

# Create your views here.

sensors = Sensorset.objects.all()
data = Data.objects.all()

def home(request):

    return render(request, 'home.html', {'sensors': sensors})

def showresult(request):
    
    sense_ip = request.POST['sensorset']
    response = requests.get(sense_ip)
    data = response.json()

    now = datetime.now()
    timestp = now.strftime("%Y, %b %d --> %X")

    return render(request, 'dash.html', { 'data': data, 'sense_ip':sense_ip, 'sensors': sensors, 'timestp': timestp } )

def analyze(request):
    
    if request.method=='POST':
        try:
            sens_id = request.POST['sensorset_ana']
            date_ini = request.POST['date_ini']
            date_fin = request.POST['date_fin']
            
            data_filter = Data.objects.filter(sensorset_id=sens_id, datetime__range=[date_ini, date_fin])

            x = [x.datetime.strftime('%y/%m/%d %H:%M') for x in data_filter]
            yt = [yt.temp for yt in data_filter]
            yh = [yh.humid for yh in data_filter]
            ym = [ym.soilh for ym in data_filter]
            yvi = [yvi.li_vis for yvi in data_filter]
            yIR = [yIR.li_IR for yIR in data_filter]
            yUV = [yUV.li_UV for yUV in data_filter]

            chart = get_plot(x, yt, yh, ym, yvi, yIR, yUV)

            date = {
                'Start Date' : date_ini,
                'End Date' : date_fin
            }

            averages = {
                'Temp' : round(fmean(yt), 1),
                'Humid' : round(fmean(yh), 1),
                'Soil mois' : round(fmean(ym), 1),
                'Vis Light' : round(fmean(yvi), 1),
                'IR' : round(fmean(yIR), 1),
                'UV' : round(fmean(yUV), 2)
            }
            
            maxs = {
                'temp' : max(yt),
                'humid' : max(yh),
                'Soil mois' : max(ym),
                'Vis Light' : max(yvi),
                'IR' : max(yIR),
                'UV' : max(yUV)
            }

            mins = {
                'temp' : min(yt),
                'humid' : min(yh),
                'Soil mois' : min(ym),
                'Vis Light' : min(yvi),
                'IR' : min(yIR),
                'UV' : min(yUV)
            }

            stdevs = {
                'temp' : round(stdev(yt), 2),
                'humid' : round(stdev(yh), 2),
                'Soil mois' : round(stdev(ym), 2),
                'Vis Light' : round(stdev(yvi), 2),
                'IR' : round(stdev(yIR), 2),
                'UV' : round(stdev(yUV), 2)
            }
        except:
            message = "There is no sufficient data to be analized. There must be at least one reading for each parameter. Try another interval or check database."
            return render(request, 'analyze.html',{'data':data, 'sensors': sensors, 'message':message,})
        
        return render(request, 'analyze.html', {'sens_id':int(sens_id), 'date':date, 'chart':chart, 'data':data, 'sensors': sensors, 'averages':averages, 'maxs':maxs, 'mins': mins, 'stdevs':stdevs,})

    else:
        return render(request, 'analyze.html',{'data':data, 'sensors': sensors,})

