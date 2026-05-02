import requests
from db_config import get_db_connection

API_URL = "https://jsonplaceholder.typicode.com/posts/"


def fetch_data():
    print("Получение данных из API...")
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()


def load_to_stg(data):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("TRUNCATE TABLE stg.posts;")

        insert_query = """
                       INSERT INTO stg.posts (user_id, id, title, body)
                       VALUES (%s, %s, %s, %s) \
                       """
        records = [(item['userId'], item['id'], item['title'], item['body']) for item in data]

        cur.executemany(insert_query, records)
        conn.commit()
        print(f"Успешно загружено {len(records)} записей в stg.posts.")

    except Exception as e:
        conn.rollback()
        print(f"Ошибка загрузки в STG: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    raw_data = fetch_data()
    load_to_stg(raw_data)