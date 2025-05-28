from sqlalchemy import create_engine
import os

# データベース接続情報 (Azure App Serviceのアプリケーション設定から取得)
# 各環境変数はAzure Portalで個別に設定されていることを前提とします
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# SSL証明書ファイルへのパスを動的に構築
# connect_MySQL.py と同じディレクトリ (db_control/) に
# DigiCertGlobalRootCA.crt.pem が存在することを想定

# 現在のファイルのディレクトリ (例: /tmp/xxxx/db_control/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# 証明書ファイルへの完全なパス
SSL_CA_PATH = os.path.join(current_dir, "DigiCertGlobalRootCA.crt.pem")


# MySQLのURL構築
# DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME がNoneでないことを確認
# (もしNoneになる場合は、Azure App Serviceの環境変数設定を見直す必要があります)
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("One or more database environment variables are not set. "
                     "Please check Azure App Service configuration for DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME.")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# エンジンの作成
engine = create_engine(
    DATABASE_URL,
    echo=True, # SQL実行ログを表示（デバッグ用）
    pool_pre_ping=True, # 接続が使用可能か定期的に確認
    pool_recycle=3600, # 接続を1時間ごとに再利用して期限切れを防ぐ
    connect_args={
        "ssl_ca": SSL_CA_PATH # 動的に構築したSSL CAファイルのパスを渡す
    }
)

print(f"DB_SSL_CAファイルパス: {SSL_CA_PATH}")
