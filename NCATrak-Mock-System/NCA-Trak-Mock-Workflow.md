# NCA-Trak-Mock Workflow

## Installation

For this installation guide, all code will be using Linux commands. This guide is strictly for developers and not how the end user should be using the file. You may have to transfer the command names
to your own OS.

## Requirements

-   [Anaconda](https://docs.anaconda.com/)

## Helpful links

-   https://docs.anaconda.com/anaconda/install/
-   https://conda.io/projects/conda/en/latest/user-guide/getting-started.html
-   https://conda.io/projects/conda/en/latest/user-guide/cheatsheet.html

## Important commands

```console
conda create --name ENVNAME [package] [package] [package] # for example conda create --name vnv python=3.10
conda activate ENVNAME

# Conda environment has to be active
conda install [package]
conda list
conda export --from-history > environment.yml # cross-platform compatible
conda env create -n ENVNAME --file ENV.yml    # Create from an ENV.yml file (environment in our case)
```

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


### Formatting

I recommend using some sort of formatter to ensure your code stays pretty. In Visual Studio Code, I recommend [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter).
