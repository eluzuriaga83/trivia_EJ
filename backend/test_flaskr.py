import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

#to test the delete function you have to change this parameter before runing the test
delete_id = 32

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://postgres:admin@localhost:5432/' + self.database_name #"postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question= {
            'question': 'What is the only state in the United States that does not have a flag in a shape with 4 edges?',
            'answer': 'Ohio', 
            'difficulty': 3,
            'category': 3
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    #test to get  the questions
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        #self.assertEqual(res.status.code,200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        #self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])


    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #create a new question
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
    '''    
    # Remember to change the parameter delete_id before running the test
    def test_delete_question(self):
        res = self.client().delete('/questions/' + str(delete_id))
        data = json.loads(res.data)

        question =Question.query.filter(Question.id == delete_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'],2)'''
    
    # Test to search a question
    def test_search_question(self):
        self.search_term = {'searchTerm': 'Tom'}
        res = self.client().post('/questions/search', json=self.search_term)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
    
    # Test to play
    def test_questions_quizzes(self):
        
        res = self.client().post('/quizzes', json={'previous_questions':['5'], 'quiz_category':{"type": "Geography", "id": 3}},)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()