import numpy as np
import time
import random
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtGui

# Simulate data stream
def simulate_data_stream(duration=60, interval=0.5):
    """
    Simulates a real-time data stream for a given duration.

    Args:
    - duration (int): Duration for which the data stream runs (in seconds).
    - interval (float): Time interval between data points (in seconds).

    Yields:
    - data_point (float): A simulated data point that represents some metric.

    Raises:
    - ValueError: If duration or interval are not positive numbers.
    """
    if duration <= 0 or interval <= 0:
        raise ValueError("Duration and interval must be positive values.")

    start_time = time.time()
    while (time.time() - start_time) < duration:
        try:
            current_time = time.time() - start_time
            # Generate regular pattern using a sine wave
            regular_pattern = 10 * np.sin(0.2 * current_time)
            # Add seasonal variation
            seasonal_variation = 5 * np.sin(0.05 * current_time)
            # Add random noise to the pattern
            noise = random.uniform(-1, 1)
            # Calculate final data point
            data_point = regular_pattern + seasonal_variation + noise
            yield data_point
        except Exception as e:
            print(f"Error generating data point: {e}")
        # Simulate real-time data stream by waiting for the interval time
        time.sleep(interval)

# Moving Average and Z-score calculation
def moving_average(data, window_size):
    """
    Calculates the moving average over the last 'window_size' data points.

    Args:
    - data (list): List of data points.
    - window_size (int): The number of data points to consider for the average.

    Returns:
    - float: The calculated moving average.
    """
    try:
        return np.mean(data[-window_size:])
    except Exception as e:
        print(f"Error calculating moving average: {e}")
        return 0

def standard_deviation(data, window_size):
    """
    Calculates the standard deviation over the last 'window_size' data points.

    Args:
    - data (list): List of data points.
    - window_size (int): The number of data points to consider for standard deviation.

    Returns:
    - float: The calculated standard deviation.
    """
    try:
        return np.std(data[-window_size:])
    except Exception as e:
        print(f"Error calculating standard deviation: {e}")
        return 0

def z_score(data_point, mean, std_dev):
    """
    Calculates the Z-score of a data point.

    Args:
    - data_point (float): The data point to calculate the Z-score for.
    - mean (float): Mean of the data.
    - std_dev (float): Standard deviation of the data.

    Returns:
    - float: The calculated Z-score, or 0 if std_dev is zero.
    """
    try:
        return (data_point - mean) / std_dev if std_dev > 0 else 0
    except Exception as e:
        print(f"Error calculating Z-score: {e}")
        return 0

