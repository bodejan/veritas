from concurrent.futures import ThreadPoolExecutor
import json
import os
from flask import Flask
from flask_cors import CORS
import random
from flask import jsonify, request
from webcrawling.app_db_crawler import crawl_and_export_data
from webcrawling.playstore_crawler import get_name_logo_url_policy_by_id
from webcrawling.androidrank_crawler import get_ids_for_category
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from NLP.NLPPredictor.predictor import predictor
from models import AndroidApp, ZERO_SCORES

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
    data = request.get_json()

    try:
        category = data.get('category')
        number = int(data.get('number'))
        ids = get_ids_for_category(category, number)
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
    data = request.get_json()
    ids = data.get('id')

    return get_apps_by_ids(ids)


@app.route('/get_db', methods=['GET'])
def name():
    try:
        with open('/app/db.json', 'r') as file:
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
        #refresh_db()
        crawl_and_export_data()
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


def get_apps_by_ids(ids):
    try:
        apps = []
        
        def process_id(id):
            name, logo_url, policy, status = get_name_logo_url_policy_by_id(id)
            if status=='Success': scores = predictor(policy)
            else: scores = ZERO_SCORES
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
        return json_apps
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return str(e)


# def run_app():
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
    # app.run()
