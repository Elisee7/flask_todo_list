from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db" # connection string for SQLite database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Disable track modifications to save resources
db = SQLAlchemy(app) # Initialize SQLAlchemy

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default= datetime.now(timezone.utc))
    #date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST']) 
def hello_world():
    #with app.app_context():
    #    db.create_all() # Create the database tables if they don't exist
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc) # Create a new Todo item
        db.session.add(todo) # Add the new todo item to the session
        db.session.commit() # Commit the session to the database
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo) # Render the index template with all todo items

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first() # Retrieve the todo item by sno
        todo.title = title  # Update the todo item with new title
        todo.desc = desc    # Update the todo item with new title and description
        db.session.add(todo) # Add the updated todo item to the session
        db.session.commit() # Commit the session to the database
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first() # Retrieve the todo item by sno
    return render_template('update.html', todo=todo)
    

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first() # Retrieve the todo item by sno
    db.session.delete(todo) # Delete the todo item from the session
    db.session.commit() # Commit the session to the database
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)