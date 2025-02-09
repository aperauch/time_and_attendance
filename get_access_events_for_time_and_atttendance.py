import requests
import datetime
import mysql.connector

# Step 1:  Get token from secret api key.
api_key = "verkada_rest_api_key"
region = "api" # US Region
get_token_from_key_api = f"https://{region}.verkada.com/token"
headers = {
    "accept": "application/json",
    "x-api-key": f"{api_key}"
}
response = requests.post(get_token_from_key_api, headers=headers)
token = response.json()["token"]

# Step 2:  Calculate start and end time in linux epoch timestamp format of the 24-hour period of the previous day.
yesterday = datetime.datetime.utcnow() - datetime.timedelta(days=1)
start_time = int(datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0).timestamp())
end_time = int(datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59).timestamp())

# Step 3:  Get all access events of previous day from API.  
device_id = "9e1d5805-86b8-4572-8bf7-fd176a270ac8"
page_size = 200

get_access_events_api_url = f"https://{region}.verkada.com/events/v1/access?start_time={start_time}&end_time={end_time}&page_size={page_size}&device_id={device_id}"

headers_with_token = {
    "accept": "application/json",
    "x-verkada-auth": f"{token}"
}

access_events_response = requests.get(get_access_events_api_url, headers=headers_with_token)

# Step 4:  Convert the JSON of the response body to a list of event objects.
access_events = access_events_response.json().get("events", [])

# Step 5:  Create database and MySQL table if they don't exist.
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "password"
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS time_and_attendance_db;")
cursor.execute("USE time_and_attendance_db;")

create_table_query = """
CREATE TABLE IF NOT EXISTS access_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    accepted BOOLEAN,
    buildingName VARCHAR(255),
    direction VARCHAR(50),
    accessControllerName VARCHAR(255),
    entityName VARCHAR(255),
    eventType VARCHAR(100),
    event_type VARCHAR(100),
    floorName VARCHAR(255),
    inputValue VARCHAR(255),
    userName VARCHAR(255),
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50)
);
"""
cursor.execute(create_table_query)
conn.commit()

# Step 6:  Insert event data into MySQL database.
insert_query = """
INSERT INTO access_events (timestamp, accepted, buildingName, direction, accessControllerName, entityName, eventType, event_type, floorName, inputValue, userName, firstName, lastName, email, phone)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for event in access_events:
    event_info = event.get("event_info", {})
    user_info = event_info.get("userInfo", {})
    
    if not event_info.get("direction"):
        continue
    
    timestamp_dt = datetime.datetime.strptime(event.get("timestamp"), "%Y-%m-%dT%H:%M:%SZ") if event.get("timestamp") else None
    
    data = (
        timestamp_dt,
        event_info.get("accepted"),
        event_info.get("buildingName"),
        event_info.get("direction"),
        event_info.get("doorInfo", {}).get("accessControllerName"),
        event_info.get("entityName"),
        event_info.get("eventType"),
        event.get("event_type"),
        event_info.get("floorName"),
        event_info.get("inputValue"),
        event_info.get("userName"),
        user_info.get("firstName"),
        user_info.get("lastName"),
        user_info.get("email"),
        user_info.get("phone")
    )
    cursor.execute(insert_query, data)

conn.commit()
cursor.close()
conn.close()
