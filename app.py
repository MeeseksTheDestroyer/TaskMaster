from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request, redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    tasks_not_completed = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks_not_completed =tasks_not_completed)

@app.route('/add-task', methods=['POST', 'GET'])
def task_add():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return 'Task was added'
        except:
            return 'There was an issue adding the task'
    else:
        
        return render_template('add-task.html')
if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True) 
#C:\Users\PC\AppData\Local\Programs\Python\Python311\python.exe