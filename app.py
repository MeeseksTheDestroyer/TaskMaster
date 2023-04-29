from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request, redirect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    
@app.context_processor
def utility_processor():

    def calculate_delta(to_do):
        date_created = datetime.strptime(str(to_do), "%Y-%m-%d").date()
        today = datetime.today().date()
        days_since_created = (date_created-today).days
        if(abs(days_since_created) == 1):
            return str(days_since_created)+" day"
        elif(abs(days_since_created) > 1):
            return str(days_since_created)+" days"
        else:
            return 'Today'
    return dict(calculate_delta=calculate_delta)

@app.route('/', methods=['POST', 'GET'])
def index():
    tasks_not_completed = Todo.query.filter_by(completed=False).order_by(Todo.date_created).all()
    return render_template('index.html', tasks_ =tasks_not_completed)

@app.route('/add-task', methods=['POST', 'GET'])
def task_add():
    if request.method == 'POST':
        task_content = request.form['content']
        date_str = request.form['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        task_title = request.form['title']
        new_task = Todo(content=task_content, date_created=date_obj, title=task_title)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        except:
            return 'There was an issue adding the task'
    else:
        return render_template('add-task.html')
    

@app.route('/delete/<int:id>')
def delete(id):
    task_completed = Todo.query.get_or_404(id)
    task_completed.completed=True
    try:
        
        db.session.commit()
    except:
        pass
    return redirect('/')

@app.route('/history')
def history():
    tasks_completed = Todo.query.filter_by(completed=True).order_by(Todo.date_created).all()
    return render_template('history.html', tasks_=tasks_completed)  
  
@app.route('/recover/<int:id>')
def recover(id):
    task_completed = Todo.query.get_or_404(id)
    task_completed.completed=False
    try:
        
        db.session.commit()
    except:
        pass
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True) 
#C:\Users\PC\AppData\Local\Programs\Python\Python311\python.exe