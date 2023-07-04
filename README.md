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
The documentation for the backend is automatically created based on docstrings using [pdoc3](https://github.com/pdoc3/pdoc) (see [backend docs](backend/docs/src/index.html)).

To update the documentation using pdoc3:

1. Navigate to the Backend directory:

```bash
cd ../backend
```

2. Run pdoc3

```bash
pdoc --html --output-dir docs --force src
```

Docs will be created/updates in ```/backend/docs/src```.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
