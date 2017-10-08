import datetime
import json
import csv
import os
from flask import Flask, render_template, url_for, redirect, request, flash
from flask import Response

app = Flask(__name__)
app.config.update(dict(Tracker=None))


class TimeTrackerMessage(object):
    def __init__(self, success, message):
        self.success = success
        self.message = message

    def as_json(self):
        resp = {'success':self.success, 'message': self.message}
        return json.dumps(resp)


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
        resp = None
        if self.start_time is None:
            self.start_time = datetime.datetime.now()
            # Write the time to a temp file as a backup
            with open("/tmp/timetracker.tmp", "w") as tmpfile:
                tmpfile.write(self.start_time.isoformat())
            resp = TimeTrackerMessage(True, "Timer started")
        else:
            resp = TimeTrackerMessage(False, "You've already started the timer")
        return resp

    def stop_timer(self):
        resp = None
        if self.start_time is not None:
            times = [
                self.start_time.isoformat(),
                datetime.datetime.now().isoformat()
            ]
            with open(self.timer_file, "a") as tfile:
                csvwriter = csv.writer(tfile)
                csvwriter.writerow(times)
            self.start_time = None
            resp = TimeTrackerMessage(True, "Timer stopped")
        else:
            if os.path.exists("/tmp/timetracker.tmp"):
                times = [datetime.datetime.now().isoformat()]
                with open("/tmp/timetracker.tmp", "r") as tmpfile:
                    times.append(datetime.datetime.strptime(
                        tmpfile.read(),
                        "%Y-%m-%dT%H:%M:%S.%f"
                    ))
                    times.reverse()
                with open(self.timer_file, "a") as tfile:
                    csvwriter = csv.writer(tfile)
                    csvwriter.writerow(times)
                self.start_time = None
                os.remove("/tmp/timetracker.tmp")
                resp = TimeTrackerMessage(True, "Timer stopped")
            else:
                resp = TimeTrackerMessage(False, "You haven't started the timer yet.")
        return resp

    def log_subject(self, subject, minutes_worked):
        resp = None
        if self.start_time is None:
            resp = TimeTrackerMessage(False, "You haven't started the timer yet.")
        else:
            log_entry = [
                minutes_worked,
                datetime.datetime.now().isoformat(),
                subject
            ]
            with open(self.logger_file, "a") as lfile:
                csvwriter = csv.writer(lfile)
                csvwriter.writerow(log_entry)
            resp = TimeTrackerMessage(
                True,
                "%s minutes of %s logged" % (minutes_worked, subject)
            )
        return resp


@app.route("/")
def index():
    subjects = app.config.Tracker.subjects
    return render_template(
        "index.html",
        subjects=subjects
    )


@app.route("/start-timer", methods=["POST"])
def start_timer():
    resp = app.config.Tracker.start_timer()
    flash(resp.message)
    return redirect(url_for("index"))


@app.route("/stop-timer", methods=["POST"])
def stop_timer():
    resp = app.config.Tracker.stop_timer()
    flash(resp.message)
    return redirect(url_for("index"))


@app.route("/log-subject", methods=["POST"])
def log_subject():
    resp =  app.config.Tracker.log_subject(
        request.form["subject"],
        request.form["minutes-worked"]
    )
    flash(resp.message)
    return redirect(url_for("index"))


@app.route("/api")
def api_info():
    return render_template("api.html")


@app.route("/api/subjects")
def api_subjects():
    data = app.config.Tracker.subjects
    resp = Response(str(data), mimetype='application/json')
    return resp


@app.route("/api/start-timer", methods=["POST"])
def api_start_timer():
    data = app.config.Tracker.start_timer()
    resp = Response(data.as_json(), mimetype='application/json')
    return resp


@app.route("/api/stop-timer", methods=["POST"])
def api_stop_timer():
    data = app.config.Tracker.stop_timer()
    resp = Response(data.as_json(), mimetype='application/json')
    return resp


@app.route("/api/log-subject", methods=["POST"])
def api_log_subject():
    data =  app.config.Tracker.log_subject(
        request.form["subject"],
        request.form["minutes-worked"]
    )
    resp = Response(data.as_json(), mimetype='application/json')
    return resp


def main():
    rawcfg = open("timetracker.json", "r")
    cfg = json.load(rawcfg)
    app.config.Tracker = TimeTracker(
        cfg['subjects'],
        cfg['timer-file'],
        cfg['logger-file']
    )
    with open("secret.key", "r") as sk:
        app.secret_key = sk.read()

main()
