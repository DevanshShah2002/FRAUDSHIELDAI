from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
import os
from fraud_detector import FraudDetector
from vendor_check import vendor_trust_score
from pathlib import Path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

detector = FraudDetector()

# In-memory "database" for uploads
uploads = []

@app.route('/')
def index():
    return render_template('index.html', uploads=reversed(uploads))

@app.route('/upload_invoice', methods=['POST'])
def upload_invoice():
    vendor_domain = request.form.get('vendor_domain', '')
    text = request.form.get('invoice_text', '')
    text= "domain:" + vendor_domain + "\n Body text:" + text
    fraud_prob, reasons = detector.predict(text)
    entry = {
        'vendor_domain': vendor_domain,
        'fraud_prob': float(fraud_prob),
        'reasons': reasons,
    }
    uploads.append(entry)
    return redirect(url_for('index'))

@app.route('/api/check_email', methods=['POST'])
def api_check_email():
    data = request.json or {}
    subject = data.get('subject','')
    body = data.get('body','')
    text = subject + '\n' + body
    fraud_prob, reasons = detector.predict(text)
    return jsonify({'fraud_prob': float(fraud_prob), 'reasons': reasons})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
