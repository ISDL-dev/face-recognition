import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "host": os.getenv("MYSQL_HOSTNAME"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            **db_config,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        return connection
    except Error as e:
        print(f"データベース接続エラー: {e}")
        return None

async def sync_users_with_db(users_data):
    added_users = []
    connection = get_db_connection()
    if not connection:
        print("データベース接続失敗")
        return added_users

    try:
        cursor = connection.cursor(dictionary=True)
        for user in users_data:
            # ユーザーがDBに存在するか確認
            cursor.execute("SELECT * FROM user_faces WHERE user_id = %s", (user['user_id'],))
            existing_user = cursor.fetchone()

            if not existing_user:
                # 新しいユーザーを追加
                insert_query = """
                INSERT INTO user_faces (user_id, name, encoding)
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_query, (user['user_id'], user['user_name'], ''))  # encodingは空文字列として保存
                added_users.append(user)
                print(f"ユーザーを追加: {user['user_name']}")

        connection.commit()
        print(f"追加されたユーザー数: {len(added_users)}")
    except Error as e:
        print(f"データベース操作エラー: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return added_users