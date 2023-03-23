
# README #

0.1.0

### What is this repository for? ###

This repository hosts the transportation optimizer project by Richard, Ella and Ziyad. You input two constraints: distance and medium. The distance is the trip distance you will be travelling over the given medium, land or water. Say, 500 km over land and 35 km over water. The optimizer will then find the best pair of vehicles for the job, measured by emissions, efficiency, cost and speed. 

### What is this repository NOT for? ###

As mentioned below, the data that comes with this repository is **sample data**. There is no guarantee of accuracy, although credible sources were used when possible, estimates were made when needed. You as the user are supposed to provide your own data. 

### How do I get set up? ###

Navigate to the [Downloads](https://bitbucket.org/rd08/transport-optimizer/downloads/) page on this repo. Click on "Download repository". Save the zip file. Open the file with your file explorer and extract it, yielding the transport optimizer repository. Make sure that you have a recent release of Python 3 installed locally. Ideally, the Python executable should be added to your PATH variable so that you can easily access it from the terminal. If you are on Linux, open your system terminal. If you are on Windows, open PowerShell. Enter the optimizer folder and copy its path using the file explorer. Paste the following commands into your terminal, one by one:

    cd <path>
    pip3 install -r requirements.txt
    cd src
    python3 main.py

The GUI should now be open. You can enter in the distances over each medium. Doing so will automatically filter the vehicle dropdown menus to show capable vehicles for the given distance and medium. Adjust the Metric dropdown to choose which metric to plot. Click on the Update button to update the charts and table at the bottom. Note that the charts will now be plotted to the right. The toolbar can be used to navigate, adjust and save the charts. Hovering your cursor over the table will display the full names of the units being used at the moment. You can change the unit system in the menu bar under Units. 

### Configuration ###

Under src/data, you will find a series of .json files containing data for each vehicle. The files that come with this program are sample files. You can add your own vehicle by following the same format. The parameters are detailed more here. You can enter zeros for lifespan and emissions, PMPGe, speed and cost, as long as at least one of them is filled in the program will still be able to optimize for that metric. Start by making a copy of an existing sample file and modifying from there. 

### Who do I talk to? ###

Found a bug? Open an issue on [the issue tracker](https://bitbucket.org/rd08/transport-optimizer/issues?status=new&status=open). 

A full Linux installation tutorial and GUI overview is available in a video format [here](https://drive.google.com/file/d/14qLKgL7f0W6G4HQuj2iPiWlnqaUBRBjr/view?usp=sharing). 