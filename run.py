# Author: Kiran Kumar
# Project: Flask-based Log Analyzer for Codeium Assignment
# Built from scratch with Flask, Chart.js, and Docker support
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)