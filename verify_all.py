"""Verification script for all project requirements."""
import json
import unittest
from unittest.mock import patch
from server import app
from EmotionDetection.emotion_detection import emotion_detector
from test_emotion_detection import TestEmotionDetection


def run_verification():
    """Run all verification steps."""
    print("=" * 60)
    print("STEP 1: RUNNING UNIT TESTS")
    print("=" * 60)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEmotionDetection)
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    assert test_result.wasSuccessful(), "Unit tests failed!"
    print("\n[PASSED] Unit tests passed successfully.")

    print("\n" + "=" * 60)
    print("STEP 2: TESTING emotion_detector DIRECTLY")
    print("=" * 60)
    with patch('EmotionDetection.emotion_detection.requests.post') as mock_post:
        # Joy / Happy test
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = json.dumps({
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.005,
                    "disgust": 0.002,
                    "fear": 0.003,
                    "joy": 0.95,
                    "sadness": 0.04
                }
            }]
        })
        happy_result = emotion_detector("I am glad this happened")
        print("Happy input result:\n", json.dumps(happy_result, indent=2))
        assert happy_result['dominant_emotion'] == 'joy'

        # Anger test
        mock_post.return_value.text = json.dumps({
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.92,
                    "disgust": 0.02,
                    "fear": 0.03,
                    "joy": 0.01,
                    "sadness": 0.02
                }
            }]
        })
        anger_result = emotion_detector("I am really mad about this")
        print("Anger input result:\n", json.dumps(anger_result, indent=2))
        assert anger_result['dominant_emotion'] == 'anger'

        # Disgust test
        mock_post.return_value.text = json.dumps({
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.05,
                    "disgust": 0.88,
                    "fear": 0.02,
                    "joy": 0.01,
                    "sadness": 0.04
                }
            }]
        })
        disgust_result = emotion_detector("I feel disgusted just hearing about this")
        print("Disgust input result:\n", json.dumps(disgust_result, indent=2))
        assert disgust_result['dominant_emotion'] == 'disgust'

        # Blank input (Watson 400 status)
        mock_post.return_value.status_code = 400
        blank_result = emotion_detector("")
        print("Blank input (status 400) result:\n", json.dumps(blank_result, indent=2))
        assert blank_result['dominant_emotion'] is None

    print("[PASSED] Direct function executions verified.")

    print("\n" + "=" * 60)
    print("STEP 3: TESTING FLASK SERVER ENDPOINTS")
    print("=" * 60)
    client = app.test_client()

    # Test GET /
    home_response = client.get('/')
    print("GET / -> Status:", home_response.status_code)
    assert home_response.status_code == 200
    assert "Emotion Detection Application" in home_response.data.decode()
    print("[PASSED] GET / renders index.html properly.")

    # Test GET /emotionDetector?textToAnalyze=I%20am%20happy
    with patch('EmotionDetection.emotion_detection.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = json.dumps({
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.005,
                    "disgust": 0.002,
                    "fear": 0.003,
                    "joy": 0.95,
                    "sadness": 0.04
                }
            }]
        })
        valid_response = client.get('/emotionDetector?textToAnalyze=I%20am%20happy')
        print("\nGET /emotionDetector?textToAnalyze=I%20am%20happy -> Status:", valid_response.status_code)
        print("Response body:\n", valid_response.data.decode())
        assert valid_response.status_code == 200
        assert "'joy': 0.95" in valid_response.data.decode()
        assert "The dominant emotion is joy." in valid_response.data.decode()
        print("[PASSED] GET /emotionDetector returned properly formatted emotion response.")

    # Test GET /emotionDetector with blank input
    blank_response_1 = client.get('/emotionDetector?textToAnalyze=')
    print("\nGET /emotionDetector?textToAnalyze= -> Status:", blank_response_1.status_code)
    print("Response body:", blank_response_1.data.decode())
    assert blank_response_1.status_code == 400
    assert blank_response_1.data.decode() == "Invalid text! Please try again!"

    blank_response_2 = client.get('/emotionDetector')
    print("\nGET /emotionDetector (no query param) -> Status:", blank_response_2.status_code)
    print("Response body:", blank_response_2.data.decode())
    assert blank_response_2.status_code == 400
    assert blank_response_2.data.decode() == "Invalid text! Please try again!"
    print("[PASSED] Blank inputs return HTTP 400 with 'Invalid text! Please try again!'.")

    print("\n" + "=" * 60)
    print("ALL VERIFICATIONS COMPLETED AND SUCCESSFUL!")
    print("=" * 60)


if __name__ == '__main__':
    run_verification()
