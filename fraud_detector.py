import os
import google.generativeai as genai

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
        You are a fraud detection AI. Analyze the following text for business fraud risk.
        Return ONLY a JSON response. No explanation outside of JSON.

        Text to analyze:
        \"\"\"{text}\"\"\"

        **Respond ONLY in this JSON format:**
        {{
        "fraud_probability": <number between 0 and 1>,
        "reasons": ["list of reasons why it is risky or safe"]
        "Prority":["High"/"Medium"/"Low"]
        

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

            return fraud_prob, reasons

        except Exception as e:
            # Failure fallback
            return 0.5, [f"⚠ Gemini analysis failed: {str(e)}"]

