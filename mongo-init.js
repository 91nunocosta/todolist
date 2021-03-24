
db = new Mongo().getDB("eve");
db.tasks.insert(
    {
        "_id": ObjectId("605b9e7052a0e74acae75fac"),
        "summary": "Existing task",
        "done": false,
        "position": 1,
        "_owner": "91nunocosta@gmail.com",
    });