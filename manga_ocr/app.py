from flask import Flask, request
import json
from mangaocr import perform_ocr, reformat_coords
import config

app = Flask(__name__)

@app.route("/mangaocr",methods=["GET", "POST"])
def main():
    data = request.get_json(force=True)
    #data = json.loads(data)
    coords = data['coords_path']
    folder_path = data['images_path']
    word_coords = perform_ocr(coords, folder_path)
    reformated_output = reformat_coords(word_coords)
    return json.dumps(reformated_output)

if __name__ == '__main__':
    app.run(config.IP, config.PORT, debug=True, threaded=True)
