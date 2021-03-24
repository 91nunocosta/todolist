# Done

Create an API for managing a TODO list with the following specification:

Register

- [x] The user should be able to register with a username and password

    - [x] store password hash instead of plaintext

- [x] Usernames must be unique across all users

Login

- [x] The user should be able to login with the credentials they provided in the register endpoint

- [x] Should return an access token than can be used for the other endpoints
   
    - [x] compare hashed password
   
    - [x] generate token

TODO List

- [x] The user should only be able to access their own tasks

    - [x] protect tasks endpoints

    - [x] check token

    - [x] filter tasks by authenticated user

- [x] The user should be able to list all tasks in the TODO list

- [x] The user should be able to add a task to the TODO list

- [x] The user should be able to update the details of a task in their TODO list

- [x] The user should be able to remove a task from the TODO list

- [x] The user should be able to reorder the tasks in the TODO list

- [x] A task in the TODO list should be able to handle being moved more than 50 times

- [x] A task in the TODO list should be able to handle being moved to more than one task away from its current position


- [x] Return proper errors with corresponding HTTP codes

Note: You can think of this as an API endpoint that will be used to handle the drag and drop feature of a TODO list application

- [x] All endpoints should return JSON responses.

# TODO

- [x] add docker compose for running locally

- [x] add instructions for running to the README

- [ ] add API documentation

- [ ] add assumptions to README

- [ ] add discussion of stack and design decisions to the REAME

- [ ] complete next steps to README

- [ ] add tox and code quality analysis

- [ ] improve code quality

- [ ] improve docker


# How to run locally

To run the application locally you will need:
- [docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

Clone this repository to some directory of your choice:

```bash
$ git clone git@github.com:91nunocosta/todolist.git
```

Go inside the project:

```bash
$ cd todolist
```

Run docker-compose to build and run the required docker containers:
```bash
$ docker-compose up
```

Do your requests:
```bash
$ curl "0.0.0.0:5000"
```

Once you are done, stop the docker containers running:
```
$ docker-compose down
``` 

# How to run unit tests locally

To test the application locally you will need:
- python3
- pip
- [docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

[Poetry](https://python-poetry.org/docs/) is used to manage the python dependencies in a auto-contained [virtual environment](https://docs.python.org/3/tutorial/venv.html).
To install it, run:
```
$ pip install poetry
```

Now you can easily install the python dependencies in the project:
```
$ poetry install
```

To be able to run the tests, an instance of MongoDB is needed. For that run:
```
$ docker-compose -f docker-file-dev.yaml up -d
```

Finally, you can run the tests:
```
$ poetry run pytest
```

For stoping the MongoDB instance (and releasing all the docker resources needed for it), run:
```
$ docker-compose -f docker-file-dev.yaml down
```

# Next steps
1. Setup CI/CD.

1. Create Helm chart.

1. Ensure atomicity of task's position changes to the DB.

1. Add JSON responses to invalid position errors.

1. Investigate optimaility of task's position operations.

1. Make test code simpler.
