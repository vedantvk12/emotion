"""Unit tests for the Emotion Detection application."""
import unittest
from unittest.mock import patch
from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """Test suite for emotion_detector function."""

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_emotion_detector_joy(self, mock_post):
        """Test joy emotion detection for glad statement."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = '''{
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.005,
                    "disgust": 0.002,
                    "fear": 0.003,
                    "joy": 0.95,
                    "sadness": 0.04
                }
            }]
        }'''
        result = emotion_detector("I am glad this happened")
        self.assertEqual(result['dominant_emotion'], 'joy')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_emotion_detector_anger(self, mock_post):
        """Test anger emotion detection for mad statement."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = '''{
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.92,
                    "disgust": 0.02,
                    "fear": 0.03,
                    "joy": 0.01,
                    "sadness": 0.02
                }
            }]
        }'''
        result = emotion_detector("I am really mad about this")
        self.assertEqual(result['dominant_emotion'], 'anger')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_emotion_detector_disgust(self, mock_post):
        """Test disgust emotion detection for disgusted statement."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = '''{
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.05,
                    "disgust": 0.88,
                    "fear": 0.02,
                    "joy": 0.01,
                    "sadness": 0.04
                }
            }]
        }'''
        result = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result['dominant_emotion'], 'disgust')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_emotion_detector_sadness(self, mock_post):
        """Test sadness emotion detection for sad statement."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = '''{
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.02,
                    "disgust": 0.01,
                    "fear": 0.03,
                    "joy": 0.01,
                    "sadness": 0.93
                }
            }]
        }'''
        result = emotion_detector("I am so sad about this")
        self.assertEqual(result['dominant_emotion'], 'sadness')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_emotion_detector_fear(self, mock_post):
        """Test fear emotion detection for afraid statement."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = '''{
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.02,
                    "disgust": 0.01,
                    "fear": 0.91,
                    "joy": 0.02,
                    "sadness": 0.04
                }
            }]
        }'''
        result = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result['dominant_emotion'], 'fear')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_emotion_detector_invalid_input(self, mock_post):
        """Test emotion detection with invalid/empty input returning 400."""
        mock_post.return_value.status_code = 400
        result = emotion_detector("")
        self.assertIsNone(result['dominant_emotion'])
        self.assertIsNone(result['anger'])
        self.assertIsNone(result['disgust'])
        self.assertIsNone(result['fear'])
        self.assertIsNone(result['joy'])
        self.assertIsNone(result['sadness'])


if __name__ == '__main__':
    unittest.main()
