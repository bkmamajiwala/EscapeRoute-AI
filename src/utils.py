def load_json(file_path):
    import json
    with open(file_path, 'r') as file:
        return json.load(file)

def load_csv(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

def save_json(data, file_path):
    import json
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def calculate_distance(coord1, coord2):
    from math import sqrt
    return sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

def rank_shelters(shelters, user_location):
    shelters['distance'] = shelters.apply(lambda row: calculate_distance((row['latitude'], row['longitude']), user_location), axis=1)
    return shelters.sort_values(by=['safety_score', 'distance'])