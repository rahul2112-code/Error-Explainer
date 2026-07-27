# Error Explainer

A "Friendly Compiler" web application designed to help beginners understand programming errors better. The application takes C or Java source code, compiles it using standard compilers (`gcc` or `javac`), and translates cryptic compiler error messages into beginner-friendly, human-readable explanations.

## Features

- **Multi-language Support:** Currently supports C and Java.
- **Friendly Translations:** Uses pattern matching to replace technical jargon with simple, actionable advice.
- **Confidence Tracking:** Learns from user feedback to improve error translations over time.
- **Interactive UI:** A simple and clean web interface to write, compile, and debug code directly in the browser.

## Setup Guide

Follow these steps to run the Error Explainer locally on your machine.

### Prerequisites

You will need the following installed on your system:
- **Python 3.x**
- **GCC** (for compiling C code)
- **Java Development Kit (JDK)** (for compiling Java code)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rahul2112-code/Error-Explainer.git
   cd Error-Explainer
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```

4. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Ensure your virtual environment is active.
2. Start the Flask server:
   ```bash
   python app.py
   ```
3. Open your web browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Project Structure

- `app.py`: The main Flask application handling web routes.
- `friendlyCompiler.py`: The core script that compiles C code and parses GCC errors.
- `java_compiler/`: Contains the Java equivalent (`friendlyJavaCompiler.py`) and Java error patterns.
- `error_patterns.json`: The database of regular expressions used to map C errors to friendly explanations.
- `templates/` & `static/`: HTML frontend and associated CSS/JS files.
