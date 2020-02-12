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
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_list_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['1'], 'Science')
        self.assertEqual(data['6'], 'Sports')

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])
        self.assertIsNotNone(data['categories'])

    def test_delete_question(self):
        question = Question("What's my name?", "FooBar", '2', 4)
        question.insert()

        res = self.client().delete('/questions/{}'.format(question.id))

        self.assertEqual(res.status_code, 200)
        self.assertIsNone(Question.query.get(question.id))

    def test_delete_unexisting_question(self):
        id = 404
        res = self.client().delete('/questions/{}'.format(id))

        self.assertEqual(res.status_code, 404)

    # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
