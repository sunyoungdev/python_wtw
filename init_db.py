from justwatch import JustWatch
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.wtw

just_watch = JustWatch(country='KR')

# provider 별 모든 영화 추출하기
# Todo : max page 20까지만 추출되어 각 provider 별로 for문 돌린 상태,
#  따라서 provider 별 중복 영화 존재

final_movie_names = []
providers = ['nfx', 'prv', 'wav', 'wac', 'nvs', 'ply']
for provider in providers:
    for index in list(range(1, 21)):
        results_full = just_watch.search_for_item(
            providers=[provider],
            content_types=['movie'],
            page=index,
            page_size=100
        )
        for film_item in results_full['items']:
            id = film_item['id']
            title = film_item['title']
            if not (title in final_movie_names):
                final_movie_names.append(title)
                doc = {
                    'id': id,
                    'title': title,
                }
                db.film_list.insert_one(doc)












