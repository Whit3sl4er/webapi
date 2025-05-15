import hashlib
import base64
from pydantic import BaseModel
import os
from fastapi import APIRouter, HTTPException, status
from db import get_connection

router = APIRouter()

# ===== Pydantic-модели =====
class RegisterData(BaseModel):
    login: str
    password: str
    email: str

class LoginData(BaseModel):
    login: str
    password: str

@router.get("/")
async def root():
    print("Проверка маршрута")
    return {"status": "API работает"}

@router.get("/users")
async def get_users():
    try:
        print("Проверка users")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT UserID, UserLogin, UserPassword, UserEmail FROM Users")
            rows = cursor.fetchall()
            users = [{"id": row[0], "login": row[1], "password":row[2], "email": row[3]} for row in rows]
            return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/Subscriptions")
async def get_subscriptions():
    try:
        print("Проверка subscriptions")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SubscriptionID, UserID, StartDate, EndDate, CreatedAt FROM Subscriptions")
            rows = cursor.fetchall()
            subscriptions = [
                {
                    "id": row[0],
                    "user_id": row[1],
                    "start_date": row[2],
                    "end_date": row[3],
                    "CreatedAt": row[4]
                }
                for row in rows
            ]
            return {"subscriptions": subscriptions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Функция регистрации
@router.post("/register")
async def register_user(data: RegisterData):
    # Подключаемся к БД
    with get_connection() as conn:
        cursor = conn.cursor()
        hashed_password = hash_password(data.password)

        # Сохраняем нового пользователя в базе данных
        cursor.execute("INSERT INTO Users (UserLogin, UserPassword, UserEmail) VALUES (?, ?, ?)",
                       (data.login, hashed_password, data.email))
        conn.commit()
    print(f"Пользователь: login - {data.login}, password - {data.password}, email - {data.email} был зарегистрирован")
    return {"message": "User registered successfully"}

# Функция авторизации
@router.post("/logIn")
async def logIn_user(data: LoginData):
    # Подключаемся к БД
    with get_connection() as conn:
        cursor = conn.cursor()

        # Ищем пользователя по логину
        cursor.execute("SELECT UserPassword FROM Users WHERE UserLogin = ?", (data.login,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="User not found")

        stored_hash = row[0]

        # Проверяем, совпадает ли введённый пароль с хэшом из базы данных
        if verify_password(data.password, stored_hash):
            print(f"Пользователь: login - {data.login}, password - {data.password} был авторизован")
            return {"valid": True}
        else:
            print(f"Пользователь: login - {data.login}, password - {data.password} не был авторизован. Неправильный пароль")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

# Хэширование пароля
def hash_password(password: str) -> str:
    iterations = 100000
    salt = os.urandom(16)
    pbkdf2 = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations, dklen=32)
    hashed_password = f"{iterations}:{base64.b64encode(salt).decode()}:{base64.b64encode(pbkdf2).decode()}"
    return hashed_password

# Проверка пароля
def verify_password(password: str, stored_hash: str) -> bool:
    iterations, salt_b64, hash_b64 = stored_hash.split(":")
    salt = base64.b64decode(salt_b64)
    original_hash = base64.b64decode(hash_b64)
    iterations = int(iterations)
    pbkdf2 = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations, dklen=32)
    return pbkdf2 == original_hash