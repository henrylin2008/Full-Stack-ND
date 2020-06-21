import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

# ----------------------------------------------------------------------------#
# App Setup
# ----------------------------------------------------------------------------#

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    """Paginate question by QUESTIONS_PER_PAGE

    Parameters:
        -request (obj): an instance of request_class
        -all_questions (list): selection of questions that are queried from database

    Returns:
        -list: a paginated question list (max 10 questions per page)
    """

    # Get page from request, default to 1 if it's not provided
    page = request.args.get('page', 1, type=int)
    # Slice: start
    start = (page - 1) * QUESTIONS_PER_PAGE
    # slice: end
    end = start + QUESTIONS_PER_PAGE
    # Format all_questions into a list of dicts and slice
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    """ Create and configure an app 'trivia_app'

    The main function of Trivia app
    This function contains 3 parts
        -Initial setups
        -Endpoint functions
        -Error handlers
    """

    # ---------------------------------------------------------------------#
    # Initial setups
    # ---------------------------------------------------------------------#
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # Set up CORS that allows '*' for origins.
    CORS(app, resources={r"/*": {"origins": "*"}})

    """Use the after_request decorator to set Access-Control-Allow"""

    @app.after_request
    def after_request(response):
        """Setting Access-Control-allow

        Parameters:
            response: an instance of response_class

        Return:
            response object with Access-Control-Allow
        """
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # ---------------------------------------------------------------------#
    # Endpoints
    # ---------------------------------------------------------------------#

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        """ An endpoint to handle GET requests for '/categories'

        Return:
            a json object with "categories": a list of all categories in database

        ErrorHandling:
            404: Resource not found if no question in the categories
            422: Unprocessable request
        """
        try:
            categories_query = Category.query.order_by(Category.id).all()
            all_categories = [category.type for category in categories_query]

            if len(all_categories) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'categories': all_categories,
            })

        except:
            abort(422)

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        """An endpoint to handle GET requests for '/questions',
           including pagination every 10 questions

        Return:
            a json object with:
                "success": True
                "questions": a list of paginated questions
                "categories": a list of category types
                "total_questions": total number of questions

        Error handling:
            404: Resource not found if no such a question
        """
        questions_query = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions_query)
        category_query = Category.query.order_by(Category.id).all()

        categories = [category.type for category in category_query]

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'categories': categories,
            'total_questions': len(questions_query)
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """An endpoint to handle DELETE requests for '/questions/<question_id>'

        Parameter:
            question_id (int): the question id to be deleted

        Return:
            A json object with
                "success": True
                "deleted question": id of the deleted question
                "questions": current page of the question that is located
                "total_questions": the total number of questions

        Error handling:
            404: resource not found if no such question
            422: unprocessable request
        """
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            questions_query = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions_query)

            return jsonify({
                'success': True,
                'deleted question': question_id,
                'questions': current_questions,
                'total_questions': len(questions_query)
            })

        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        """ An endpoint to handle POST requests for '/questions'
        if question or answer fields are empty, return 422

        Parameters:
            -question: text/strings
            -answer: text/strings
            -category: id of the category (1-6)
            -difficulty: int (1-5)

        Return:
            a json object with
                "Success": True
                "Question ID": id of the new question
                "Category": the category of the new question
                "Questions": questions on paginated page
                "Total questions": total amount of questions

        Error handling:
            422: unprocessable request if new question or answer is blank
        """
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            new_question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty
            )
            if new_question.question == "" or new_question.answer == "":
                abort(422)
            else:
                new_question.insert()

            current_category = Category.query.get(new_category).type
            questions_query = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions_query)

            return jsonify({
                'Success': True,
                'Question ID': new_question.id,
                'Category': current_category,
                'Questions': current_questions,
                'Total Questions': len(questions_query)
            })

        except:
            abort(422)

    @app.route('/search_questions', methods=['POST'])
    def search_questions():
        """An endpoint to handle POST requests for '/search_questions'

        Get questions based on a search term; It should return any questions for whom
        the search term is a substring of the question

        Return:
              "success": True
              "questions": list of paginated questions
              "total_questions": the total number of questions

        Error Handling:
            404: Resource not found if no such question
            422: unprocessable request
        """
        search_term = request.json.get('searchTerm', None)
        try:
            search_question = Question.query.filter(Question.question.ilike('%{}%'.format(search_term)))\
                .order_by(Question.id).all()
            current_questions = paginate_questions(request, search_question)

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(category_id):
        """An endpoint to handle GET requests for '/categories/<int:category_id>/questions'

        Parameters:
            category_id (int): the id of the category that retrieves a list of questions

        Return:
            a json object with
                "success": True
                "questions": a list of paginated questions belongs to the selected category
                "current_category": the selected category
                "total_questions": the total number of questions

        Error handling:
            404: resource not found if no question in the category
        """
        questions_query = Question.query.filter(Question.category == str(category_id)).order_by(Question.id).all()
        current_questions = paginate_questions(request, questions_query)

        if len(current_questions) == 0:
            abort(404)

        current_category = Category.query.get(category_id).type

        return jsonify({
            'success': True,
            'questions': current_questions,
            'current_category': current_category,
            'total_questions': len(Question.query.all())
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        """An endpoint to handle POST request for '/quizzes'

        Getting questions to play the quiz. This endpoint should take category and previous question parameters and
        return a random questions within the given category, if provided, and that is not one of the previous questions.

        Parameters:
            previous_questions = previous questions
            quiz_category = category of current question

        Return:
            a json object with:
                "success": True
                "question": random selection of the question

        Error handling:
            422: unprocessable request
        """
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        try:
            if quiz_category['id'] == 0:
                questions_query = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                questions_query = Question.query.filter(Question.category == quiz_category['id'],
                                                        Question.id.notin_(previous_questions)).all()
            questions = [question.format() for question in questions_query]
            if len(questions) == 0:
                return jsonify({
                    "success:": True,
                    "question": None
                })

            random_question = random.choice(questions)

            if random_question:
                return jsonify({
                    "success": True,
                    "question": random_question
                })

        except:
            abort(422)

    # ---------------------------------------------------------------------#
    # Error Handlers
    # ---------------------------------------------------------------------#
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    return app
