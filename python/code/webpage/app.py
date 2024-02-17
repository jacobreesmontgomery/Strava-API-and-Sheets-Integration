"""
CLASS: app.py
AUTHOR: Jacob Montgomery
OVERVIEW: This file will drive the front-end webpage.
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/basic_stats')
def basic_stats():
    return render_template('basic_stats.html')

@app.route('/database')
def database():
    return render_template('database.html')

if __name__ == '__main__':
    app.run(debug=True)

