# pyClocker

A Cli app that keeps track of time spent on hobbies. This app can track time for multiple hobbies over a period of time.
I wanted to measure how much time I actually spend on programming daily.

### Database Model:

The application's database model consists of a single entity called "worksessions" with the following attributes:
* ```id```: Primary key
* ```date```: Date when a work session started 
* ```activity```: Name of the activity being tracked
* ```start_time```: Timestamp when a work session started
* ```stop_time```: Timestamp when the current work session stopped

### Commands

pyClocker offers the following commands.

* ```start```: This creates a new record in a database with ```date``` as current date and ```start_time``` as current timestamp.
If there already exists an on going worksession(a record with ```date``` as current date and ```stop_time``` as null), the app notifies the user to end the current worksession first. Optionally, one can specify the name of the activity with the flag ```--activity <activity name>``` default activity is ```programming```.

* ```stop```: Ends the current work session by updating the ```stop_time``` to the current timestamp. This updates the ```stop_time``` of the record in a database that has ```date``` as current date, ```start_time``` as the timestamp with the latest value and ```stop_time``` as null, with the current timestamp.
If such a record does not exist in the database, the app notifies the user to start a new worksession first.

* ```today```: Displays the total hours spent on each activity for the current day in a tabular format.

* ```daily```:  Generates a graph showing the hours invested in various hobbies each day.
  ![daily activity report](daily_time_spent.png)

## To run

1. To install the CLI, after activating a virtual environment run ```pip install .```
 
2. run ```pyClocker init``` to set the sqlite database file location.

3. Optionally, generate fake data for visualization purposes by navigating to the ```fakedatagen``` directory and running ```python3 datagen.py```.

4. Move the generated SQLite database file (```worksessions.db```) to the location set in step 2.

5. Run ```pyClocker daily``` to visualize the time spent on various activities each day.


## TODO

- [x] Add the ability to track time for multiple activities.
- [x] Create a plot to visualize time spent in each activity each day over time.

## Credits

pyClocker relies on the following amazing projects 
* [Typer](https://github.com/tiangolo/typer)
* [Plotly](https://github.com/plotly)
* [Tabulate](https://github.com/astanin/python-tabulate)
