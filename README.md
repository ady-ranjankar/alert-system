## DESIGN:


•	User inputs credentials 

•	Server starts cron job and calls the controller

•	Controller polls the Clinician Status API for the current clinician Id

•	Controller checks if the response sent by the API is present in cache

•	If it isn’t, the boundary algorithm is called to check if the clinician is inside the boundary

•	If the clinician isn't inside the boundary, the alert service is called which sends an alert email

![Alert](https://user-images.githubusercontent.com/41305151/183332839-35ca5712-5432-485a-b64f-3e81f4db70d3.jpg)



## BOUNDARY ENGINE:

A Boundary engine is used to get the status of the clinician. This is implemented using the Factory Design Pattern. Based on which boundary algorithm is used, the controller decides if an alert needs to be sent.



## CACHING SERVICE:

For caching, a json file is used which stores the clinician ID as the key. The value contains the point coordinate of the clinician, boundary coordinates, whether the clinician is present in the boundary and the time stamp.

When a response from the Clinician Status API is made, the controller checks the cache for the clinician ID. 

If found, it checks how old the timestamp is. 

If it is less than 10 minutes old, it then checks if the clinician has moved from their previous position. 

If they haven’t then no alert is sent even if they are outside the boundary. 

If the clinician has moved or if the timestamp is old, the boundary engine is called again and the updated results are written to the cache.


## RUNNING:

Installing dependencies:

	pip install flask

	pip install Flask-APScheduler

	pip install shapely


To start the service:

Run:

    python server.py
    
•	Enter your gmail id 

•	Enter your Google App generated password (https://support.google.com/accounts/answer/185833?hl=en)


To run tests:

Run:

    python -W ignore -m unittest test/tests.py

    
## References:

•	https://danhwashere.com/python-flask-cron-jobs

•	https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon

•	https://pypi.org/project/shapely/


	


