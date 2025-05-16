import models
import other_functions
from datetime import datetime, timezone
from fastapi import HTTPException
from db import get_connection

async def activate_license_key(request: models.KeyActivateRequest):
    key = request.keyValue
    created_at = datetime.now(timezone.utc)

    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO LicenseKeys (KeyValue, DurationDays, IsUsed, CreatedAt)
                VALUES (%s, %s, false, %s)
                RETURNING KeyID
            """, (key_string, duration, created_at))
            key_id = cursor.fetchone()[0]
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return {
        "key": key_string,
        "duration_days": duration,
        "key_id": key_id
    }

async def create_license_key(request: models.KeyCreateRequest):
    duration = request.keyDuration
    if duration not in [7, 30, 180]:
        raise HTTPException(status_code=400, detail="Invalid key type")

    key_string = other_functions.generate_activation_key()
    created_at = datetime.now(timezone.utc)

    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO LicenseKeys (KeyValue, DurationDays, IsUsed, CreatedAt)
                VALUES (%s, %s, false, %s)
                RETURNING KeyID
            """, (key_string, duration, created_at))
            key_id = cursor.fetchone()[0]
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return {
        "key": key_string,
        "duration_days": duration,
        "key_id": key_id
    }