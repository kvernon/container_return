import os
import sqlite3

# May be helpful for initial env setup:
# You can suppress this print once you have it sorted out
print("Connecting to/creating challenge.db at:", os.getcwd())

DB_NAME = "challenge.db"
sqlite3.enable_callback_tracebacks(True)
db_connection = sqlite3.connect(DB_NAME,
                                check_same_thread=False,
                                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
db_connection.set_trace_callback(print)
