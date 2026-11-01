from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/purelily')
def purelily():
    return render_template('purelily.html')

@app.route('/mogra')
def mogra():
    return render_template('mogra.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
