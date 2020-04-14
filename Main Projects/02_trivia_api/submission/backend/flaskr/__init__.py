import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})
  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  '''
  @app.route('/')
  def index():
    return jsonify({
      'message' : 'Hello There!'
    }) 
  '''
  
  @app.route('/categories', methods = ['GET'])
  def categories():
    categories = Category.query.all()
    data = [{'succes':True}]
    for c in categories:
      c_dict = {
        'id' : c.id,
        'type' : c.type
      }
      data.append(c_dict)
    formatted_categos = [c.format() for c in categories]
    categories_s = [c.type for c in categories]
    #return data
    return jsonify({
      'success' : True,
      'categories' : categories_s,
      'total categories:' : len(formatted_categos)
    })


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
  @app.route('/questions', methods = ['GET'])
  def get_questions():
    questions = Question.query.all()
    page = request.args.get('page', 1, type =int)
    start = (page - 1) * 10
    end = start + 10
    formatted_qs = [q.format() for q in questions]
    curr_catgs = []
    for q in formatted_qs[start:end]:
      cat_name = q['category'] #or q.get('category')
      if cat_name not in curr_catgs:
        curr_catgs.append(cat_name)

    #forgot this
    catgs = Category.query.all()
    #categories = [c.format() for c in catgs]
    categories = [c.type for c in catgs]
    
    return jsonify({
      'success' : True,
      'questions' : formatted_qs[start:end],
      'total_questions' : len(formatted_qs),
      'categories' : categories,
      'current_category' : None #curr_catgs #just for now hardcoded
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods = ['DELETE'])
  def delete_question(question_id):
    #try:
    q = Question.query.filter_by(id = question_id).one_or_none()
    if q is None:
      abort(404)

    q.delete()
    #return redirect(url_for('get_questions'))
    return jsonify({
      'success' : True
    })

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods = ['POST'])
  def create_question ():
    body = request.get_json()

    if 'question' in body:
      qs = body.get('question')
    if 'answer' in body:
      a = body.get('answer')
    if 'category' in body:
      cat = body.get('category')
    if 'difficulty' in body:
      s = body.get('difficulty')

    q = Question(qs,s,cat,s)
    q.insert()

    #return redirect(url_for('get_questions'))
    return jsonify ({
      'success' : True
    })
    

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods = ['POST'])
  def search_questions ():
    req = request.get_json()
    search_term=req.get('searchTerm')
    #search_term=request.args.get('searchTerm', '')
    result = Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
    if not result:
      abort(404)
    formated_result = [q.format() for q in result]
    return jsonify({
      'success' : True,
      'questions' : formated_result,
      'no. results' : len(formated_result)
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods = ['GET'])
  def cat_questions(category_id):
    categoryy = Category.query.filter_by(id = category_id).one_or_none()
    if categoryy is None:
      abort(404)
    cat_id_str = str(categoryy.id)
    #cat_id_str = str(categoryy.format().get('id'))
    qs = Question.query.filter_by(category = cat_id_str).all()

    data = [q.format() for q in qs]
    if qs is None:
      data = 'not found'
      abort(404)


    return jsonify({
      'success' : True,
      'questions' : data,
      'total_questions' : len(data)
    })


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
  @app.route('/quiz', methods = ['POST'])
  def play_quiz():
    body = request.get_json()
    #curr_category = request.args.get('quiz_category')
    #prev_qs = request.args.get('previous_questions')
    curr_category = body.get('quiz_category')
    prev_qs = body.get('previous_questions')
    catego = Category.query.filter_by(type = curr_category).one_or_none()
    if catego is None:
      abort(404)
    cat_id = str(catego.id)
    cat_qs = Question.query.filter_by(category = cat_id).all()
    cat_qs_ids = [q.id for q in cat_qs]
    if cat_qs is None:
      abort(404)
    #new_qs = [q.format() for q in cat_qs and not in prev_qs ]
    new_qs = []
    for q in cat_qs:
      if str(q.id) not in prev_qs:
        new_qs.append(q.format())

    

    valid_list = list(set(cat_qs_ids) - set(prev_qs))
    #random.choice(valid_list)

    new_question = cat_qs[cat_qs_ids.index(random.choice(valid_list))]

    return jsonify({
      'success' : True,
      'question' : new_question.format() #cat_qs[random.choice(valid_list)].question #valid_list
    })
    

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False, 
          "error": 404,
          "message": "Not found"
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
          "message": "Bad request"
          }), 400
  
  return app

    