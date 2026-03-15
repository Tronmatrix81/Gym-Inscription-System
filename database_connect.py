import sqlite3
import os

def connect_database():
    # Takes the actual path to the database
    actualPath=os.path.dirname(os.path.abspath(__file__))

    # Add the database name to the path
    actualPath1=os.path.join(actualPath, "gimansio.db")

    # Connects to the database
    return sqlite3.connect(actualPath1)