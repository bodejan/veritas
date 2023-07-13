"""
The script initializes and runs the flask app. Furthermore, it provides the app routes and orchestrates functions from the nlp and webcrawling modules.
"""

from concurrent.futures import ThreadPoolExecutor
import json
import os
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from selenium import webdriver
from src.webcrawling.app_db_crawler import crawl_db
from src.webcrawling.playstore_crawler import get_name_logo_url_policy_by_id
from src.webcrawling.androidrank_crawler import get_ids_for_category
from src.NLP.NLPPredictor.predictor import predictor
from src.models import AndroidApp, ZERO_SCORES

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

# Configuration settings
app.config['DEBUG'] = True


@app.route('/')
def index():
    """
    API endpoint for the root URL.

    Returns:
        tuple: A tuple containing the JSON response data and the HTTP status code.

    """
    data = {"key": "value"}
    print(data)
    return jsonify(data), 500


@app.route('/category', methods=['POST'])
def category():
    """
    API endpoint for getting apps by category.

    Args:
        request (flask.Request): The HTTP request object containing the JSON payload.

    Returns:
        str: JSON string containing the app information.

    Raises:
        ValueError: If the 'number' field in the request payload is not a valid integer.
        Exception: If an error occurs during the process.

    """
    data = request.get_json()

    try:
        start_time = time.time()
        category = data.get('category')
        number = int(data.get('number'))
        ids = get_ids_for_category(category, number)
        end_time = time.time()
        print(f'Androidrank Crawler: Crawled {number} apps in {end_time-start_time}s')
        return get_apps_by_ids(ids)

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
    """
    API endpoint for getting apps by IDs.

    Args:
        request (flask.Request): The HTTP request object containing the JSON payload.

    Returns:
        str: JSON string containing the app information.

    """
    data = request.get_json()
    ids = data.get('id')

    return get_apps_by_ids(ids)


@app.route('/get_db', methods=['GET'])
def get_db():
    """
    API endpoint for getting the database file.

    Returns:
        str: JSON string containing the database file contents.

    Raises:
        FileNotFoundError: If the database file is not found.
        Exception: If an error occurs during the process.

    """
    try:
        with open('/app/src/db.json', 'r') as file:
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
    """
    API endpoint for refreshing the database.

    Returns:
        str: JSON string with a success message.

    Raises:
        Exception: If an error occurs during the process.

    """
    try:
        start_time = time.time()
        crawl_db()
        end_time = time.time()
        print(f'DB Crawler: Refreshed db in {end_time-start_time}s')
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
    """
    API endpoint for testing purposes.

    Returns:
        str: The page source of the test URL.

    """
    print(request)
    # Create a new instance of the Chrome driver
    driver = webdriver.Remote('http://chrome:4444/wd/hub', options=webdriver.ChromeOptions())

    # Navigate to Google
    driver.get("https://play.google.com/store/apps/details?id=")

    s = driver.page_source
    print(s)
    return s


def get_apps_by_ids(ids):
    """
    Retrieve app information for the given IDs.

    Args:
        ids (list): List of app IDs.

    Returns:
        str: JSON string containing the app information.

    Raises:
        Exception: If an error occurs during the process.

    """
    try:
        apps = []
        start_time = time.time()

        def process_id(id):
            name, logo_url, policy, status = get_name_logo_url_policy_by_id(id)
            if status == 'Success':
                scores = predictor(policy)
            else:
                scores = ZERO_SCORES
            app = AndroidApp(name, id, logo_url, policy, scores, status)
            return app.__dict__

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_id, id) for id in ids]

            for future in futures:
                try:
                    app_dict = future.result()
                    apps.append(app_dict)
                except Exception as e:
                    print(f"An error occurred: {str(e)}")

        json_apps = json.dumps(apps)
        end_time = time.time()
        print(f'Playstore Crawler: Crawled {len(apps)} apps in {end_time-start_time}s')
        return json_apps

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return str(e)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
