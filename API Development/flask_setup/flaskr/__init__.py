from flask import Flask, jsonify
from models import setup_db, Plant
from flask_cors import CORS

def create_app(test_config=None): 
	app = Flask(__name__)
	setup_db(app)
	CORS(app)
	#CORS(app, resources={r"*/api/*": {origins: '*'}}) # any origins can access the resources: {what resources: what origins from the client can access}

	@app.after_request
	def after_request(response):
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization') # allow headers: content-type, Authorization
		response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS') # allow methods: GET, POST, PATCH, DELETE, OPTIONS 
		return response

	@app.route('/')
	# @cross_origin # any end-point to allow cross-origin 
	def hello():
		return jsonify({'message': 'HELLO WORLD'})

	return app 