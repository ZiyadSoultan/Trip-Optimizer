from src.vehicle import Vehicle


def test_vehicle():
    values = {"Name": "Car", "Medium": 1, "Bounds": [1, 100], "Lifespan": 100, "Emissions": 0.2, "MEmissions": 600, "PMPGe": 20, "Speed": 80, "Cost": 0.3}
    car = Vehicle(values)
    assert str(car) == values["Name"]
    car_2 = Vehicle(values)
    assert car == car_2
    car_2.name = "Not car"
    assert car != car_2
    assert car.generate_emissions(100)[0] == 600
    assert car.generate_emissions(100)[-1] == 620
    assert round(car.generate_energy_usage(100, True)[-1]) == 5
    assert len(car.generate_time(100)) == 101
