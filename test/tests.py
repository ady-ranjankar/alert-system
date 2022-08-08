from ctypes.wintypes import POINT
import datetime
import unittest
import json
import server
import controller
from services import cache_service


import warnings
warnings.filterwarnings("ignore")


class AlertTester(unittest.TestCase):
 
    def test_generate_url(self):
        self.assertEqual(controller.generate_url("1"), "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/1")
        
    def test_extract_coordinates(self):
        with open('demo.json') as f:
            coordinates = json.load(f)
            
        point_coordinates = coordinates['features'][0]['geometry']['coordinates']
        area_coordinates = coordinates['features'][1]['geometry']['coordinates']
        self.assertEquals(controller.extract_coordinates(coordinates),(point_coordinates,area_coordinates))
        
    def test_key_not_in_cache(self):
        with open("Cache.json", "r") as json_file:
            memory = json.load(json_file)
        
        POINT_1 = [-121.94353337287903,
            37.31217050790307]
            
        BOUNDARY_1 =  [[[-121.93468093872069, 37.33631625612842],
            [-121.96249008178712, 37.33617976989369],
            [-121.96523666381836, 37.304644804751106],
            [-121.93708419799805, 37.30491789153446],
            [-121.93777084350586, 37.31761533167621],
            [-121.95150375366211, 37.316796206705085],
            [-121.95219039916992, 37.32607910032697],
            [-121.93708419799805, 37.32648861334206],
            [-121.93468093872069, 37.33631625612842]]]
        
        self.assertFalse(cache_service.check_cache("90", POINT_1, BOUNDARY_1))
        
    def test_key_in_cache_without_expired_timestamp(self):
        
        POINT_1 = [-121.94353337287903,
            37.31217050790307]
            
        BOUNDARY_1 =  [[[-121.93468093872069, 37.33631625612842],
            [-121.96249008178712, 37.33617976989369],
            [-121.96523666381836, 37.304644804751106],
            [-121.93708419799805, 37.30491789153446],
            [-121.93777084350586, 37.31761533167621],
            [-121.95150375366211, 37.316796206705085],
            [-121.95219039916992, 37.32607910032697],
            [-121.93708419799805, 37.32648861334206],
            [-121.93468093872069, 37.33631625612842]]]
        memory = dict()
        memory["1"] = [POINT_1, BOUNDARY_1, True, datetime.datetime.now().timestamp()]
        with open("Cache.json", "w") as jsonFile:
            json.dump(memory, jsonFile)  
        self.assertTrue(cache_service.check_cache("1", POINT_1, BOUNDARY_1))
        
    def test_key_in_cache_with_expired_timestamp(self):
        POINT_1 = [-121.94353337287903,
            37.31217050790307]
            
        BOUNDARY_1 =  [[[-121.93468093872069, 37.33631625612842],
            [-121.96249008178712, 37.33617976989369],
            [-121.96523666381836, 37.304644804751106],
            [-121.93708419799805, 37.30491789153446],
            [-121.93777084350586, 37.31761533167621],
            [-121.95150375366211, 37.316796206705085],
            [-121.95219039916992, 37.32607910032697],
            [-121.93708419799805, 37.32648861334206],
            [-121.93468093872069, 37.33631625612842]]]
        memory = dict()
        memory["1"] = [POINT_1, BOUNDARY_1, True, datetime.datetime.now().timestamp() - 2400]
        with open("Cache.json", "w") as jsonFile:
            json.dump(memory, jsonFile)  
        self.assertFalse(cache_service.check_cache("1", POINT_1, BOUNDARY_1))
            
    def test_is_alert_send_with_key_not_in_cache(self):
        self.assertFalse(cache_service.is_alert_sent("90"))
        

    def test_controller(self):
        email, password = server.get_credentials() 
        
        self.assertFalse(controller.check_if_present_in_boundary("7", email, password))
        
        
    
        
        
if __name__ == '__main__':
    unittest.main()