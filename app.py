from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
          #Naah! it sucks 
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def gen():
    text_data = ""
    
    # upload section yoo
    if 'file' in request.files and request.files['file'].filename != '':
        f = request.files['file']
        text_data = f.read().decode('utf-8', errors='ignore')
    else:
        text_data = request.form.get('text', '')

    if text_data == "":
        return jsonify({"success": False, "error": "bro u wrote nothing"})
    
    # just split by new line
    lines = text_data.split('\n')
    
    my_mcqs = []
    count = 1
    for line in lines:
        if len(line) > 4: # ignore short lines
            my_mcqs.append({
                "id": count,
                "question": "What does this mean: " + line,
                "options": [
                    line,
                    "wrong option 1",
                    "wrong option 2",
                    "idk"
                ],
                "correct": 0 # first one is always correct
            })
            count = count + 1
            if count > 5: # stop at 5 questions
                break

    if len(my_mcqs) == 0:
        return jsonify({"success": False, "error": "text too short or empty lines only"})

    return jsonify({"success": True, "mcqs": my_mcqs})

if __name__ == '__main__':
    app.run(debug=True)