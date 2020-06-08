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


def paginate_questions(request, all_questions):
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
    questions = [question.format() for question in all_questions]
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
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return response

    # ---------------------------------------------------------------------#
    # Endpoints
    # ---------------------------------------------------------------------#

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        """ An endpoint to handle GET requests '/categories'

        Handling Get requests for all available categories

        Return:
            json: a json object with "categories": a list of all categories in database

        ErrorHandling:
            404: Resource not found if no question in the categories
            422: Unprocessable request
        """

        try:
            categories = Category.query.order_by(Category.id).all()
            categories = [category.type for category in categories]

            if len(categories) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'categories': categories,
            })

        except:
            abort(422)

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        """An endpoint to handle GET requests '/questions'

        Handling Get requests for all questions, including pagination for every 10 questions

        Return:
            a json object with:
                "success": True
                "questions": a list of paginated questions
                "categories": a list of all categories' type
                "current_category": None
                "total_questions": total number of questions

        Error handling:
            404: Resource not found if no such a question
        """
        all_questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, all_questions)

        if len(current_questions) == 0:
            abort(404)

        categories = set()
        for question in current_questions:
            categories.add(question['category'])

        all_categories = Category.query.order_by(Category.id).all()
        categories = [category.type for category in all_categories]

        return jsonify({
            'success': True,
            'questions': current_questions,
            'categories': categories,
            'current_category': None,
            'total_questions': len(all_questions)
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """An endpoint to handle DELETE requests '/questions/<question_id>'

        Deleting a question matched with designated question ID.

        Parameter:
            question_id (int): the question id to delete

        Return:
            A json object with
                "success": True
                "deleted": id of deleted question
                "total_questions": the total number of questions

        Error handling:
            404: resource not found if no such a question
            422: unprocessable request
        """
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            all_questions = Question.query.order_by(Question.id).all()

            if len(all_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'total_questions': len(all_questions)
            })

        except:
            abort(422)

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
    
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        """ An endpoint to handle POST requests for '/questions'

        Parameters:
            -question: text/strings
            -answer: text/strings
            -category: id of the category (1-6)
            -difficulty: int (1-5)

        Return:
            a json object with
                "success": True
                "created": id of the new question
                "current_category": type of the category selected
                "total_questions": the total questions

        Error handling:
            422: unprocessable request
        """
        try:
            body = request.get_json()
            category_id = body.get('category', None)
            new_question = Question(
                question=body.get('question', None),
                answer=body.get('answer', None),
                category=category_id,
                difficulty=body.get('difficulty', None)
            )
            new_question.insert()

            all_questions = Question.query.order_by(Question.id).all()
            category_type = Category.query.get(category_id).type

            return jsonify({
                'success': True,
                'created': new_question.id,
                'current_category': category_type,
                'total_questions': len(all_questions)
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
              "current_category": None
              "total_questions": the total number of questions

        Error Handling:
            404: Resource not found if no such a question
            422: unprocessable request
        """
        try:
            body = request.get_json()
            search_term = body.get('searchTerm', None)
            searched_questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))) \
                .order_by(Question.id).all()
            current_questions = paginate_questions(request, searched_questions)

            if len(current_questions) == 0:
                abort(404)

            categories = set()
            for question in current_questions:
                categories.add(Category.query.get(question['category']).type)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'current_category': None,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(category_id):
        try:
            questions_by_category = Question.query.filter(Question.category == str(category_id)).order_by(
                Question.id).all()
            current_questions = paginate_questions(request, questions_by_category)

            if len(current_questions) == 0:
                abort(404)

            current_category = Category.query.get(category_id).type

            return jsonify({
                'success': True,
                'questions': current_questions,
                'current_category': current_category,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)
            if quiz_category['id'] == 0:
                questions_for_quiz = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                questions_for_quiz = Question.query.filter(Question.category == quiz_category['id'],
                                                           Question.id.notin_(previous_questions)).all()

            questions = [question.format() for question in questions_for_quiz]

            if len(questions) == 0:
                abort(404)

            random_question = random.choice(questions)

            return jsonify({
                'success': True,
                'question': random_question,
                'current_category': quiz_category['type']
            })

        except:
            abort(422)
    # @app.route("/quizzes", methods=['POST'])
    # def play_quiz_question():
    #     '''
    #     retrieves questions to play the quiz.
    #     '''
    #     if request.data:
    #         search_key = json.loads(request.data.decode('utf-8'))
    #         if (('quiz_category' in search_key
    #              and 'id' in search_key['quiz_category'])
    #                 and 'previous_questions' in search_key):
    #             questions_query = Question.query.filter_by(
    #                 category=search_key['quiz_category']['id']
    #             ).filter(
    #                 Question.id.notin_(search_key["previous_questions"])
    #             ).all()
    #             length_of_available_question = len(questions_query)
    #             if length_of_available_question > 0:
    #                 result = {
    #                     "success": True,
    #                     "question": Question.format(
    #                         questions_query[random.randrange(
    #                             0,
    #                             length_of_available_question
    #                         )]
    #                     )
    #                 }
    #             else:
    #                 result = {
    #                     "success": True,
    #                     "question": None
    #                 }
    #             return jsonify(result)
    #         abort(404)
    #     abort(422)
    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        })

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
