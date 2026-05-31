# AGENTS.md

AI コーディングエージェント共通の作業ガイド。
ツール固有の補足は各ファイルに分離し、ここではこのリポジトリで共通に守る方針のみを記す。

## プロジェクト概要

- 目的: 不動産価格予測を題材に、Snowflake / dbt / Databricks を使ったデータ基盤と ML パイプラインを一気通貫で検証する
- 主対象: GCS 取り込み、Snowflake DWH、dbt 変換、Snowflake ガバナンス、Databricks ML、Snowflake への予測結果書き戻し
- 現状: `doc/01` に全体設計を整理済み。実装はこれから具体化する段階

## 基本方針

- Snowflake を DWH / ガバナンス基盤として扱う
- dbt を Snowflake 内変換の正規ルートにする
- Databricks を ML 専用処理へ寄せる
- 表形式 ML を優先し、Deep Learning を初期主対象外にする

## 権威順位

```text
doc/02_移行ロードマップ.md
> doc/01_仕様と設計.md
> README.md
```

補助的な運用ルールは [`doc/README.md`](doc/README.md) を参照する。

## 更新ルール

- スコープや採否の変更は `doc/02_移行ロードマップ.md` を先に直し、その後 `doc/01_仕様と設計.md` と `README.md` を合わせる
- 実装物や構成変更は `doc/03_実装カタログ.md` を更新する
- 実行手順や環境構築の変更は `doc/04_運用.md` と `Makefile` を更新する
- 関連ドキュメントは同一変更でそろえる

## 作業上の注意

- `Makefile` はまだひな形であり、存在だけでコマンド成立を前提にしない
- Snowflake / dbt / Databricks の責務を曖昧にしない
- Deep Learning、リアルタイム推論、過度な Web アプリ化は初期スコープ外として扱う
- 非機密は `env/config.yaml`、ローカル秘密情報は `env/secret.yaml`、共有・本番秘密情報は Doppler（`doppler.yaml`）で管理する
- 秘密情報はコミットしない
