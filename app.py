from flask import Flask, render_template, request, jsonify, send_file
from main import login, get_followers, get_followings, determine_nonfollowers
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    username = data['username']
    password = data['password']
    message = login(username, password)
    return jsonify(message=message)

@app.route('/get_followers', methods=['POST'])
def get_followers_route():
    followers_dict = get_followers()
    return jsonify(followers=followers_dict)

@app.route('/get_followings', methods=['POST'])
def get_followings_route():
    followings_dict = get_followings()
    return jsonify(followings=followings_dict)

@app.route('/determine_nonfollowers', methods=['POST'])
def determine_nonfollowers_route():
    data = request.get_json()
    followers_dict = data['followers']
    followings_dict = data['followings']
    nonfollowers = determine_nonfollowers(followers_dict, followings_dict)
    return jsonify(nonfollowers=nonfollowers)

@app.route('/proxy_image')
def proxy_image():
    url = request.args.get('url')
    response = requests.get(url)
    return send_file(BytesIO(response.content), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)