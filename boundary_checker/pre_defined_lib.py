from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
 

def check_if_point_in_boundary(point_coordinates, area_coordinates):

    #Check if point on boundary
    for boundary in area_coordinates:
        for i in range(len(boundary) - 1):
            if onSegment(boundary[i], point_coordinates, boundary[i+1]):
                return(True)
        
    point = Point(point_coordinates)
    for boundary in area_coordinates:
        polygon = Polygon(boundary)
        if polygon.contains(point):
            return True
    return False

def onSegment(p1, p2, p3):
     
    if ((p2[0] <= max(p1[0], p3[0])) &
        (p2[0] >= min(p1[0], p3[0])) &
        (p2[1] <= max(p1[1], p3[1])) &
        (p2[1] >= min(p1[1], p3[1]))):
        return True
         
    return False

