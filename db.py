import os
import psycopg2
from psycopg2 import sql

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def create_tables():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    UserID SERIAL PRIMARY KEY,
                    UserLogin VARCHAR(50) NOT NULL,
                    UserPassword VARCHAR(255) NOT NULL,
                    UserEmail VARCHAR(100)
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS Subscriptions (
                    SubscriptionID SERIAL PRIMARY KEY,
                    UserID INTEGER REFERENCES Users(UserID),
                    StartDate DATE,
                    EndDate DATE,
                    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

        conn.commit()
        print("Таблицы успешно созданы.")
