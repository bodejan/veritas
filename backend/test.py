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


# test_index_route()
test_id_route()
# test_category_route()
