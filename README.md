# Insight Hub Application

This is a FastAPI application project for Insight Hub.

## Prerequisites

Make sure you have Docker installed on your machine. You can download Docker from [here](https://www.docker.com/get-started).

## Getting Started

To run the application, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone <repository_url>
   ```

2. Navigate to the project directory:
    ```
    cd InsightHub
    ```

3. Create a `.env` file in the root directory of your project and define your environment variables:
    ```
    PROJECT_NAME="InsightHub"
    APP_HOST=0.0.0.0
    APP_PORT=8000
    API_KEY=your_api_key
    DATABASE_URL=your_database_url
    ```

4. Build the Docker image:
    ```
    docker build -t insight-hub-app .
    ```

5. Run the Docker container:
    ```
    docker run -p 8000:8000 --env-file .env insight-hub-app
    ```

6. Once the container is running, you can access the FastAPI application at http://localhost:8000.
