from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# API Key để dùng ScraperAPI (giúp render JS)
SCRAPER_API_KEY = "92b2061e42f8148790a1d3d2d2ad32bb"  # <-- Bạn có thể cho vào biến môi trường sau

@app.route("/scrape", methods=["GET"])
def scrape():
    url = request.args.get("url")

    if not url:
        return jsonify({"status": "error", "message": "Missing URL parameter ?url=..."}), 400

    try:
        # Cấu hình URL gọi đến ScraperAPI
        scrape_url = f"https://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={url}&render=true"

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"  # giả lập trình duyệt
        }

        # Gửi yêu cầu đến ScraperAPI
        response = requests.get(scrape_url, headers=headers, timeout=30)

        if response.status_code != 200:
            return jsonify({"status": "error", "message": f"ScraperAPI error: {response.status_code}"}), 502

        # Parse nội dung HTML bằng BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        return jsonify({
            "status": "success",
            "source_url": url,
            "length": len(text),
            "content": text[:3000]  # Giới hạn 3000 ký tự
        })

    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "message": "Request timed out"}), 504

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"✅ API running at http://0.0.0.0:{port}/scrape?url=https://...")
    app.run(debug=True, host="0.0.0.0", port=port)
