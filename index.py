import time
import json
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    subjects = [
        {
            'name': 'Introduction to Computer Science Theory',
            'shortname': 'CS Theory',
            'link': '#',
            'color': 'blue',
            'icon': 'CS1.svg'
        },
        {
            'name': 'The Mechanics of Programming',
            'shortname': 'MoPs',
            'link': '#',
            'color': 'blue',
            'icon': 'CS2.svg'
        },
        {
            'name': 'Modern Philosophy',
            'shortname': 'Philosophy',
            'link': '#',
            'color': 'green',
            'icon': 'Philosophy.svg'
        },
        {
            'name': 'Probability and Statistics I',
            'shortname': 'Prob & Stat',
            'link': '#',
            'color': 'green',
            'icon': 'Math.svg'
        },
        {
            'name': 'University Physics II',
            'shortname': 'UP II',
            'link': '#',
            'color': 'red',
            'icon': 'Physics.svg'
        },
        {
            'name': 'Functional Yoga',
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
