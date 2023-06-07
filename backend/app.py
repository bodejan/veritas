import os
from flask import Flask
from flask_cors import CORS
import random
from flask import jsonify, request
from webcrawling.playstore_crawler import get_policy
from webcrawling.androidrank_crawler import get_applist
from NLP.NLPPredictor.predictor import predictor

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

    #print(policy)
    scores = predictor(policy)
    #print(scores)

    result = {
        'id': id,
        'name': id,
        'image': 'image',
        'policies': scores
        }
    return result


#def run_app():
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
    #app.run()