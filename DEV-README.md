# Introduction

Hi, my name is Zane, and I was on the 2024F capstone team. I am now hopefully a full stack developer somewhere. This 
document was created with my recommendations for the project having worked on it for a semester. 
It also contains small information on how some of the systems and  scripts of the project actually work. If you have 
any questions feel free to 
[email me](mailto:zanelesley@outlook.com?subject=OU%20CS%20Capstone%20Question).

# Systems

## Database

### Description

The database needs to be created through [PostgreSQL](https://www.postgresql.org/). This is a widely used Relational 
Database currently in industry and works well for our needs. You can create it on each individual developers host PC, 
or run a remote instance of it and have everyone connect. I, however, recommended having each dev team member have 
their own instance of it. The setup is quite easy and is outlined in the [README](README.md).

### Code

The code relies on a couple of main files. Most importantly note that we used 
[psycopg2](https://www.psycopg.org/docs/) for our postgres drivers.
From the [wizard.py](app/wizard.py) you can track the call order and what 
files are being used. The most important of these are database.ini(created by wizard), 
[create_table.py](app/database/create_tables.py), and [populate_database.py](app/database/populate_database.py). 
Note: on `tables_to_fill` order is important. This depends on foreign keys and primary keys, so be careful and 
test when messing with these orderings. The [connect.py](app/database/connect.py) script is trivial, but used in 
almost every script above it. [Config.py](app/database/config.py) is used everytime 
[connect.py](app/database/connect.py) is called as well.

## Generator

### Description

This generates random data (depending on `seed` settings, see more information below) outputted as .csv files. The 
use is pretty simple and can all be contained within the [wizard.py](app/wizard.py) script.

### Code

The code is pretty straight forward and uses the python library [Faker](https://faker.readthedocs.io/en/master/),
this also has an even more powerful library in [JavaScript](https://fakerjs.dev/). Not every column from the 
database is currently filled out by the code in [data_generator.py](app/generator/data_generator.py), so be 
cautious of that. If you want to use a common seed among all developers you can all occurrences of the code in 
the generator. This could (and should) also be declared globally and replaced, but I didn't do that cause uhh :).

```python
#fake.seed_instance(0)
```

You will also see many lines like this:
```python
person["language_id"] = None
person["race_id"] = None
person["religion_id"] = None
```

Where you see `None` no value will be added to the database for this. I will add this to my recommendations below, 
but I advise you go back and fill in the rest of the tables. Just like before, the order you call the generator 
functions in is important. As the data has to be generated as relational to each other.

Note, some tables are not created as we never used them, specifically

```python
#util.write_to_csv(data=state_data, name="state_data")
#util.write_to_csv(data=employee_data, name="employee_data")
#util.write_to_csv(data=employee_account_data, name="employee_account_data")
```

## App and Interfaces

### Description

You can think of the [app.py](app/app.py) file as the main "manager" of the application. It calls upon all the 
interfaces to display them. The interfaces are done through [tkinter](https://docs.python.org/3/library/tkinter.html)
. This is an older library launched in 2007. This library is most likely what will hold the application back from 
scale, as it is not that efficient for what we want.

**This is why I recommend a switch to [React.js](https://react.dev/) for the interfaces**. 

I will talk more on this below in the recommendations section.

### Code

For this section, I won't talk a lot about the specific interface codes, you'll have to look at those yourselves, it 
is quite a lot and quite convoluted, but a lot of it is 'copy and paste' in terms of the ideology behind it. What I 
will say is currently the interfaces read from a file called `case_id.txt`. This really shouldn't be the case and 
should be replaced with a getter and setter from the [app.py](app/app.py) file.

An important line in the app.py file is this:

```python
frames_list = [
    database_lookup_search.lookup_interface,
    ...
    case_notes.case_notes_interface
]
```

If you are going to continue to use tkinter, this is where you can add new frames at to be rendered.

# Recommendations

The following are my recommendations that you do to have a successful software and semester. Note: you don't have to 
follow this list, but I think it might be wise to talk about each of these and see if you have a better idea.

### Switch from tkinter

The current tkinter app is not that good for scaling up, this is mostly due to the outdated nature of tkinter. It is 
also quite ugly and not as flexible as a lot of modern libraries are. For this, you have a couple options that I can 
think of off the top of my head

#### JavaScript

This is what I personally would do, it will come with its own set of challenges, but those challenges are outweighed 
when you think about the scalability of the application. I would use either [React.js](https://react.dev/) or 
[Angular](https://angular.dev/). The learning curve here might be the most challenging step, but there are a lot of 
good resources out there for both of these, one such resource is the [Odin Project](https://www.theodinproject.com/) 
which can teach you the basics (and more advanced) aspects of HTML, CSS, JavaScript, React.js, Node.js, and PostgreSQL.

#### PyQt

[PyQT](https://www.riverbankcomputing.com/software/pyqt/) is a way for python to use the original C++ 
[Qt application framework](https://www.qt.io/product/framework). This setup is not the easiest, and is also a STEEP 
learning curve, probably more so than JavaScript. The QT Framework is used in industry, and would look good on a 
résumé, but it's up to you if you want to choose this. You have access to QT using your OU student email, 
information on that can be found [here](https://www.qt.io/qt-educational-license).

#### Kivy

I don't know the most for [Kivy](https://kivy.org/doc/stable/gettingstarted/intro.html), but I do know it is used 
and works quite well, it is not as difficult a setup as PyQT as it was made for python, this would be my 
recommendation if you didn't want to switch to a JavaScript framework.

### Add more data to data-generation file

You can generate more of the data in these files and get them in the database. Some of the data to be added is 
trivial, some might take more complex functions to get them to work. It will make the database be more filled, and 
resulting the generated application will have more data. It is important to not let this slow down development 
though, keep working through interfaces even if you don't have data to test. *trust me*.

### Key logging information with python

I have heard that this may be a requirement for future dev teams, if so, I have a recommendation here as well, there 
is a library called [pynput](https://pynput.readthedocs.io/en/latest/index.html) which I think may be perfect for 
this use case. You can combine this with the [logging](https://docs.python.org/3/library/logging.html) module and 
have extremely detailed and logged information from what the client is currently doing. You can also easily send 
this data to another application. This can be achieved using a 
[socket,](https://www.geeksforgeeks.org/socket-programming-python/) or you can use the Flask/FastAPI application 
(discussed later). Socket is, however,  considerably easier for this use case *most likely*. 
Be mindful of security and privacy implications when using keyloggers, you should not be sending this data anywhere, 
and it should **NEVER** be able to run outside the script. This data should not really be broadcast in any way that 
isn't a direct pipe.

### Main application with threading

With all this stuff above that I've suggested, and all the different scripts this program will have to run, it might 
be a good idea to run different scripts on different threads, you can see examples and information 
[here](https://www.geeksforgeeks.org/multithreading-python-set-1/). This will help run things faster depending on 
how big the database is, but this isn't a necessity.

### Tips for Javascript/HTML front-end and python backend

Connecting from python to a front-end is something you have probably never done before. It is not that hard, but it 
is different. You have a lot of options, but I'd recommend [Flask](https://flask.palletsprojects.com/en/stable/) or 
[FastAPI](https://fastapi.tiangolo.com/). I have personally used Flask, and it is not too hard to do. There is a 
good amount of information on both of these (most likely more on Flask). Here is a 
[good resource](https://www.geeksforgeeks.org/flask-tutorial/) for Flask. FastAPI has 
[some information too](https://www.geeksforgeeks.org/fastapi-introduction/) but not nearly as much as you are going 
to get with Flask.

### Creation of Docker

With adding more and more libraries, and with python's terrible packaging system, it might be ideal to switch from 
anaconda to [docker](https://www.docker.com/). This is not the easiest thing in the world, and would take some 
research, but would probably save you and future teams more troubles. If you don't do this, you will have to think 
about how to keep everything contained for easy launching of the application in the future. It's also possible to
use a Dockerfile and docker-compose to spin up a unified environment that includes the database, backend, and 
possibly even a frontend. This might be a bit complicated though (maybe someone from OU IT/CS Department can help?).

### Keep cross-compatibility

Currently, the application can run on the big 3 OSes, Windows, Linux, MacOS. I recommend you attempt to keep it this 
way, one way to make sure it can run is to use 
[Linux on Windows with WSL](https://learn.microsoft.com/en-us/windows/wsl/install) to test latest branches on. Most 
of this just consist of using the `os` module and make sure you don't hardcode in data paths.

### Add getters / setters in interfaces

If you don't end up switching to JavaScript, I would go back and instead of reading from a file like `case_id.txt` 
I would make a getter and a setter to handle that information, it would clean the code up a lot.

# Conclusion

That is all the recommendations I can think of at this current point, again as stated above if you need to contact me
with any questions, I am avaliable by [email](mailto:zanelesley@outlook.com?subject=OU%20CS%20Capstone%20Question).

Thanks, have a good year!


# Further Answer to Dr. Kang Question

His question is as follows:

Also, as briefly discussed during your team's poster presentation on Friday, the project will continue in Spring 2025. I am wondering whether you'd be able to provide a short documentation on your thoughts about what we discussed as follows, and two questions are provided below:



(Some background)

The next phase is to define areas of interests (AOIs) on the interface screens. Simply stated, the screen will be divided into many different sized grids or boxes. Each AOI will contain (x,y) coordinates to keep track of the invisible box location for each interface screen. Keylogging events are recorded in real-time. In addition, mouse movements are tracked in real-time, and if a mouseover event happens on an important AOI, then such event is recorded in a text file such as:

| **Timestamp** | **MouseOverEvent**      | **MouseCoordinate (X, Y)** | **MouseButtonClick** | **TextInputAOI (Yes/No)** | **TextTypingActivity** |
|---------------|--------------------------|----------------------------|-----------------------|---------------------------|-------------------------|
| 00:00:00      | occurred on AOI1         | (234, 452)                 | No                    | Yes                       |                         |
| 00:00:01      | occurred on AOI1         | (238, 457)                 | Yes                   | Yes                       | Z                       |
| 00:00:02      | occurred on AOI1         | (238, 457)                 | Yes                   | Yes                       | a                       |
| 00:00:03      | occurred on AOI1         | (238, 457)                 | Yes                   | Yes                       | n                       |
| 00:00:04      | occurred on AOI1         | (238, 457)                 | Yes                   | Yes                       | e                       |
| 00:00:04      | occurred on AOI2         | (438, 657)                 | No                    | No                        |                         |
                              


Questions:

1. Re-structure the current "only" Python-based program into Javascript-based interface (possibly running the 
   Javascript files from python)?

2. Recommendations on whether we should use either python or javascript for keylogging and mouse features?

## Answer

Yes it's feasible, I will leave you with an answer that answers both. Below is the code I came up with in 2ish hours 
of research and googling which shows you how to use Flask to run a python app, which can connect to a javascript or 
HTML front end.

First, we have the Flask app which is in python which looks like this

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/keylog', methods=['POST'])
def keylog():
    key_data = request.json
    print(f"Key logged: {key_data['key']}\n")
    return jsonify({"message": "Key logged successfully"}), 200

@app.route('/mouse_events', methods=['POST'])
def handle_mouse_events():
    data = request.json
    if data and "events" in data:
        for event in data["events"]:
            print(f"Received mouse event: {event}")
        return jsonify({"message": "Mouse events logged successfully"}), 200
    return jsonify({"error": "Invalid data"}), 400

if __name__ == '__main__':
    app.run()
```
Here, we are basically making two routes that accept data, those are `/keylog` and `/mouse_events`. They provide an 
endpoint for us to send data too and record it. You can do whatever you want with the information here, it's just 
showing how to send some information from file x to file y. Here is the keylogger code that sends the information.

```python
from pynput import keyboard, mouse
import requests
import threading
import time

# Alternatives to this using javascript see:
# https://www.geeksforgeeks.org/javascript-coordinates-of-mouse/
# https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/key
# https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent/pageX

# Global Stuff
url = "http://127.0.0.1:5000/keylog"
url_mouse = "http://127.0.0.1:5000/mouse_events"
stop_threads = False
mouse_data = []

def on_press(key):
    key_str = str(key).strip("'")
    print(key_str, flush=True)
    response = requests.post(url, json={"key": key_str})
    if response.status_code == 200:
        pass
    else:
        print(f"Error sending key '{key_str}'")

def on_release(key):
    global stop_threads
    if key == keyboard.Key.esc:
        print("Esc pressed. Stopping listeners and threads...")
        stop_threads = True
        listener.stop()
        return False

def get_mouse_events():
    global mouse_data
    if mouse_data:
            # Send the logged mouse data
            response = requests.post(url_mouse, json={"events": mouse_data})
            if response.status_code == 200:
                print("Mouse data sent successfully:")
                mouse_data = []
            else:
                print("Failed to send mouse data:", response.status_code, response.text)

def on_move(x, y):
    global mouse_data
    mouse_data.append({"event": "move", "x": x, "y": y})

def on_click(x, y, button, pressed):
    global mouse_data
    action = "pressed" if pressed else "released"
    mouse_data.append({"event": "click", "x": x, "y": y, "button": str(button), "action": action})
    print(f"Mouse {action} at ({x}, {y}) with {button}")

def periodic_event_sender(interval=1):
    global stop_threads
    while not stop_threads:
        get_mouse_events()
        time.sleep(interval)

if __name__ == "__main__":
    sender_thread = threading.Thread(target=periodic_event_sender, daemon=True)
    sender_thread.start()

    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
    mouse_listener.start()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    mouse_listener.stop()
    mouse_listener.join()
    print("All listeners and threads stopped.")
```

In this you can also see I provided alternatives to if you just wanted to use javascript to keep track of all the 
information. It has much less code, and is much cleaner, but has the downside of only being able to track the 
webpage (for example, the only mouse and keyboard it can get has to come from when the client has the webpage opened 
and focused, whereas the keylogger from pynput can track global information.). Both work, both are viable, it 
really is up to you which you want to use. If you want to add this dynamically to a page, you can listen to it in 
the javascript or html file with something like this 

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mouse Tracker</title>
    <script defer src="script.js"></script>
</head>
<body>
    <div id="container">
        <h2>Mouse Events</h2>
        <ul id="mouse-events"></ul>
    </div>
</body>
</html>
```

with the backing JavaScript looking like (for mouse events only, works the same way with keyboard):

```javascript
document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("mouse-events");

    async function fetchMouseEvents() {
        try {
            const response = await fetch("http://127.0.0.1:5000/mouse_events");
            const events = await response.json();
            
            events.forEach(event => {
                const listItem = document.createElement("ul");
                listItem.textContent = JSON.stringify(event);
                container.appendChild(listItem);
            });
        } 
    }
```

Basically all that is happening above is we are listening to the Flask application from our forward facing front-end 
application. The pipeline is essentially:

python keylogger/mouse logger -> 'back-end' flask -> 'front-end HTML/Javascript'. 

Some of these files are buggy, I didn't test them too hard and is really just a proof of concept.

## TLDR

So again, you have two ways of doing it, 

Python, Javascript, HTML

or 

Javascript, HTML.

In order to link Python and Javascript together, you can use flask applications that POST/GET data and retrieve it 
from the Javascript/HTML using the javascript method above.

To get information that he wants to use for AIO, simply get the elements position and create a 'bounding box' around 
it and just create some logic to tell if the x,y coords match. See https://www.geeksforgeeks.org/how-to-find-the-position-of-html-elements-in-javascript/
and https://stackoverflow.com/questions/72120789/detecting-cursor-in-a-certain-range (can also probably ask 
[Dr. Weaver](https://www.ou.edu/coe/cs/people/faculty/chris-weaver) for 
help on this in terms of x, y coords, he is the computer graphics professor I had and knows the math behind this).