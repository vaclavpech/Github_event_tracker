GitHub Event Tracker by Vaclav Pech


This Python application, built with Flask, tracks GitHub events (WatchEvent, PullRequestEvent, and IssuesEvent) in real-time. 
It fetches data from the GitHub API every minute and stores it in-memory for processing and analysis.

Features
    - Calculates the average time interval between 'PullRequestEvent' events in the last ten minutes.
    - Provides a visual representation (a bar plot) of the event counts for the last ten minutes.
    - Supports analysis and visualizations for a given repository.


Endpoints
    - 'Root endpoint (/)': Displays a welcome message.
    - '/average_pr_time': Returns the average time between 'PullRequestEvent' events, event counts ("/average_pr_time?repo=<repository-name>" for a given repository), and a list of repository names.
    - '/event_counts_plot': Provides a visual representation of event counts ("/event_counts_plot?repo=<repository-name>" for a given repository).


Code Structure
The code of the application is structured as follows:
    - app.py: Contains the main application code.
    - utils.py: Includes utility functions.
    - requirements.txt: Lists the dependencies required by the application. 


Getting Started
To run the application locally, follow these steps:
    1. Ensure you have Poetry installed. If not, you can install it using the following command:
            pip install poetry
    2. Clone this repository and navigate to the project directory.
    3. Set up a virtual environment using Poetry:
            poetry shell
    4. Install the project's dependencies:
            poetry install
    5. Start the Flask server:
            python app.py
    6. The application will now be accessible at http://localhost:5000.


Example Requests and Responses
- '/average_pr_time'
    Request: GET /average_pr_time?repo=<repository-name>
    Response:
        {
        "repository": "<repository-name>",
        "average_time": "2 hours",
        "event_counts": {
            "PullRequestEvent": 15,
            "WatchEvent": 10,
            "IssuesEvent": 5
        }
    }
- '/event_counts_plot
    Request: GET /event_counts_plot?repo=<repository-name>
    Response:
        Events Counts Plot

