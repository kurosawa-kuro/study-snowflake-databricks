# src

本ディレクトリは、`study-snowflake-databricks` の実装置き場である。

## 最初にコピーしたもの

参考プロジェクト [`study-databricks-gcp-pipeline`](/home/ubuntu/repos/study-databricks-gcp-pipeline/README.md) から、最初の雛形として以下を持ち込んだ。

| コピー先 | 元ファイル | 目的 |
|---|---|---|
| `reference/study_databricks_gcp_pipeline/sql_connectivity.py` | `src/sql_connectivity.py` | 接続確認 CLI の構成パターンを流用するため |
| `reference/study_databricks_gcp_pipeline/volume_uploader.py` | `src/volume_uploader.py` | GCS 経由ジョブの責務分離を参照するため |
| `data/reference/customers.csv` | `data/customers.csv` | fixture の持ち方を参照するため |
| `data/reference/orders.csv` | `data/orders.csv` | 複数テーブル fixture の持ち方を参照するため |

これらは本体実装ではなく、構成と書き方の参照用である。本リポジトリの主対象は `Snowflake -> dbt -> Databricks -> Snowflake` なので、実装本体は下記の責務別ディレクトリへ積んでいく。

## 本体ディレクトリ

- `sql/`
  Snowflake の foundation, raw, governance, serving SQL を置く。
- `dbt/`
  Snowflake 向け dbt project を置く。
- `databricks/`
  notebook, job, experiment など Databricks 資産を置く。
- `data/`
  `reference/` はコピー元の参照 fixture、`sample/` は本リポジトリ固有の学習用データを置く。
- `docs/`
  実行証跡や補助メモを置く。
