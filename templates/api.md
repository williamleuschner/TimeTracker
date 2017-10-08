# TimeTracker API

In order to facilitate integrations with with whatever systems make time
tracking easiest for you, TimeTracker offers the following API endpoints:

* `GET /api/subjects` — Return a JSON object containing all information known
about the subjects that can be logged. 
```
[
    {
        "name": string,         // Full course name
        "shortname": string,    // Abbreviated course name
        "color": string,        // One of green, blue, red, or purple
        "icon": string          // Name of the icon file for the button
    }
]
```
* `POST /api/start-timer` — Start the work timer. Return a JSON object
indicating status:
```
{
    "status": boolean, // Did the request succeed?
    "message": string  // Displayable message about success
}
```
* `POST /api/stop-timer` — Stop the work timer. Return a JSON object indicating
status:
```
{
    "status": boolean, // Did the request succeed?
    "message": string  // Displayable message about success
}
```
* `POST /api/log-subject` — Log a specific amount of time spent working on a
subject. Takes two form-encoded arguments: `subject` and `minutes-worked`.
`subject` is the full name of the subject to log time for; `minutes-worked` is
how many minutes to log for that subject. Returns a JSON object indicating
status:
```
{
    "status": boolean, // Did the request succeed?
    "message": string  // Displayable message about success
}
```
