import json
from datetime import datetime

# JSONファイルを読み込む関数
def load_data_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# 時間をカテゴリー分けする関数
def categorize_time(time):
    morning_start = datetime.strptime("06:00:00", "%H:%M:%S").time()
    morning_end = datetime.strptime("11:00:00", "%H:%M:%S").time()
    afternoon_start = datetime.strptime("11:00:00", "%H:%M:%S").time()
    afternoon_end = datetime.strptime("17:00:00", "%H:%M:%S").time()

    if morning_start <= time < morning_end:
        return 'morning'
    elif afternoon_start <= time < afternoon_end:
        return 'afternoon'
    else:
        return 'night'

# データを読み込む
data = load_data_from_json('data.json')

# 朝・昼・夜のカウントを初期化
counts = {"morning": 0, "afternoon": 0, "night": 0}

# 各エントリーの時間を確認してカウントを更新
for entry in data:
    # 'date_time' を datetime オブジェクトに変換
    date_time = datetime.strptime(entry['date_time'], "%Y.%m.%d.%H.%M.%S")
    # 時間帯を判定
    time_of_day = categorize_time(date_time.time())
    # カウントを更新
    counts[time_of_day] += 1

# 結果を出力
print("Time of Day Counts:")
for period, count in counts.items():
    print(f"{period}: {count}")
