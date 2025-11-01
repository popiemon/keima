# Keima system

fastAPIによるAPIサーバー。
競馬の単勝のようなチケットを購入し、レース結果に応じて賞金が決まるシステム。

## 実行方法 (開発用)

このリポジトリは軽量なサンプル実装です。簡易的な in-memory ストアを用いて動作します。

依存関係をインストールして `uvicorn`（ユーザーの指示に従い "uv" = uvicorn と仮定）で起動します。

推奨手順（シェル）:

```bash
# 仮想環境作成（任意）
python -m venv .venv
source .venv/bin/activate

# 依存関係をインストール
pip install -r requirements.txt

# 開発サーバー起動（uvicorn を使用）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

上記でサーバーが立ち上がったら `http://127.0.0.1:8000` にアクセスできます。

API ドキュメント (自動生成):

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

注意:
- この実装はデモ用の in-memory 実装であり、本番用の永続化や認証は含んでいません。
- 賞金（payout）は実装上の仮定値を使用しています（`win` -> +5 coin, `trifecta` -> +20 coin）。

