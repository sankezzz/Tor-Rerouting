from flask import Flask, request, Response
import requests

app = Flask(__name__)

# The site you want to mirror
TARGET_SITE = "https://crypto-track-vault-ahsaasd5.replit.app"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def proxy(path):
    url = f"{TARGET_SITE}/{path}"

    # Forward method, headers, and data
    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for key, value in request.headers if key.lower() != 'host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    # Exclude problematic headers
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    # Return the response to the client
    response = Response(resp.content, resp.status_code, headers)
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
