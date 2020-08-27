from justwatch import JustWatch
from pymongo import MongoClient
import requests

client = MongoClient('localhost', 27017)
db = client.wtw

just_watch = JustWatch(country='KR')

# provider 별 모든 영화 추출하기
# Todo : 스케쥴링 매주 디비 업데이트

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
            try:
                id = film_item['id']
                title = film_item['title']
                poster = film_item['poster']
                if not (title in final_movie_names):
                    final_movie_names.append(title)
                    doc = {
                        'id': id,
                        'title': title,
                        'poster': poster
                    }
                    db.film_list.insert_one(doc, {'$ordered': False})
                    # print(doc)
            except Exception as ex:
                print('에러가 발생 했습니다', ex)





# # test
#
# all_lists = list(db.film_list.find({}, {'_id': 0}))
#
# # print(all_lists)
#
# doc=[]
# for list in all_lists:
#     id = list['id']
#     doc.append(id)
#
#
# # print(doc)
#
# for idx in range(len(doc)):
#     id = doc[idx]
#
#     url = 'https://apis.justwatch.com/content/titles/movie/' + str(id) + '/locale/ko_KR'
#     response_data = requests.get(url)
#
#     infos = response_data.json()
#     id_num = infos['id']
#     genre_ids = infos['genre_ids']
#     print(id_num, genre_ids)

# 1 액션
# 2 애니메이션
# 3 코미디
# 4 범죄
# 5 다큐멘터리
# 6 드라마
# 7 판타지
# 8 역사
# 9 공포
# 10 가족
# 11 음악
# 12 스릴러
# 13 로맨스
# 14 SF
# 15 스포츠
# 16 전쟁
# 17 서부
# 18 Made in Europe
# genre_ids = [1,18,9]
#
# for idx in range(len(genre_ids)):
#     if genre_ids[idx] == 1:
#         genre_ids[idx] = '액션'
#     elif genre_ids[idx] == 2:
#         genre_ids[idx] = '애니메이션'
#     elif genre_ids[idx] == 3:
#         genre_ids[idx] = '코미디'
#     elif genre_ids[idx] == 4:
#         genre_ids[idx] = '범죄'
#     elif genre_ids[idx] == 5:
#         genre_ids[idx] = '다큐멘터리'
#     elif genre_ids[idx] == 6:
#         genre_ids[idx] = '드라마'
#     elif genre_ids[idx] == 7:
#         genre_ids[idx] = '판타지'
#     elif genre_ids[idx] == 8:
#         genre_ids[idx] = '역사'
#     elif genre_ids[idx] == 9:
#         genre_ids[idx] = '공포'
#     elif genre_ids[idx] == 10:
#         genre_ids[idx] = '가족'
#     elif genre_ids[idx] == 11:
#         genre_ids[idx] = '음악'
#     elif genre_ids[idx] == 12:
#         genre_ids[idx] = '스릴러'
#     elif genre_ids[idx] == 13:
#         genre_ids[idx] = '로맨스'
#     elif genre_ids[idx] == 14:
#         genre_ids[idx] = 'SF'
#     elif genre_ids[idx] == 15:
#         genre_ids[idx] = '스포츠'
#     elif genre_ids[idx] == 16:
#         genre_ids[idx] = '전쟁'
#     elif genre_ids[idx] == 17:
#         genre_ids[idx] = '서부'
#     elif genre_ids[idx] == 18:
#         genre_ids[idx] = 'Made in Europe'
#
#
# print(genre_ids)




