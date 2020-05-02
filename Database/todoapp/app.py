from flask import Flask, render_template,request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy 
import sys 
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mango:mango@localhost:5432/todoapp' # database configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disable overhead  
db = SQLAlchemy(app)  # linking SQLAlchemy with the app

migrate = Migrate(app, db) # initized migration, update/downgrade database 

class Todo(db.Model): 
	__tablename__ = 'todos'  # table name
	id = db.Column(db.Integer, primary_key=True) # id attribute
	description = db.Column(db.String(), nullable=False) # description attribute 
	completed = db.Column(db.Boolean, nullable=False, default=False)

	def __repr__(self): # debugging statement
		return f'<Todo {self.id} {self.description}>'

# db.create_all() # sync table and model, ensure talbe is created from decleared model 

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


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
	try: 
		completed = request.get_json()['completed']
		todo = Todo.query.get(todo_id) # grab todo_id 
		todo.completed = completed
		db.session.commit() # push to db
	except:
		db.session.rollback() # if any errors, rollback the changes 
	finally:
		db.session.close() # close out the session regards what happened 
	return redirect(url_for('index')) # grab refreshed list items in index page 

@app.route('/')
def index():
	return render_template('index.html', data = Todo.query.order_by('id').all())	
	# Todo.query.all(): select * from Todo (in DB) 

if __name__ == '__main__':
	app.run(debug=True, port='5000')