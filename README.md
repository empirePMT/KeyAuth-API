# KeyAuth-API
A lightweight, high-performance license key authentication system built with Python and FastAPI. It provides secure key generation, hardware identification (HWID) binding, and session-based access verification. This repository is open-source and easy to integrate into native applications (C++/C#), web interfaces (HTML/JS), or loaders.

# Features
Secure key creation and HWID management using a master token.
Automatically binds a key to the user"s hardware signature on the first login.
Supports flexible key lifetimes calculated from the moment of activation.
Uses short-lived session tokens to verify active users without re-exposing the license key.

# Installation
Python 3.9 or neweRR
PiP

# Setup

Clone the repository and navigate to the project folder:
```
git clone https://github.com/empirePMT/KeyAuth-API.git
```
Then
```
cd KeyAuth-API
```
Then
```
pip install fastapi uvicorn pydantic
```
Then
Open the source file and locate the verifyadmin function. Change the placeholder to your own password:
```
if not key or key != "pass123":
```

# Local Development and Running

To launch the backend application locally for testing, run the Uvicorn server:

```
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

# API

API Base URL: [http://127.0.0.1:8000](http://127.0.0.1:8000)
Interactive Documentation : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
Alternative Documentation : [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

# cURL Testing

## Create Key

```
curl -X POST "http://127.0.0.1:8000/key" \
     -H "Content-Type: application/json" \
     -H "xkeyauth: xxx123" \
     -d '{"duration": 86400, "level": 1}'
```

Response:

```
{
  "key": "key-xxx123",
  "expires": 0,
  "level": 1
}
```

## User login

```
curl -X POST "http://127.0.0.1:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"key": "key-xxx123", "hwid": "UID hererrr"}'
```

Response:

```
{
  "session": "9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a6f5e4d3c2b1a0f9e8d",
  "expires": 1782345600,
  "level": 1
}

```

## Verify session

```
curl -X GET "http://127.0.0.1:8000/verify" \
     -H "xkeyauth: 9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a6f5e4d3c2b1a0f9e8d"
```

Response:

```
{
  "status": "active", // or inactive
  "level": 1,
  "remaining": 3599
}

```

## Reset HWID

```
curl -X POST "http://127.0.0.1:8000/reset" \
     -H "Content-Type: application/json" \
     -H "xkeyauth: xxx123" \
     -d '{"key": "key-xxx123", "hwid": "UID hererr"}'
```

Response:

```
{
  "status": "success"
}
```
