# Evaluating Privacy Policies of Android Apps (IOSL ST 23)

Description here .....


The project consists of a Frontend (React), and a Backend (Python Flask webcrawler and NLP).


```
App
│
├── Frontend
├── Backend
│   ├── webcrawling
│   ├── NLP_predictor
│   └── app.py
└── docker-compose.yml
```
## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.



## Installation from Source

### Frontend

1. Navigate to the Frontend directory:

```bash
cd frontend
```

2. Install the necessary packages:

```bash
npm install
```

3. Start the server:

```bash
npm start
```

### Backend

1. Navigate to the Backend directory:

```bash
cd ../backend
```

2. Create a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```

3. Install the necessary packages:

```bash
pip install -r requirements.txt
```

4. Run the Flask application:

```bash
python app.py
```

## Installation using Docker Compose

1. Navigate to the root directory:

```bash
cd IOSL-ST-23
```

2. Build and run the Docker containers:

```bash
docker-compose up --build
```

This will start the Frontend and Backend services as defined in the `docker-compose.yml` file.

## Documentation

### Frontend

### Backend
The documentation for the backend is automatically created based on docstrings using [pdoc3](https://github.com/pdoc3/pdoc). <br> (See [backend docs](backend/docs/src/index.html)).

To update the documentation using pdoc3:

1. Navigate to the Backend directory:

```bash
cd ../backend
```

2. Generate docs in ```/backend/docs/src```:

```bash
pdoc --html --output-dir docs --force src
```

3. Open ```/backend/docs/src/index.html``` in your web-browser of choice.

## Usage
1. Install frontend and backend following the installation guide.
2. Access ```http://localhost:3000``` in your web-browser of choice.
3. Generate a score for the completenes of an android apps' privacy policy via.:

    3.1. The apps' category

    3.2. The apps' id

    3.3. The apps' name

## Troubleshooting
1. Recreate the frontend and backend container using the installation guide.
2. Check your internet connection. The web-crawler heavily rely on a stable internet connection to access webpages from androidrank and the google play store.
3. Analyze the logs within the docker container.
4. Check if the structure or links of web-pages has changed. To do so, inspect the ```driver.find_element()``` functions in the source code. 

## Contributing
For contributions please open a pull-request. Future features may include: 
1. Multi-class prediction of privacy policy categories.
2. Text highlighting and matching of sentences with the privacy policies and their corresponding categories.
3. Crawler robustness improvements e.g., creation of variables for crucial html elements for better maintainability. 
4. There is no limit! Test the application, expand and improve it as you please.

## Authors and Acknowledgment
The tool has been developed by master students at TU Berlin at School IV - Electrical Engineering and Computer Science: Department of Telecommunication Systems (Chair of Service-centric Networking).

The following authors contributed to this project:
* [Ahmet Sevim](https://www.linkedin.com/in/sevimahmet/)
* [Daria Seita](https://www.linkedin.com/in/daria-seita-b346b7187/)
* [Furat Hamdan](https://www.linkedin.com/in/furat-hamdan-9b77b8256/)
* [Heyi Li]()
* [Jan Bode](https://www.linkedin.com/in/bode-jan/), and 
* [Richard Detlefs]().

The project was closely supervised and evaluated by Thomas Cory and Prof. Dr. Axel Küpper.

## License
MIT.

