import sqlite3

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.database_file = "database.db"

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.database_file)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("[CONNECTION ERROR!] ", e)

    def close(self):
        try:
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print("[CLOSE CONNECTION ERROR!] ", e)

    def ask_only(self, sql):
        try:
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records
        except Exception as e:
            print("[SQL ASK ERROR!] ", e)
    
    def ask(self, sql):
        self.connect()
        data = self.ask_only(sql)
        self.close()
        return data


    def valid_stream_key(self, stream_key):
        # makes sure the stream key is accually exist and if he is not already streaming
        if stream_key.count('-') != 4 or len(stream_key) != 36:
            # invalid key, probably sql injection! 
            return
        data = self.ask(f"SELECT * FROM Streamers WHERE StreamKey='{stream_key}';")
        return data != [] and data[0][2] == "False"

    def get_username_by_streamkey(self, stream_key):
        return self.ask(f"SELECT Username FROM Streamers WHERE StreamKey='{stream_key}';")[0][0]
    
    def start_live(self, username):
        self.ask(f"UPDATE Streamers SET IsLive='True' WHERE Username='{username}';")
    
    def stop_live(self, username):
        self.ask(f"UPDATE Streamers SET IsLive='False' WHERE Username='{username}';")