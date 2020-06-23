from flask import Flask, request, abort
from functools import wraps

def get_token_auth_header(): 
	if 'Authorization' not in request.headers:
		abort(401)

	auth_header = request.headers['Authorization']
	header_parts = auth_header.split(' ')

	if len(header_parts) != 2: # abort(401) if len != 2 
		abort(401)
	elif header_parts[0].lower() != 'bearer': # if first word in header_parts != 'bearer'
		abort(401)

	return header_parts[1] # return second item in header_parts 

def requires_auth(f): 
	@wraps(f)
	def wrapper(*args, **kwargs): 
		jwt = get_token_auth_header()
		return f(jwt, *args, **kwargs)
	return wrapper

app = Flask(__name__)

@app.route('/headers') #@app.route('/myapp')
@requires_auth
def headers(jwt):	#def myapp(jwt)
	print(jwt)
	return "not implemented"

# export FLASK_APP=app.py
# flask run --reload