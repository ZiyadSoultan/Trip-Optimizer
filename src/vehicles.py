import matplotlib.pyplot as plt
import numpy as np

from vehicle import Vehicle


class Vehicles(list):
    def __init__(self, *vehicles):
        super().__init__(vehicles)
        self.filtered_land = [vehicle for vehicle in self if vehicle.medium in (1, 3)]
        self.filtered_water = [vehicle for vehicle in self if vehicle.medium in (2, 3)]

    def __contains__(self, vehicle: Vehicle) -> bool:
        for v in self:
            if v.name == vehicle.name:
                return True
        return False

    def __getitem__(self, key: str or int) -> Vehicle:
        if type(key) == int:
            return super().__getitem__(key)
        else:
            for v in self:
                if str(v) == key:
                    return v
            vehicle = Vehicle({"Name": '', "Medium": 3, "Bounds": [0, 0], "Lifespan": 0, "Emissions": 0, "MEmissions": 0, "PMPGe": 0, "Speed": 0, "Cost": 0})
            vehicle.total_emissions, vehicle.total_time, vehicle.total_cost, vehicle.total_energy_usage = [0], [0], [0], [0]
            return vehicle

    def process(self, distance: int, medium: int, imperial: bool = False) -> None:

        methods = ("generate_emissions", "generate_cost", "generate_energy_usage", "generate_time")
        keys = ("Lowest Emissions", "Cheapest", "Most Efficient", "Fastest")

        if not imperial:
            lower_bound = lambda v: v.bounds[0]
            upper_bound = lambda v: v.bounds[1]
        else:
            lower_bound = lambda v: v.bounds[0] * 0.621371
            upper_bound = lambda v: v.bounds[1] * 0.621371

        if medium == 1:
            # These are the x values for plotting
            self.distance_land = np.arange(0, distance + 1)

            # FILTERING:
            # These two lists will contain vehicles that are capable of travelling over the given trip distance over water and
            # land. For example, you cannot drive over water so the car vehicle would not be in filtered_water. You can take a
            # train over land, however trains do not make trips of 1 km so if your trip is 1 km long, a train is not a valid
            # mode of transport either and therefore would not be in filtered_land. Walking however can be done over land and
            # can be done at a distance of 1 km, and therefore it would go into filtered_land as a valid mode of transport over
            # the land portion of this trip.
            self.filtered_land = list()
            for vehicle in self:
                if vehicle.medium in (1, 3) and lower_bound(vehicle) <= distance <= upper_bound(vehicle):
                    self.filtered_land.append(vehicle)
            # If no vehicles are available, exit prematurely
            if len(self.filtered_land) == 0:
                return None

            # OPTIMIZING
            # These dictionaries contain the optimized vehicles (ex. least emissions, cheapest, etc)
            self.optimized_land = dict()
            for i in range(4):
                self.optimized_land[keys[i]] = eval(f"sorted(self.filtered_land, key=lambda v: v.{methods[i]}({distance}, {imperial})[-1])[0]")

        else:
            self.distance_water = np.arange(0, distance + 1)

            self.filtered_water = list()
            for vehicle in self:
                if vehicle.medium in (2, 3) and lower_bound(vehicle) <= distance <= upper_bound(vehicle):
                    self.filtered_water.append(vehicle)
            if len(self.filtered_water) == 0:
                return None

            self.optimized_water = dict()
            for i in range(4):
                self.optimized_water[keys[i]] = eval(f"sorted(self.filtered_water, key=lambda v: v.{methods[i]}({distance}, {imperial})[-1])[0]")

    def make_plots(self, land: str, water: str, metric: str, imperial: bool = False) -> plt.figure:
        if metric == "Emissions":
            attr = "total_emissions"
            unit = "kg CO2e per passenger km" if not imperial else "lb CO2e per passenger mi"
        elif metric == "Efficiency":
            attr = "total_energy_usage"
            unit = "GJ per passenger km" if not imperial else "GGE per passenger mi"
        elif metric == "Cost":
            attr = "total_cost"
            unit = "CAD" if not imperial else "USD"
        else:
            attr = "total_time"
            unit = "Hours per km" if not imperial else "Hours per mi"

        plt.close("all")
        plt.style.use("seaborn")
        fig, (ax_land, ax_water) = plt.subplots(2)
        fig.suptitle(f"{metric} per Kilometer" if not imperial else f"{metric} per Mile")

        # Land
        if not land:
            fig.delaxes(ax_land)
        else:
            ax_land.set_ylabel(unit)
            ax_land.set_xlabel(f"Distance by {land} (km)" if not imperial else f"Distance of {land} (mi)")
            for v in self.filtered_land:
                if v != land:
                    ax_land.plot(self.distance_land, getattr(v, attr), color="tab:gray", linestyle="dashed")
                else:
                    ax_land.plot(self.distance_land, getattr(v, attr), color="green", linestyle="solid", label=land)
            ax_land.legend()

        # Water
        if not water:
            fig.delaxes(ax_water)
        else:
            ax_water.set_ylabel(unit)
            ax_water.set_xlabel(f"Distance by {water} (km)" if not imperial else f"Distance of {water} (mi)")
            for v in self.filtered_water:
                if v != water:
                    ax_water.plot(self.distance_water, getattr(v, attr), color="tab:gray", linestyle="dashed")
                else:
                    ax_water.plot(self.distance_water, getattr(v, attr), color="blue", linestyle="solid", label=water)
            ax_water.legend()

        fig.tight_layout()
        return fig
