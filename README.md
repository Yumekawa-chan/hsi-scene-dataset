## 概要

本リポジトリは，HSI (Hyperspectral Imaging) データの可視化と撮影データの記録を行うためのツールセットを提供します．

## 機能

### hs_to_rgb

HSIデータをRGB画像として可視化します．

- HSIファイルを読み込み，RGB画像に変換します．
- 変換されたRGB画像を本日の日付のフォルダーに保存します．

### 使用方法

`python hs_to_rgb.py [path-to-日付（例：08292024）]`

### annotation

HSIデータのアノテーションを行います．撮影ファイルに対応するJSONデータを作成し，保存します．

- ファイル名から時刻，カラーチェッカーの有無，カメラパラメータを抽出します．
- アノテーション結果をdata.jsonに保存します．既存のデータは保持され，新しいデータが追加されます．


#### 使用方法

`python annotation.py <directory> <weather>`

- directory：データが保存されている日付フォルダーのパス
- weather：撮影時の天候 (sunny, cloud, rain, snow のいずれか)