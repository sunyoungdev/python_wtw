from justwatch import JustWatch
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.wtw

just_watch = JustWatch(country='KR')

# provider 별 모든 영화 추출하기
# Todo : max page 20까지만 추출되어 각 provider 별로 for문 돌린 상태,
#  따라서 provider 별 중복 영화 존재
for index in list(range(1, 21)):
    results_full = just_watch.search_for_item(
        # providers=['nfx', 'prv', 'wav', 'wac', 'nvs', 'ply'],
        providers=['ply'],
        content_types=['movie'],
        page=index,
        page_size=100
    )
    print(results_full)

    # title, full_path 만 추출해서 db에 넣기
    film_items = results_full['items']
    for film_item in film_items:
        title = film_item['title']
        path = film_item['full_path']

        doc = {
            'title': title,
            'path': path
        }

        db.film_list.insert_one(doc)












