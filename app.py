from flask import Flask, request, jsonify, send_file, abort
from gpt_translate import translate
import os

app = Flask(__name__)

@app.route('/healthcheck')
def health():
    try:
        return jsonify({"status":"healthy"})
    except Exception as e:
        return jsonify({"status": "failure"})

@app.route('/rabyte-translation', methods=['POST'])
def rabyte():
    try:
        # Check if the post request has the file part
        if 'file' not in request.files:
            return "No file part in the request", 400
        file = request.files['file']

        # Check if additional data is provided
        profanity = request.form.get('remove_profanity', 'No')
        language = request.form.get('language', 'English')

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return "No selected file", 400
        
        if file and file.filename.endswith('.mp4'):
            # Save the file (optionally process it before saving)
            filepath = os.path.join('/videos', file.filename)
            file.save(filepath)
            
            # Optionally process the file here
            translate(file.filename, profanity, language)
            # Send the file back
            return send_file(filepath, as_attachment=True, attachment_filename=file.filename)
        
        return "Invalid file format", 400
    except Exception as e:
        return "Error occurred", 500

if __name__ == '__main__':  
   app.run()