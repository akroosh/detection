# Vehicle Tracker and License Plate Detection System
Welcome to the Vehicle Tracker and License Plate Detection System! This project allows you to upload an image containing vehicles, and our powerful YOLO-based model will detect and track vehicles in the image, as well as track car plates. You can then view the results, including the tracked vehicles and their associated license plates.

## Features

- **Upload Image**: Upload an image containing vehicles via a simple web interface.
- **Vehicle Detection and Tracking**: Our advanced YOLO-based model detects vehicles in the uploaded image and tracks their coordinates.
- **License Plate Detection**: The model also identifies license plates on the detected vehicles.
- **View Results**: After processing the image, you can view the tracked vehicles and their license plates.

## Local installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/akroosh/detection.git
    ```
2. Create a virtual environment and activate it
    ```bash
    virtualenv venv
   . venv/bin/activate
    ```
3. Install the required dependencies:

    ```bash
    pip install -r requirements/app_requirements.txt
    ```

4. Add .env file inserting your variables, using .env.example file

5. Apply the migrations:

    ```bash
    python vehicle_detection_app/manage.py migrate
    ```

6. Run the Django server:

    ```bash
    python vehicle_detection_app/manage.py runserver
    ```

7. Open your web browser and navigate to `http://localhost:8000/upload/`.

## Docker installation
1. Add .env file inserting your variables, using .env.example file

2. Build the image
    ```bash
    docker-compose build
    ```
3. Run the system
   ```bash
    docker-compose up -d
    ```
4. Access your application on `http://0.0.0.0:8000`

## Usage

1. Access the upload page by visiting `http://localhost:8000/upload/` or `http://0.0.0.0:8000/upload`  in your web browser.
2. Choose an image file containing vehicles and click the "Upload" button.
3. Wait for the image to be processed. Once done, you will see the tracked vehicles and their associated license plates.
4. Enjoy exploring the results by visitins `http://localhost:8000/results/` or `http://0.0.0.0:8000/results`


