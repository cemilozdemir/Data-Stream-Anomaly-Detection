# Efficient Data Stream Anomaly Detection

## Demo Video

[Click here to watch the demo video](demoVideo.mov)

This video demonstrates the key features of the anomaly detection visualization, including real-time interactions.

## Features Demonstrated in the Video

1. **Real-Time Data Stream Visualization**:
   - Shows the data stream being plotted in real time with consistent updates.
2. **Anomaly Detection and Highlighting**:
   - Demonstrates how anomalies are detected and highlighted both on the graph and in the anomaly table.
3. **Interactive Graph**:
   - Allows the user to click on anomaly points to view detailed information and highlight corresponding entries in the anomaly table.
4. **Data Tables**:
   - Features two tables displaying all data points and anomalies detected, with real-time updates.
5. **Dynamic Updates**:
   - Data points are continuously plotted, with detected anomalies automatically highlighted to visualize unusual behavior.


## Project Overview
This project is part of the application process for the Graduate Software Engineer role at Cobblestone Energy. The goal of this project is to develop a Python script capable of detecting anomalies in a continuous data stream. This data stream simulates real-time sequences of floating-point numbers that could represent various metrics such as financial transactions or system performance metrics.

The primary focus of the project is on identifying unusual patterns, such as exceptionally high values or deviations from the expected norm, and effectively flagging these anomalies in real-time. This README provides an explanation of the chosen anomaly detection algorithm, its effectiveness, and how it meets the project requirements.

## Algorithm Explanation
### Algorithm Selection: Z-Score Method
For detecting anomalies in the data stream, the Z-score method was chosen as the primary approach. The Z-score is a statistical measure that indicates how many standard deviations a data point is from the mean of the data set. This method is effective for identifying outliers, as it quantifies the degree of deviation of a value from the normal distribution.

The Z-score is calculated as follows:

\[ Z = \frac{{(X - \mu)}}{{\sigma}} \]

Where:
- **X**: The current data point.
- **\(\mu\)**: The mean of the data points in the current window.
- **\(\sigma\)**: The standard deviation of the data points in the current window.

The Z-score method is particularly useful for detecting anomalies in real-time data streams where values that deviate significantly from the expected range are considered outliers.

### Why Z-Score?
- **Simplicity and Efficiency**: The Z-score calculation is computationally inexpensive and suitable for real-time scenarios. It involves simple arithmetic operations, making it efficient for real-time anomaly detection.
- **Adaptable to Concept Drift**: By maintaining a rolling window for calculating the mean and standard deviation, the Z-score method can adapt to gradual changes in the data (i.e., concept drift). This ensures that the detection process remains relevant even as the characteristics of the data change over time.
- **Effectiveness for Normally Distributed Data**: The Z-score method works well when the data follows a roughly normal distribution, making it suitable for identifying extreme deviations.

### Effectiveness of the Approach
The Z-score approach is effective in identifying anomalies that fall outside the normal range of expected values. By setting a threshold (e.g., Z-score > 3), we can flag data points that significantly deviate from the average behavior of the data stream.

However, it is important to note that while the Z-score is effective for detecting individual outliers, it may not perform well with highly skewed data distributions or when anomalies are subtle and hidden within complex patterns. In such cases, more advanced methods like machine learning-based anomaly detection or statistical models could be considered.

## Real-Time Visualization
In addition to detecting anomalies, the project includes a real-time visualization tool using PyQtGraph. This tool provides a graphical representation of the data stream, highlighting anomalies as they occur. The visualization includes:
- **Plot of the Data Stream**: Displays the real-time data stream as it is generated.
- **Anomaly Markers**: Anomalies are marked on the plot for easy identification.
- **Data Tables**: Two tables are displayed alongside the plot:
  - **All Data Points**: Shows all data points with their corresponding Z-scores.
  - **Anomalies Detected**: Lists only the data points that were flagged as anomalies.

## How to Run the Project
1. Install the required dependencies listed in the `requirements.txt` file.
2. Run the Python script to start the real-time data stream simulation and anomaly detection.

## Future Improvements
- **Advanced Anomaly Detection Algorithms**: Implement more sophisticated algorithms, such as Isolation Forest or LSTM-based models, to handle non-normal data distributions or subtle anomalies.
- **Scalability**: Optimize the current implementation to handle larger data volumes and faster data streams.

## Requirements
- Python 3.x
- NumPy
- PyQtGraph

Please refer to the `requirements.txt` file for detailed dependency information.




