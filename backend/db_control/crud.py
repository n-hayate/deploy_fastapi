# uname() error回避
import platform
print("platform", platform.uname())


from sqlalchemy import create_engine, insert, delete, update, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
import pandas as pd
from db_control.connect_MySQL import engine
from db_control.mymodels_MySQL import Customers


def myinsert(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    query = insert(mymodel).values(values)
    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()

    # セッションを閉じる
    session.close()
    return "inserted"


def myselect(mymodel, customer_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel).filter(mymodel.customer_id == customer_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for customer_info in result:
            result_dict_list.append({
                "customer_id": customer_info.customer_id,
                "customer_name": customer_info.customer_name,
                "age": customer_info.age,
                "gender": customer_info.gender
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")

    # セッションを閉じる
    session.close()
    return result_json


def myselectAll(mymodel):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = select(mymodel)
    try:
        # トランザクションを開始
        with session.begin():
            df = pd.read_sql_query(query, con=engine)
            result_json = df.to_json(orient='records', force_ascii=False)

    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        result_json = None

    # セッションを閉じる
    session.close()
    return result_json


def myupdate(mymodel, values: dict):
    """
    指定されたモデルのレコードを更新します（シンプルな構造）。
    'values' 辞書には 'customer_id' と、更新する他のフィールドが含まれている必要があります。
    """
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # 'values' 辞書から 'customer_id' を取り出す。
    # これがWHERE句の条件となり、残りの要素がSET句の更新内容となる。
    # 'customer_id' が 'values' に存在しない場合、ここで KeyError が発生します。
    customer_id_val = values.pop("customer_id")

    # SQLAlchemyのupdateステートメントを構築
    # update(モデルクラス).where(条件).values(更新する値の辞書)
    # 'values' に customer_id を除いた更新対象のフィールドが残っていることを期待。
    # もし 'values' が pop 後に空の場合、.values(**{}) となり、
    # SQLAlchemy や DB の挙動によってはエラーまたは何も更新しない結果になります。
    query = (
        update(mymodel)
        .where(mymodel.customer_id == customer_id_val)
        .values(**values)  # 辞書の残りの要素を展開してSET句に指定
    )

    try:
        # トランザクションを開始 (成功すれば自動コミット、失敗すれば自動ロールバック)
        with session.begin():
            result = session.execute(query)
            # mydelete の例に合わせて、result.rowcount のチェックや詳細な結果分析は省略
    except sqlalchemy.exc.IntegrityError:
        # mydelete のエラー処理構造を模倣
        print(f"一意制約違反により、顧客ID {customer_id_val} の更新に失敗しました")
        session.rollback() # mydelete の構造に合わせて明示的に rollback を記述

    # mydelete の構造に合わせて、try-exceptブロックの外でセッションを閉じる
    session.close()

    # mydelete の戻り値の形式を模倣し、シンプルな文字列を返す。
    # 元の (問題のあった) myupdate が "put" を返していたので、それに近い形も可能です。
    return f"Customer ID {customer_id_val} の更新処理が試行されました。"
    # もし元の "put" という文字列を返したい場合は以下のようにします:
    # return "put"

def mydelete(mymodel, customer_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = delete(mymodel).where(mymodel.customer_id == customer_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()

    # セッションを閉じる
    session.close()
    return customer_id + " is deleted"