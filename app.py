import threading

from flask import Flask
from utils import fetch_events, average_pr_time_wrap, event_counts_plot, root


# create Flask app
app = Flask(__name__)

# Start the background thread that runs the fetch_events function
threading.Thread(target = fetch_events).start()

# Route handlers for average_pr_time
@app.route('/average_pr_time', methods=['GET'])
def average_pr_time_wrapper():
    return average_pr_time_wrap()


# Route handlers for event_counts_plot
@app.route('/event_counts_plot', methods=['GET'])
def event_counts_plot_wrapper():
    return event_counts_plot()


# Route handler for the root URL ("/")
@app.route('/', methods=['GET'])
def root_wrapper():
    return root()

if __name__ == '__main__':
    app.run(debug=True)
