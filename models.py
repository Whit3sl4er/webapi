from pydantic import BaseModel
# ===== Pydantic-модели =====
class RegisterData(BaseModel):
    login: str
    password: str
    email: str

class LoginData(BaseModel):
    login: str
    password: str

class KeyCreateRequest(BaseModel):
    keyDuration: int

class KeyActivateRequest(BaseModel):
    keyValue: str
    user_id: int

class ActivateKeyRequest(BaseModel):
    user_id: int
    key: str