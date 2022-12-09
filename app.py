from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return self.id


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form["content"]
        newTask = Todo(content=content)
        try:
            if content != "":
                db.session.add(newTask)
                db.session.commit()
            return redirect("/")
        except Exception as e:
            return "There was an issue!"
    else:
        tasks = Todo.query.order_by(Todo.dateCreated).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    takskToDelete = Todo.query.get_or_404(id)
    try:
        db.session.delete(takskToDelete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return "There was an issue"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    tasktoUpdate = Todo.query.get_or_404(id)
    if request.method == "POST":
        tasktoUpdate.content = request.form["content"]
        db.session.commit()
        return redirect("/")
    else:
        return render_template("update.html", task=tasktoUpdate)


if __name__ == "__main__":
    app.run(debug=True)
