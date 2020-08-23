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


# @app.route('/search', methods=['GET'])
# def get_filmlists():
#     # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
#     result = list(db.film_list.find({}, {'_id': 0}))
#
#     # 2. filmlists라는 키 값으로 filmlists 정보 보내주기
#     return jsonify({'result': 'success', 'filmlists': result})



# 검색어와 일치하는 영화 리스트 조회
@app.route('/search', methods=['GET'])
def find_matches():
    title_receive = request.args.get('search-title')
    match_array = list(db.film_list.find({'title': title_receive}, {'_id': False}))

    # return jsonify({'result': 'success', 'title_receive': title_receive})
    return render_template('index.html')





# 전달받은 path 값으로 poster url 크롤링
# @app.route('/search', methods=['POST'])
# def show_posters():
#     path_receive = request.form['path_give']
#     # 크롤링
#
#     # posters 응답 데이터 보내주기
#     return jsonify({'result': 'success', 'posters': posters})






if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
