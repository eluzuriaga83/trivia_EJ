# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*



## Endpoints
```
1. To enable cross-domain requests usse FLASK Cors and set response headers. 
    Access-Control-Allow-Headers
    Access-Control-Allow-Methods

2. GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, 
number of total questions, current category, categories. 

GET '/api/v1.0/questions'
- Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
    {
        'questions': [
            {
                'id': 1,
                'question': 'This is a question',
                'answer': 'This is an answer', 
                'difficulty': 5,
                'category': 2
            },
        ],
        'totalQuestions': 100,
        'categories': { '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports" },
        'currentCategory': 'History'
    }

3. GET requests for all available categories. 
GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
    {'1' : "Science",
     '2' : "Art",
     '3' : "Geography",
     '4' : "History",
     '5' : "Entertainment",
     '6' : "Sports"}


4. DELETE question using a question ID. 
DELETE '/api/v1.0/questions/<int:id>'
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. 

5. POST a new question, which will require the question and answer text, category, and difficulty score. 
POST '/api/v1.0/questions'
- Sends a post request in order to add a new question
- Request Body: 
    {
        'question':  'Heres a new question string',
        'answer':  'Heres a new answer string',
        'difficulty': 1,
        'category': 3,
    }
- Returns: Does not return any new data

6. Get questions based on category. 
GET '/api/v1.0/categories/<int:id>/questions'
- Fetches questions for a category specified by id request argument 
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string 
    {
        'questions': [
            {
                'id': 1,
                'question': 'This is a question',
                'answer': 'This is an answer', 
                'difficulty': 5,
                'category': 4
            },
        ],
        'totalQuestions': 100,
        'currentCategory': 'History'
    }

7. Get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
POST '/api/v1.0/questions'
- Sends a post request in order to search for a specific question by search term 
- Request Body: 
    {
        'searchTerm': 'this is the term the user is looking for'
    }
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string 
    {
        'questions': [
            {
                'id': 1,
                'question': 'This is a question',
                'answer': 'This is an answer', 
                'difficulty': 5,
                'category': 5
            },
        ],
        'totalQuestions': 100,
        'currentCategory': 'Entertainment'
    }

8. POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 

POST '/api/v1.0/quizzes'
- Sends a post request in order to get the next question 
- Request Body: 
    {'previous_questions':  an array of question id's such as [1, 4, 20, 15]
'quiz_category': a string of the current category }
- Returns: a single new question object 
    {
        'question': {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        }
    }
9. Error Handling
- Errors are returned as JSON objects in the following format:
    {
       "success": False, 
       "error": 400,
       "message": "bad request"
    } 
The API will return three error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Not Processable
```
## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
