import json
from collections import Counter

# data.json を読み込む
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# location を抽出してリスト化
locations = [entry['location'] for entry in data]

# location ごとにデータ数をカウント
location_counts = Counter(locations)

# 結果を表示
for location, count in location_counts.items():
    print(f"{location}: {count}")
