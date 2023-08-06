# pyClocker
I wanted to measure how much time I actually spend on programming daily.

Database Model:

It just consists of one entity called worksessions with the following attributes:
* ```id``` primary key
* ```date``` on what date a worksession started 
* ```start_time``` timestamp when a worksession started 
* ```stop_time``` timestamp when the current work session stopped 


This cli has the following commands.

* ```start```: This creates a new record in a database with ```date``` as current date and ```start_time``` as current timestamp.
If there already exists an on going worksession(a record with ```date``` as current date and ```stop_time``` as null), the app notifies the user to end the current worksession first.

* ```stop```: This updates the ```stop_time``` of the record in a database that has ```date``` as current date, ```start_time``` as the timestamp with the latest value and ```stop_time``` as null, with  current timestamp.
If such a record does not exist in the database, the app notifies the user to start a new worksession first.

* ```today```: This returns the total hours one has invested in programming today.
it does this by computing the sum of difference between ```stop_time``` and ```start_time``` having ```date``` as current date and ```stop_time``` as not null.

* ```daily```: This displays a graph showing hours invested in programming every day.

It is built using Typer.

## To run

* To install the cli, after activating a virtual environment run ```pip install .```
* run ```pyClocker <command>```

## TODO

- [x] Add the ability to track time for multiple activities.
