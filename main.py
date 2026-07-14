from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("API_Key_GROQ")

client = Groq(api_key=api_key)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def Ask():
    question = request.form.get("question")

    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
        messages = [
            {
                "role": "system",
                "content": "Act like helpful personal assistant",
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        temperature = 0.7,
        max_tokens = 512
    )
    answer = response.choices[0].message.content.strip()
    return jsonify({"response": answer}), 200

@app.route("/summarize", methods=["POST"])
def summary():
    email_text = request.form.get("email")
    prompt = f"summarize the email into 2-3 lines.. {email_text}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages = [
            {
                "role": "system",
                "content": "Act like personal summarize assistant",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature = 0.7,
        max_tokens = 512
    )
    summary = response.choices[0].message.content.strip()
    return jsonify({"response": summary}), 200

if __name__ == "main":
    app.run(debug=True)