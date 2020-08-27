from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pprint
from functools import reduce

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.wtw


@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/detail')
# def detail():
#     return render_template('detail.html')


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


@app.route('/film_detail', methods=['GET'])
def find_film_detail():
    id_receive = request.args.get('id_give')
    film_full_url = 'https://apis.justwatch.com/content/titles/movie/' + id_receive + '/locale/ko_KR'
    # print(film_full_url)

    proxies = {'http': None, 'https': None}
    response_data = requests.get(film_full_url, proxies=proxies)
    infos = response_data.json()

    # 메인 이미지 주소
    main_image = infos['backdrops'][0]['backdrop_url'].replace('{profile}', 's1440')
    main_image_url = 'https://images.justwatch.com' + main_image
    # print(main_image_url)

    # 타이틀, 개봉연도
    title = infos['title']
    original_release_year = infos['original_release_year']
    # print(title, original_release_year)

    # 장르 텍스트로 변환
    genre_ids = infos['genre_ids']
    genre_type = {
        1: '액션', 2: '애니메이션', 3: '코미디', 4: '범죄', 5: '다큐멘터리', 6: '드라마', 7: '판타지', 8: '역사', 9: '공포',
        10: '가족', 11: '음악', 12: '스릴러', 13: '로맨스', 14: 'SF', 15: '스포츠', 16: '전쟁', 17: '서부', 18: 'Made in Europe'
    }

    def get_filtered_genre(genre_id):
        return genre_type[genre_id]

    filtered_genre = list(map(get_filtered_genre, genre_ids))
    # print(filtered_genre)

    # 런타임
    runtime = infos['runtime']
    # print(runtime)

    # 스코어링
    scores = infos['scoring']
    for idx in range(len(scores)):
        if scores[idx]['provider_type'] == 'imdb:score':
            imdb_score = scores[idx]['value']
            # print(imdb_score)

    # offer by provider
    offers = infos['offers']
    monetizationType = {
        'buy': '구매',
        'rent': '대여'
    }
    providerType = {
        3: 'Google Play', 96: 'Naver', 356: 'Wavve', 8: 'Netflix', 97: 'Watcha', 119: 'Prime Video'
    }

    def get_filtered_offer(offer):
        return {
            'monetization_type': monetizationType[offer['monetization_type']],
            'provider_name': providerType[offer['provider_id']],
            'retail_price': offer['retail_price'],
            'urls_standard_web': offer['urls']['standard_web']
        }

    filtered_offer = list(map(get_filtered_offer, offers))
    # pprint.pprint(filtered_offer)

    # description
    description = infos['short_description']
    # print(description)

    # credits(감독/배우)
    credits = infos['credits']
    actors = []
    directors = []
    for credit in credits:
        if credit['role'] == 'ACTOR':
            actors.append(credit['name'])
        elif credit['role'] == 'DIRECTOR':
            directors.append(credit['name'])

    # print(actors)
    # print(directors)

    doc = {
        'main_image_url': main_image_url,
        'title': title,
        'original_release_year': original_release_year,
        'genre': filtered_genre,
        'runtime': runtime,
        'score': imdb_score,
        'offers': filtered_offer,
        'description': description,
        'actors': actors,
        'directors': directors
    }

    return render_template('detail.html', doc=doc)






if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
