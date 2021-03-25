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

- [x] add discussion of stack and design decisions to the README

- [x] complete next steps on README

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
This request returns you the Open API spec mentioned in the next section.

You can find some examples of requests in [examples.sh](examples.sh). Running the script should also work. The docker-compose configuration sets up the database with the needed data. The configuration also contains a JWT secret. The JWT token used in the script was generated for that secret and the username created in the beginning. Note that docker-compose is not intended for production. A different secret (not stored in git) would be used in production.

If you prefer to use [Postman](https://www.postman.com/), you can import [postman_collection](postman_collection.json) and try the requests there.

Once you are done, stop the docker containers running:
```
$ docker-compose down
``` 

# API

You can find the full [Open API](https://swagger.io/specification/) specification in [open-api-spec.json](open-api-spec.json).

It can also be viewed in a nice format in [Swagger Hub](https://app.swaggerhub.com/apis-docs/nunocosta2/Todolist/0.1.0).

Here are some examples of requests from [examples.sh](examples.sh).

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

When the position of a task is updated (or some task is added or removed) the positions of the remaining tasks of the same user are also updated. The positions are always kept contiguous from _1_ to _n_ (as if in an array), where _n_ is the number of tasks of the authenticated user. The order of each task in relation with the other tasks is perserved. The only execption is for the task whose position changed.

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

# Discussion

Here is some explanation for my choices in this exercise.

## API design

I chose to follow [REST architectural style](https://en.wikipedia.org/wiki/Representational_state_transfer). REST is suitable for the CRUD (Create, Read, Update, Delete) interface described in the requirements, and it positively affects:

* _Performance_ in component interactions.

* _Scalability_ — allowing the support of large numbers of components and interactions among components.

* _Simplicity_ of a uniform interface.

* _Modifiability_ of components to meet changing needs (even while the application is running).

* _Visibility_ of communication between components by service agents.

* _Portability_ of components by moving program code with the data.

* _Reliability_ in the resistance to failure at the system level in the presence of failures within components, connectors, or data.

The operation of reordering tasks is the more challenging to model with the CRUD interface. But if we see the position of a task as part of its status, then reordering is also an update operation. This approach has some important benefits:

1. The uniform interface is preserved. It avoids adding an extra operation whose semantics would be ad-hoc.

1. Adding, removing and moving items with positions has a well-known semantics: the same as the arrays.

1. The front-end can add or remove tasks at any position with a single request. When a task is moved, the front-end only need to track how its position changed. The front-end doesn't need to care about any other task.

## Implementation

The only non-trivial aspect of the implementation is managing the task's positions. A (possibly non-optimal) option is to store a _position_ field in the tasks. In this approach adding, removing or moving a task implies, in the worst case, to shift the positions of all tasks. By other words, the time complexity of those operations is _O(n)_, for _n_ tasks.

But if we take into account that _n_ is not all tasks in DB, but only the tasks of a particular user, the scenario seems much better. It's reasonable to assume that there is a constant limit (say _c=10000_, but you can change it) of tasks that is manageable by a single human user. Creating more tasks than that wouldn't be an easy task for anyone (and certainly not very useful.) Under this assumption _n_ becomes _c_, and time complexity _O(1)_ (assuming that the DB can find each task of the user in _O(1)_ time).

For this reason, I chose to follow this simple approach of storing the _positions_ inside the tasks. But if the above assumption changed, or the constant factor in the time complexity needs to be minimal, it could make sense to look for a more optimal solution. 

## Stack

The stack I chose to use is.
1. python3 
1. [MongoDB](https://www.mongodb.com/)
1. [python eve](https://docs.python-eve.org/en/stable/)

Here are the reasons for the choice.

### python

It's the programming language with which I'm more proficient. It's not as performant as a compiled language. But in a REST back-end mainly concerned with data persistence, it's reasonable to assume that the such difference is not important. The agility of development would be more important. As a high-level language, with powerful abstractions, python makes agility easy to achieve.

## MongoDB

Modeling a RESTful resource as a collection of documents is usually easier than modeling it with a relation (aka table). In the documents case, the mapping is, most of the time, one-to-one. An item of the API with certain fields can be stored as a document with exactly the same fields (including any nesting). 

Consider the following requests.
```
POST /tasks
{
    "summary": "A task.",
    "done": true,
    "type": "simple",
}
```

```

POST /tasks
{
    "summary": "A task.",
    "done": true,
    "type": "custom",
    "custom_fields": {
        "status": "Approved"
    }
}
```

In a MonoDB both items can be created in a collection _tasks_ with exactly the same structure they have in the requests. In this way, there is no need to spend extra time thinking about the DB schema: it is equal to the API schema. There may be cases where the mapping can't be one-to-one. But many times it can. That is the case in the API developed here.

It's possible to argue that the same could be achieved in relational DB as well. The nested `custom_fields` document could be stored as json field. The difference it that Mongo can query for any field of a nested document (e.g. `status`) as efficiently as for any other non-nested field (e.g `summary`). That is not usually the case in a relational DB.

Other more general advantages of MongoDB are:
1. *Flexible document schemas*.

1. *Code native data access* — data can be accessed using native programming language's data structures (e.g. python's dict, JavaScript's associative array, Java's Map). There is no need for ORM or other kind of wrappers.

1. *Change-friendly design* — changing the DB schema doesn't imply any downtime or complex migration process. It is possible to start writing the data in a new format at any time without disruptions. Older data can be migrated to the new format at any time. 

1. *Easy horizontal scale out* — MongoDB is designed to be a distributed database. It is possible to create clusters with real-time replication, and shard large or high-throughput collections across multiple clusters to sustain performance and scaler horizontally.

There are some situations where using MongoDB would not be appropriate. MongoDB violates [ACID](https://en.wikipedia.org/wiki/ACID) (atomicity, consistency, isolation, durability) (see [here](https://en.wikipedia.org/wiki/MongoDB#Transactions)). This means that failed operations (e.g. after power failures) may make the stored data invalid. There are contexts where this is not acceptable (e.g. banking). I assumed that it's not the case in this exercise.

## python eve

[Eve](https://docs.python-eve.org/en/stable/) is a [Flask](https://flask.palletsprojects.com/) extension for building RESTful APIs. It only needs a definition of the resources (see [todolist/settings.py](todolist/settings.py)). Then it provides the CRUD operations for those resources on top of a MongoDB. Most of the time, adding or changing an endpoint is a small change in the definition. In case that such is not possible we can still rely on Flask (see, for example, [todolist/login.py](todolist/login.py)) flexibility. This is why I chose eve. 

With eve we also benefit from the REST constraints without extra work. In particular, some _uniform interface_ constraints that would be laborious to implement:
1. Resource identification in requests
1. Self-descriptive messages
1. Hypermedia as the engine of application state (HATEOAS)

 
# Next steps

There are some steps that I know that I would follow if this was a long term project. But given that it's a one-week project, I will only list them here. This list is not sorted in any particular order. The order would depend on the priorities of the projects.

* *Setup HTTPS*. Without HTTPS, a man-in-the-middle attack would easily compromise a user account. The user's tasks information would be compromised. Also, the user account would be entirely compromised. By eavesdropping the authorization token, the attacker would get indefinitely (because the token don't expire — see the next point) access to the user account. That can be prevented if all the HTTP requests are encrypted.

* *Manage the expiration of authorization tokens.* The first thing to do would be to add the _exp_ field to the JWT token. That would allow the receivers of the token to reject it when expired. The next step would be to design some mechanism to revoke tokens, which is less trivial. Sending to the auth service a request for revoking a token would not be enough. The previously emitted tokens would still be accepted. 

* *Move authorization to a separate service.* In real-life context, the authorization would likely be used by many services. It would make sense having it has a distinct service. The implementation I did is simple to understand and flexible (e.g. it's easy to change the accounts' schema). But I would also consider some open source authentication server. That would bring more confidence on the system and possibily support more complex authorization protocols (e.g. OpenID Connect). For curiosity I explored some options and found [ORY Hydra](https://www.ory.sh/hydra/), for OpenID Connect, and [https://www.ory.sh/kratos/](https://www.ory.sh/kratos/), for simpler protocols.

* *Ensure the consistency of task's positions in the DB*. The positions of the tasks are updated in 2 steps: 1) shift the positions that need to be shifted; 2) update the position of the task whose change was requested. There is a small chance that one of the operations fail, bringing the DB to an inconsistent status. I would investigate how to make these sequence of operations atomic.

* *Add JSON responses to invalid position errors.* The positions are managed through a hook. That isn't done by eve directly, so we don't have the nice eve's error response format. I could still implement that on my hooks. 


* *Ensure optimal management of the positions*. As mentioned above, it's possible that the chosen solution for managing the positions of the tasks is not has efficient as it can. I would spend some time looking for better solutions, until I find some improvement, or I'm convinced that it's not possible to do any better.

* *Setup CI/CD.* An operational project is not only development. It's important to make sure that moving code to production is a smooth (and frequent) process. That is achieved through good CI/CD pipelines. Some tools and techniques with which I had successful experiences are:
    * [_Trunk based development_](https://trunkbaseddevelopment.com/) — there is a single long-lived git branch. Any other branch should be dedicated to specific features, and should be merged as soon as possible. This approach minimizes technical debt. The less time alternative branches are open, the less the changes that lead to integration problems to solve later.
    * [_Jenkins_](https://www.jenkins.io/) — it's not the most user-friendly (developer-friendly ?) CI/CD tool. But it's open source and allows to materialize any imaginable CI/CD pipeline.
    * [_Kubernetes_](https://kubernetes.io/) — it's a very flexible way (e.g. avoids vendor lock-in with respect to cloud providers) to make sure that things that work in my machine also work in production. I had some good experiences with it. So, I could create the Kubernetes files in the repo and setup the CI/CD to apply them to the hosting environments. Another options, which I want to explore some day is [_Helm_](https://helm.sh/). It makes the management of complex Kubernetes configurations easier.

There would be 2 CI/CD pipelines. One for the feature branches and another for the master branch. The master branch would be protected. The feature branches could only be merged through a Pull Request passing the CI/CD. 

The Pull Requests CI/CD pipeline would have the following steps:

1. Run the static analysis code quality checks.

1. Build the python library with the codebase (the API implementation).

1. Run the unit tests on the library.

1. Build a docker image with the library.

1. Run some smoke tests to verify that the docker image works as expected.

1. Push the image to some docker registry.

1. Apply the Kubernetes files (or Helm charts) in some testing Kubernetes cluster (or namespace).

1. Run some smoke tests to verify that the deployment works as expected.

1. Send the success status to the Pull Request.

The CI/CD pipeline for the master branch would be only applying the Kubernetes files to production. The docker images were already built in the Pull Request. The deployment was already tested in the PR as well.

There are always things to improve. For sure, in a long term project I would find many others. But these are the ones I can think of now.
