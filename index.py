import datetime
import json
import csv
import os
from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)
app.config.update(dict(Tracker=None))


class TimeTracker(object):
    def __init__(self, subjects, timer_file, logger_file):
        self.subjects = subjects
        self.timer_file = timer_file
        self.logger_file = logger_file
        self.start_time = None

    def __str__(self):
        return "TimeTracker: timer_file: %s, logger_file: %s, subjects: %s" % (
            self.timer_file,
            self.logger_file,
            ", ".join([s.name for s in self.subjects])
        )

    def start_timer(self):
        if self.start_time is None:
            self.start_time = datetime.datetime.now()
            # Write the time to a temp file as a backup
            with open("/tmp/timetracker.tmp", "w") as tmpfile:
                tmpfile.write(self.start_time.isoformat())
            return redirect(url_for("index"))
        else:
            return "You've already started the timer."

    def stop_timer(self):
        if self.start_time is not None:
            times = [
                self.start_time.isoformat(),
                datetime.datetime.now().isoformat()
            ]
            with open(self.timer_file, "a") as tfile:
                csvwriter = csv.writer(tfile)
                csvwriter.writerow(times)
            return redirect(url_for("index"))
        else:
            if os.path.exists("/tmp/timetracker.tmp"):
                pass
            else:
                return "You haven't started the timer yet."

    def log_subject(self, subject, minutes_worked):
        if self.start_time is None:
            return "You haven't started the timer yet."
        else:
            log_entry = [
                minutes_worked,
                datetime.datetime.now().isoformat(),
                subject
            ]
            with open(self.logger_file, "a") as lfile:
                csvwriter = csv.writer(lfile)
                csvwriter.writerow(log_entry)
            return redirect(url_for("index"))


@app.route("/")
def index():
    subjects = app.config.Tracker.subjects
    return render_template(
        "index.html",
        subjects=subjects
    )


@app.route("/start-timer", methods=["POST"])
def start_timer():
    return app.config.Tracker.start_timer()


@app.route("/stop-timer", methods=["POST"])
def stop_timer():
    return app.config.Tracker.stop_timer()


@app.route("/log-subject", methods=["POST"])
def log_subject():
    return "This will do something eventually"


def main():
    rawcfg = open("timetracker.json", "r")
    cfg = json.load(rawcfg)
    app.config.Tracker = TimeTracker(
        cfg['subjects'],
        cfg['timer-file'],
        cfg['logger-file']
    )

main()
