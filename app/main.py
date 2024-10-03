import face_recognition
import uvicorn
from fastapi import FastAPI, File, UploadFile
from mysql.connector import connect, Error
import os
from dotenv import load_dotenv

load_dotenv()  # .env ファイルから環境変数を読み込む

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

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)