# Real-time anomaly detection and visualization with interactive tooltips
def detect_anomalies_with_visualization(data_stream, window_size=10, z_threshold=3):
    """
    Detects anomalies in a real-time data stream and visualizes the data.

    Args:
    - data_stream (generator): A generator that yields data points.
    - window_size (int): The number of data points to use for calculating the moving average and standard deviation.
    - z_threshold (float): Z-score threshold above which a data point is considered an anomaly.

    Raises:
    - ValueError: If window_size or z_threshold are not positive values.
    """
    if window_size <= 0 or z_threshold <= 0:
        raise ValueError("Window size and Z-score threshold must be positive values.")

    try:
        # Set up the PyQtGraph window
        app = QtWidgets.QApplication([])
        win = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        win.setLayout(layout)

        # Create plot and table widgets
        plot_widget = pg.GraphicsLayoutWidget()

        # Table for displaying all data points
        table_widget = QtWidgets.QTableWidget()
        table_widget.setColumnCount(3)
        table_widget.setHorizontalHeaderLabels(["Time", "Value", "Z-score"])
        table_widget.setColumnWidth(0, 60)
        table_widget.setColumnWidth(1, 80)
        table_widget.setColumnWidth(2, 80)

        # Table for displaying only anomalies
        anomaly_table_widget = QtWidgets.QTableWidget()
        anomaly_title = QtWidgets.QLabel("Anomalies Detected")
        anomaly_table_widget.setColumnCount(3)
        anomaly_table_widget.setHorizontalHeaderLabels(["Time", "Value", "Z-score"])
        anomaly_table_widget.setColumnWidth(0, 60)
        anomaly_table_widget.setColumnWidth(1, 80)
        anomaly_table_widget.setColumnWidth(2, 80)

        # Add widgets to the layout
        anomaly_table_layout = QtWidgets.QVBoxLayout()
        data_title = QtWidgets.QLabel("All Data Points")
        anomaly_table_layout.addWidget(anomaly_title)
        anomaly_table_layout.addWidget(anomaly_table_widget)
        layout.addLayout(anomaly_table_layout)

        layout.addWidget(plot_widget)
        data_table_layout = QtWidgets.QVBoxLayout()
        data_table_layout.addWidget(data_title)
        data_table_layout.addWidget(table_widget)
        layout.addLayout(data_table_layout)

        # Set up the plot
        plot = plot_widget.addPlot(title="Data Stream")
        curve = plot.plot(pen='b')  # Line for the data stream
        scatter = pg.ScatterPlotItem(pen='r', symbol='o', size=10)  # Points for anomalies
        plot.addItem(scatter)

        data_points = []
        time_points = []
        anomaly_points = []

        # Define the function to add data to the anomaly table
        def add_row_to_anomaly_table(time, value, z_score):
            """
            Adds an anomaly data point to the anomaly table.

            Args:
            - time (int): Time index of the anomaly.
            - value (float): Value of the anomaly.
            - z_score (float): Z-score of the anomaly.
            """
            row_position = anomaly_table_widget.rowCount()
            anomaly_table_widget.insertRow(row_position)

            # Add time, value, and Z-score to the table
            time_item = QtWidgets.QTableWidgetItem(str(time))
            value_item = QtWidgets.QTableWidgetItem(f"{value:.2f}")
            z_score_item = QtWidgets.QTableWidgetItem(f"{z_score:.2f}")

            anomaly_table_widget.setItem(row_position, 0, time_item)
            anomaly_table_widget.setItem(row_position, 1, value_item)
            anomaly_table_widget.setItem(row_position, 2, z_score_item)

        # Define the function to add data to the main table
        def add_row_to_table(time, value, z_score, is_anomaly):
            """
            Adds a data point to the main data table.

            Args:
            - time (int): Time index of the data point.
            - value (float): Value of the data point.
            - z_score (float): Z-score of the data point.
            - is_anomaly (bool): Indicates if the data point is an anomaly.
            """
            row_position = table_widget.rowCount()
            table_widget.insertRow(row_position)

            # Add time, value, and Z-score to the table
            time_item = QtWidgets.QTableWidgetItem(str(time))
            value_item = QtWidgets.QTableWidgetItem(f"{value:.2f}")
            z_score_item = QtWidgets.QTableWidgetItem(f"{z_score:.2f}" if z_score is not None else "N/A")

            table_widget.setItem(row_position, 0, time_item)
            table_widget.setItem(row_position, 1, value_item)
            table_widget.setItem(row_position, 2, z_score_item)

            # Highlight anomaly rows
            if is_anomaly:
                for item in [time_item, value_item, z_score_item]:
                    item.setBackground(QtGui.QColor(255, 0, 0, 100))

        # Update function to be called periodically
        def update():
            """
            Periodically fetches the next data point from the data stream, detects anomalies, and updates the UI.
            """
            try:
                data_point = next(data_stream)
            except StopIteration:
                timer.stop()
                return
            except Exception as e:
                print(f"Error fetching next data point: {e}")
                return

            frame = len(data_points)
            time_points.append(frame)
            data_points.append(data_point)

            if len(data_points) > window_size:
                try:
                    mean = moving_average(data_points, window_size)
                    std_dev = standard_deviation(data_points, window_size)
                    z = z_score(data_point, mean, std_dev)

                    if abs(z) > z_threshold:
                        # Anomaly detected, add to the anomaly list and update the UI
                        print(f"Anomaly detected: {data_point} (Z-score: {z:.2f})")
                        anomaly_points.append({
                            'pos': (frame, data_point),
                            'data': {'z_score': z, 'value': data_point, 'time': frame},
                            'brush': pg.mkBrush(255, 0, 0)
                        })
                        add_row_to_anomaly_table(frame, data_point, z)
                        add_row_to_table(frame, data_point, z, is_anomaly=True)
                    else:
                        # Normal data point, update the UI
                        print(f"Data: {data_point} (Z-score: {z:.2f})")
                        add_row_to_table(frame, data_point, z, is_anomaly=False)
                except Exception as e:
                    print(f"Error during anomaly detection: {e}")
            else:
                # Collecting data to calculate moving average and standard deviation
                print(f"Data: {data_point} (Collecting data...)")
                add_row_to_table(frame, data_point, None, is_anomaly=False)

            # Update plot data
            try:
                curve.setData(time_points, data_points)
                scatter.setData([pt['pos'][0] for pt in anomaly_points], [pt['pos'][1] for pt in anomaly_points])
                scatter.setData(pos=[pt['pos'] for pt in anomaly_points], data=[pt['data'] for pt in anomaly_points])
            except Exception as e:
                print(f"Error updating plot data: {e}")

        # Set up timer to call the update function periodically
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(100)  # Update every 100 milliseconds

        # Add click functionality to the scatter plot for displaying details about anomalies
        def on_click(plot_item, points):
            """
            Handles click events on anomaly points in the scatter plot.

            Args:
            - plot_item: The scatter plot item.
            - points (list): List of points clicked.
            """
            for point in points:
                point_data = point.data()
                if point_data is not None:
                    time_value = point_data['time']
                    # Print the information in the console
                    print(f"Clicked on point with Value: {point_data['value']}, Z-score: {point_data['z_score']:.2f}")

                    # Highlight corresponding row in the anomaly table
                    for row in range(anomaly_table_widget.rowCount()):
                        if int(anomaly_table_widget.item(row, 0).text()) == time_value:
                            anomaly_table_widget.selectRow(row)

        # Connect the click event to the on_click function
        scatter.sigClicked.connect(on_click)

        # Show the window
        win.resize(1200, 600)
        win.show()

        # Start the application
        app.exec_()

    except Exception as e:
        print(f"Error setting up the visualization: {e}")

# Example usage
if __name__ == "__main__":
    # Start data stream and detect anomalies
    stream = simulate_data_stream(duration=60, interval=0.5)
    detect_anomalies_with_visualization(stream, window_size=10, z_threshold=2)
