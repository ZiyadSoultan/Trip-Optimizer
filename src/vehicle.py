import numpy as np


class Vehicle:
    def __init__(self, vehicle):
        self.name = vehicle["Name"]
        self.medium = vehicle["Medium"]
        self.bounds = vehicle["Bounds"]
        self.lifespan = vehicle["Lifespan"]
        self.emissions = vehicle["Emissions"]
        self.MEmissions = vehicle["MEmissions"]
        self.PMPGe = vehicle["PMPGe"]
        self.speed = vehicle["Speed"]
        self.cost = vehicle["Cost"]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        # return f"{self.name=}\n{self.medium=}\n{self.bounds=}\n{self.lifespan=}\n{self.emissions=}\n{self.MEmissions=}\n{self.PMPGe=}\n{self.speed=}\n{self.cost=}"
        return str(self)

    def __eq__(self, vehicle) -> bool:
        if str(self) == str(vehicle):
            return True
        return False

    def generate_emissions(self, distance: int, imperial: bool = False) -> np.array:
        # Recall (from tests.txt) that self.emissions is the emissions per km per passenger, and that self.MEmissions is
        # the emissions to manufacture the vehicle. (trip distance/vehicle lifespan) = percentage of lifespan that a
        # trip accounts for. This percentage * MEmissions evenly distributes the manufacturing emissions over the
        # lifetime of the vehicle.
        if not imperial:
            # kg CO2e per passenger km
            b = distance / self.lifespan * self.MEmissions
            self.total_emissions = np.array([self.emissions * i + b for i in range(distance + 1)])
        else:
            # lb CO2e per passenger mi
            emissions_imperial, MEmissions_imperial = self.emissions * 3.548, self.MEmissions * 2.20462
            lifespan_imperial = self.lifespan * 0.621371
            b = distance / lifespan_imperial * MEmissions_imperial
            self.total_emissions = np.array([emissions_imperial * i + b for i in range(distance + 1)])
        return self.total_emissions

    def generate_energy_usage(self, distance: int, imperial: bool = False) -> np.array:
        if not imperial:
            # GJ per passenger km
            GJ_per_km = self.PMPGe * 0.0753959377224
            self.total_energy_usage = np.array([GJ_per_km * i for i in range(distance + 1)])
        else:
            # GGE per passenger mi
            gas_gal_equiv_per_mi = 1 / self.PMPGe
            self.total_energy_usage = np.array([gas_gal_equiv_per_mi * i for i in range(distance + 1)])
        return self.total_energy_usage

    def generate_cost(self, distance: int, imperial: bool = False) -> np.array:
        if not imperial:
            # CAD per km
            self.total_cost = np.array([self.cost * i for i in range(distance + 1)])
        else:
            # USD per mile
            with open("USD.txt", 'r') as file:
                USD = float(file.read())
            USD_per_mi = self.cost * USD / 0.621371
            self.total_cost = np.array([USD_per_mi * i for i in range(distance + 1)])
        return self.total_cost

    def generate_time(self, distance: int, imperial: bool = False) -> np.array:
        if not imperial:
            # Hours per km
            self.total_time = np.array([i / self.speed for i in range(distance + 1)])
        else:
            # Hours per mi
            mph = self.speed * 0.621371
            self.total_time = np.array([i / mph for i in range(distance + 1)])
        return self.total_time
