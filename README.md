# study-snowflake-databricks

不動産価格予測を題材に、`GCS -> Snowflake -> dbt -> Databricks -> Snowflake` の流れでデータ基盤と ML パイプラインを一気通貫で検証するリポジトリ。
Snowflake を DWH / ガバナンス基盤、Databricks を ML 加工 / 実験基盤、dbt を Snowflake 内変換管理として扱う。

## 目的

- GCS への raw データ配置と Snowflake 取り込みを検証する
- dbt による raw / staging / intermediate / mart の責務分離を検証する
- Databricks で表形式データ向け ML 学習と MLflow 実験管理を行う
- 予測結果を Snowflake へ戻し、BI / API 向けの活用面まで見据える

## 技術方針

- DWH / ガバナンス: Snowflake
- DWH 変換: dbt Core
- ML 基盤: Databricks
- ML ライブラリ: scikit-learn / LightGBM
- 実験管理: MLflow
- ストレージ: GCS

## 初期スコープ

- raw データの GCS 配置
- Snowflake External Stage + `COPY INTO`
- dbt による staged / intermediate / mart 生成
- Snowflake RBAC / Masking Policy / Row Access Policy / Secure View
- Databricks での特徴量生成、学習、バッチスコアリング
- Snowflake への予測結果書き戻し

## 対象外

- Deep Learning 中心構成
- Vertex AI 中心構成
- BigQuery 中心構成
- リアルタイム推論
- 過度な Web アプリ開発

## 想定ディレクトリ

```text
.
├── AGENTS.md
├── CLAUDE.md
├── Makefile
├── README.md
├── env/
│   ├── config.yaml
│   └── secret.yaml
├── doc/
│   ├── 01_仕様と設計.md
│   ├── 02_移行ロードマップ.md
│   ├── 03_実装カタログ.md
│   ├── 04_運用.md
│   └── README.md
├── app/
├── gcs/
├── snowflake/
├── dbt/
├── databricks/
├── ml/
└── infra_optional/
```

## コマンド

`Makefile` はまだひな形であり、以下は将来の反映先である。

```bash
make setup
make build
make run
make test
make lint
```

## ドキュメント

詳細は [`doc/`](doc/) を参照。権威順位と更新規約は [`doc/README.md`](doc/README.md) に従う。

- [`doc/01_仕様と設計.md`](doc/01_仕様と設計.md) — Snowflake / dbt / Databricks / ML / ガバナンスの仕様と設計
- [`doc/02_移行ロードマップ.md`](doc/02_移行ロードマップ.md) — 作る / 作らないの決定的仕様
- [`doc/03_実装カタログ.md`](doc/03_実装カタログ.md) — 実装物の所在記録
- [`doc/04_運用.md`](doc/04_運用.md) — 環境構築、定常運用、実行手順

## 設定管理

- 非機密: `env/config.yaml`
- ローカル秘密情報: `env/secret.yaml`
- 共有・本番秘密情報: `doppler.yaml`

`env/secret.yaml` はコミットしない。
