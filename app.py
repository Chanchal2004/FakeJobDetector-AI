import os
import pickle
from flask import Flask, request, render_template

# Disable TensorFlow logs
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

app = Flask(__name__)

# Safe tokenizer loading
try:
    print("Loading tokenizer...")

    with open("tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)

    print("Tokenizer loaded!")

except Exception as e:
    print("Tokenizer loading failed:", e)
    tokenizer = None

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    combined_text = request.form.get("combined_text")

    if not combined_text:
        return render_template(
            "index.html",
            prediction="Please enter the job description."
        )

    text = combined_text.lower()

    # AI-like scam logic
    scam_keywords = [
        "registration fee",
        "refundable deposit",
        "deposit required",
        "pay fee",
        "training fee",
        "whatsapp",
        "telegram",
        "quick money",
        "earn money",
        "no experience required",
        "work from home",
        "limited seats",
        "immediate hiring",
        "international clients",
        "easy income",
        "guaranteed job"
    ]

    score = 0
    matched_keywords = []

    for word in scam_keywords:
        if word in text:
            score += 1
            matched_keywords.append(word)

    if score >= 2:
        result = "⚠ Fraudulent Job Post Detected"

        explanation = f"""
Reasons:
- Suspicious wording detected
- Possible scam tactics
- Unrealistic promises or urgency

Detected Keywords:
{', '.join(matched_keywords)}
"""

    else:
        result = "✅ Legitimate Looking Job Post"

        explanation = """
No major scam indicators detected.
"""

    return render_template(
        "index.html",
        prediction=result,
        explanation=explanation
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
