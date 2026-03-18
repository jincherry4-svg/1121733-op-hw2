# -*- coding: utf-8 -*-
import requests
import json
import csv

# 🔑 你的 Spotify API 資訊
CLIENT_ID = "58117acacb3d404ea8c18505f509bf97"
CLIENT_SECRET = "68c15ddce70a436a9eee7c7ace8a39dc"

# 🎤 Fujii Kaze 的 Artist ID
ARTIST_ID = "6bDWAcdtVR3WHz2xtiIPUi"

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    # 使用 data 傳送 grant_type，並使用 auth 參數處理 Basic Auth
    response = requests.post(
        url, 
        data={"grant_type": "client_credentials"}, 
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    
    res_data = response.json()
    if "access_token" not in res_data:
        print("認證失敗，請檢查 Client ID/Secret:", res_data)
        return None
    return res_data["access_token"]

def get_top_tracks(token):
    # 確保使用 https
    url = f"https://api.spotify.com/v1/artists/{ARTIST_ID}/top-tracks?market=JP"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def save_json(data):
    with open("fujii_kaze_tracks.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_csv(data):
    # 關鍵修正：先檢查有沒有 'tracks' 這個 Key
    if "tracks" not in data:
        print("錯誤：回傳資料中找不到 'tracks'。API 回傳內容為：", data)
        return

    tracks = data["tracks"]
    with open("fujii_kaze_tracks.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["歌曲名稱", "專輯名稱", "人氣"])
        for track in tracks:
            writer.writerow([
                track["name"],
                track["album"]["name"],
                track["popularity"]
            ])

def main():
    print("取得 Access Token...")
    token = get_access_token()
    if not token:
        return

    print("抓取 Fujii Kaze 熱門歌曲...")
    data = get_top_tracks(token)

    # 檢查是否 API 報錯
    if "error" in data:
        print("抓取失敗:", data["error"])
        return

    print("儲存 JSON...")
    save_json(data)

    print("儲存 CSV...")
    save_csv(data)

    print("完成！檔案已生成：fujii_kaze_tracks.json, fujii_kaze_tracks.csv")

if __name__ == "__main__":
    main()
