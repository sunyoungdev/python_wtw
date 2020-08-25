from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.wtw


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detail')
def detail():
    return render_template('detail.html')


# 검색어와 일치하는 영화 리스트 조회
@app.route('/search', methods=['GET'])
def find_matches():
    title_receive = request.args.get('title_give')
    # db에서 title_receive 값을 포함한 db만 조회
    str = '.*' + title_receive + '.*'
    matches = list(db.film_list.find({'title': {'$regex': str, '$options': 'i'}}, {'_id': False}))

    # post url 가져오기
    match_list = []
    for match in matches:
        id = match['id']
        title = match['title']
        poster = match['poster']
        poster_url = poster.replace('{profile}', 's592')
        doc = {
            'id': id,
            'title': title,
            'poster_url': poster_url
        }
        match_list.append(doc)

    return jsonify({'result': 'success', 'match_list': match_list})


@app.route('/film_detail')
def find_film_detail():
    id_receive = request.args.get('id_give')

    return jsonify({'result': 'success', 'match_list': id_receive})





# path 값으로 poster url 크롤링
# @app.route('/test', methods=['GET'])
# def show_posters():
#     path = 'https://www.justwatch.com/kr/%EC%98%81%ED%99%94/1917'
#
#     # poster url 크롤링
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#     data = requests.get(path, headers=headers)
#     soup = BeautifulSoup(data.text, 'html.parser')
#
#     title_poster = soup.select_one('.title-poster > .title-poster__image')['src']
#     print(title_poster)
#     # posters 응답 데이터 보내주기
#     return jsonify({'result': 'success', 'posters': title_poster})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
