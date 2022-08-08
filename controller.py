from boundary_checker.algorithm import check_if_point_in_boundary as algorithm
from boundary_checker.pre_defined_lib import check_if_point_in_boundary as pre_def

import json

import requests

from services.alert_message import send_alert
from services.cache_service import check_cache, update_cache, is_alert_sent


BOUNDARY_CHECK = 'ALGORITHM'

URL_PREFIX = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/"

def generate_url(clinician_id):
    global URL_PREFIX
    return URL_PREFIX + clinician_id

def extract_coordinates(coordinates):
    point_coordinates = coordinates['features'][0]['geometry']['coordinates']
    area_coordinates = coordinates['features'][1]['geometry']['coordinates']

    return(point_coordinates, area_coordinates)
    
def check_if_present_in_boundary(clinician_id, email, password):
    url = generate_url(clinician_id)
    is_present = False
    try:
        r = requests.get(url)
        
        if r.status_code != 200 :
            if is_alert_sent(clinician_id) == False:
                send_alert(clinician_id, email, password)
            return
                
          
        coordinates = r.json()

        point_coordinates, area_coordinates = extract_coordinates(coordinates)
        
        #Checks if alert was sent in the past 20 minutes
        if(check_cache(clinician_id, point_coordinates, area_coordinates) == False):
            is_present = call_boundary_algorithm(BOUNDARY_CHECK, point_coordinates, area_coordinates)
            if(is_present == False):
                send_alert(clinician_id, email, password)
            
            update_cache(clinician_id, point_coordinates, area_coordinates, is_present)
            
    except:
        print("damn")
        send_alert(clinician_id, email, password)
    return is_present
        
def call_boundary_algorithm(boundary_check, point_coordinates, area_coordinates):
    if boundary_check == 'ALGORITHM':
        return algorithm(point_coordinates, area_coordinates)
    
    if boundary_check == 'LIBRARY':
        return pre_def(point_coordinates, area_coordinates)
        
    
    
        
        

    