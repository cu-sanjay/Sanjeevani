# Sanjeevani

## Overview
**Sanjeevani** is a Python web application built around a **Flask**-based architecture. The application’s entry point is `main.py`, which creates the web app via `create_app()` and (when executed directly) runs a server listening on **all network interfaces** at **port 5000** with **debug mode enabled**.

The project uses common Flask ecosystem components to support HTTP routing, database integration, data handling, and production deployment.

---

## Key Features
- **Flask web application entry point**
  - `main.py` bootstraps the app using `create_app()`.
  - Runs on `0.0.0.0:5000` with `debug=True` when started directly.
- **Database integration**
  - Uses **Flask-SQLAlchemy** for ORM/database integration.
- **Data processing capabilities**
  - Uses **pandas** for data manipulation and analysis.
- **External HTTP/network interactions**
  - Uses **requests** for making outbound API/network calls.
- **Production-ready deployment**
  - Uses **gunicorn** as a WSGI server.

---

## Tech Stack
- **Python**
- **Flask** — web framework
- **Flask-SQLAlchemy** — ORM/database integration for Flask
- **gunicorn** — production WSGI server
- **pandas** — data manipulation/analysis
- **requests** — HTTP client for external calls

---

## Project Architecture
Based on the provided repository summaries, the architecture is organized around a Flask application factory pattern:

1. **`main.py` (Application entry point)**
   - Imports/uses `create_app()` to construct the Flask application instance.
   - When executed as the main module:
     - Starts the server on **host `0.0.0.0`**
     - Uses **port `5000`**
     - Enables **debug mode**

2. **`create_app()` (Flask app factory)**
   - While its implementation is not shown in the summaries, it is referenced by `main.py` and is responsible for configuring and returning the Flask application object.

3. **Dependencies (`requirements.txt`)**
   - Defines the runtime and deployment dependencies:
     - Flask, Flask-SQLAlchemy, gunicorn, pandas, requests

---

## Installation (Placeholder)
> **Note:** Exact steps may vary depending on how this repo is structured beyond the summarized files.

1. Clone the repository:
   bash
   git clone <REPO_URL>
   cd Sanjeevani
   
2. Create and activate a virtual environment (recommended):
   bash
   python -m venv .venv
   # Linux/macOS
   source .venv/bin/activate
   # Windows
   .venv\Scripts\activate
   
3. Install dependencies:
   bash
   pip install -r requirements.txt
   

---

## Usage (Placeholder)
### Development (run via `main.py`)
bash
python main.py

- The server listens on **0.0.0.0:5000**
- **Debug mode** is enabled (as described in `main.py`)

### Production (run with gunicorn)
> Use gunicorn for production deployments (aligned with the dependencies listed).
bash
gunicorn <app_module>:<app_object> --bind 0.0.0.0:5000

- Replace `<app_module>` and `<app_object>` with the correct module/object names used by `create_app()` in your codebase.

---

## Notes for Developers
- The application is designed around an **application factory** (`create_app()`), which typically improves testability and configuration management.
- If you extend the app, ensure any new routes, database models, or integrations follow the same Flask/Flask-SQLAlchemy patterns already implied by the dependency choices.

---
*This README was generated with [PresentMe](https://www.presentmeapp.xyz/). View the full presentation [here](https://www.presentmeapp.xyz/p/fef8c457-dfb9-4abc-b972-281dfed2a058).*
