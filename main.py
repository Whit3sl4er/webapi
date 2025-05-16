from fastapi import FastAPI
from routes import router

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("Приложение запускается...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Приложение завершает работу...")

# Подключаем роутер с эндпоинтами
app.include_router(router)
