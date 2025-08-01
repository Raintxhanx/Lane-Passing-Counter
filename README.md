# Lane Passing Counter

## Overview
The Lane Passing Counter is a Python application designed to count individuals passing through a defined line using object detection techniques. It utilizes the YOLOv5 model for real-time detection and provides a user-friendly interface for monitoring and logging events.

## Features
- Real-time counting of individuals passing through a designated line.
- Utilizes YOLOv5 for accurate object detection.
- Logs counting events to a SQLite database.
- Visual representation of detected objects and counting line.

## Project Structure
```
lane-passing-counter
├── src
│   ├── main.py          # Entry point of the application
│   ├── counter.py       # Logic for counting individuals
│   ├── utils.py         # Utility functions for model and drawing
├── tests
│   └── test_counter.py   # Unit tests for the counter functionality
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd lane-passing-counter
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Download the YOLOv5 model:
   - Place the `yolov5s.pt` model file in the `models` directory.

## Usage
To start the lane passing counter, run the following command:
```
python src/main.py
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.