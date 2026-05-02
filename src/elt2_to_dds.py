from db_config import get_db_connection

def transform_stg_to_dds():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        print("Начало загрузки в слой DDS")

        cur.execute("""
            INSERT INTO dds.hub_user (hk_user_id, user_id, load_dt, record_source)
            SELECT DISTINCT 
                MD5(user_id::varchar) AS hk_user_id,
                user_id,
                CURRENT_TIMESTAMP AS load_dt,
                'api_jsonplaceholder' AS record_source
            FROM stg.posts
            ON CONFLICT (hk_user_id) DO NOTHING;
        """)
        print(f"Вставлено в dds.hub_user: {cur.rowcount} строк.")

        cur.execute("""
            INSERT INTO dds.hub_post (hk_post_id, post_id, load_dt, record_source)
            SELECT DISTINCT 
                MD5(id::varchar) AS hk_post_id,
                id AS post_id,
                CURRENT_TIMESTAMP AS load_dt,
                'api_jsonplaceholder' AS record_source
            FROM stg.posts
            ON CONFLICT (hk_post_id) DO NOTHING;
        """)
        print(f"Вставлено в dds.hub_post: {cur.rowcount} строк.")

        cur.execute("""
            INSERT INTO dds.link_user_post (hk_user_post, hk_user_id, hk_post_id, load_dt, record_source)
            SELECT DISTINCT 
                MD5(user_id::varchar || ';' || id::varchar) AS hk_user_post,
                MD5(user_id::varchar) AS hk_user_id,
                MD5(id::varchar) AS hk_post_id,
                CURRENT_TIMESTAMP AS load_dt,
                'api_jsonplaceholder' AS record_source
            FROM stg.posts
            ON CONFLICT (hk_user_post) DO NOTHING;
        """)
        print(f"Вставлено в dds.link_user_post: {cur.rowcount} строк.")

        cur.execute("""
            INSERT INTO dds.sat_post (hk_post_id, load_dt, hash_diff, title, body, record_source)
            SELECT 
                MD5(id::varchar) AS hk_post_id,
                CURRENT_TIMESTAMP AS load_dt,
                MD5(COALESCE(title, '') || ';' || COALESCE(body, '')) AS hash_diff,
                title,
                body,
                'api_jsonplaceholder' AS record_source
            FROM stg.posts s
            WHERE NOT EXISTS (
                SELECT 1 FROM dds.sat_post sat 
                WHERE sat.hk_post_id = MD5(s.id::varchar) 
                  AND sat.hash_diff = MD5(COALESCE(s.title, '') || ';' || COALESCE(s.body, ''))
            );
        """)
        print(f"Вставлено в dds.sat_post: {cur.rowcount} строк.")

        conn.commit()
        print("Слой DDS успешно обновлен!")

    except Exception as e:
        conn.rollback()
        print(f"Ошибка при загрузке в DDS: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    transform_stg_to_dds()