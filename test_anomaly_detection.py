import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import random
from main import simulate_data_stream, moving_average, standard_deviation, z_score

class TestAnomalyDetection(unittest.TestCase):
    def test_simulate_data_stream(self):
        # Test that the simulate_data_stream function returns a generator with expected number of data points
        duration = 5
        interval = 1
        generator = simulate_data_stream(duration=duration, interval=interval)
        data_points = list(generator)
        expected_length = duration // interval
        self.assertEqual(len(data_points), expected_length, "The number of data points generated is incorrect.")

        # Test that the data points are floats
        for data_point in data_points:
            self.assertIsInstance(data_point, float, "Data points should be of type float.")

    def test_moving_average(self):
        # Test that the moving average function calculates the correct average
        data = [1, 2, 3, 4, 5]
        window_size = 3
        result = moving_average(data, window_size)
        expected_average = np.mean(data[-window_size:])
        self.assertAlmostEqual(result, expected_average, "The calculated moving average is incorrect.")

    def test_standard_deviation(self):
        # Test that the standard deviation function calculates the correct value
        data = [1, 2, 3, 4, 5]
        window_size = 3
        result = standard_deviation(data, window_size)
        expected_std_dev = np.std(data[-window_size:])
        self.assertAlmostEqual(result, expected_std_dev, "The calculated standard deviation is incorrect.")

    def test_z_score(self):
        # Test that the Z-score calculation is correct
        data_point = 10
        mean = 5
        std_dev = 2
        result = z_score(data_point, mean, std_dev)
        expected_z_score = (data_point - mean) / std_dev
        self.assertAlmostEqual(result, expected_z_score, "The calculated Z-score is incorrect.")

        # Test for zero standard deviation
        result = z_score(data_point, mean, 0)
        self.assertEqual(result, 0, "Z-score should be zero when standard deviation is zero.")

if __name__ == '__main__':
    unittest.main()
