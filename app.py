from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy(model_class=Base)

def create_tables():
    with app.app_context():
        db.create_all()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    '''
    show all
    todos
    '''
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    # add a new item
    todo_title = request.form.get("title")
    new_todo = Todo(title=todo_title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # update a todo item
    update_todo = Todo.query.filter_by(id=todo_id).first()
    update_todo.complete = not update_todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # update a todo item
    delete_todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect(url_for("index"))

# @app.route('/about')
# def about():
#     return "About page"

if __name__ == "__main__":
    db.init_app(app)
    create_tables()

    # with app.app_context():
    #     dummy_todo = Todo(title="Sample Todo", complete=False)  # Set the due date
    #     db.session.add(dummy_todo)
    #     db.session.commit()

    app.run(debug=True)
