# Intelligent Traffic Congestion Detection

## Project ID
P_291

## Project Category
Embedded IoT / Smart City

## Project Title
Intelligent Traffic Congestion Detection

## Technologies Used

- Python
- OpenCV
- PyTorch
- YOLO11n
- MQTT
- Mosquitto
- SQLite
- Streamlit
- Pandas
- Plotly

## Project Description

This project detects vehicles from traffic video using computer vision and
determines the traffic congestion level based on the number of detected
vehicles.

The detected traffic information is published through MQTT and stored in
an SQLite database. A Streamlit dashboard provides real-time monitoring
and visualization of the collected traffic data.

## System Architecture

Traffic Video
      |
      v
OpenCV
      |
      v
YOLO11n Vehicle Detection
      |
      v
Vehicle Count
      |
      v
Congestion Detection
      |
      +------------------+
      |                  |
      v                  v
    MQTT              SQLite
      |                  |
      v                  v
Subscriber        Traffic Database
                         |
                         v
                 Streamlit Dashboard

## Vehicle Classes

The system detects:

- Car
- Motorcycle
- Bus
- Truck

## Congestion Levels

The current project uses the following vehicle-count thresholds:

- LOW: fewer than 10 vehicles
- MEDIUM: 10 to 24 vehicles
- HIGH: 25 or more vehicles

## MQTT Topic

traffic/congestion

## Camera ID

CAM_01

## Database

SQLite database:

database/traffic.db

## Dashboard

The Streamlit dashboard displays:

- Current vehicle count
- Current congestion level
- Camera ID
- Total traffic records
- Vehicle count over time
- Congestion distribution
- Average vehicle count
- Maximum vehicle count
- Minimum vehicle count
- High congestion events
- Recent traffic events
- CSV data export

## How to Run

### 1. Start Mosquitto

```powershell
& "C:\Program Files\Mosquitto\mosquitto.exe" -v