from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from db import get_db_connection
import json
from werkzeug.utils import secure_filename
import docx
import os
from apscheduler.schedulers.background import BackgroundScheduler
import time
import atexit


app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "*"}, r"/uploads/*": {"origins": "*"}})

# Get the absolute path to the parent folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # summariser-backend
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def home():
    return "Server is running!"

@app.route('/api/templates', methods=['POST'])
def save_template():
    data = request.get_json()
    template_name = data.get('templateName')
    style = data.get('style')
    sections = data.get('sections')

    if not template_name or not sections:
        return jsonify({'error': 'Missing fields'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO templates (template_name, style, structure) VALUES (%s, %s, %s)",
        (template_name, style, json.dumps(sections))
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': 'Template saved successfully'}), 201


@app.route('/api/templates', methods=['GET'])
def get_templates():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, template_name, style, structure FROM templates')
    rows = cur.fetchall()
    cur.close()
    conn.close()

    templates = []
    for row in rows:
        templates.append({
            'id': row[0],
            'name': row[1],
            'style': row[2],
            'structure': row[3]
        })

    return jsonify(templates)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return jsonify({'filename': filename, 'url': f'/uploads/{filename}'})
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/uploads/<filename>')
@cross_origin()
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/preview/<filename>')
@cross_origin()
def preview_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    ext = filename.rsplit('.', 1)[1].lower()
    
    if ext == 'txt':
        with open(filepath, 'r', encoding='utf-8') as f:
            return jsonify({'content': f.read()})
    elif ext == 'docx':
        doc = docx.Document(filepath)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return jsonify({'content': text})
    else:
        return jsonify({'error': 'Unsupported preview format'}), 400

EXPIRY_SECONDS = 60 * 60 *24  # 1 day
def cleanup_uploads():
    now = time.time()
    for filename in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(path):
            age = now - os.path.getmtime(path)
            if age > EXPIRY_SECONDS:
                os.remove(path)
                print(f"Deleted expired file: {filename}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=cleanup_uploads, trigger="interval", hours = 12)
scheduler.start()

# === Ensure scheduler stops on shutdown ===
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True)
