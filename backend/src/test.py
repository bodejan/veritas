"""
This script contains test cases for the Flask application.

The script sends HTTP requests to different routes of the Flask application and prints the response data or error
information. It is used for testing the functionality and correctness of the application's API endpoints.

Note: The Flask application should be running before executing the test cases.

"""

import requests

url = 'http://127.0.0.1:5000'
headers = {'Content-Type': 'application/json'}  # Set the headers to indicate JSON data


def test_index_route():
    """
    Test the index route of the Flask application.

    Sends a GET request to the index route and checks the response status code.

    Returns:
        None

    """
    response = requests.get(url, headers=headers)
    assert response.status_code == 500
    print(response.json())


def test_id_route():
    """
    Test the ID route of the Flask application.

    Sends a POST request to the ID route with example ID values and prints the response status code and content.

    Returns:
        None

    """
    # Example ID value
    id = ['com.digibites.calendar', 'com.one.goodnight', 'com.marmalade.monopoly']

    payload = {'id': id}
    response = requests.post(f'{url}/id', json=payload, headers=headers)

    print('Response Status Code:', response.status_code)
    print('Response Content:', response.json())


def test_category_route():
    """
    Test the category route of the Flask application.

    Sends a POST request to the category route with a category and number parameters,
    and prints the response content.

    Returns:
        None

    """
    # Set the category and number parameters
    category = 'Communication'
    number = 5

    # Set the JSON payload
    payload = {
        'category': category,
        'number': number
    }

    # Send a POST request to the Flask route with the JSON payload
    response = requests.post(f'{url}/category', json=payload, headers=headers)

    print(response.json())


def test_db_refresh():
    """
    Test the database refresh route of the Flask application.

    Sends a POST request to the database refresh route and prints the success message or error information.

    Returns:
        None

    """
    url = 'http://127.0.0.1:8000/db_refresh'
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print('Database refreshed successfully.')
        else:
            print('An error occurred while refreshing the database.')
            print('Status code:', response.status_code)
            print('Error message:', response.json())
    except requests.exceptions.RequestException as e:
        print('An error occurred while making the request:', e)


def test_get_db():
    """
    Test the get database route of the Flask application.

    Sends a GET request to the get database route and prints the response data or error information.

    Returns:
        None

    """
    url = 'http://127.0.0.1:8000/get_db'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Perform assertions or validations on the data
        print(data)
    else:
        print('Error:', response.status_code)


if __name__ == '__main__':
    test_db_refresh()
    # test_get_db()
