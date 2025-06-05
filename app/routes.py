from flask import Blueprint, render_template, request, send_file
import os
import re
from io import BytesIO
import json
from datetime import datetime
main = Blueprint('main', __name__)
@main.route('/', methods=['GET'])
def index():
    print("🚀 Flask is running from:", os.getcwd())
    return render_template('index.html')
@main.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('logfile')
    if not file:
        return render_template('index.html', logs=[], summary={})

    log_level = request.form.get('log_level')
    keyword = request.form.get('keyword')
    content = file.read().decode('utf-8').splitlines()
    logs = []
    summary = {
        'INFO': 0,
        'ERROR': 0,
        'DEBUG': 0
    }
    pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)$'
    for line in content:
        match = re.match(pattern, line)
        if match:
            timestamp = match.group(1)
            level = match.group(2)
            message = match.group(3)

            if log_level and level != log_level:
                continue
            if keyword and keyword.lower() not in message.lower():
                continue

            summary[level] = summary.get(level, 0) + 1

            logs.append({
                'timestamp': timestamp,
                'level': level,
                'message': message
            })

    # Save filtered logs to JSON
    if not os.path.exists("saved_logs"):
        os.makedirs("saved_logs")

    save_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = f"saved_logs/logs_{save_time}.json"
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4)

    return render_template('index.html', logs=logs, summary=summary)

@main.route('/download', methods=['POST'])
def download():
    log_data = request.form.get('log_data')

    if not log_data:
        return "No data to download", 400

    byte_data = BytesIO(log_data.encode('utf-8'))

    return send_file(
        byte_data,
        as_attachment=True,
        download_name="filtered_logs.txt",
        mimetype="text/plain"
    )

@main.route('/saved')
def view_saved():
    log_files = []

    if os.path.exists('saved_logs'):
        for file in os.listdir('saved_logs'):
            if file.endswith('.json'):
                log_files.append(file)

    return render_template('saved.html', log_files=log_files)

@main.route('/show_log/<filename>')
def show_log(filename):
    filepath = os.path.join('saved_logs', filename)
    if not os.path.exists(filepath):
        return "File not found.", 404

    with open(filepath, 'r', encoding='utf-8') as f:
        logs = json.load(f)

    # Optional: calculate summary again if needed
    summary = {
        'INFO': 0,
        'ERROR': 0,
        'DEBUG': 0
    }
    for log in logs:
        level = log['level']
        summary[level] = summary.get(level,0)+ 1
    return render_template('index.html', logs=logs, summary=summary)