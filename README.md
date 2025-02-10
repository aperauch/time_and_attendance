# Time and Attendance Tracking with Verkada Access Control

## Overview

This example Python script retrieves access events for an In/Out door used for employee time tracking from the Verkada Events REST API, processes the door access event data, and stores it in a MySQL database. It automates the collection of access logs from the previous day and ensures that the relevant database and table exist before inserting data.

## Features

- Authenticates with the Verkada API using an API key.
- Fetches access events from the previous 24-hour period.
- Extracts key attributes from the API response.
- Creates a MySQL database (`time_and_attendance_db`) and table (`access_events`) if they do not exist.
- Inserts relevant event data into the MySQL table.

## Prerequisites

- Python 3.x
- MySQL server
- Required Python libraries:
  - `requests`
  - `mysql-connector-python`

## Setup

1. Install dependencies:
   ```sh
   pip3 install requests mysql-connector-python
   ```
2. Update the script with your MySQL credentials:
   ```python
   db_config = {
       "host": "your_db_host",
       "user": "your_db_user",
       "password": "your_db_password"
   }
   ```
3. Replace `verkada_rest_api_key` with your actual Verkada API key in the script.

## Usage

Run the script:

```sh
python3 get_access_events_for_time_and_attendance.py
```

## Database Schema

The script creates the following MySQL table if it does not exist:

```sql
CREATE TABLE access_events (
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
```

## Notes

- Ensure that the MySQL server is running before executing the script.
- The script skips events without a `direction` attribute.
- The `timestamp` field is converted to a MySQL `DATETIME` format.

## Troubleshooting

- **API Request Failure:** Ensure the API key is valid and that the Verkada API is accessible.

## License

This script is provided as-is without any warranty. Modify and use it as needed for your purposes.

