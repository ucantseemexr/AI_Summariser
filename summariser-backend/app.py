from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
from flask_cors import CORS, cross_origin
from db import get_db_connection
import json
from werkzeug.utils import secure_filename
import docx
import os
from apscheduler.schedulers.background import BackgroundScheduler
import time
import atexit
from llm import generate_summary, stream_summary, convert_to_JSON, flatten_json_to_text, stream_summary
from build_prompt import build_prompt, examples
from PyPDF2 import PdfReader
from build_adjustment_prompt import build_adjustment_prompt
from FAISS import chunk_text, build_faiss_index, retrieve_relevant_chunks
from extract_docx_content import extract_docx_content
from extract_pdf_content import extract_pdf_content

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

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
            content = []
            content.append({"type": "paragraph", "text": f.read()})
            return jsonify({'content': content})
    elif ext == 'docx':
        content = extract_docx_content(filepath)
        return jsonify({'content': content})
    elif ext == 'pdf':
        content = extract_pdf_content(filepath)
        return jsonify({'content': content})
    else:
        return jsonify({'error': 'Unsupported preview format'}), 400



@app.route('/api/summarise', methods=['POST'])
def summarise():
    data = request.get_json()
    raw_text = data['text']
    sections = data['sections']
    
    sectionSummaries = {}  # To collect all sections' summaries
    full_summary = ''
    for section in sections:
        # Wrap each section into the same format expected by build_prompt
        single_section_structure = [section]  
        # Construct prompt based on individual section
        prompt = build_prompt(raw_text, single_section_structure)
        section_summary = generate_summary(prompt, "summary")
        title = section['title']
        sectionSummaries[title] = section_summary.strip()
        full_summary += f"{section_summary.strip()}\n\n"
    
        
    return sectionSummaries

@app.route('/api/adjust_summary', methods=['POST'])
@cross_origin()
def adjust_summary():
    data = request.get_json()
    
    content = data.get('text', '')
    sections = data.get('sections', [])
    original_summaries = data.get('originalSummaries', {})

    if not content or not sections or not original_summaries:
        return jsonify({'error': 'Missing required fields'}), 400

    raw_texts = []
    for block in content:
        if block["type"] == "paragraph":
            raw_texts.append(block["text"])
        else:
            JSON_data = convert_to_JSON(block["rows"])
            print(JSON_data)
            if isinstance(JSON_data, list):
                print('=== is list ===')
                all_texts = [flatten_json_to_text(blks) for blks in JSON_data]
                plain_text = "\n".join(all_texts)
            else:
                plain_text = flatten_json_to_text(JSON_data)
            raw_texts.append(plain_text)
    all_text = "\n".join(raw_texts)
    print(all_text)
    all_chunks = chunk_text(all_text)
    index, embeddings, chunk_list = build_faiss_index(all_chunks)
    
    section = sections[0]
    section_title = section["title"]
    query = f"{section_title}\n"
    print("section:", section)
    print("subsections:", section["subsections"])
    for instruction in section["subsections"]:
        query += f"{instruction}\n"
    print("query:" + query)
    
    if section_title == 'Paragraph Summary' or section_title == 'Bullet Point Summary':
            relevant_chunks = all_chunks
    else:
        relevant_chunks = retrieve_relevant_chunks(index, chunk_list, query)
    input_text = "\n\n".join(relevant_chunks)
    
    # Construct prompt using the revised template
    prompt = build_adjustment_prompt(
        text=input_text,
        sections=sections,
        original_summary_by_section=original_summaries,
        
    )

    # Generate updated summary from model
    revised_output = generate_summary(prompt, "adjusted")

    # You can optionally parse the output per section, but here we return raw string
    return jsonify({"revised_summary": revised_output.strip()})

@app.route('/api/summarise_FAISS', methods=['POST'])
def generate_summary_FAISS():
    data = request.get_json()
    content = data['text']
    sections = data['sections']
    raw_texts = []
    for block in content:
        if block["type"] == "paragraph":
            raw_texts.append(block["text"])
        else:
            JSON_data = convert_to_JSON(block["rows"])
            print(JSON_data)
            if isinstance(JSON_data, list):
                print('=== is list ===')
                all_texts = [flatten_json_to_text(blks) for blks in JSON_data]
                plain_text = "\n".join(all_texts)
            else:
                print('=== is not list ===')
                plain_text = flatten_json_to_text(JSON_data)
            raw_texts.append(plain_text)
    all_text = "\n".join(raw_texts)
    print(all_text)
    all_chunks = chunk_text(all_text)
    index, embeddings, chunk_list = build_faiss_index(all_chunks)
    
    sectionSummaries = {}  # To collect all sections' summaries
    
    for section in sections:
        section_title = section["title"]
        # Wrap each section into the same format expected by build_prompt
        single_section_structure = [section]
        
        query = f"{section_title}\n"
        
        for instruction in section["subsections"]:
            query += f"{instruction}\n"
        if section_title == 'Paragraph Summary' or section_title == 'Bullet Point Summary':
            relevant_chunks = all_chunks
        else:
            relevant_chunks = retrieve_relevant_chunks(index, chunk_list, query)
        input_text = "\n\n".join(relevant_chunks)
         # Construct prompt based on individual section
        prompt = build_prompt(input_text, single_section_structure)
        section_summary = generate_summary(prompt, "summary")
        sectionSummaries[section_title] = section_summary.strip()
        
    return sectionSummaries

@app.route('/stream-summary', methods=['POST'])
def stream_summary_route():
    data = request.get_json()
    content = data['text']
    sections = data['sections']
    raw_texts = []
    for block in content:
        if block["type"] == "paragraph":
            raw_texts.append(block["text"])
        else:
            JSON_data = convert_to_JSON(block["rows"])
            print(JSON_data)
            if isinstance(JSON_data, list):
                print('=== is list ===')
                all_texts = [flatten_json_to_text(blks) for blks in JSON_data]
                plain_text = "\n".join(all_texts)
            else:
                print('=== is not list ===')
                plain_text = flatten_json_to_text(JSON_data)
            raw_texts.append(plain_text)
    all_text = "\n".join(raw_texts)
    print(all_text)
    all_chunks = chunk_text(all_text)
    index, embeddings, chunk_list = build_faiss_index(all_chunks)
    
    for section in sections:
        section_title = section["title"]
        # Wrap each section into the same format expected by build_prompt
        single_section_structure = [section]
        
        query = f"{section_title}\n"
        
        for instruction in section["subsections"]:
            query += f"{instruction}\n"
        if section_title == 'Paragraph Summary' or section_title == 'Bullet Point Summary':
            relevant_chunks = all_chunks
        else:
            relevant_chunks = retrieve_relevant_chunks(index, chunk_list, query)
        input_text = "\n\n".join(relevant_chunks)
         # Construct prompt based on individual section
        prompt = build_prompt(input_text, single_section_structure)

    def generate():
        for chunk in stream_summary(prompt):
            print(chunk, end =' ', flush = True)
            yield chunk.encode("utf-8")

    return Response(generate(), mimetype='text/plain')  # or 'text/event-stream'
        
    

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
