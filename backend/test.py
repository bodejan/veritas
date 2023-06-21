import requests

url = 'http://127.0.0.1:5000'
headers = {'Content-Type': 'application/json'}  # Set the headers to indicate JSON data


def test_index_route():
    response = requests.get(url, headers=headers)
    assert response.status_code == 500
    # assert response.json() == {"key": "value"}
    print(response.json())


def test_id_route():
    # Example ID value
    id = ['com.digibites.calendar', 'com.one.goodnight', 'com.marmalade.monopoly']

    payload = {'id': id}
    response = requests.post(f'{url}/id', json=payload, headers=headers)

    # Print the response status code and content
    print('Response Status Code:', response.status_code)
    print('Response Content:', response.json())


def test_category_route():
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

    # Print the response content
    print(response.json())

def test_db_refresh():
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
    #test_get_db()

