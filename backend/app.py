import os
from flask import Flask
from flask_cors import CORS
import random
from flask import jsonify, request
from webcrawling.playstore_crawler import get_policy
from webcrawling.androidrank_crawler import get_applist
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from NLP.NLPPredictor.predictor import predictor
from webcrawling.appname_crawler import refresh_db

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

# Configuration settings
app.config['DEBUG'] = True


# app.config['SECRET_KEY'] = 'your_secret_key'


@app.route('/')
def index():
    data = {"key": "value"}
    print(data)
    return jsonify(data), 500


@app.route('/category', methods=['POST'])
def category():
    results = []
    data = request.get_json()
    print(data)
    try:
        print(data)
        category = data.get('category')
        number = int(data.get('number'))

        # Perform processing or any other operations with the variables
        applist = get_applist(category, number)
        print(f'Getting top {number} of {category}... ')
        print(applist, '\n')

        for app_name in applist:
            result = get_result_from_id(app_name)
            results.append(result)

        return jsonify(results)

    except ValueError:
        error_message = 'Invalid number format.'
        error = {
            'error': error_message
        }
        return jsonify(error), 400

    except Exception as e:
        error_message = 'An error occurred.'
        error = {
            'error': error_message,
            'exception': str(e)
        }
        return jsonify(error), 500


@app.route('/id', methods=['POST'])
def id():
    print(request)
    data = request.get_json()
    try:
        ids = data.get('id')
        print(ids)
        results = []
        for id in ids:
            # Check if the ID value exists and meets your validation criteria
            if id is None or not is_valid_id(id):
                error_message = 'Invalid ID.'
                error = {
                    'error': error_message
                }
                return jsonify(error), 400

            result = get_result_from_id(id)
            print(result)
            results.append(result)
        return jsonify(results)

    except Exception as e:
        error_message = 'An error occurred.'
        error = {
            'error': error_message,
            'exception': str(e)
        }
        return jsonify(error), 500


@app.route('/name', methods=['GET'])
def name():
    try:
        with open('backend/src/webcrawling/policy_export/app_data.json', 'r') as file:
            data = file.read()
            return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        error_message = 'An error occurred.'
        error = {
            'error': error_message,
            'exception': str(e)
        }
        return jsonify(error), 500


@app.route('/db_refresh', methods=['POST'])
def db_refresh():
    try:
        refresh_db()
        return jsonify({'message': 'Database refreshed'}), 200
    except Exception as e:
        error_message = 'An error occurred.'
        error = {
            'error': error_message,
            'exception': str(e)
        }
        return jsonify(error), 500


@app.route('/test', methods=['POST'])
def test():
    print(request)
    # Create a new instance of the Chrome driver
    driver = webdriver.Remote('http://chrome:4444/wd/hub', options=webdriver.ChromeOptions())

    # Navigate to Google
    driver.get("https://play.google.com/store/apps/details?id=")

    s = driver.page_source
    print(s)
    return s


def is_valid_id(id):
    # TODO add your validation criteria here
    return True


def get_result_from_id(id):
    print(f'Getting policy for {id}...')
    success, policy = get_policy(id)
    if success:
        print('Success', '\n')
    else:
        print('Fail', '\n')

    # print(policy)
    scores = predictor(policy)
    # scores = ""
    # print(scores)

    result = {
        'id': id,
        'name': id,
        'image': 'image',
        'policies': scores
    }
    return result


# def run_app():
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
    # app.run()
