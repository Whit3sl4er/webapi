import models
import key_logic
import get_tables
import authentication
from fastapi import APIRouter

router = APIRouter()

@router.get("/Users")
async def get_users():
    return await get_tables.get_users()

@router.get("/Subscriptions")
async def get_subscriptions():
    return await get_tables.get_subscriptions()

@router.get("/LicenseKeys")
async def get_license_keys():
    return await get_tables.get_license_keys()

@router.post("/create-key")
async def create_license_key(request: models.KeyCreateRequest):
    return await key_logic.create_license_key(request)

@router.post("/activate-key")
async def activate_license_key(request: models.KeyActivateRequest):
    return await key_logic.activate_license_key(request)

# Функция регистрации
@router.post("/register")
async def register_user(request: models.RegisterData):
    return await authentication.register_user(request)

# Функция авторизации
@router.post("/logIn")
async def login_user(request: models.LoginData):
    return await authentication.logIn_user(request)