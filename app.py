from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return f"<h1>CloudOps Sample App</h1><p>Build: {os.getenv('BUILD_NUMBER', 'local')}</p>"

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)