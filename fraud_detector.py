import os
import google.generativeai as genai
from datetime import datetime

# Load API key from environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not found. Please set it before running.")

genai.configure(api_key=GEMINI_API_KEY)

class FraudDetector:
    def __init__(self):
        # You can customize model here if needed
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")

    def predict(self, text):
        """
        Sends text to Gemini model and expects a fraud probability + reasons.
        Returns: (fraud_probability, reasons_list)
        """
        if not text or len(text.strip()) == 0:
            return 0.0, ["Empty input"]

        prompt = f"""
        You are a fraud detection AI. Analyze the following text for fraud risk. See if email is spam or not. Also take out words which shows its a spam or not.
        Summarize the email and also tell the priority of that email. 
        today date is {datetime.now()}
        Return ONLY a JSON response. No explanation outside of JSON.

        Text to analyze:
        \"\"\"{text}\"\"\"

        **Respond ONLY in this JSON format:**
        {{
        "fraud_probability": <number between 0 and 1>,
        "reasons": ["list of reasons why it is risky or safe"]
        "priority":<"High"/"Medium"/"Low">
        "summary" : <summary(make it either 2/3 size of content or 1 line summary whatever is bigger)> 


        }}
        """

        try:
            response = self.model.generate_content(prompt)

            # Extract response text safely
            result_text = response.text.strip()

            # Some Gemini responses may include ```json ... ``` wrapper → clean it
            if result_text.startswith("```"):
                import re
                result_text = re.sub(r"```json|```", "", result_text).strip()

            # Parse JSON safely
            import json
            result = json.loads(result_text)

            fraud_prob = float(result.get("fraud_probability", 0.0))
            reasons = result.get("reasons", [])
            if not isinstance(reasons, list):
                reasons = [str(reasons)]
            summary= str(result.get("summary"))
            priority= str(result.get("priority"))
            return fraud_prob, reasons, priority, summary

        except Exception as e:
            # Failure fallback
            return 0.5, [f"⚠ Gemini analysis failed: {str(e)}"]

