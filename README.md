# 日本株 配当利回り可視化ツール

このアプリケーションは、日本株の証券コードを入力することで、直近5年間の月次配当利回りと月末終値をグラフ表示するDjangoウェブアプリです。

## 機能
- 証券コード（例: 7203）を入力して検索
- 自動的に「.T」を付与して東京証券取引所のデータを取得
- Plotlyによるインタラクティブな複合グラフ（配当利回りの棒グラフ + 株価の折れ線グラフ）
- PostgreSQLによるデータのキャッシュ（1日経過したデータは再取得）
- レスポンシブでモダンなダークテーマUI

## 技術スタック
- **Backend:** Python, Django
- **Frontend:** Bootstrap 5, Plotly.js
- **Data Source:** yfinance
- **Database:** PostgreSQL (Production) / SQLite (Development)
- **Deployment:** Render

## セットアップ手順

### ローカル開発環境
1. リポジトリをクローン
2. 仮想環境を作成して有効化
3. 依存ライブラリをインストール
   ```bash
   pip install -r requirements.txt
   ```
4. マイグレーションを実行
   ```bash
   python manage.py migrate
   ```
5. 開発サーバーを起動
   ```bash
   python manage.py runserver
   ```
6. ブラウザで `http://127.0.0.1:8000/` にアクセス

### 環境変数
- `SECRET_KEY`: Djangoのシークレットキー
- `DATABASE_URL`: PostgreSQLの接続URL（Render等で自動設定）
- `DEBUG`: `True` または `False` (本番環境では `False`)

## デプロイ方法 (Render)
1. GitHubにリポジトリをプッシュ
2. Renderのダッシュボードから `Blueprint` を選択し、リポジトリを接続
3. `render.yaml` の設定に従って自動的にWebサービスとデータベースが作成・デプロイされます
