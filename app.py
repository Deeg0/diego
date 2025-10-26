from flask import Flask, request, jsonify, send_from_directory
import requests, os

app = Flask(__name__, static_folder="static")

# Serve the HTML file
@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

# ChatGPT endpoint
@app.post("/chat")
def chat():
    msg = request.json.get("message", "")
    if not msg:
        return jsonify({"reply": "Empty message"}), 400

    try:
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-5",
                "messages": [{"role": "user", "content": msg}]
            }
        )
        data = r.json()
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

