from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import urllib3
import os

# Tắt cảnh báo SSL nếu dùng verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# ScraperAPI Key (có thể thay bằng biến môi trường nếu cần)
SCRAPER_API_KEY = "92b2061e42f8148790a1d3d2d2ad32bb"

@app.route("/scrape", methods=["GET"])
def scrape():
    url = request.args.get("url")

    if not url:
        return jsonify({"status": "error", "message": "Missing URL parameter ?url=..."}), 400

    try:
        # Tạo URL ScraperAPI
        scrape_url = f"https://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={url}&render=true"

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"
        }

        # Gửi request đến ScraperAPI (tăng timeout + bỏ kiểm tra SSL)
        response = requests.get(
            scrape_url,
            headers=headers,
            timeout=(10, 60),  # (connect timeout, read timeout)
            verify=False
        )

        if response.status_code != 200:
            return jsonify({"status": "error", "message": f"ScraperAPI error: HTTP {response.status_code}"}), 502

        # Parse nội dung bằng BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        return jsonify({
            "status": "success",
            "source_url": url,
            "length": len(text),
            "content": text[:3000]  # Giới hạn độ dài trả về
        })

    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "message": "Scraping timeout (server may be slow)"}), 504

    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Request error: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"✅ API running at http://0.0.0.0:{port}/scrape?url=https://...")
    app.run(debug=True, host="0.0.0.0", port=port)
