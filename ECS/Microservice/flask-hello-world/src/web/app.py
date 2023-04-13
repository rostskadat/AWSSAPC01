from flask import Flask, render_template
import os
import random
import time


app = Flask(__name__)

def busy_wait(dt):   
    current_time = time.time()
    while (time.time() < current_time + dt):
        # NA
        pass

@app.route('/')
def render_index():
    # Simulate an expansive request
    process_time = random.uniform(0, 5)
    busy_wait(process_time)
    return render_template("index.html", process_time=process_time)


@app.route('/health')
def render_home():
    return "OK"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = bool(os.environ.get("DEBUG", False))
    app.run(debug=debug, host='0.0.0.0', port=port)
