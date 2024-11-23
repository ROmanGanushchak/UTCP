import requests, lxml
from bs4 import BeautifulSoup
import json
import time



# words = []
#
# # with open("words.json", "r") as f:
# #     print(json.loads(f.readlines()[0]))
#
# with open("words_urls.txt", "r") as f_r:
#     for letter_pair_url in f_r.readlines():
#         letter_pair_url = letter_pair_url.replace("\n", "")
#         q = requests.get(letter_pair_url)
#         code = q.content
#         soup = BeautifulSoup(code, "lxml")
#
#         for word_list in soup.find_all("div", class_="word-list"):
#             for word in word_list.find_all("li", class_="word-list__item"):
#                 words.append(word.a.text)
#
#         time.sleep(1)
#         print("letter_done")
#
#
# with open("words.json", "w") as f:
#     f.write(json.dumps(words))



# url = "http://ukrlit.org/slovnyk"
# with open("words_urls.txt", "w") as f:
#     q = requests.get(url)
#     code = q.content
#     soup = BeautifulSoup(code, "lxml")
#
#     for table in