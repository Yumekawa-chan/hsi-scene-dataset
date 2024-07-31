import os
import time
import json
import re
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys

# JSONファイルのパス
json_file_path = 'data.json'

# 監視するフォルダのパス
path = sys.argv[1]
dark_path = os.path.join(path, "dark")

# JSONファイルが存在しない場合は空のリストで初期化
if not os.path.exists(json_file_path):
    with open(json_file_path, 'w') as f:
        json.dump([], f)

# hs_dataフォルダが存在しない場合は作成
if not os.path.exists(path):
    os.makedirs(path)

# darkフォルダが存在しない場合は作成
if not os.path.exists(dark_path):
    os.makedirs(dark_path)

# ファイル名から情報を抽出する正規表現
filename_pattern = re.compile(r'Scan-d\(s(\d+),g(\d+),([\d\.]+)ms,(\d+-\d+)\)_(\d{8})_(\d{6})\.nh9')

# イベントハンドラ
class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith('.nh9'):
            process_file(event.src_path)

# 半角文字のみを許可し、空入力を許可しない関数
def input_halfwidth(prompt):
    while True:
        value = input(prompt)
        if value and all(ord(char) < 128 for char in value):
            return value
        else:
            print("半角文字で入力してください。")

# カラーチェッカーの有無を検証する関数
def input_yes_no(prompt):
    while True:
        value = input(prompt).lower()
        if value in ['yes', 'no']:
            return value
        else:
            print("yes か no を入力してください。")

# ファイル処理関数
def process_file(file_path):
    file_name = os.path.basename(file_path)
    if file_name.startswith('Dark'):
        # ファイルがアクセス可能になるまで待機
        while True:
            try:
                shutil.move(file_path, os.path.join(dark_path, file_name))
                print(f"ファイル {file_name} を {dark_path} に移動しました。")
                break
            except PermissionError:
                print(f"黒画像補正データを検出！処理中・・・")
                time.sleep(5)
    else:
        match = filename_pattern.match(file_name)
        if match:
            # 自動抽出情報
            camera_param = {
                's': match.group(1),
                'g': match.group(2),
                'exposure': match.group(3),
                'wavelength': match.group(4)
            }

            # タイムスタンプの抽出
            date = match.group(5)
            time_str = match.group(6)
            timestamp = f"{date[:4]}-{date[4:6]}-{date[6:8]} {time_str[:2]}:{time_str[2:4]}:{time_str[4:6]}"

            # 手動入力情報
            weather = input_halfwidth("天気(s/c/r): ")
            location = input_halfwidth("場所: ")
            has_color_checker = input_yes_no("カラーチェッカーの有無 (yes/no): ")

            # データの構造
            data_entry = {
                'file_name': file_name,
                'timestamp': timestamp,
                'weather': weather,
                'location': location,
                'has_color_checker': has_color_checker.lower() == 'yes',
                'camera_param': camera_param
            }

            # JSONファイルに追加W
            with open(json_file_path, 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                data.append(data_entry)
                f.seek(0)
                json.dump(data, f, indent=4)

if __name__ == "__main__":
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    print("Monitoring...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
