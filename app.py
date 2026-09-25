from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def gen():
    text_data = ""
    
    # check file upload
    if 'file' in request.files:
        f = request.files['file']
        if f.filename != '':
            try:
                text_data = f.read().decode('utf-8', errors='ignore')
            except Exception as e:
                return jsonify({"success": False, "error": "File read error: " + str(e)})
    
    # check text area input
    if not text_data.strip():
        text_data = request.form.get('text', '')

    if not text_data.strip():
        return jsonify({"success": False, "error": "Bro u need to type text or upload a file first!"})
    
    # Split text into clean sentences based on periods
    sentences = [s.strip() for s in text_data.replace('\n', ' ').split('.') if len(s.strip()) > 15]
    
    if len(sentences) < 4:
        return jsonify({"success": False, "error": "Text is too short! Please provide at least 4 proper sentences so I can make choices."})

    # Shuffle sentences so we pick different facts every time
    random.shuffle(sentences)
    
    my_mcqs = []
    num_questions = min(3, len(sentences))

    for i in range(num_questions):
        correct_sent = sentences[i]
        
        # Use other actual sentences from your notes as the wrong options (distractors)
        other_sentences = [s for s in sentences if s != correct_sent]
        wrong_choices = random.sample(other_sentences, min(3, len(other_sentences)))
        
        # Fallback padding if text is slightly short on sentences
        while len(wrong_choices) < 3:
            wrong_choices.append("This option is completely unrelated to your notes.")

        # Combine correct answer with wrong choices and shuffle them
        options = wrong_choices + [correct_sent]
        random.shuffle(options)
        correct_index = options.index(correct_sent)

        my_mcqs.append({
            "id": i + 1,
            "question": f"Based on your notes, which of the following statements is true?",
            "options": options,
            "correct": correct_index
        })

    return jsonify({"success": True, "mcqs": my_mcqs})

if __name__ == '__main__':
    app.run(debug=True)