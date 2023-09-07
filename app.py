from flask import Flask, render_template, jsonify
import datetime
import threading
import random

app = Flask(__name__)

# Variables and calculations
current_time = datetime.datetime.now()
end_time = datetime.datetime(current_time.year, 9, 29, 20, 15)
if current_time > end_time:
    end_time = end_time.replace(year=current_time.year + 1)
    
total_duration = (end_time - current_time).total_seconds()

count_start = 9_970_000
count_end = 10_000_000
counter = count_start

weekday_speed = 2.0  # Times slower than the base interval
weekend_day_speed = 1.0  # Base speed
weekend_night_speed = 0.5  # Times faster than the base interval

def random_increment(hour):
    if 14 <= hour <= 20:  # Peak business hours
        return random.choices([1, 2, 3, 4, 5], [0.1, 0.2, 0.3, 0.2, 0.2])[0]
    elif 20 < hour < 24 or 0 <= hour < 2:  # Evening and night
        return random.choices([1, 2, 3, 4, 5], [0.3, 0.3, 0.2, 0.1, 0.1])[0]
    else:  # Regular business hours
        return random.choices([1, 2, 3, 4, 5], [0.2, 0.2, 0.2, 0.2, 0.2])[0]

def increment_counter():
    global counter
    current_time = datetime.datetime.now()
    weekday = current_time.weekday()

    # Check if it's a weekday
    if 0 <= weekday <= 4:
        if 12 <= current_time.hour < 24:
            interval = total_duration / (count_end - count_start) * weekday_speed
        else:
            return  # Business is closed

    # Check if it's a weekend
    elif 0 <= current_time.hour < 2 or 12 <= current_time.hour < 24:
        if 0 <= current_time.hour < 2:
            interval = total_duration / (count_end - count_start) * weekend_night_speed
        else:
            interval = total_duration / (count_end - count_start) * weekend_day_speed
    else:
        return  # Business is closed

    increment = random_increment(current_time.hour)
    counter += increment

    if counter > count_end:
        counter = count_end

    threading.Timer(interval, increment_counter).start()

increment_counter()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_count')
def get_count():
    global counter
    return jsonify({'count': counter})

if __name__ == '__main__':
    app.run(debug=True)
