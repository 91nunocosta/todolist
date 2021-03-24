# Done

Create an API for managing a TODO list with the following specification:

Register

- [x] The user should be able to register with a username and password

    - [x] store password hash instead of plaintext

- [x] Usernames must be unique across all users

Login

- [x] The user should be able to log in with the credentials they provided in the register endpoint

- [x] Should return an access token that can be used for the other endpoints
   
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

- [x] add API documentation

- [ ] add assumptions to README

- [ ] add discussion of stack and design decisions to the README

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
$ curl "http://0.0.0.0:5000/api-docs"
```
By the way, this request returns you the Open API spec mentioned in the next section.

You can find some examples of requests in [examples.sh](examples.sh). Running the script should also work. The docker-compose configuration sets up the database with the needed data. The configuration also contains a JWT secret. The JWT token used in the script was generated for that secret and the username created in the beginning. Note that docker-compose is not intended for production. A different secret (not stored in git) would be used in production.

If you prefer to use [Postman](https://www.postman.com/), you can import [postman_collection](postman_collection) and try the requests there.

Once you are done, stop the docker containers running:
```
$ docker-compose down
``` 

# API

You can find the full [Open API](https://swagger.io/specification/) specification in [open-api-spec.json](open-api-spec.json).

It can also be viewed in a nice format in [Swagger Hub](https://app.swaggerhub.com/apis-docs/nunocosta2/Todolist/0.1.0).

Here are some examples from [examples.sh](examples.sh).

## Create account

```bash
curl --location --request POST 'http://0.0.0.0:5000/accounts' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "91nunocosta@gmail.com",
    "password": "unsercurepassword"
}'
```

##  Login
```bash
curl --location --request POST 'http://0.0.0.0:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "91nunocosta@gmail.com",
    "password": "unsercurepassword"
}'
```

## Create task
```bash
curl --location --request POST 'http://0.0.0.0:5000/tasks' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE2MTY2MTY5NjN9.tMQoy_6ROA_sxWR1exWVeRZZZFR4qvMbO2Szos_XIMI' \
--data-raw '{
    "summary": "Check that task can be created.",
    "done": false,
    "position": 1
}'
```

## List tasks
```bash
curl --location --request GET 'http://0.0.0.0:5000/tasks' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE2MTY2MTY5NjN9.tMQoy_6ROA_sxWR1exWVeRZZZFR4qvMbO2Szos_XIMI'
```

## Update task
```bash
curl --location --request PATCH 'http://0.0.0.0:5000/tasks/605b9e7052a0e74acae75fac' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE2MTY2MTY5NjN9.tMQoy_6ROA_sxWR1exWVeRZZZFR4qvMbO2Szos_XIMI' \
--data-raw '{
    "done": true
}'
```

## Delete task
```bash
curl --location --request DELETE 'http://0.0.0.0:5000/tasks/605b9e7052a0e74acae75fac' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE2MTY2MTY5NjN9.tMQoy_6ROA_sxWR1exWVeRZZZFR4qvMbO2Szos_XIMI'
```

## Reorder tasks

To move a task simply change its position value. You can think of the resource tasks as a dynamic array (which is most likely what the front-end would use for holding a list of tasks). The same restrictions apply:

1. The position can’t be less than the initial position, which in this case is 1.

1. The position can’t be larger than the largest position.

Only the tasks of the authenticated user are considered. Using the above analogy, each user as an isolated an independent array of tasks. 

# How to run unit tests locally

To test the application locally you will need:
- python3
- pip
- [docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

[Poetry](https://python-poetry.org/docs/) is used to manage the python dependencies in an auto-contained [virtual environment](https://docs.python.org/3/tutorial/venv.html).
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

For stopping the MongoDB instance (and releasing all the docker resources needed for it), run:
```
$ docker-compose -f docker-file-dev.yaml down
```

# Next steps
1. Configure HTTPS.

1. Manage expiration of authorization tokens.

1. Add keyword `Bearer` to the authorization tokens.

1. Setup CI/CD.

1. Create Helm chart.

1. Ensure atomicity of task’s position changes to the DB.

1. Add JSON responses to invalid position errors.

1. Investigate if task’s position operations implementation is optimal.

1. Make test code simpler.
