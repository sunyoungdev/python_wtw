from justwatch import JustWatch
from pymongo import MongoClient

# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://sunyoungdev:sunyoung12!@3.34.95.220', 27017)
db = client.wtw
# just_watch = JustWatch(country='KR')
#
#
# # provider 별 모든 영화 추출하기
# # Todo : 스케쥴링 매주 디비 업데이트
#
#
# def get_film_db():
#     # 기존 콜렉션 삭제
#     db.film_list.drop()
#
#     # db 추출
#     saved_film_titles = []
#     providers = ['nfx', 'prv', 'wav', 'wac', 'nvs', 'ply']
#     for provider in providers:
#         for index in list(range(1, 21)):
#             results_full = just_watch.search_for_item(
#                 providers=[provider],
#                 content_types=['movie'],
#                 page=index,
#                 page_size=100
#             )
#             for film_item in results_full['items']:
#                 try:
#                     id = film_item['id']
#                     title = film_item['title']
#                     poster = film_item['poster']
#                     if not (title in saved_film_titles):
#                         saved_film_titles.append(title)
#                         doc = {
#                             'id': id,
#                             'title': title,
#                             'poster': poster
#                         }
#                         db.film_list.insert_one(doc, {'$ordered': False})
#                         # print(saved_film_titles)
#                 except Exception as ex:
#                     print('에러가 발생 했습니다', ex)
#     print(saved_film_titles)
