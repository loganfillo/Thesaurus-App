import os
import time

from dotenv import load_dotenv
load_dotenv()

from .process_text import InputTextProcessor
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
    start = time.time()
    if request.is_json and 'inputText' in request.get_json().keys():
        input_text = request.get_json()['inputText']
        output_text = processer.process(input_text)
        end = time.time()
        print("Total time for request: ", end-start )
        return jsonify({"outputText" : output_text})
    else:
        abort(500)


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='0.0.0.0',debug=True)