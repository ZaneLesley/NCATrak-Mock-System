# NCATrak-Mock-System

## Introduction

This software aims to give professors at the [University of Oklahoma Health Science Center](https://www.ouhsc.edu/) a mock database where they can simulate tests on data input to improve the data validity and quality for child advocacy centers.

## Requirements

-   [Anaconda](https://docs.anaconda.com/)
-   [PostgreSQL](https://www.postgresql.org/)

## Installation

WIP (I'll do this towards the end, okay...)

### Anaconda Setup Instructions

This section will walk you thorough the installation and setup of Anaconda, which ensures that all of our code is cross-platform compatible.

#### Step 1: Install Anaconda

Follow Anaconda's [Installation Guide](https://docs.anaconda.com/anaconda/install/). Be sure to select the correct guide for your operating system.

#### Step 2: Setup a Virtual Environment

- On Linux or MacOS, open a terminal window. On Windows, open Anaconda Prompt.
- Navigate to the folder containing the current version of the NCA mock system using the command:

```shell
cd directory/of/mock/system/install
```

- Run the following command to create a virtual enviornment called NCA-Trak that installs all of the dependencies listed in the environment.yml file:

```shell
conda env create -n NCA-Trak --file environment.yml
```

- Activate the virtual environment by running the command:

```shell
conda activate NCA-Trak
```

- Verify the virtual environment is running by entering the command 

```shell
conda info
```

and confirming that the 'active environment' is "NCA-Trak". Then, verify that all of the dependencies have been installed by running the command

```shell
conda list
```

and confirming that all of the packages listed in the environment.yml file are listed. *Note: there will be more packages listed than are included in the environment.yml file. This is fine - just be sure that all of the desired packages are included in the list.*


Once all packages have been installed, your Anaconda VNV should now be up and running!

*Note: The virtual environment name "NCA-Trak" is currently a placeholder, and will be changed for future versions.*

### Database Setup Instructions

The purpose of this section is to walk you through setting up the initial database on your local machine so that you can run all of the programs we have developed so far. 

#### Step 1: Install PostgreSQL

Follow PostgreSQL's [Installation Guide](https://www.postgresqltutorial.com/postgresql-getting-started/). Depending on your operating system select the walkthrough guide provided by PostgreSQL to ensure correct installation.

*NOTE: For MacOS and/or Linux, you may skip the portion of the walkthrough titled “Load the sample database.” This section walks through creating a sample database that is not needed to run the code for this project.*

#### Step 2: Create Database

- First, open psql, the PostgreSQL terminal. To do this, open either Command Prompt (on Windows machines) or the terminal (on UNIX-like machines), and enter the command 

```shell
psql -U postgres
```

- When prompted, enter the password you chose during the installation in Step 1. The command prompt will change to look like this:

```shell
postgres=#
```

- Enter the command

```shell
CREATE DATABASE test_setup_database;
```

- You can now exit psql by entering the command:

```shell
exit
```

#### Step 3: Create database.ini file

*(NOTE: This section assumes that you have already downloaded all of the code and have an up-and-running Conda environment with all of the correct packages installed.)*

- Open the location where you have downloaded the current version of the NCA mock system in either an IDE or a terminal.

- In the Database folder, create a new file called “database.ini”

- Copy-paste the following into the database.ini file:

```shell
[postgresql]
host=localhost
database=test_setup_database
user=postgres
password=<password>
```

- Replace *<password>* with the same password you used to log into PostgreSQL. Save the file.

- Verify that you can connect to the database by running the connect.py script. This script should run successfully with no output and no errors if it has connected successfully.

#### Step 4: Create and populate the database tables

- Run the script “create_tables.py”. This will create the table currently being used for the personal profile page.

- Next, run the script “populate_database.py”. This pulls the mock data stored in the data.csv file and populates the newly-created data table.

And that’s it! You should now be able to run the script “database_lookup_search.py” to search and select personal profiles by name.
