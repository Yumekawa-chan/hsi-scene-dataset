## 概要

本リポジトリは，HSI (Hyperspectral Imaging) データの可視化と撮影データの記録を行うためのツールセットを提供します．

## 機能

### hs_to_rgb

HSIデータをRGB画像として可視化します．

- HSIファイルを読み込み，RGB画像に変換します．
- 変換されたRGB画像を表示します．

### folder_monitor

指定されたフォルダを監視し，新しいHSIファイルが追加された際に自動的に処理します．

- 新しいファイルが追加された際に，ファイル名から情報を抽出し，ユーザーから追加情報を取得してJSONファイルに保存します．
- ファイル名が "Dark" で始まる場合はJSON入力をスキップします．

#### 使用方法

1. `folder_monitor.py` を実行します．
2. `hs_data` フォルダ内に新しいHSIファイルを追加します．
3. ファイル名に基づいて自動的に情報を抽出し，ユーザーから追加情報を取得して `data.json` に保存します．

## インストールと設定

1. リポジトリをクローンします:
   ```sh
   git clone https://github.com/Yumekawa-chan/hsi-scene-dataset.git
   cd hsi-scene-dataset
