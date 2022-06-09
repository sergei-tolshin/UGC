# FastAPI web-producer for Kafka

Тестовый post-запрос:
```
curl -XPOST -H "Content-Type: application/json" -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZWQxOWJlYzktZTQ4Ni00ZTk5LThlOGMtODE4YjA0ODMxMDRkIn0.fX-PBxj0mGYAe774TRsEaVef_UN-lV1bYOgmjcz_ykA" -d '{"user_id":"ed19bec9-e486-4e99-8e8c-818b0483104d","movie_id":"d0893172-5503-428e-ae00-445dc70b1416","viewed_frame":"123","duration":"123","event_time":"123"}' http://localhost:8000/api/v1/views/
```

Код для генерации тестового jwt:
```
import jwt

encoded_jwt = jwt.encode({"user_id": "ed19bec9-e486-4e99-8e8c-818b0483104d"}, "secret", algorithm="HS256")
print(encoded_jwt)
```
