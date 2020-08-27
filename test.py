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
    print(filtered_offer)
    # pprint.pprint(filtered_offer)
    films = sorted(filtered_offer, key=itemgetter('provider_name'))
    print(films)
    temp_list = []
    for key, value in itertools.groupby(films, key=itemgetter('provider_name')):
        print(key)
        min_price = 100000000
        for i in value:
            print(i)
            if i['retail_price'] < min_price:
                min_price = i['retail_price']
                temp_list.append(i)
    print(temp_list)
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