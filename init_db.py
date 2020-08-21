from flask import Flask, render_template, jsonify, request
import requests
from justwatch import JustWatch
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.wtw

just_watch = JustWatch(country='KR')

results_full = just_watch.search_for_item(
    providers=['nfx', 'prv', 'wav', 'wac', 'nvs', 'ply'],
    content_types=['movie'],
    page_size=100
)

film_items = results_full['items']

for film_item in film_items:
    title = film_item['title']
    path = film_item['full_path']

    doc = {
        'title': title,
        'path': path
    }

    db.film_list.insert_one(doc)
    print('완료', title)

# print(results_full)
