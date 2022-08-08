from controller import check_if_present_in_boundary
from flask import Flask
from flask_apscheduler import APScheduler
import json

TOTAL_NUM_OF_CLINICIAN = 6
ALERT_TIME = 300

app = Flask(__name__)
scheduler = APScheduler()
memory = dict()
clinicianIdCount = 1

@app.route("/")
def index():
      
    return "Welcome to the Alert System!"
  
def cron_job(email, password):
      
    clinician_id = get_clinician_id()
    check_if_present_in_boundary(clinician_id, email, password) 
  
def get_credentials():
      
    email = input("Enter sender email (gmail)\n")
    password = input("Enter Google Generated app password\n")
    return(email, password)
    
def initialize_clinician_id():
      
    clinician_id = 1
    file = open('clinician_id.txt', 'w')
    file.write(str(clinician_id))
    file.close()
      
def initialize_Cache():
      
    with open("Cache.json", "w") as jsonFile:
      json.dump({}, jsonFile)

      
def get_clinician_id():
      
    global TOTAL_NUM_OF_CLINICIAN  
    content = open('clinician_id.txt', 'r').readline()

    for line in content:
        clinician_id = int(line)
        
    clinician_id = (clinician_id) % TOTAL_NUM_OF_CLINICIAN
    
    file = open('clinician_id.txt', 'w')
    file.write(str(clinician_id+1))
    file.close()
    
    if clinician_id == 0 :
          clinician_id = TOTAL_NUM_OF_CLINICIAN
    
    return str(clinician_id)
          
if __name__ == '__main__':
      
    initialize_clinician_id()
    initialize_Cache()
    email, password = get_credentials() 
    time_interval = int(ALERT_TIME / TOTAL_NUM_OF_CLINICIAN) - 5
    scheduler.add_job(id ='Scheduled task', func = cron_job, args = [email, password], trigger = 'interval', seconds = time_interval)
    scheduler.start()
    app.run()