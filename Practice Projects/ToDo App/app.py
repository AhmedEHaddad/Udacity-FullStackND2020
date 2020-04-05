from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://devuser:devpass@localhost:5432/todoDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    #return 'Welcome to TODO App!' 
    render_template('index.html', data=[{
        'description': 'Todo 1'
    },{
        'description': 'Todo 2'
    },{
        'description': 'Todo 3'
    
    }])