import json
import datetime

def read_from_cache():
    
    with open("Cache.json", "r") as json_file:
        memory = json.load(json_file)
    
    return memory

def check_cache(clincican_id, point_coordinates, area_coordinates):
    key = clincican_id
    memory = read_from_cache()
    
    if key in memory:
        
        if is_timestamp_old(memory, key):
            memory.pop(key)
            write_to_cache(memory)
            return False
        
        elif memory[key][0] == point_coordinates and memory[key][1] == area_coordinates:
            return True
        
        else:
            return False

    else:
        return False
        
def is_alert_sent(clincican_id):
    key = clincican_id
    memory = read_from_cache()
    
    if key in memory: 
        #Check if last position was inside the boundary
        if memory[key][2] == True:
            return False
        
        #Check when was the last position outside the boundary
        else:
            if is_timestamp_old(memory, key):
                return False
            return True   
    else:
        return False
    
def update_cache(clincican_id, point_coordinates, area_coordinates, is_present):
    key = clincican_id
    memory = read_from_cache()
    memory[key] = [point_coordinates, area_coordinates, is_present, datetime.datetime.now().timestamp()]
    write_to_cache(memory)
    
def is_timestamp_old(memory, key):
    if(datetime.datetime.now().timestamp() - memory[key][3] > 1200):
        return(True)
    return(False)
    
def write_to_cache(memory):
    with open("Cache.json", "w") as jsonFile:
        json.dump(memory, jsonFile)
    
    
    