from mitmproxy import http
import httpx
import json

API_URL = "http://localhost:8000/api/predict"


def request(flow: http.HTTPFlow):
    if flow.request.pretty_host in ["localhost", "127.0.0.1"]:
        return

    url = flow.request.pretty_url

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(API_URL, json={"url": url})
            result = response.json()

            if result.get("is_phishing"):
                flow.response = http.Response.make(
                    403,
                    b"<h1>Blocked: Phishing URL Detected</h1><p>This site was blocked by the Phishing Detector.</p>",
                    {"Content-Type": "text/html"}
                )
    except Exception as e:
        print(f"Proxy prediction error for {url}: {e}")

# run using mitmdump -s proxy/addon.py --mode regular --listen-host 127.0.0.1 --listen-port 8080
# uvicorn ml_service.main:app --reload --port 8000