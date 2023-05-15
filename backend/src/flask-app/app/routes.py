import random
from flask import jsonify, request
from app import app
# from webcrawling.playstore_crawler import get_policy
# from backend.src.webcrawling.androidrank_crawler import get_applist


@app.route('/')
def index():
    data = {"key" : "value"}
    return jsonify(data), 500

@app.route('/category', methods=['POST'])
def category():
    results = []
    data = request.get_json()
    try:
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
        id = data.get('id')
        
        # Check if the ID value exists and meets your validation criteria
        if id is None or not is_valid_id(id):
            error_message = 'Invalid ID.'
            error = {
                'error': error_message
            }
            return jsonify(error), 400

        result = get_result_from_id(id)
        print(result)
        return jsonify(result)
    
    except Exception as e:
        error_message = 'An error occurred.'
        error = {
            'error': error_message,
            'exception': str(e)
        }
        return jsonify(error), 500

def is_valid_id(id_value):
    # TODO add your validation criteria here
    return id_value.isdigit() and len(id_value) == 6


def get_result_from_id(id):
    print(f'Getting policy for {id}...')
    get_policy(id)
    print('Success', '\n')
    # TODO integrate nlp, define format for result (dict.)
    # policy = get_policy(app_name)
    # score = nlp(policy)
    result = {
            'id': id,
            'score': round(random.random(), 2)
        }
    return result
