from flask import Flask, render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mango:mango@localhost:5433/todoapp' # database configuration
db = SQLAlchemy(app)  # linking SQLAlchemy with the app

class Todo(db.Model): 
	__tablename__ = 'todos'  # table name
	id = db.Column(db.Integer, primary_key=True) # id attribute
	description = db.Column(db.String(), nullable=False) # description attribute 

	def __repr__(self): # debugging statement
		return f'<Todo {self.id} {self.description}>'

db.create_all() # sync table and model, ensure talbe is created from decleared model 

@app.route('/todos/create', methods=['POST'])
def create_todo():
	description = request.form.get('description', '') # '': default empty string if nothing comes in
	todo = Todo(description=description) # create a object 
	db.session.add(todo) # add todo to pending stage
	db.session.commit() # push it to the database 
	return redirect(url_for('index')) # return to index page when it's done 

@app.route('/')
def index():
	return render_template('index.html', data = Todo.query.all())	
	# Todo.query.all(): select * from Todo (in DB) 

if __name__ == '__main__':
	app.run(debug=True, port='5000')
