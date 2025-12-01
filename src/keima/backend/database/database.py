from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from dotenv import load_dotenv
import os

load_dotenv()

# 環境変数からデータベース接続情報を取得
db_user = os.getenv("POSTGRES_USER", "postgres")
db_password = os.getenv("POSTGRES_PASSWORD", "password")
db_name = os.getenv("POSTGRES_DB", "postgres")

# 接続URL: postgresql+asyncpg://ユーザー名:パスワード@ホスト:ポート/DB名
DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@localhost/{db_name}"

# 非同期エンジンの作成
engine = create_async_engine(DATABASE_URL, echo=True)

# セッションファクトリの作成
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ベースクラス（モデル定義用）
class Base(DeclarativeBase):
    pass

# 依存性注入用関数: リクエストごとにセッションを作成し、終了後に閉じる
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session