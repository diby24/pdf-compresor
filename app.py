from flask import Flask, request, send_file, render_template
import fitz  # PyMuPDF
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
COMPRESSED_FOLDER = "compressed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

def compress_pdf(input_path, output_path):
    doc = fitz.open(input_path)
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()

@app.route("/")
def upload_page():
    return render_template("index.html")

@app.route("/compress", methods=["POST"])
def compress():
    if "pdf" not in request.files:
        return "No file uploaded", 400

    pdf_file = request.files["pdf"]
    input_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    output_path = os.path.join(COMPRESSED_FOLDER, "compressed_" + pdf_file.filename)
    
    pdf_file.save(input_path)
    compress_pdf(input_path, output_path)
    
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
