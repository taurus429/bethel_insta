# util.py
import pandas as pd
import sqlite3

def save(file_path):
    try:
        # 파일 확장자에 따라 pandas로 파일 읽기
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file type")

        # SQLite 데이터베이스에 연결 (db.sqlite3 파일로 저장)
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # 데이터프레임을 테이블로 저장 (테이블 이름: data_table)
        df.to_sql('data_table', conn, if_exists='replace', index=False)

        # 커밋 및 연결 종료
        conn.commit()
        conn.close()

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False