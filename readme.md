# Event Management

## Overview

This project is a Django-based web application that has the following api's.

1. GET /events: Lists all available events with details like name, date, location, and available tickets.

2. POST /events: Adds a new event to the system via admin pannel.

3. GET /events/{id}: Retrieves detailed information about a specific event.

4. POST /events/{id}/book: Books tickets for an event.


## Local Setup and Execution

Follow these steps to set up and run the project locally:

- Start redis service
    ```
    localhost:6379
    ```

- Clone the repository to your local machine.
    ```
    git clone https://github.com/username/repository.git
    ```

- Navigate to the project directory.
    ```
    cd repository
    ```

- Install the required dependencies.
    ```
    pip install -r requirements.txt
    ```

- Run the Django migrations.
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

- Start the Django development server.
    ```
    python manage.py runserver
    ```

The application should now be running at `http://localhost:8000`.

## Swagger
```
http://localhost:8000/swagger/
```

## Docker Setup

Follow these steps to set up and run the project using Docker:

1. Build the Docker image.
    ```
    docker build -t event_management .
    ```

2. Run the Docker container.
    ```
    docker run -p 8000:8000 event_management
    ```

The application should now be running at `http://localhost:8000`.

## Assumptions
- Redirection to google maps api
- writing few sample test cases
- using sqlLite as sample database
