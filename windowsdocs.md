Windows Docs for PowerSHELL
# Key creation
```
curl.exe -X POST "http://127.0.0.1:8000/key" `
     -H "Content-Type: application/json" `
     -H "xkeyauth: pass123" `
     -d '{\"duration\": 86400, \"level\": 1}'
```
# Login
```
curl.exe -X POST "http://127.0.0.1:8000/login" `
     -H "Content-Type: application/json" `
     -d '{\"key\": \"key-xxx123\", \"hwid\": \"UID hererrr\"}'
```
# Verify Session
```
curl.exe -X GET "http://127.0.0.1:8000/verify" `
     -H "xkeyauth: 9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a6f5e4d3c2b1a0f9e8d"
```
# Reset HWID

```
curl.exe -X POST "http://127.0.0.1:8000/reset" `
     -H "Content-Type: application/json" `
     -H "xkeyauth: pass123" `
     -d '{\"key\": \"key-xxx123\", \"hwid\": \"UID hererr\"}'
```
