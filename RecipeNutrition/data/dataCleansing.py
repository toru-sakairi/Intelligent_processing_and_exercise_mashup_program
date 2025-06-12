# エクセルファイルが終わってるのでデータクレンジングを行ってからデータベースを作成します
# その際のデータクレンジングを行うスクリプトです
import pandas as pd

# 設定
# 読み込むエクセルファイルのパス
EXCEL_FILE_PATH = 'RecipeNutrition/data/クレンジングデータ.xlsx'
# 作成するエクセルファイル
CSV_OUTPUT_PATH = 'RecipeNutrition/data/クレンジング後データ.csv'

df = pd.read_excel(EXCEL_FILE_PATH)

try:
    # 1. エクセルファイルを読み込む
    df = pd.read_excel(EXCEL_FILE_PATH)
    print("--- Excelファイルの読み込み完了 ---")

    # 2. クレンジング対象の列を指定
    numeric_columns = [
        '水分(g)', 'たんぱく質(g)', '脂質(g)', '炭水化物(g)', '食物繊維総量(g)',
        'ナトリウム(mg)', 'カリウム(mg)', 'カルシウム(mg)', 'マグネシウム(mg)', 'リン(mg)',
        '鉄(mg)', '亜鉛(mg)', '銅(mg)', 'マンガン(mg)', 'ヨウ素(μg)', 'セレン(μg)',
        'クロム(μg)', 'モリブデン(μg)', 'レチノール(μg)', 'αーカロテン(μg)',
        'βーカロテン(μg)', 'βークリプトキサンチン(μg)', 'βーカロテン当量(μg)',
        'レチノール活性当量(μg)', 'ビタミンD(μg)', 'αートコフェロール(mg)',
        'βートコフェロール(mg)', 'γートコフェロール(mg)', 'δートコフェロール(mg)',
        'ビタミンK(μg)', 'ビタミンB1(mg)', 'ビタミンB2(mg)', 'ナイアシン当量(mg)',
        'ビタミンB6(mg)', 'ビタミンB12(μg)', '葉酸(μg)', 'パントテン酸(mg)',
        'ビオチン(μg)', 'ビタミンC(mg)', '食塩相当量g'
    ]

    print("\n--- データクレンジングを開始します ---")
    # 3. 各列に対してクレンジング処理をループで実行
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(
                r'[()\s-]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(0)

    print("--- データクレンジングが完了しました ---")
    # 4. クレンジング後のデータ型を最終確認
    print("\n--- クレンジング後のデータ情報 ---")
    df.info()

    # 5. ★クレンジング後のデータをCSVファイルとして出力
    df.to_csv(CSV_OUTPUT_PATH, index=False, encoding='utf-8-sig')
    
    print(f"\n成功: クレンジング後のデータを '{CSV_OUTPUT_PATH}' に保存しました。")

except FileNotFoundError:
    print("ファイルが見つかりません")
except Exception as e:
    print(e)
