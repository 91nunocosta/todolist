Requirements
============

Create an API for managing a TODO list with the following specification:

Register

1) The user should be able to register with a username and password

#) Usernames must be unique across all users

Login

3) The user should be able to login with the credentials they provided in the register endpoint

#) Should return an access token than can be used for the other endpoints

TODO List

5) The user should only be able to access their own tasks

#) The user should be able to list all tasks in the TODO list

#) The user should be able to add a task to the TODO list

#) The user should be able to update the details of a task in their TODO list

#) The user should be able to remove a task from the TODO list

#) The user should be able to reorder the tasks in the TODO list

#) A task in the TODO list should be able to handle being moved more than 50 times

#) A task in the TODO list should be able to handle being moved to more than one task away from its current position


A - Return proper errors with corresponding HTTP codes

Note: You can think of this as an API endpoint that will be used to handle the drag and drop feature of a TODO list application

B - All endpoints should return JSON responses.
