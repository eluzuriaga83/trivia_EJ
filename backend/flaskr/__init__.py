import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route("/categories", methods=['GET'])
    def get_allcategories():

        categories = Category.query.order_by(Category.id).all()
        if len(categories) == 0:
            abort(404)

        # formatting the categories to return json
        current_categories = {
            category.id: category.type for category in categories}

        return jsonify({
            'categories': current_categories
        })

    # GET requests for questions, including pagination (every 10 questions).
    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    # get categories
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        if len(categories) == 0:
            abort(404)

        # formatting the categories and adding them to a dictionary
        current_categories = {
            category.id: category.type for category in categories}

        return current_categories

    # get questions
    @app.route("/questions", methods=['GET'])
    def get_questions():

        # query to get all the questions
        questions = Question.query.all()
        # give format to the questions and applying pagination
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': get_categories(),
            'currentCategory': None

        })

    # delete questions
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        # query to get the question through the id
        question = Question.query.filter(Question.id == id).one_or_none()

        if(question is None):
            abort(404)

        try:
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': id,

            })

        except Exception as e:
            print('Exception >>>', e)
            abort(422)

    # create a new question

    @app.route('/questions', methods=['POST'])
    def add_questions():
        # get the information from the request
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)

        try:
            # adding the new question to the database
            new_question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category)
            new_question.insert()

            return jsonify({
                'success': True,
                'created': new_question.id})

        except BaseException:
            abort(422)

    # search questions

    @app.route("/questions/search", methods=['POST'])
    def search_questions():

        try:
            search_term = ''
            if request.method == "POST":
                search_term = request.json['searchTerm']

            query = Question.query.filter(
                Question.question.ilike(
                    "%" + search_term + "%")).all()
            
            current_questions = [question.format() for question in query]

            return jsonify({
                'success': True,
                'questions': current_questions,
                'totalQuestions': len(query),
                'currentCategory': None})

        except Exception as e:
            abort(405)

    # get questions based in category
    @app.route("/categories/<int:id>/questions", methods=['GET'])
    def get_category_questions(id):
        questions = Question.query.filter(Question.category == id).all()
        if questions is None:
            abort(404)

        current_questions = [question.format() for question in questions]

        return jsonify({
            'questions': current_questions,
            'totalQuestions': len(questions),
            'currentCategory': id})

    # Functionality for the tab Play
    @app.route('/quizzes', methods=['POST'])
    def get_questions_quizzes():
        # initialize the variable for result
        result_questions = []
        success = False
        try:
            # getting the information from the request
            body = request.get_json()
            previous_questions = body.get('previous_questions', [])
            quiz_category = body.get('quiz_category', None)
            category_id = quiz_category["id"]

            # Conditional: if there id ==0, meaning that the user chose ALL and
            # the previous questions is empty. I will select all the questions
            if category_id == 0 and previous_questions == []:
                questions = Question.query.all()

            # If not I will get the questions by the category sent in the
            # request
            questions = Question.query.filter(Question.category == category_id)
                       
            # I iterate each question to check if the question is part of the
            # previos question
            for question in questions:
                if question.id not in previous_questions:
                    # if not the question is added to the list result_questions
                    result_questions.append(question.format())
                    success = True

            # Return json with empty list or with results
            return jsonify({"success": success, "question": random.choice(
                result_questions) if len(result_questions) != 0 else None})

        except BaseException:
            abort(405)

    # handlers for all expected errors including 404 and 422.

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
    
    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
        "success": False, 
        "error": 405,
        "message": "method not allowed"
        }), 405


    return app
