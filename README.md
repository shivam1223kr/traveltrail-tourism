# TravelTrail - Smart Tourism Management System

A BTech CSE mini-project demonstrating online tour booking, hotel price comparison, smart destination recommendations and an AI-style travel chatbot.

## Features
- Browse curated Indian destinations
- Smart recommendation engine based on interest and budget
- Hotel price comparison across demo providers
- Booking request form with booking ID
- Rule-based tourism chatbot
- MySQL database schema for users, hotels, destinations and bookings

## Run locally
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`.

## Open in VS Code
1. In VS Code, select **File → Open Folder**.
2. Choose this `tourist manager` folder.
3. Select the Python interpreter from `.venv`.
4. Press `F5` and choose **Run TravelTrail Flask App**, or run `python app.py` from the integrated terminal.
5. Open `http://127.0.0.1:5000`.

## Deploy on Render
This repository contains a `render.yaml`, `Procfile`, runtime file and `/health` endpoint for a Render web-service deployment.

1. Create a GitHub repository and push this project to it.
2. Sign in to Render and choose **New → Blueprint**.
3. Connect the GitHub repository and select `render.yaml`.
4. Render installs `requirements.txt`, starts Gunicorn and exposes the public website URL.

Do not commit `.env` or MySQL passwords. Use the Render dashboard's environment-variable settings for production secrets.

## MySQL setup
1. Start MySQL Server and create a user if needed.
2. Run `mysql -u root -p < database.sql`.
3. The current prototype intentionally uses in-memory sample data so it works without MySQL. For production, replace the lists in `app.py` with MySQL queries using `mysql-connector-python`.

## Tech stack
HTML5, CSS3, JavaScript, Python Flask, MySQL and mysql-connector-python.
