import sqlite3
import pandas as pd
from datetime import datetime, timedelta

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


def read():
    try:
        # SQLite 데이터베이스에 연결
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # SQL 쿼리를 사용하여 테이블에서 데이터 읽기
        query = "SELECT * FROM data_table"
        df = pd.read_sql_query(query, conn)
        print(df)
        # 연결 종료
        conn.close()

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

def save_to_db(file_path):
    try:
        # 파일 확장자에 따라 pandas로 파일 읽기
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file type")

        # 필요한 컬럼이 있는지 확인
        expected_columns = ['또래 이름', '생일']
        if not all(column in df.columns for column in expected_columns):
            raise ValueError("엑셀 파일에 필요한 컬럼이 없습니다.")

        # 새로운 데이터프레임 생성
        new_df = pd.DataFrame()
        new_df['생년'] = df['생일'].astype(str).str[:2]
        new_df['생일'] = df['생일'].astype(str).str[2:]
        new_df['이름'] = df['또래 이름'].str.split().str[1]

        # SQLite 데이터베이스에 연결 (db.sqlite3 파일로 저장)
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # 새로운 테이블에 데이터 저장
        new_df.to_sql('birthday', conn, if_exists='replace', index=False)

        # 커밋 및 연결 종료
        conn.commit()
        conn.close()

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

def read_from_db():
    try:
        # SQLite 데이터베이스에 연결
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # SQL 쿼리를 사용하여 테이블에서 데이터 읽기
        query = "SELECT * FROM birthday ORDER BY 생일"
        df = pd.read_sql_query(query, conn)
        # 연결 종료
        conn.close()

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

def check_birthday_db():
    try:
        # SQLite 데이터베이스에 연결
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # SQL 쿼리를 사용하여 테이블에서 데이터 읽기
        query = "SELECT * FROM birthday ORDER BY 생일"
        df = pd.read_sql_query(query, conn)
        # 연결 종료
        conn.close()

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

def count_birthday_db():
    try:
        # SQLite 데이터베이스에 연결
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # SQL 쿼리를 사용하여 테이블에서 데이터 읽기
        query = "SELECT COUNT(*) as COUNT FROM birthday"
        res = pd.read_sql_query(query, conn)
        res = res.at[0, 'COUNT']

        # 연결 종료
        conn.close()
        print(res)
        return int(res)

    except Exception as e:
        print(f"Error: {e}")
        return None


def get_birthday_week(yymmdd):
    try:
        # 입력 날짜를 datetime 객체로 변환
        base_date = datetime.strptime(yymmdd, "%y%m%d")
        end_date = base_date + timedelta(days=6)

        # 시작 날짜와 종료 날짜의 mmdd 형식을 추출
        base_mmdd = base_date.strftime("%m%d")
        end_mmdd = end_date.strftime("%m%d")

        # SQLite 데이터베이스에 연결
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # SQL 쿼리를 사용하여 yymmdd의 날짜로부터 7일 이내의 모든 생일자를 추출
        query = f"""
        SELECT 생년, 생일, 이름 FROM birthday
        WHERE 
            생일 BETWEEN '{base_mmdd}' AND '{end_mmdd}'
        ORDER BY 생일
        """
        res = pd.read_sql_query(query, conn)

        # 결과를 'YY또래 이름(dd일)' 형식으로 포맷
        birthday_list = []
        for index,row in res.iterrows():
            birthday_list.append(f"{row['생년']}또래 {row['이름']}({int(row['생일'][2:])}일)")

        # 연결 종료
        conn.close()

        return birthday_list


    except Exception as e:
        print(f"Error: {e}")
        return None


def drop_table(table_name):
    try:
        # SQLite 데이터베이스에 연결
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # SQL 쿼리를 사용하여 테이블 삭제하기
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        # 변경 사항 커밋
        conn.commit()

        # 연결 종료
        conn.close()

        return True

    except Exception as e:
        print(f"Error: {e}")
        return None