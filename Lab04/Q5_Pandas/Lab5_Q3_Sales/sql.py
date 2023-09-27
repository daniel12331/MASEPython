import mysql.connector
import pandas as pd

def main():
    conn = mysql.connector.connect(
        host = "localhost",
        user="root",
        password="root",
        database="lab1"
    )

    query = "SELECT * FROM courses"
    df = pd.read_sql(query, conn)

    print(df)

if __name__ == '__main__':
    main()




