# PredictionSA20

## Overview

PredictionSA20 is a Django-based web application that aims to provide predictions and insights for the SA20 cricket league. This project allows users to submit their predictions for match outcomes and player performances, and displays these predictions on a leaderboard. The goal is to create a user-friendly platform where cricket enthusiasts can engage with the game and compare their predictions with others.

## Features

- **User Authentication**: Secure user registration and login system.
- **Match Predictions**: Predictions for upcoming matches based on historical data and current player forms.
- **Player Analysis**: Detailed analysis of player performances, including batting and bowling statistics.
- **Interactive Dashboard**: A user-friendly interface with interactive charts and graphs to visualize data.
- **Admin Panel**: A robust admin panel for managing users, matches, and predictions.
- **API Endpoints**: Expose data and predictions through RESTful API endpoints.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/Pruthviraj-2004/PredictionSA20.git
    cd PredictionSA20
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run database migrations**:
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser** (for accessing the admin panel):
    ```sh
    python manage.py createsuperuser
    ```

6. **Collect static files**:
    ```sh
    python manage.py collectstatic
    ```

7. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

Visit `http://127.0.0.1:8000/` in your browser to view the application.

## Usage

- **Home Page**: The home page displays the latest match predictions and player analyses.
- **Admin Panel**: Access the admin panel at `http://127.0.0.1:8000/admin/` to manage the site.
- **User Dashboard**: Registered users can log in to view personalized predictions and statistics.

## API Endpoints

PredictionSA20 provides several API endpoints to access data and predictions programmatically. Below is a list of available endpoints:

### 1. List Matches

**Endpoint**: `/api/matches/`

**Method**: GET

**Description**: Retrieve a list of all matches.

### 2. Match Details

**Endpoint**: `/api/matches/<id>/`

**Method**: GET

**Description**: Retrieve details of a specific match.

### 3. List Players

**Endpoint**: `/api/players/`

**Method**: GET

**Description**: Retrieve a list of all players.

### 4. Player Details

**Endpoint**: `/api/players/<id>/`

**Method**: GET

**Description**: Retrieve details of a specific player.

### 5. Create Prediction

**Endpoint**: `/api/predictions/`

**Method**: POST

**Description**: Create a new prediction for a match.

## Project Structure

- `predict20/`: Contains the main Django project settings and URLs.
- `static/`: Static files such as CSS, JavaScript, and images.
- `templates/`: HTML templates for rendering the web pages.
- `app/`: Contains the core application logic including models, views, and forms.
- `requirements.txt`: Lists the Python dependencies for the project.

## Contributing

We welcome contributions to improve PredictionSA20. To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```sh
    git checkout -b feature-branch
    ```
3. Make your changes and commit them:
    ```sh
    git commit -m 'Add new feature'
    ```
4. Push to the branch:
    ```sh
    git push origin feature-branch
    ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- The Django community for their comprehensive documentation and support.
- Contributors who have helped improve this project.
