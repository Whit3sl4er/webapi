from db import get_connection
from datetime import datetime

def register_user(login, password, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Users (UserLogin, UserPassword, UserEmail)
        VALUES (?, ?, ?)
    """, (login, password, email))
    conn.commit()
    conn.close()

def get_user_by_login(login):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT UserID, UserPassword FROM Users WHERE UserLogin = ?
    """, (login,))
    result = cursor.fetchone()
    conn.close()
    return result

def is_subscription_active(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1 FROM Subscription
        WHERE UserID = ?
        AND StartDate <= ?
        AND EndDate >= ?
    """, (user_id, datetime.utcnow(), datetime.utcnow()))
    result = cursor.fetchone()
    conn.close()
    return result is not None
