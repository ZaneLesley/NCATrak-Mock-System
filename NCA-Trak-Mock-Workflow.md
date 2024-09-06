# NCA-Trak-Mock Workflow

## Installation

For this installation guide, all code will be using Linux commands. This guide is strictly for developers and not how the end user should be using the file.

## Requirements

-   [Python 3.10](https://www.python.org/downloads/) or higher (tested with Python 3.10, may work with lower versions)

## Helpful links

- https://docs.python.org/3/library/venv.html
- https://pip.pypa.io/en/latest/user_guide/#requirements-files

### Get the repository

First get the repository with

```
git clone https://github.com/ZaneLesley/NCATrak-Mock-System
```

### Configure the .venv

First, install the venv package.

```
sudo apt install python3.10-venv
```

Next, go into the project directory and create the venv

```
python3 -m venv --prompt NCA-Trak-env .venv
```

Next, ensure proper venv creation by typing

```
. .venv/bin/activate
```

**Note: I like to alias this, you can do so by adding an alias to the .bashrc file**

```
vim ~/.bashrc
# go into insert mode with 'i'
alias vnv='. .venv/bin/activate'
# ESC => ; => x => ENTER
```

### Getting Requirements

Next, we need to get all the requirements, do this by doing the following

```
# If you aren't in the venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
```

After this, you should be set up to be able to start developing in the NCA-Trak-Mock software. Please refer to the next section on the workflow

# Workflow

## Kanban Board (OU Capstone Students)

### Creating a ticket

When creating tickets, please try to keep the title to 50 characters or less. Be descriptive in the description section. Ensure you're ticket is understandable by others and in enough detail that they can understand what you want by just reading and not needing to ask you afterward. Each task you complete in the codebase **SHOULD** have a ticket that goes with it. When you complete the task, mark it as complete.

## Github

### Commit Messages

Commit message titles should be closely related to the ticket you are doing. Again, 50 characters or less for these commits are generally good for the title. The body should be a paragraph or two and what you actually did and what it fixes. It shouldn't need to explain the actual code detail of how you fixed it.

### Branches

**_DO NOT PUSH TO MAIN._**

Ensure you are working on your own branch **PER FEATURE** we should have a lot more than 5 branches, each feature should have its own branch. Here is a useful [guide](https://www.w3schools.com/git/git_branch.asp?remote=github) if you don't completely understand branching in git.

## Code

### Requirements.txt

Make sure you are writing the requirements to run your packages into the txt file

```
python -m pip freeze > requirements.txt
cat requirements.txt # recommend doing this to ensure that it looks correct. (ensures you didn't do it outside of the venv.)
```

**Note: Make sure you are in the venv when you do this.**

### Formatting

I recommend using some sort of formatter to ensure your code stays pretty. In Visual Studio Code, I recommend [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter).

### Installing with venv

Ensure you are inside the venv and run this on packages you want to install:
```
pip install <package>
```

