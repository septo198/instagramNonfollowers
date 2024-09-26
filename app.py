from flask import Flask, render_template, request, jsonify, send_file, make_response
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
    response = make_response(jsonify(message=message))
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/get_followers', methods=['POST'])
def get_followers_route():
    followers_dict = get_followers()
    response = make_response(jsonify(followers=followers_dict))
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/get_followings', methods=['POST'])
def get_followings_route():
    followings_dict = get_followings()
    response = make_response(jsonify(followings=followings_dict))
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/determine_nonfollowers', methods=['POST'])
def determine_nonfollowers_route():
    data = request.get_json()
    followers_dict = data['followers']
    followings_dict = data['followings']
    nonfollowers = determine_nonfollowers(followers_dict, followings_dict)
    response = make_response(jsonify(nonfollowers=nonfollowers))
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/proxy_image')
def proxy_image():
    url = request.args.get('url')
    response = requests.get(url)
    return send_file(BytesIO(response.content), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)