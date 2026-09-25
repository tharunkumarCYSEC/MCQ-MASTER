from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def gen():
    text_data = ""
    
    # check if a file was uploaded
    if 'file' in request.files:
        f = request.files['file']
        if f.filename != '':
            try:
                text_data = f.read().decode('utf-8', errors='ignore')
            except Exception as e:
                return jsonify({"success": False, "error": "Could not read file: " + str(e)})
    
    # if no file or empty file, check text area
    if not text_data.strip():
        text_data = request.form.get('text', '')

    if not text_data.strip():
        return jsonify({"success": False, "error": "Bro u need to upload a file or type text first!"})
    
    # split text into individual sentences based on periods
    raw_sentences = [s.strip() for s in text_data.replace('\n', ' ').split('.') if len(s.strip()) > 10]
    
    if len(raw_sentences) < 3:
        return jsonify({"success": False, "error": "Text is too short! Write or upload more content so I can make 3 questions."})

    # pick up to 3 sentences from the actual text provided
    chosen_sentences = random.sample(raw_sentences, min(3, len(raw_sentences)))
    
    # create a pool of other sentences from the text to use as fake answers/distractors
    other_sentences = [s for s in raw_sentences if s not in chosen_sentences]
    if not other_sentences:
        other_sentences = [
            "This concept is completely unrelated to the core topic.",
            "This statement contradicts the provided notes entirely.",
            "This is a minor footnote not relevant to the main theme."
        ]

    my_mcqs = []

    for i, sentence in enumerate(chosen_sentences):
        # generate a proper question based on the actual note sentence
        question_text = f"According to your notes, which of the following is true regarding: \"{sentence[:45]}...\"?"
        
        correct_answer = f"Yes: {sentence}"
        
        # pick 3 wrong options from other parts of the text or generic distractors
        wrong_pool = [f"False: {s}" for s in other_sentences]
        while len(wrong_pool) < 3:
            wrong_pool.append("This option has no mention in the text provided.")
            
        selected_wrongs = random.sample(wrong_pool, 3)
        
        options = selected_wrongs + [correct_answer]
        random.shuffle(options)
        correct_index = options.index(correct_answer)

        my_mcqs.append({
            "id": i + 1,
            "question": question_text,
            "options": options,
            "correct": correct_index
        })

    return jsonify({"success": True, "mcqs": my_mcqs})

if __name__ == '__main__':
    app.run(debug=True)