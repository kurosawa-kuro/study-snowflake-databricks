# CLAUDE.md

このファイルは Claude Code が `study-snowflake-databricks` リポジトリで作業する際の補助ガイドである。

## リポジトリの前提

- このリポジトリは、不動産価格予測を題材にした Snowflake × Databricks × dbt の検証基盤を扱う
- Snowflake は DWH / ガバナンス基盤、Databricks は ML 加工 / 実験基盤、dbt は Snowflake 内変換管理として扱う
- Deep Learning は初期主対象外であり、scikit-learn / LightGBM による表形式 ML を主軸にする

## コマンド

`Makefile` はまだひな形であり、以下のコマンドは実装済み手順ではない。

```bash
make setup
make build
make run
make dev
make test
make fmt
make lint
```

コマンドを案内・更新する場合は、実際に成立する内容にしてから記述すること。

## ドキュメント優先順位

矛盾した場合は以下の順で扱う。

```text
doc/02_移行ロードマップ.md
> doc/01_仕様と設計.md
> README.md
```

更新規約の詳細は [`doc/README.md`](doc/README.md) を参照する。

## 作業ルール

- 推測で仕様を書かない。決まっていないものは明示する
- 仕様変更は `doc/01`、`doc/02`、必要に応じて `README.md` を同一変更で更新する
- Snowflake / dbt / Databricks の責務分離を崩さない
- Deep Learning、Vertex AI 中心構成、BigQuery 中心構成、リアルタイム推論など、`doc/01` でスコープ外としたものを先に広げない
- 非機密は `env/config.yaml`、ローカル秘密情報は `env/secret.yaml`、共有・本番秘密情報は Doppler（`doppler.yaml`）で管理する
