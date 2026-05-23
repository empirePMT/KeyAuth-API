import time
import secrets
from typing import Dict, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader

app = FastAPI()
apikeyheader = APIKeyHeader(name="xkeyauth", auto_error=False)

dbkeys: Dict[str, dict] = {}
dbhwids: Dict[str, str] = {}
dbsessions: Dict[str, dict] = {}

class KeyCreate(BaseModel):
    duration: int = Field(default=86400)
    level: int = Field(default=1)

class KeyResponse(BaseModel):
    key: str
    expires: int
    level: int

class UserLogin(BaseModel):
    key: str
    hwid: str

class LoginResponse(BaseModel):
    session: str
    expires: int
    level: int

def verifyadmin(key: Optional[str] = Depends(apikeyheader)):
    if not key or key != "pass123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid admin token"
        )
    return key

def verifysession(session: Optional[str] = Depends(apikeyheader)):
    if not session or session not in dbsessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid session"
        )
    sessiondata = dbsessions[session]
    if time.time() > sessiondata["expires"]:
        del dbsessions[session]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="session expired"
        )
    return sessiondata

@app.post("/key", response_model=KeyResponse)
def createkey(data: KeyCreate, admin: str = Depends(verifyadmin)):
    newkey = f"key-{secrets.token_hex(16)}"
    dbkeys[newkey] = {
        "expires": 0,
        "duration": data.duration,
        "level": data.level,
        "used": False
    }
    return {
        "key": newkey,
        "expires": 0,
        "level": data.level
    }

@app.post("/login", response_model=LoginResponse)
def loginuser(data: UserLogin):
    if data.key not in dbkeys:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="key not found"
        )
    keydata = dbkeys[data.key]
    current = int(time.time())
    if not keydata["used"]:
        keydata["used"] = True
        keydata["expires"] = current + keydata["duration"]
        dbhwids[data.key] = data.hwid
    else:
        if current > keydata["expires"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="key expired"
            )
        if dbhwids.get(data.key) != data.hwid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="hwid mismatch"
            )
    newsession = secrets.token_hex(32)
    sessionexpiry = current + 3600
    dbsessions[newsession] = {
        "key": data.key,
        "level": keydata["level"],
        "expires": sessionexpiry
    }
    return {
        "session": newsession,
        "expires": sessionexpiry,
        "level": keydata["level"]
    }

@app.get("/verify")
def checkstatus(session: dict = Depends(verifysession)):
    return {
        "status": "active",
        "level": session["level"],
        "remaining": int(session["expires"] - time.time())
    }

@app.post("/reset")
def resethwid(data: UserLogin, admin: str = Depends(verifyadmin)):
    if data.key not in dbkeys:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="key not found"
        )
    dbhwids[data.key] = data.hwid
    return {"status": "success"}
