import requests
import json
import csv

# 🔑 你的 Spotify API 資訊（要自己填）
CLIENT_ID = "58117acacb3d404ea8c18505f509bf97"
CLIENT_SECRET = "68c15ddce70a436a9eee7c7ace8a39dc"

# 🎤 Fujii Kaze 的 Artist ID
ARTIST_ID = "6bDWAcdtVR3WHz2xtiIPUi"

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    response = requests.post(url, {
        "grant_type": "client_credentials"
    }, auth=(CLIENT_ID, CLIENT_SECRET))

    return response.json()["access_token"]


def get_top_tracks(token):
    url = f"https://api.spotify.com/v1/artists/{ARTIST_ID}/top-tracks?market=JP"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()


def save_json(data):
    with open("fujii_kaze_tracks.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_csv(data):
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

    print("抓取 Fujii Kaze 熱門歌曲...")
    data = get_top_tracks(token)

    print("儲存 JSON...")
    save_json(data)

    print("儲存 CSV...")
    save_csv(data)

    print("完成！")


if __name__ == "__main__":
    main()