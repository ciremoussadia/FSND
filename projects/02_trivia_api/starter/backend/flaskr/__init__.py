import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def formatted_categories(categories):
    return {str(category.id): category.type for category in categories}


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app)
    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,true')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,POST,DELETE')
        return response
    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories')
    def list_categories():
        categories = Category.query.all()
        return jsonify(formatted_categories(categories)), 200
    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.


  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

    @app.route('/questions', methods=['GET'])
    def list_questions():
        page = request.args.get('page', 1, int)
        offset = (page - 1) * 10
        questions = Question.query.offset(
            offset).limit(QUESTIONS_PER_PAGE).all()
        categories = Category.query.all()

        return jsonify({
            'questions': [question.format() for question in questions],
            'total_questions': len(Question.query.all()),
            'categories': formatted_categories(categories)
        }
        ), 200

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        if question is None:
            abort(404)
        else:
            question.delete()
            return jsonify({'success': True}), 200

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

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
        data = request.get_json()
        if 'searchTerm' in data:
            term = data['searchTerm']
            questions = Question.query.filter(
                Question.question.ilike('%{}%'.format(term)))
            return jsonify([question.format() for question in questions]), 200
        else:
            try:
                question = Question(
                    data['question'], data['answer'], data['category'], data['difficulty'])
                question.insert()
                return jsonify({}), 201
            except:
                abort(422)

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:category_id>/questions')
    def categories_questions(category_id):
        page = request.args.get('page', 1, int)
        offset = (page - 1) * 10
        categories = Category.query.all()
        Category.query.get_or_404(category_id)
        questions = Question.query.filter_by(category=category_id).offset(
            offset).limit(QUESTIONS_PER_PAGE)

        return jsonify({
            'questions': [question.format() for question in questions],
            'total_questions': len(questions.all()),
            'categories': formatted_categories(categories)
        }), 200

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
    def get_quizz():
        params = request.get_json()

        query = Question.query
        if params['quiz_category']['id'] != 0:
            Category.query.get_or_404(params['quiz_category']['id'])
            query = Question.query.filter_by(
                category=params['quiz_category']['id'])

        if params['previous_questions']:
            ids = [q['id'] for q in params['previous_questions']]
            query.filter(~Question.id.in_(ids))

        question = random.choice(query.all())
        return jsonify(question.format()), 200
    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return error

    return app
