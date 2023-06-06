# Loop-Kitchen-Intern-Assignment

The solution devised is a backend API built using the Python framework, Flask and SQLlite3 DB. Jinja template was used for creating dynamic HTML pages. SQL was used for the creation and insertion of static values into the table.

A modular, typings-based system was chosen and implemented using classes, modules and type hints. 

A trigger+polling architecture was developed with the help of threads. Multithreading was implemented for micro tasks, independent of other parallel tasks. Synchronization with locks was deployed for performing database operations and writes to global variables to avoid race conditions. The application allows multiple parallel client requests for report generations as well.

To account for the lack of continuos, consistent information, a ratio-based interpolation strategy was implemented to compute results from the data available in the DB. 

The cumulative report is converted into a dataframe and sent as a csv file to the client browser for download.

