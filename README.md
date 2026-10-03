# IBM Emotion Detection Application

A web-based Emotion Detection application built using Python, Flask, and IBM Watson NLP. The application analyzes text for five core emotions (anger, disgust, fear, joy, and sadness) and identifies the dominant emotion.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Requirements & Installation](#requirements--installation)
- [Usage](#usage)
  - [Using the Python Module](#using-the-python-module)
  - [Running the Flask Web Application](#running-the-flask-web-application)
- [Unit Testing](#unit-testing)
- [Static Code Analysis](#static-code-analysis)
- [API Reference & Error Handling](#api-reference--error-handling)

---

## Project Overview

This project implements a web-based emotion detection solution using IBM Watson's Natural Language Processing (NLP) EmotionPredict service (`emotion_aggregated-workflow_lang_en_stock`).

Given a user-submitted text string, the application:
1. Calls the Watson NLP EmotionPredict API.
2. Extracts confidence scores for **anger**, **disgust**, **fear**, **joy**, and **sadness**.
3. Determines the **dominant_emotion** (the emotion with the highest score).
4. Handles empty or invalid inputs gracefully by returning `None` values and appropriate HTTP 400 responses.

---

## Project Structure

```text
EmotionDetectionProject/
│
├── EmotionDetection/
│   ├── __init__.py           # Package initialization exposing emotion_detector
│   └── emotion_detection.py  # Watson NLP Emotion detection logic
│
├── templates/
│   └── index.html            # Web interface UI
│
├── static/
│   └── mywebscript.js        # Client-side AJAX script for emotion detection
│
├── test_emotion_detection.py # Unit tests covering all 5 emotions and error cases
├── server.py                 # Flask server implementation
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## Requirements & Installation

### Prerequisites
- Python 3.8+
- `pip` (Python package manager)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vedantvk12/emotion.git
   cd emotion
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Using the Python Module

You can import and use `emotion_detector` directly in Python:

```python
from EmotionDetection.emotion_detection import emotion_detector

response = emotion_detector("I am glad this happened")
print(response)
```

**Output:**
```python
{
    'anger': 0.005,
    'disgust': 0.002,
    'fear': 0.003,
    'joy': 0.95,
    'sadness': 0.04,
    'dominant_emotion': 'joy'
}
```

### Running the Flask Web Application

1. **Start the Flask server:**
   ```bash
   python server.py
   ```

2. **Access the web application:**
   - Open your web browser and navigate to `http://localhost:5000/`.
   - Enter text into the textarea and click **Run Emotion Detection**.

3. **Direct Endpoint Testing:**
   - **Valid Text:**
     `http://localhost:5000/emotionDetector?textToAnalyze=I%20am%20happy`
     
     **Response (HTTP 200):**
     ```text
     For the given statement, the system response is 'anger': 0.005, 'disgust': 0.002, 'fear': 0.003, 'joy': 0.95 and 'sadness': 0.04. The dominant emotion is joy.
     ```

   - **Blank / Invalid Text:**
     `http://localhost:5000/emotionDetector?textToAnalyze=`
     
     **Response (HTTP 400):**
     ```text
     Invalid text! Please try again!
     ```

---

## Unit Testing

Run the unit tests covering all 5 emotions (`joy`, `anger`, `disgust`, `sadness`, `fear`) and invalid input handling:

```bash
python -m unittest test_emotion_detection.py -v
```

Or run test discovery:

```bash
python -m unittest discover
```

All tests execute with mock Watson NLP responses to ensure deterministic, offline execution.

---

## Static Code Analysis

Check compliance with PEP 8 and clean coding standards using `pylint`:

```bash
pylint server.py
pylint EmotionDetection/emotion_detection.py
```

Target Score: **10.00/10**

---

## API Reference & Error Handling

| Endpoint | Method | Parameter | Description |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | None | Renders `templates/index.html` |
| `/emotionDetector` | `GET` | `textToAnalyze` | Analyzes text and returns formatted emotion response |

### Error Behavior
- When `textToAnalyze` is blank, empty, or Watson returns status code 400, `emotion_detector` returns `None` for all emotion scores and `dominant_emotion`.
- The Flask endpoint detects blank input or `dominant_emotion is None` and responds with HTTP status 400 and message `"Invalid text! Please try again!"`.
