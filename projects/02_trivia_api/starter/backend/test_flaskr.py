import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        """Test case for retrieve categories function"""
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_paginated_questions(self):
        """Test case for retrieve paginated questions"""
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']) <= 10)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])

    def test_404_sent_requesting_beyond_valid_page(self):
        """Test case for 404 sending request beyond total pages"""
        response = self.client().get('/questions&page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_question(self):
        """Test case to delete a question"""
        total_questions_before_delete = len(Question.query.all())
        response = self.client().delete('/questions/6')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 6)
        deleted_question = total_questions_before_delete - data['total_questions']
        self.assertEqual(deleted_question, 1)

    def test_404_sent_deleting_non_existing_question(self):
        """Test case for deleting a non-existing question"""
        response = self.client().delete('/question/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_create_a_question(self):
        total_questions_before_add = len(Question.query.all())
        new_question = {
            "question": "adding a test question",
            "answer": "answer",
            "category": "3",
            "difficulty": "1"
        }
        response = self.client().post('questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        num_of_added_question = data['total_questions'] - total_questions_before_add
        self.assertEqual(num_of_added_question, 1)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()