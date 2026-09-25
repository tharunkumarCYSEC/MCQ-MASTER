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
            text_data = f.read().decode('utf-8', errors='ignore')
    
    # check text area input
    if not text_data.strip():
        text_data = request.form.get('text', '')

    if not text_data.strip():
        return jsonify({"success": False, "error": "bro u uploaded an empty file or typed nothing smh"})
    
    # split into meaningful sentences/lines
    lines = [l.strip() for l in text_data.split('\n') if len(l.strip()) > 15]
    
    if len(lines) < 3:
        lines = [
            "Python is a popular programming language used for web development.",
            "Flask is a lightweight framework built for python applications.",
            "HTML files are rendered by browsers to display website content."
        ]

    # pick up to 3 lines
    selected = lines[:3]
    my_mcqs = []

    for i, sentence in enumerate(selected):
        words = sentence.split()
        if len(words) > 4:
            # pick a random word from the sentence to hide as the answer
            target_idx = random.randint(1, len(words) - 2)
            correct_word = words[target_idx].strip('.,')
            
            # create a fill-in-the-blank style question
            words[target_idx] = "_____"
            question_text = " ".join(words)
            
            # create fake distractors based on other words or dummy choices
            distractors = [w.strip('.,') for w in words if w.lower() != correct_word.lower() and len(w) > 3]
            while len(distractors) < 3:
                distractors.extend(["system", "process", "module", "element", "function"])
            
            selected_wrongs = random.sample(list(set(distractors)), 3)
            
            options = selected_wrongs + [correct_word]
            random.shuffle(options)
            correct_index = options.index(correct_word)
            
            my_mcqs.append({
                "id": i + 1,
                "question": f"Fill in the blank: {question_text}",
                "options": options,
                "correct": correct_index
            })
        else:
            # fallback if line is short
            my_mcqs.append({
                "id": i + 1,
                "question": f"What is true about: '{sentence}'?",
                "options": ["It is a core concept", "It is an error code", "It is deprecated syntax", "None of the above"],
                "correct": 0
            })

    return jsonify({"success": True, "mcqs": my_mcqs})

if __name__ == '__main__':
    app.run(debug=True)