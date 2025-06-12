"""import pandas as pd
import sqlite3

# 設定
# 読み込むエクセルファイルのパス
EXCEL_FINE_PATH = 'data/20201225-mxt_kagsei-mext_01110_012.xlsx'
# 作成するデータベースファイルのパス
DB_FILE_PATH = 'recipe_app/nutrition.db'
# データベース内に作成するテーブル名
TABLE_NAME = 'nutrition'

def create_database():
    エクセルファイルを読み込んでSQLiteデータベースを作成する
    try:
        # エクセルファイルをPandasで読み込む
        print(f"'{EXCEL_FINE_PATH}'を読み込んでいます...")
        df = pd.read_excel(EXCEL_FINE_PATH)
        
        # SQLiteデータベースに接続（ファイルがなければ新規作成）
        print(f"'{DB_FILE_PATH}'にデータベースを作成中...")
        conn = sqlite3.connect(DB_FILE_PATH)
        
        # PandasのDataFrameをそのままデータベースのテーブルに変換保存
        # if_exists='replace'はもしすでにテーブルがあれば作り直す設定
        df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
        
        # 接続を閉じる
        conn.close()
        
        print("-" * 20)
        print("🎉 データベースの作成が完了しました！")
        print(f"テーブル名: '{TABLE_NAME}'")
        print(f"保存先: '{DB_FILE_PATH}'")
        print("-" * 20)
        
    except FileNotFoundError:
        print(f"エラー：Excelファイルが見つかりません。パスを確認してください：'{EXCEL_FINE_PATH}'")
    except Exception as e:
        print(f"エラーが発生しました：{e}")
        
    if __name__ == '__main__':
        create_database()
        
"""