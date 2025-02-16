from flask import Flask, request, render_template, send_from_directory
import os
from model_loader import predict_image

app = Flask(__name__, template_folder="templates", static_folder="static")


UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part in request", 400

        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        predictions = predict_image(file_path)

        return render_template("index.html", 
                               predictions=predictions, 
                               image_path=file_path)

    return render_template("index.html", predictions=None, image_path=None)

@app.route("/static/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

