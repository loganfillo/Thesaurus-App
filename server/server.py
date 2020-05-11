import os

from process_text import InputTextProcessor
processer = InputTextProcessor()

from flask import Flask, jsonify, send_from_directory, request, abort
app = Flask(__name__, static_folder=(os.path.join(os.getcwd(), 'client', 'build')),  static_url_path='/')


"""
Returns the index.html of the build of the React client
"""
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


"""
Processes the input text recieved as the payload of a Post request from the web client.

If the request is json and has the inputText key, processes the text and returns a json
response with outputText being the processed text, otherwise aborts with error code 500
"""
@app.route('/process-text', methods=['Post'])
def process_text_endpoint():
    if request.is_json and 'inputText' in request.get_json().keys():
        input_text = request.get_json()['inputText']
        return jsonify({"outputText" : processer.process(input_text)})
    else:
        abort(500)


if __name__ == "__main__":
    app.run(debug=True)