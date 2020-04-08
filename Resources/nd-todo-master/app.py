from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)

# Connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres@localhost:5432/nd-todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)


# Define db Model with db.Model
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


db.create_all()


@app.route('/')
def index():  # Controller piece (of MVC layers)
    """
    We order by id in order to control it rather than its default behavior.
    """
    return render_template('index.html', data=Todo.query.order_by('id').all())


@app.route('/todos/create', methods=['POST'])
def create_todo():
    # description = request.form.get('description', '')  # '' -> default empty string
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)
    # return redirect(url_for('index'))


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    """
    Listens to events on the specified route. The route is triggered whenever
    a todo item is changed.
    :param todo_id: coming from JavaScript
    :return: Go back to index.html, although the page does not refresh 🤔
    """
    try:
        completed = request.get_json()['completed']
        # print('completed', completed) # is printed to the server, not console!
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/success')
def success():
    return 'Success!'


if __name__ == '__main__':
    app.run(debug=True)


# Models manage data and business logic for us. What happens inside models and database,
# capturing logical relationships and properties across the web app objects
# Views handles display and representation logic. What the user sees (HTML, CSS, JS from the user's perspective)
# Controllers: routes commands to the models and views, containing control logic.
# Control how commands are sent to models and views, and how models and views wound up interacting with each other.
