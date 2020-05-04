from flask import Flask, render_template,request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy 
import sys 
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mango:mango@localhost:5432/todoapp' # database configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disable overhead  
db = SQLAlchemy(app)  # linking SQLAlchemy with the app

migrate = Migrate(app, db) # initized migration, update/downgrade database 

class Todo(db.Model):  # child model of TodoList class 
	__tablename__ = 'todos'  # table name
	id = db.Column(db.Integer, primary_key=True) # id attribute
	description = db.Column(db.String(), nullable=False) # description attribute 
	completed = db.Column(db.Boolean, nullable=False, default=False)
	list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)
	 	# db.Foreginkey('todolists.id'): ('parent_name.primary_key')
	 	# nullable=False: Foreignkey must be have a value

	def __repr__(self): # debugging statement
		return f'<Todo {self.id} {self.description}>'

# db.create_all() # sync table and model, ensure talbe is created from decleared model 

class TodoList(db.Model): # this is the parent model, and map Todo table as the child 
	__tablename__ = 'todolists'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(), nullable=False)
	todos = db.relationship('Todo', backref='list', lazy=True)  #linking child table, 
		# lazy=True: no initial load, load data only as needed 

@app.route('/todos/create', methods=['POST'])
def create_todo():
	error = False
	body = {}
	try: 
		description = request.get_json()['description'] # get (json) content from description field 
		# description = request.form.get('description', '') # '': default empty string if nothing comes in
		todo = Todo(description=description) # create a object 
		db.session.add(todo) # add todo to pending stage
		db.session.commit() # push it to the database 
		body['description'] = todo.description
	except: 
		error = True
		db.session.rollback()
		print(sys.exc_info())
	finally:
		db.session.close()
	if error:
		abort (400)
	else: 
		return jsonify(body)
	# return jsonify({ # return json data to the client 
	# 	'description': todo.description
		# })
	#redirect(url_for('index')) # return to index page when it's done 


@app.route('/todos/<todo_id>/set-completed', methods=['POST']) # listen to post request comes in
def set_completed_todo(todo_id):
	try: 
		completed = request.get_json()['completed']
		todo = Todo.query.get(todo_id) # grab todo item  
		todo.completed = completed
		db.session.commit() # push to db
	except:
		db.session.rollback() # if any errors, rollback the changes 
	finally:
		db.session.close() # close out the session regards what happened 
	return redirect(url_for('index')) # return to index page and grab refreshed list items on index page 


@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
	try:
		Todo.query.filter_by(id=todo_id).delete()
		db.session.commit()
	except: 
		db.session.rollback()
	finally:
		db.session.close()
	return jsonify({'success': True})

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
	return render_template('index.html', 
	lists=TodoList.query.all(), # all possible lists in todolists table
	active_list=TodoList.query.get(list_id), 
	todos = Todo.query.filter_by(list_id=list_id).order_by('id').all()
	)	
	# Todo.query.all(): select * from Todo (in DB) 

@app.route('/')
def index():
	return redirect(url_for('get_list_todos', list_id=1)) # route home page to list_id=1 

if __name__ == '__main__':
	app.run(debug=True, port='5000')