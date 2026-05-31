# sql

Snowflake 向け SQL を責務別に分けて置く。

- `foundation/`
  接続確認、database / schema 作成、基本 DDL
- `raw/`
  stage, file format, COPY INTO, RAW テーブル
- `governance/`
  role, grant, masking, row access, secure view
- `serving/`
  prediction table, prediction mart, 公開 view
