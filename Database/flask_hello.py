from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mango:mango@localhost:5433/mangodb' # database configuration
										# dialect://username:password@host:port/db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence deprecation warnning in the terminal 
db = SQLAlchemy(app) # instance of the database

class Person(db.Model): 
	__tablename__ = 'persons' # table name
	id = db.Column(db.Integer, primary_key=True )  # db.Integer: data type; primary_key = primary_key 
	name = db.Column(db.String(), nullable=False) 

	def __repr__(self): # For debugging 
		return f'<Person ID: {self.id}, name:{self.name}>'

db.create_all() # detects models and creates tables for them (if they don't exist)

@app.route('/')
def index(): 
	person = Person.query.first() 
	return "Hello " + person.name

# Debug mode: enable dynamic updates (without needed a restart the service)
if __name__ == '__main__':
	app.run(debug=True, port='3000')