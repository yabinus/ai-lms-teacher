# import psycopg2

# conn = psycopg2.connect(
#     host="sokrates-db.cdfbx956wjyn.ap-southeast-1.rds.amazonaws.com",
#     port="5432",
#     database="sokrates_dev_student",
#     user="sokrates",
#     password="Pecan1-Harvest-Overfill-Morally-SoKr4t3S-190421"
# )

# cur = conn.cursor()
# cur.execute("SELECT * FROM student")
# rows = cur.fetchall()

# for row in rows:
#     print(row)

import psycopg2
import traceback
from psycopg2 import extensions as ext

class PostgreSQL:
    def __init__(self, database):
        self.database = database
        self.conn = None
    
    def get_connection(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    database= "sokrates_dev_student",
                    host="sokrates-db.cdfbx956wjyn.ap-southeast-1.rds.amazonaws.com",
                    port="5432",
                    user="sokrates",
                    password="Pecan1-Harvest-Overfill-Morally-SoKr4t3S-190421"
                )
                print("Database connected successfully!")            
            except psycopg2.DatabaseError:
                print("Unable to connect to the database.")
                
        return self.conn
    
    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            print("Database connection closed.")
            self.conn = None

