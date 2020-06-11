# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Reference
Getting Started
- Backend Base URL: http://127.0.0.1:5000/
- Frontend Base URL: http://localhost:3000

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

### Endpoints 

#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
- Sample: curl http://127.0.0.1:5000/categories
```
{ 
  "categories": [
    {
     '1' : "Science",
     '2' : "Art",
     '3' : "Geography",
     '4' : "History",
     '5' : "Entertainment",
     '6' : "Sports"
    }
  ], 
 "success": true, 
 "categories": 6
}
```

#### GET '/questions'
- Fetches a list of question objects, total number of questions, and the category that question belongs to
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1
- Sample: curl http://127.0.0.1:5000/questions

```
{ "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 39
}
```


#### DELETE /questions/<int:question_id>
- Deleting a question matched with designated question ID of it exists. 
- Returns the id of the deleted question, success value, and total questions. 
- Sample: curl -X DELETE http://127.0.0.1:5000/questions/21

```
{
   "questions": [
        {
          "answer": "Alexander Fleming", 
          "category": 3, 
          "difficulty": 1, 
          "id": 21, 
          "question": "Who discovered penicillin?"
        }
   ],
  "deleted": 21, 
  "success": true, 
  "total_questions": 38
}
```

#### POST /questions
- Creates a new question with the question, answer, difficulty, and category. 
- Returns the id of the question, current category, success value, and total questions
- Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d 
'{"question":"new question", "answer":"answer", "difficulty":"1", "category":"6"}'
```
{
   "questions": [
        {
          "answer": "answer", 
          "category": 6, 
          "difficulty": 1, 
          "id": 120, 
          "question": "new question"
        }
   ],
   "created": 120, 
   "current_category": "Sports", 
   "success": true, 
   "total_questions": 38
}
```

#### POST /search_questions
- This endpoint to get questions based on a search term. It should return any questions for whom the search term is a 
  substring of the question.
- Returns success value, total number of questions
- Sample: curl http://127.0.0.1:5000/search_questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"movie"}'

```
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "success": true, 
  "total_questions": 39
}
```

#### GET /categories/<int:category_id>/questions
- This endpoint GET questions based on the category. It should return current category, questions in this category, 
  success value, and total questions
- Returns success value, and total number of questions 
- Sample: curl 127.0.0.1:5000/categories/1/questions
```
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 39
}
```

#### POST /quizzes
- Getting questions to play the quiz. This endpoint should take category and previous question parameters and return
  a random questions within the given category, if provided, and that is not one of the previous questions.
- Returns: multiple key/value pairs object with the following content: 
    * success: True or False 
    * question: random question from the list of available questions in the category/categories, which it contains
                details about the question: answer, category, difficulty, id, and question content
    * current_category: the category type of current question
```
{
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 21, 
    "question": "Who discovered penicillin?"
  }, 
  "success": true,
  "question": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }
  ],
  "current_category": "Science" 
}
```

### Error Handling
```
Errors are returned as JSON objects in the following format:
{   
    "success": False, 
    "error": 422, 
    "message": "Unprocessable"
}
```
The API will return five error types when requests fail: 
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Server Error


