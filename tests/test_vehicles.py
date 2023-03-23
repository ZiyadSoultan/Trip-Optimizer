# THIS TEST ONLY RUNS CORRECTLY ON THE SAMPLE VEHICLES!!!!!!
from glob import glob
import json

from src.vehicles import Vehicles
from src.vehicle import Vehicle


def test_vehicles():
    vehicles = []
    files = []
    for filename in glob("../vehicles/*.json"):
        print(files)
        files.append(filename)
        with open(filename) as f:
            vehicles.append(Vehicle(json.load(f)))


    vehicles = Vehicles(*vehicles)
    assert len(vehicles) == len(files)
    assert vehicles["invalid string index"] == ''  # Indexing by string returns the vehicle object of the same name
    vehicles.process(10, 1)
    assert type(vehicles.filtered_land) == list
