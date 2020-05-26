import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8


def paginate_books(request, selection):
    page = request.args.get('page', 1, type=int) # looked at request object and args value, get the value of key 'page'; if key doesn't exist, set default to 1 and type is integer.  
    start = (page - 1) * BOOKS_PER_SHELF # starting index (of the page)
    end = start + BOOKS_PER_SHELF # ending index (of the page)

    books = [book.format() for book in selection] # get all the books and display book details in the format that defined in models.py (including id, title, author, rating)
    current_books = books[start:end] # current page 

    return current_books


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/books')
    def retrieve_books():
        selection = Book.query.order_by(Book.id).all()
        current_books = paginate_books(request, selection)

        if len(current_books) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'books': current_books, # current page
            'total_books': len(Book.query.all()) # total pages
        })

    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def update_book(book_id):

        body = request.get_json() # get the body from the request 

        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None: # if no book matches the id, abort(404)
                abort(404)

            if 'rating' in body: # update rating 
                book.rating = int(body.get('rating'))

            book.update() # update 

            return jsonify({
                'success': True,
                'id': book.id 
            })

        except: # any failure finding that book or failed to update it, send a (400) error 
            abort(400)

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none() # check if the book exists 

            if book is None: # return 404 if not exist 
                abort(404)

            book.delete() # delete the book 
            selection = Book.query.order_by(Book.id).all() 
            current_books = paginate_books(request, selection) #paginate the page based off current location

            return jsonify({
                'success': True,
                'deleted': book_id,
                'books': current_books,
                'total_books': len(Book.query.all())
            })

        except:
            abort(422)

    @app.route('/books', methods=['POST'])
    def create_book():
        body = request.get_json()

        new_title = body.get('title', None) # get title from the body, if nothing in title, set its value to None
        new_author = body.get('author', None) # get author from the body, if nothing in author, set its value to None
        new_rating = body.get('rating', None) # get rating from the body, if no rating, then set its value to None (initially)
        search = body.get('search', None)

        try:
            if search:
                selection = Book.query.order_by(Book.id).filter(Book.title.ilike('%{}%'.format(search)))
                current_books = paginate_books(request, selection)

                return jsonify({
                    'success': True,
                    'books': current_books,
                    'total_books': len(selection.all())
                    })

            else:
                book = Book(title=new_title, author=new_author, rating=new_rating)
                book.insert()

                selection = Book.query.order_by(Book.id).all()
                current_books = paginate_books(request, selection)

                return jsonify({
                    'success': True,
                    'created': book.id,
                    'books': current_books,
                    'total_books': len(Book.query.all())
                    })

            except: #unprocessable
                abort(422)

    # @TODO: Create a new endpoint or update a previous endpoint to handle searching for a team in the title
    #        the body argument is called 'search' coming from the frontend.
    #        If you use a different argument, make sure to update it in the frontend code.
    #        The endpoint will need to return success value, a list of books for the search and the number of books with the search term
    #        Response body keys: 'success', 'books' and 'total_books'

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app

