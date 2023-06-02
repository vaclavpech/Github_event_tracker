import base64
import io
import matplotlib.pyplot as plt
import requests
import time

from datetime import datetime, timedelta
from flask import jsonify, render_template_string, request
from matplotlib.ticker import MaxNLocator


# Store different types of events in-memory
events = {
    'WatchEvent': [],
    'PullRequestEvent': [],
    'IssuesEvent': []
}

def calculate_event_counts(time_limit):
    """
    Calculates the number of events of each type that have occurred since the given time limit by checking 
    if its timestamp is after the time limit.
    """
    
    return {event_type: sum(1 for event in event_list if datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ") >= time_limit) for event_type, event_list in events.items()}


def fetch_events():
    """
    Makes a GET request to the GitHub API every minute to fetch the latest events. 
    If the request is successful (status code 200), it adds the event to the corresponding list in the 'events' dictionary,
    otherwise it prints an error message.
    """
    
    while True:
        try:
            response = requests.get('https://api.github.com/events')
            response.raise_for_status() 
            data = response.json()

            for event in data:
                if event['type'] in events:
                    events[event['type']].append({
                        'created_at': event['created_at'],
                        'repo': event['repo']['name'],
                    })

        except requests.exceptions.RequestException as e:
            print(f"Request to GitHub API failed: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        time.sleep(60)
        

def average_pr_time_wrap():
    """
    Calculates and returns the average time between pull requests and the number of events of each type that have occurred in the last 10 minutes.
    """

    # Calculate the timestamp of the offset time.
    offset = 10
    time_limit = datetime.utcnow() - timedelta(minutes = offset)

    # Get all PR events in the last 10 minutes
    pr_events = [event for event in events['PullRequestEvent'] if datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ") >= time_limit]

    if len(pr_events) < 2:
        return jsonify({'average_time_between_PRs_(seconds)': None, 'event_counts': calculate_event_counts(time_limit)})

    # Sort PR events by their creation time
    pr_events.sort(key=lambda x: x['created_at'])

    # Calculate time differences between consecutive PR events
    time_diffs = []
    for i in range(1, len(pr_events)):
        time1 = datetime.strptime(pr_events[i-1]['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        time2 = datetime.strptime(pr_events[i]['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        time_diffs.append((time2 - time1).total_seconds())

    # Calculate average time difference
    average_time = sum(time_diffs) / len(time_diffs)

    # Calculate event counts
    event_counts = calculate_event_counts(time_limit)

    return jsonify({'average_time_between_PRs_(seconds)': average_time, 'event_counts': event_counts})


def event_counts_plot():
    """
    Creates a new route in your Flask application that generates a bar plot of the counts of each event type for a given repository
    over the last 10 minutes. It then converts the plot to a PNG image and sends it as a response.
    """
    repository = request.args.get('repo', default=None, type=str)  # Get the repository name from the query parameters

    offset = 10  # Hardcoded offset value in minutes.
    time_limit = datetime.utcnow() - timedelta(minutes=offset)  # Calculate the timestamp of the offset time.

    # Prepare counts for each event type for the specified repository
    event_counts = calculate_event_counts(time_limit)
    if repository:
        event_counts = {event_type: count for event_type, count in event_counts.items() if event_type in events and events[event_type]['repo'] == repository}

    # Create a bar plot using Matplotlib
    fig, ax = plt.subplots()
    ax.bar(event_counts.keys(), event_counts.values())
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.title('GitHub Event Counts in Last 10 Minutes')
    plt.xlabel('Event Type')
    plt.ylabel('Count')
    plt.ylim(bottom=0)  # Ensure Y-axis starts at 0

    # Convert the plot to a PNG image
    png_image = io.BytesIO()
    plt.savefig(png_image, format='png')
    png_image.seek(0)

    # Convert the PNG image to a data URL
    png_image_b64_string = "data:image/png;base64,"
    png_image_b64_string += base64.b64encode(png_image.getvalue()).decode('utf8')

    # Clear the current figure for future requests
    plt.clf()

    # Render the image in an HTML page
    html = "<img src='{}'>".format(png_image_b64_string)
    return render_template_string(html)


def root():    
    return "Welcome to the GitHub event tracking app by Vaclav Pech!"
