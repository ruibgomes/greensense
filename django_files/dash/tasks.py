from celery import shared_task
from .models import Sensorset, Data
from datetime import datetime
from django.utils import timezone
from time import sleep

import requests

@shared_task
def write_data():   
    # Apend list with all IPs
    for obj in reversed(Sensorset.objects.all()): 
        # Get data from JSON API and store in a dict
        ip_address = obj.ip_address
        response = requests.get(ip_address)
        data_dict = response.json()
        # get sensorset primary key to pass as foreing key
        sensorset_id = Sensorset.objects.get(ip_address=ip_address).pk

        # getting data elements from the dict
        temp = data_dict['Temp'] 
        humid = data_dict['Humid'] 
        soilh = data_dict['SoilM'] 
        li_vis = data_dict['Vis']
        li_IR = data_dict['IR'] 
        li_UV = data_dict['UV']

        # set datetime for now
        timenow = datetime.now()
        timenow_str = timenow.strftime("%Y-%m-%d %H:%M:%S")

        # Saving parameters in database
        data_entry = Data(sensorset_id = sensorset_id, temp = temp, humid = humid, soilh = soilh, li_vis = li_vis, li_IR = li_IR, li_UV = li_UV, datetime = timenow)
        data_entry.save()

        #Print success message
        message = print(f'Data saved @{timenow} for {sensorset_id}')       
        
    return message
write_data()



