import models
import key_logic
import get_tables
import authentication
from fastapi import APIRouter

router = APIRouter()

@router.get("/Users")
async def get_users():
    await get_tables.get_users()

@router.get("/Subscriptions")
async def get_subscriptions():
    await get_tables.get_subscriptions()

@router.get("/LicenseKeys")
async def get_license_keys():
    await get_tables.get_license_keys()

@router.post("/create-key")
async def create_license_key(request: models.KeyCreateRequest):
    await key_logic.create_license_key(request)

@router.post("/activate-key")
async def activate_license_key(request: models.KeyActivateRequest):
    await key_logic.activate_license_key(request)

# Функция регистрации
@router.post("/register")
async def register_user(data: models.RegisterData):
    await authentication.register_user(data)

# Функция авторизации
@router.post("/login")
async def login_user(data: models.LoginData):
    await authentication.logIn_user(data)