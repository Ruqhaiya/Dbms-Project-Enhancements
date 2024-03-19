import pymysql
import decimal
from pymongo import MongoClient

mysql_conn = pymysql.connect(host='CSSQL', user='mm_team02_02', password='mm_team02_02Pass-', database='mm_team02_02')
mysql_cursor = mysql_conn.cursor()

mongo_client = MongoClient('localhost', 27017)
mongo_db = mongo_client['mm_team02_02']

def convert_row_data(row, cursor_description):
    data = {}
    for i, field in enumerate(cursor_description):
        if isinstance(row[i], decimal.Decimal):
            # Convert Decimal to float or string (as per your precision requirement)
            data[field[0]] = float(row[i])  # or str(row[i])
        else:
            data[field[0]] = row[i]
    return data

# Getting all table names from MySQL database
mysql_cursor.execute("SHOW TABLES")
tables = [table[0] for table in mysql_cursor.fetchall()]
for table_name in tables:
    mysql_cursor.execute(f"SELECT * FROM `{table_name}`")
    rows = mysql_cursor.fetchall()
    
    # Defining the collection name in MongoDB
    mongo_collection = mongo_db[table_name]
    
    # Drop the collection if it exists
    mongo_collection.drop()

    # Inserting data into MongoDB
    for row in rows:
        data = convert_row_data(row, mysql_cursor.description)
        mongo_collection.insert_one(data)

mysql_cursor.close()
mysql_conn.close()
mongo_client.close()
