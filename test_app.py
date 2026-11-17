"""
Automated unit tests for Weather App calculation, unit conversions, and JSON parsing.
Run with: python -m unittest test_app.py
"""

import json
import os
import unittest
from utils import c_to_f, get_weather_description, kmh_to_mph


class TestWeatherUtilities(unittest.TestCase):
    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(c_to_f(0), 32.0)
        self.assertAlmostEqual(c_to_f(100), 212.0)
        self.assertAlmostEqual(c_to_f(-40), -40.0)
        self.assertAlmostEqual(c_to_f(25), 77.0)

    def test_kmh_to_mph(self):
        self.assertAlmostEqual(kmh_to_mph(100), 62.1371, places=3)
        self.assertAlmostEqual(kmh_to_mph(0), 0.0)

    def test_weather_description_mapping(self):
        desc_0, icon_0 = get_weather_description(0)
        self.assertEqual(desc_0, "Clear Sky")
        self.assertEqual(icon_0, "☀️")

        desc_61, icon_61 = get_weather_description(61)
        self.assertEqual(desc_61, "Slight Rain")

        # Unknown code should return fallback without crashing
        desc_unknown, _ = get_weather_description(9999)
        self.assertIn("Variable", desc_unknown)


class TestWeatherDataParsing(unittest.TestCase):
    def test_sample_json_structure(self):
        json_path = os.path.join(os.path.dirname(__file__), "sample_weather.json")
        self.assertTrue(os.path.exists(json_path), "sample_weather.json must exist")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check required fields
        required_keys = [
            "city", "country", "temp_c", "temp_f", "feels_like_c",
            "humidity", "wind_speed_kmh", "pressure_hpa", "condition", "forecast"
        ]
        for key in required_keys:
            self.assertIn(key, data, f"Missing required key: {key}")

        # Check forecast list
        self.assertIsInstance(data["forecast"], list)
        if data["forecast"]:
            day = data["forecast"][0]
            self.assertIn("date", day)
            self.assertIn("temp_max_c", day)
            self.assertIn("temp_min_c", day)


if __name__ == "__main__":
    unittest.main()
