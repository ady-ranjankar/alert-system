def is_point_onSegment(p1, p2, p3):
     
    if ((p2[0] <= max(p1[0], p3[0])) &
        (p2[0] >= min(p1[0], p3[0])) &
        (p2[1] <= max(p1[1], p3[1])) &
        (p2[1] >= min(p1[1], p3[1]))):
        return True
         
    return False

def get_orientation(p1, p2, p3):
     
    val = (((p2[1] - p1[1]) *
            (p3[0] - p2[0])) -
           ((p2[0] - p1[0]) *
            (p3[1] - p2[1])))
    
            
    if val == 0:
        return 0
    if val > 0:
        return 1 
    else:
        return 2 
 
def check_intersection(p1, q1, p2, q2):

    o1 = get_orientation(p1, q1, p2)
    o2 = get_orientation(p1, q1, q2)
    o3 = get_orientation(p2, q2, p1)
    o4 = get_orientation(p2, q2, q1)
 

    if (o1 != o2) and (o3 != o4):
        return True
     
    if (o1 == 0) and (is_point_onSegment(p1, p2, q1)):
        return True

    if (o2 == 0) and (is_point_onSegment(p1, q2, q1)):
        return True
 
    if (o3 == 0) and (is_point_onSegment(p2, p1, q2)):
        return True
 
    if (o4 == 0) and (is_point_onSegment(p2, q1, q2)):
        return True
 
    return False
 
def check_if_point_in_boundary(point_coordinates, area_coordinates):
    decrease = 0
    point = point_coordinates
    polygon = area_coordinates[0]
    no_of_intersections = 0
    m1 = point[0]
    for i in polygon[1:]:
        if i[0] > m1:
            m1 = i[0]

    point_2 = [m1+0.1, point[1]]

    for i in range(len(polygon) - 1):
        if(polygon[i][1] == point[1]):
            if(i==0):
                prev = len(polygon)-2
            else:
                prev = i-1
            if(get_orientation(point,polygon[i],polygon[i+1]) != get_orientation(point,polygon[i],polygon[prev])):
                decrease += 1
        if(check_intersection(point, point_2, polygon[i], polygon[i+1])):
            if get_orientation(polygon[i], point,
                           polygon[i+1]) == 0:
                return is_point_onSegment(polygon[i], point,
                                 polygon[i+1])
            no_of_intersections += 1
            
    no_of_intersections -= decrease
    
    if( no_of_intersections > 0):
        return (no_of_intersections % 2 == 1)
    return(False)
    