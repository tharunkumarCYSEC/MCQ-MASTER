
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({"success": False, "error": "No text provided"})
    
    lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 3]
    
    mcqs = []
    for i, line in enumerate(lines[:3], 1):  # Keep it simple: max 3 questions for v1
        mcqs.append({
            "id": i,
            "question": f"What is the main point of: '{line}'?",
            "options": [
                "Correct: " + line,
                "An incorrect distractor option.",
                "Another unrelated concept.",
                "None of the above."
            ],
            "answer": "A"
        })
        
    return jsonify({"success": True, "mcqs": mcqs})

if __name__ == '__main__':
    app.run(debug=True, port=5000)