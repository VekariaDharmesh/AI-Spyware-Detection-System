import sqlite3
import json
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path='universal_device_manager.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create scan_logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scan_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                threats_count INTEGER DEFAULT 0,
                details TEXT
            )
        ''')
        
        # Create system_metrics table (optional, for historical data)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu_percent REAL,
                memory_percent REAL,
                disk_percent REAL
            )
        ''')
        
        conn.commit()
        conn.close()

    def add_scan_log(self, threats_count, details):
        """Add a new scan log entry."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        if isinstance(details, (dict, list)):
            details = json.dumps(details)
            
        cursor.execute('''
            INSERT INTO scan_logs (timestamp, threats_count, details)
            VALUES (?, ?, ?)
        ''', (timestamp, threats_count, details))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid

    def get_scan_logs(self, limit=50):
        """Retrieve recent scan logs."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM scan_logs 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def log_metrics(self, cpu, memory, disk):
        """Log system metrics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO system_metrics (timestamp, cpu_percent, memory_percent, disk_percent)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, cpu, memory, disk))
        
        conn.commit()
        conn.close()
