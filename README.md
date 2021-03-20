# Requirements

Create an API for managing a TODO list with the following specification:

Register

- [ ] The user should be able to register with a username and password

- [ ] Usernames must be unique across all users

Login

- [ ] The user should be able to login with the credentials they provided in the register endpoint

- [ ] Should return an access token than can be used for the other endpoints

TODO List [tests](./todolist/tests/test_todolist.py)

- [ ] The user should only be able to access their own tasks

- [ ] The user should be able to list all tasks in the TODO list

- [x] The user should be able to add a task to the TODO list

- [ ] The user should be able to update the details of a task in their TODO list

- [ ] The user should be able to remove a task from the TODO list

- [ ] The user should be able to reorder the tasks in the TODO list

- [ ] A task in the TODO list should be able to handle being moved more than - [ ]times

- [ ] A task in the TODO list should be able to handle being moved to more than one task away from its current position


i. Return proper errors with corresponding HTTP codes

Note: You can think of this as an API endpoint that will be used to handle the drag and drop feature of a TODO list application

ii. All endpoints should return JSON responses.

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

Finally, you can run the tests:
```
$ poetry run pytest
```
