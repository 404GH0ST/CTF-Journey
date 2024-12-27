import jwt

JWT_SECRET = "replican"

jwtData = { "user": "admin" }

print(jwt.encode(jwtData, JWT_SECRET, algorithm="HS256"))