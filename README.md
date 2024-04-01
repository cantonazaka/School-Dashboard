# School Dashboard App

This is a dashboard application developed to assist educational advisors in prioritizing students for support based on various academic indicators.

## Installation

### Option 1: Virtual Environment

1. Clone this repository to your local machine

2. Navigate to the project directory:

    ```bash
    cd School-Dashboard
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment

5. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Run the application:

    ```bash
    python app.py
    ```

7. Access the application in your web browser at [http://localhost:8080](http://localhost:8080).

### Option 2: Docker

1. Clone this repository to your local machine

2. Navigate to the project directory:

    ```bash
    cd School-Dashboard
    ```

3. Build the Docker image:

    ```bash
    docker build -t school-dashboard-app .
    ```

4. Run the Docker container:

    ```bash
    docker run -p 4500:8080 --name dash-container school-dashboard-app
    ```

5. Access the application in your web browser at [http://localhost:4500](http://localhost:4500).

## Usage

- Once the application is running, you can access it in your web browser at the specified URL.
- Use the dropdown menus and interactive components to explore the data and prioritize students based on academic indicators.

## Contributor

- Cantona ZAKAVOLAMIHANTA