import os

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    msg = 'Hello! I\'m running on: {}\n'.format(os.getenv('RELEASE', 'master'))
    return msg


@app.route('/health')
def health():
    return 'OK\n'

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host, port)
