import sqlite3
from datetime import datetime


DATABASE = "database/traffic.db"


def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traffic_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            camera_id TEXT,
            vehicle_count INTEGER,
            congestion_level TEXT,
            timestamp TEXT
        )
    """)

    connection.commit()
    connection.close()


def insert_traffic_data(
    camera_id,
    vehicle_count,
    congestion_level
):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO traffic_data
        (
            camera_id,
            vehicle_count,
            congestion_level,
            timestamp
        )
        VALUES (?, ?, ?, ?)
    """, (
        camera_id,
        vehicle_count,
        congestion_level,
        timestamp
    ))

    connection.commit()
    connection.close()


def get_traffic_data():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            camera_id,
            vehicle_count,
            congestion_level,
            timestamp
        FROM traffic_data
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data


if __name__ == "__main__":

    create_database()

    print("Database created successfully.")