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
        self.database_name = "triviaDB"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        self.new_question = {
            'question' : 'testQuestion',
            'answer' : 'testAnswer',
            'category' : 6,
            'difficulty' : 5
        }
        self.new_category = {
            'type' : 'testCategory'
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        qs = Question.query.all()
        catgs = Category.query.all()
        cat_data = [c.type for c in catgs]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], len(qs))
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['categories'], cat_data)
        #self.


    def test_404_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000', json={'rating':1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    '''def test_create_question(self):


    def test_delete_question(self):

    def test_update_question(self):
        
    

    def test_search_questions(self):
    
    def test_category_questions(self):

    def test_quiz(self):







'''

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()