# app.py
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# SCRAPER_API_KEY = "YOUR_SCRAPERAPI_KEY"  # thay bằng key thực tế
SCRAPER_API_KEY = "92b2061e42f8148790a1d3d2d2ad32bb"  # 👈 bạn đã có


@app.route("/scrape", methods=["GET"])
def scrape():
    url = request.args.get("url")
    if not url:
        return jsonify({"status": "error", "message": "Missing URL"}), 400

    try:
        scrape_url = f"https://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={url}&render=true"
        response = requests.get(scrape_url, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        return jsonify({
            "status": "success",
            "length": len(text),
            "content": text[:3000]  # gới hạn 3000 ký tự
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    print("API running on http://0.0.0.0:5000/scrape?url=https://...")
    app.run(debug=True, host="0.0.0.0", port=5000)
