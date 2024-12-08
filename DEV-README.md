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





