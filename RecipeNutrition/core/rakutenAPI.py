import requests
import pandas as pd
from pprint import pprint

APP_ID = "1029142912605577857"
url = f"https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?applicationId={APP_ID}"

json_data = None # 初期化
try:
    res = requests.get(url)
    res.raise_for_status()
    # jsonの使い方
    json_data = res.json()
    # pprint(json_data) # 必要に応じて表示

except requests.exceptions.RequestException as e:
    print(f"リクエスト中にエラーが発生しました: {e}")
    # エラーが発生したら、以降の処理は行わないようにする
    exit() # または適切なエラー処理
except Exception as e: # .json() でのパースエラーなども含む
    print(f"データ取得またはJSON解析中にエラーが発生しました: {e}")
    exit() # または適切なエラー処理

# json_data が正常に取得できなかった場合は処理を中断
if json_data is None or 'result' not in json_data:
    print("エラー: APIから有効なデータを取得できませんでした。")
    exit()

# DataFrameに格納するための行データを一時的に保持するリスト
rows_list = []
parent_dict = {}

# 大カテゴリ
# json_dataのresultというキーの値の中に、largeというキーが存在しているか確認
if 'large' in json_data['result']:
    # largeが存在する場合、json_data['result']['large']の中身から、各カテゴリの情報を１つずつ取り出してcategoryという変数に入れる。
    for category in json_data['result']['large']:
        # category変数には、１つの大カテゴリに関する情報が辞書として入っている。これをrows_listに追加していく
        rows_list.append({
            'category1': category['categoryId'],
            'category2': "",
            'category3': "",
            'categoryId': category['categoryId'],
            'categoryName': category['categoryName']
        })
else:
    print("警告: 大カテゴリデータ ('result.large') が見つかりません。")

# 中カテゴリ
if 'medium' in json_data['result']:
    for category in json_data['result']['medium']:
        rows_list.append({
            'category1': category['parentCategoryId'],
            'category2': category['categoryId'],
            'category3': "",
            'categoryId': f"{category['parentCategoryId']}-{category['categoryId']}", # f-stringを使うとスッキリします
            'categoryName': category['categoryName']
        })
        parent_dict[str(category['categoryId'])] = str(category['parentCategoryId']) # キーも値も文字列で統一しておくと安全
else:
    print("警告: 中カテゴリデータ ('result.medium') が見つかりません。")

# 小カテゴリ
if 'small' in json_data['result']:
    for category in json_data['result']['small']:
        parent_cat_id_str = str(category['parentCategoryId'])
        # parent_dictにキーが存在するか確認
        grandparent_cat_id = parent_dict.get(parent_cat_id_str)

        if grandparent_cat_id is None:
            print(f"警告: parent_dict にキー '{parent_cat_id_str}' (中カテゴリID) が見つかりません。")
            print(f"       小カテゴリ '{category['categoryName']}' (ID: {category['categoryId']}) の category1 (大カテゴリID) が正しく設定できません。")
            grandparent_cat_id = "不明" # または、このデータ行をスキップするなどの処理

        rows_list.append({
            'category1': grandparent_cat_id,
            'category2': parent_cat_id_str, # str型に統一
            'category3': str(category['categoryId']), # str型に統一
            'categoryId': f"{grandparent_cat_id}-{parent_cat_id_str}-{category['categoryId']}",
            'categoryName': category['categoryName']
        })
else:
    print("警告: 小カテゴリデータ ('result.small') が見つかりません。")


# リストが空でなければDataFrameを作成
if rows_list:
    df = pd.DataFrame(rows_list, columns=['category1', 'category2', 'category3', 'categoryId', 'categoryName'])
    print("--- DataFrame作成成功 ---")
    #print(df.to_string()) # 全件表示したい場合
    #print(df.head())
    print(df)
    print(f"\nDataFrameの形状: {df.shape}")
else:
    print("DataFrameを作成するためのデータがありませんでした。")
    # 空のDataFrameを定義しておく
    df = pd.DataFrame(columns=['category1', 'category2', 'category3', 'categoryId', 'categoryName'])