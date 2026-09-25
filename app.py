from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def gen():
    # only grab from text box now, no file handling needed
    text_data = request.form.get('text', '')

    if not text_data.strip():
        return jsonify({"success": False, "error": "bro u pasted nothing smh"})
    
    # split text into clean sentences
    sentences = [s.strip() for s in text_data.replace('\n', ' ').split('.') if len(s.strip()) > 15]
    
    if len(sentences) < 4:
        return jsonify({"success": False, "error": "need more text (at least 4 proper sentences) to make a quiz!"})

    random.shuffle(sentences)
    my_mcqs = []
    num_q = min(3, len(sentences))

    for i in range(num_q):
        correct_sent = sentences[i]
        
        # use other lines from the pasted text as wrong choices
        other_sentences = [s for s in sentences if s != correct_sent]
        wrong_choices = random.sample(other_sentences, min(3, len(other_sentences)))
        
        while len(wrong_choices) < 3:
            wrong_choices.append("This option is completely unrelated to your text.")

        options = wrong_choices + [correct_sent]
        random.shuffle(options)
        correct_index = options.index(correct_sent)

        my_mcqs.append({
            "id": i + 1,
            "question": "Based on your notes, which of the following statements is correct?",
            "options": options,
            "correct": correct_index
        })

    return jsonify({"success": True, "mcqs": my_mcqs})

if __name__ == '__main__':
    app.run(debug=True)