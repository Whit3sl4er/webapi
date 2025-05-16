import models
from db import get_connection
import other_functions
from fastapi import HTTPException, status

async def register_user(data: models.RegisterData):
    # Подключаемся к БД
    with get_connection() as conn:
        cursor = conn.cursor()
        hashed_password = other_functions.hash_password(data.password)

        # Сохраняем нового пользователя в базе данных
        cursor.execute("INSERT INTO Users (UserLogin, UserPassword, UserEmail) VALUES (%s, %s, %s)",
                       (data.login, hashed_password, data.email))
        conn.commit()
    print(f"Пользователь: login - {data.login}, password - {data.password}, email - {data.email} был зарегистрирован")
    return {"message": "User registered successfully"}

async def logIn_user(data: models.LoginData):
    # Подключаемся к БД
    with get_connection() as conn:
        cursor = conn.cursor()

        # Ищем пользователя по логину
        cursor.execute("SELECT UserPassword FROM Users WHERE UserLogin = %s", (data.login,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="User not found")

        stored_hash = row[0]

        # Проверяем, совпадает ли введённый пароль с хэшом из базы данных
        if other_functions.verify_password(data.password, stored_hash):
            print(f"Пользователь: login - {data.login}, password - {data.password} был авторизован")
            return {"valid": True}
        else:
            print(f"Пользователь: login - {data.login}, password - {data.password} не был авторизован. Неправильный пароль")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")