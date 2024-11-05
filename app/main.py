import face_recognition
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from mysql.connector import connect, Error
import os
from dotenv import load_dotenv
import httpx
from fetch_user import sync_users_with_db

load_dotenv()

app = FastAPI()

# データベース接続設定
db_config = {
    "host": os.getenv("MYSQL_HOSTNAME"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}

@app.get("/")
def read_root():
    return {"message": "顔認証システムが稼働中です"}

@app.post("/recognize")
async def recognize_face(file: UploadFile = File(...)):
    contents = await file.read()
    with open("captured_image.jpg", "wb") as f:
        f.write(contents)

    image = face_recognition.load_image_file("captured_image.jpg")
    face_locations = face_recognition.face_locations(image)
    
    if not face_locations:
        return {"message": "顔が検出されませんでした"}
    try:
        with connect(**db_config) as connection:
            print("データベース接続成功")
    except Error as e:
        print(f"データベース接続エラー: {e}")
        return {"message": "データベース接続エラー"}

    return {"message": f"{len(face_locations)}個の顔を検出しました", "locations": face_locations}

@app.get("/fetch_user")
async def fetch_user():
    api_url = os.getenv("ISDL_SENTINEL_ENDPOINT") + "/users"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url)
            response.raise_for_status()
            users_data = response.json()
            user_count = len(users_data)  
            added_users = await sync_users_with_db(users_data)     
            return {
                "user": f"{user_count}個のユーザを取得しました",
                "locations": users_data
            }
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"外部APIからデータを取得できませんでした: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)