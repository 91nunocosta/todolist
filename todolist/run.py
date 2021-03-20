from eve import Eve

from todolist.login import login

app = Eve()
app.add_url_rule("/login", view_func=login, methods=["POST"])

if __name__ == "__main__":
    app.run()