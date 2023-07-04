# Use a base Python image
FROM python:3.9-slim

# Set the working directory within the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Download nltk
RUN python -c "import nltk; nltk.download('punkt', quiet=True)"
RUN python -c "import nltk; nltk.download('stopwords', quiet=True)"

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port that the Flask app will run on
EXPOSE 8000

ENV FLASK_DEBUG=1

# Set the FLASK_APP environment variable to the module's name
ENV FLASK_APP=src.app

# Run the Flask app
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "8000", "--reload"]