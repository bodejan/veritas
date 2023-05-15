import requests

url = 'http://127.0.0.1:5000'

def test_index_route():
    response = requests.get(url)
    assert response.status_code == 500
    assert response.json() == {"key": "value"}
    print(response.json)

def test_id_route():
    headers = {'Content-Type': 'application/json'}  # Set the headers to indicate JSON data
    
    # Example ID value
    id = 'com.facebook.orca'
    
    payload = {'id': id}
    response = requests.post(url, json=payload, headers=headers)
    
    # Print the response status code and content
    print('Response Status Code:', response.status_code)
    print('Response Content:', response.json())

test_index_route()
# test_id_route()