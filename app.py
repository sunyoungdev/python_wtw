from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

app = Flask(__name__)

# URL 별로 함수명이 같거나,
# route('/') 등의 주소가 같으면 안됩니다.
client = MongoClient('localhost', 27017)
db = client.wtw


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/detail')
def detail():
    return render_template('detail.html')


@app.route('/search', methods=['GET'])
def get_filmlists():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    result = list(db.film_list.find({}, {'_id': 0}))

    # 2. filmlists라는 키 값으로 filmlists 정보 보내주기
    return jsonify({'result': 'success', 'filmlists': result})







if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
