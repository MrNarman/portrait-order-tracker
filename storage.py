import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "orders.json")

def load_data():
    """
    """
    with open(DATA_PATH, "r") as file:
        return json.load(file)
    
def save_data(data:dict):
    """
        Writes to json file that stores orders.
    """
    with open(DATA_PATH, "w") as file:
        return json.dump(data, file, indent=2)

