import pandas as pd
from haversine import haversine

def calculate_distance(data: pd.DataFrame, p1_lat, p1_lng, p2_lat, p2_lng):
    
    def calculate_haversine(row):
        p1 = (row[p1_lat], row[p1_lng])
        p2 = (row[p2_lat], row[p2_lng])
        distance = haversine(p1, p2, unit='km')
        return distance
    
    distance = data.apply(calculate_haversine, axis=1)
    return distance