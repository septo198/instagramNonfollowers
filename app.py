from flask import Flask, render_template, request, jsonify
from main import get_nonfollowers

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_nonfollowers', methods=['POST'])
def get_nonfollowers_route():
    data = request.get_json()
    username = data['username']
    password = data['password']
    nonfollowers = get_nonfollowers(username, password)
    return jsonify(nonfollowers=nonfollowers)

if __name__ == '__main__':
    app.run(debug=True)