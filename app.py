from flask import Flask, render_template, request, jsonify
from commands import execute_command

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    result = execute_command(user_msg)

    # if command returns dict (url etc.)
    if isinstance(result, dict):
        return jsonify(result)

    # normal text reply
    return jsonify({"reply": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
