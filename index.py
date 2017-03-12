import time
import json
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    subjects = [
        {
            'shortname': 'CS Theory',
            'link': '#',
            'color': 'blue',
            'icon': 'CS1.svg'
        },
        {
            'shortname': 'MoPs',
            'link': '#',
            'color': 'blue',
            'icon': 'CS2.svg'
        },
        {
            'shortname': 'Philosophy',
            'link': '#',
            'color': 'green',
            'icon': 'Philosophy.svg'
        },
        {
            'shortname': 'Prob & Stat',
            'link': '#',
            'color': 'green',
            'icon': 'Math.svg'
        },
        {
            'shortname': 'UP II',
            'link': '#',
            'color': 'red',
            'icon': 'Physics.svg'
        },
        {
            'shortname': 'Yoga',
            'link': '#',
            'color': 'purple',
            'icon': 'Yoga.svg'
        }
    ]
    return render_template(
        "index.html",
        subjects=subjects
    )
