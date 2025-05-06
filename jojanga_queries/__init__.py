import os
import sqlite3

# May be helpful for initial env setup:
# You can suppress this print once you have it sorted out
print("Connecting to/creating challenge.db at:", os.getcwd())

DB_NAME = "challenge.db"
db_connection = sqlite3.connect(DB_NAME)
