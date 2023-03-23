import json
from glob import glob
import webbrowser
from math import ceil

import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from vehicles import Vehicles
from vehicle import Vehicle
from USD import update_USD


# This function is copied and slightly modified from https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Matplotlib_Embedded_Toolbar.py
def draw(canvas, figure, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()

    figure_canvas_agg = FigureCanvasTkAgg(figure, master=canvas)
    figure_canvas_agg.draw()
    toolbar = NavigationToolbar2Tk(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


def distance_validation(chars: str) -> bool:
    # Checks if a given string is a positive float
    try:
        float(chars)
        return 0 <= float(chars)
    except ValueError as _:
        return False


vehicles = []
files = []
for filename in glob("data/*.json"):
    files.append(filename)
    with open(filename) as f:
        vehicles.append(Vehicle(json.load(f)))
if len(files) > len(set(files)):
    sg.popup("Two vehicles cannot have identical names.", no_titlebar=True, grab_anywhere=True)
    raise ValueError("Two vehicles cannot have identical names.")
if len(files) == 0:
    sg.popup("No vehicle files have been provided.", no_titlebar=True, grab_anywhere=True)
    raise ValueError("No vehicle files have been provided.")

vehicles = Vehicles(*vehicles)
# TODO: custom units
units = {"Distance": "km", "Currency": "CAD"}
imperial = False
metrics = ("Emissions", "Efficiency", "Cost", "Time")
tooltip = f"Distance ({units['Distance']}) should be a positive number. "
empty = list('' for _ in range(6))
table = [["Selected"] + empty,
         ["Lowest Emissions"] + empty,
         ["Cheapest"] + empty,
         ["Most Efficient"] + empty,
         ["Fastest"] + empty
         ]
table_info_metric = "- Emissions: kg CO2 equivalents per passenger" \
                    "\n- Cost: CAD per passenger" \
                    "\n- Energy: gigajoules per passenger" \
                    "\n- Time: hours"
table_info_imperial = "- Emissions: lb CO2 equivalents per passenger" \
                      "\n- Cost: USD per passenger" \
                      "\n- Energy: gasoline gallon equivalent per passenger" \
                      "\n- Time: hours"

frame_land = [[sg.Text("Distance", size=(10, 1)), sg.Input(key="-LAND DISTANCE-", size=(17, 1), tooltip=tooltip, enable_events=True), sg.Text(units["Distance"], key="-LAND DISTANCE UNIT-", size=(3, 1))],
              [sg.Text("Vehicle", size=(10, 1)), sg.Combo(key="-LAND VEHICLE-", size=(15, 1), values=[], enable_events=True)],
              ]
frame_water = [[sg.Text("Distance", size=(10, 1)), sg.Input(key="-WATER DISTANCE-", size=(17, 1), tooltip=tooltip, enable_events=True), sg.Text(units["Distance"], key="-WATER DISTANCE UNIT-", size=(3, 1))],
               [sg.Text("Vehicle", size=(10, 1)), sg.Combo(key="-WATER VEHICLE-", size=(15, 1), values=[], enable_events=True)],
               ]
col_left = sg.Column(layout=[[sg.Frame("Land", frame_land)],
                             [sg.Frame("Water", frame_water)],
                             [sg.Frame('', [[sg.Text("Metric", size=(10, 1)), sg.Combo(key="-METRIC-", size=(15, 1), values=metrics, default_value=metrics[0]), sg.Text('', size=(3, 1))]])],
                             [sg.Button("Update", bind_return_key=True)],
                             [sg.Column([], size=(0, 15))],  # For spacing
                             [sg.Table(table, ["Configuration", "Land Vehicle", "Marine Vehicle", "Emissions", "Cost", "Energy", "Time"], justification="c", num_rows=5, bind_return_key=True, key="-TABLE-", hide_vertical_scroll=True, tooltip=table_info_metric if not imperial else table_info_imperial, def_col_width=16, auto_size_columns=False)]
                             ]
                     )

col_right = sg.Column(layout=[[sg.Canvas(key="-FIGURE-")],
                              [sg.Canvas(key="-CONTROLS-", size=(800, 400))]
                              ]
                      )

menu = [["Units", ["✓ Metric", "_ Imperial"]], ["Help", ["Documentation", "Adding Vehicles", "Report a Bug"]]]

layout = [[sg.Menu(menu, key="-MENU-")],
          [col_left, sg.VerticalSeparator(), col_right]]

sg.theme("DarkBlue13")
window = sg.Window('Transport Optimizer', layout, element_justification='c', resizable=True)

# Event loop
while True:
    event, values = window.read()
    print(f"{event=}    {values=}")

    # If user closes window, end the program
    if event == sg.WIN_CLOSED:
        window.close()
        break

    if event == "-LAND DISTANCE-":

        # If the user has deleted their input until the text box is empty, empty the dropdown menu and continue
        if not values["-LAND DISTANCE-"]:
            window["-LAND VEHICLE-"].update(values=[])
            continue

        # If a given distance is not a positive float, clear that distance and inform the user with a popup and do nothing
        if not distance_validation(values["-LAND DISTANCE-"]):
            window["-LAND DISTANCE-"]('')
            sg.popup("Distance should be a positive number.", no_titlebar=True, grab_anywhere=True)
            continue

        # Round distances up to nearest integer
        distance_land = ceil(float(values["-LAND DISTANCE-"]))
        # Create filtered list
        vehicles.process(distance_land, 1, imperial)

        # If no vehicles are available at all for a given distance, clear that distance and inform the user with a popup
        if len(vehicles.filtered_land) == 0:
            window["-LAND DISTANCE-"]('')
            sg.popup("No vehicles are available for the given distance.", no_titlebar=True, grab_anywhere=True)
            continue

        # Update combo elements
        window["-LAND VEHICLE-"](values=[str(vehicle) for vehicle in vehicles.filtered_land])

        # Clear existing vehicle choice
        values["-LAND VEHICLE-"] = ''

    if event == "-WATER DISTANCE-":

        if not values["-WATER DISTANCE-"]:
            window["-WATER VEHICLE-"].update(values=[])
            continue

        if not distance_validation(values["-WATER DISTANCE-"]):
            window["-WATER DISTANCE-"]('')
            sg.popup("Distance should be a positive number.", no_titlebar=True, grab_anywhere=True)
            continue

        distance_water = ceil(float(values["-WATER DISTANCE-"]))
        vehicles.process(distance_water, 2, imperial)

        if len(vehicles.filtered_water) == 0:
            window["-WATER DISTANCE-"]('')
            sg.popup("No vehicles are available for the given distance.", no_titlebar=True, grab_anywhere=True)
            continue

        window["-WATER VEHICLE-"](values=[str(vehicle) for vehicle in vehicles.filtered_water])

        values["-WATER VEHICLE-"] = ''

    if event == "-LAND VEHICLE-":

        # If distance has not been set, clear and inform the user with a popup
        if not values["-LAND DISTANCE-"]:
            values["-LAND DISTANCE-"] = ''
            sg.popup("Please set a distance first.", no_titlebar=True, grab_anywhere=True)
            continue

    if event == "-WATER VEHICLE-":

        if not values["-WATER DISTANCE-"]:
            values["-WATER DISTANCE-"] = ''
            sg.popup("Please set a distance first.", no_titlebar=True, grab_anywhere=True)
            continue

    if event == "Update":

        # If neither distance is set, inform the user with a popup and do nothing
        if not values["-LAND DISTANCE-"] and not values["-WATER DISTANCE-"]:
            sg.popup("Please set the distance first.", no_titlebar=True, grab_anywhere=True)
            continue

        # If one distance is not set, clear its corresponding vehicle
        if not values["-LAND DISTANCE-"]:
            values["-LAND VEHICLE-"] = ''
        if not values["-WATER DISTANCE-"]:
            values["-WATER VEHICLE-"] = ''

        # If a distance has been set but its corresponding vehicle hasn't, inform the user with a popup and do nothing
        if values["-LAND DISTANCE-"] and not values["-LAND VEHICLE-"]:
            sg.popup("You cannot set a distance without a vehicle.", no_titlebar=True, grab_anywhere=True)
            continue
        if values["-WATER DISTANCE-"] and not values["-WATER VEHICLE-"]:
            sg.popup("You cannot set a distance without a vehicle.", no_titlebar=True, grab_anywhere=True)
            continue

        # Handle situation where user types into dropdown instead of selecting a predefined option
        if values["-LAND VEHICLE-"] not in vehicles.filtered_land and values["-LAND VEHICLE-"]:
            values["-LAND VEHICLE-"] = ''
            sg.popup("Please select a vehicle from the dropdown menu.", no_titlebar=True, grab_anywhere=True)
            continue
        if values["-WATER VEHICLE-"] not in vehicles.filtered_water and values["-WATER VEHICLE-"]:
            values["-WATER VEHICLE-"] = ''
            sg.popup("Please select a vehicle from the dropdown menu.", no_titlebar=True, grab_anywhere=True)
            continue

        # Plot
        fig = vehicles.make_plots(values["-LAND VEHICLE-"], values["-WATER VEHICLE-"], values["-METRIC-"], imperial)
        draw(window["-FIGURE-"].TKCanvas, fig, window["-CONTROLS-"].TKCanvas)

        # Fill in table
        # First row needs to be filled in with data from values dict
        attributes = ("total_emissions", "total_cost", "total_energy_usage", "total_time")
        keys = ("Lowest Emissions", "Cheapest", "Most Efficient", "Fastest")
        land, water = values["-LAND VEHICLE-"], values["-WATER VEHICLE-"]
        table[0][1], table[0][2] = land, water
        for i in range(3, 7):
            # Tuple referring to attributes
            table[0][i] = round(eval(f"vehicles[land].{attributes[i-3]}[-1] + vehicles[water].{attributes[i-3]}[-1]"), 2)
        # Next 4 rows are filled in with data from vehicles.optimized_land/water
        vehicle = Vehicle({"Name": '', "Medium": 3, "Bounds": [0, 0], "Lifespan": 0, "Emissions": 0, "MEmissions": 0, "PMPGe": 0, "Speed": 0, "Cost": 0})
        vehicle.total_emissions, vehicle.total_time, vehicle.total_cost, vehicle.total_energy_usage = [0], [0], [0], [0]
        for i in range(4):
            row = i + 1
            land = vehicles.optimized_land[keys[i]] if hasattr(vehicles, 'optimized_land') else vehicle
            water = vehicles.optimized_water[keys[i]] if hasattr(vehicles, 'optimized_water') else vehicle
            table[row][1], table[row][2] = str(land), str(water)
            for j in range(3, 7):
                table[row][j] = round(eval(f"land.{attributes[j-3]}[-1] + water.{attributes[j-3]}[-1]"), 2)

        # Update table element
        window["-TABLE-"](values=table)

    if event == "-TABLE-":
        # TODO: table event charts row
        # continue if row clicked on is the selected row
        # Otherwise, load vehicle with selected metric
        pass

    if event == "Documentation":
        webbrowser.open("https://bitbucket.org/rd08/transport-optimizer/src/master/")

    if event == "Adding Vehicles":
        webbrowser.open("https://bitbucket.org/rd08/transport-optimizer/src/master/src/data/info.txt")

    if event == "Report a Bug":
        webbrowser.open("https://bitbucket.org/rd08/transport-optimizer/issues?status=new&status=open")

    if event == "_ Metric":
        imperial = False
        units = {"Distance": "km", "Currency": "CAD"}
        window["-LAND DISTANCE-"].set_tooltip(f"Distance ({units['Distance']}) should be a positive number. ")
        window["-WATER DISTANCE-"].set_tooltip(f"Distance ({units['Distance']}) should be a positive number. ")
        window["-LAND DISTANCE UNIT-"](units["Distance"])
        window["-WATER DISTANCE UNIT-"](units["Distance"])
        window["-TABLE-"].set_tooltip(table_info_metric)
        window["-MENU-"]([["Units", ["✓ Metric", "_ Imperial"]], ["Help", ["Documentation", "Adding Vehicles", "Report a Bug"]]])
        window["-LAND DISTANCE-"]('')
        window["-WATER DISTANCE-"]('')
        window["-LAND VEHICLE-"].update(values=[])
        window["-WATER VEHICLE-"].update(values=[])

    if event == "_ Imperial":
        update_USD()
        imperial = True
        units = {"Distance": "mi", "Currency": "USD"}
        window["-LAND DISTANCE-"].set_tooltip(f"Distance ({units['Distance']}) should be a positive number. ")
        window["-WATER DISTANCE-"].set_tooltip(f"Distance ({units['Distance']}) should be a positive number. ")
        window["-LAND DISTANCE UNIT-"](units["Distance"])
        window["-WATER DISTANCE UNIT-"](units["Distance"])
        window["-TABLE-"].set_tooltip(table_info_imperial)
        window["-MENU-"]([["Units", ["_ Metric", "✓ Imperial"]], ["Help", ["Documentation", "Adding Vehicles", "Report a Bug"]]])
        window["-LAND DISTANCE-"]('')
        window["-WATER DISTANCE-"]('')
        window["-LAND VEHICLE-"].update(values=[])
        window["-WATER VEHICLE-"].update(values=[])
