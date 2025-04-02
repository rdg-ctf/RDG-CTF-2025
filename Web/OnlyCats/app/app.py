from flask import Flask, request, jsonify, render_template
from flask_basicauth import BasicAuth

from os import getenv

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'cat' 
app.config['BASIC_AUTH_PASSWORD'] = 'icr34t3d0nlyc4tsjustt0sh4res0m3c4tp1ctur3s'  
basic_auth = BasicAuth(app)

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
@basic_auth.required
def admin():
    flag = getenv('FLAG')  
    return render_template('admin.html', flag = flag)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)