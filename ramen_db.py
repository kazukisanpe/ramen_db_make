from bs4 import BeautifulSoup    # importする
import sys
import requests
import re
import time

#実行処理時間計測開始
start = time.time()

# Webページを取得して解析する
search_pref = "宮城県"
load_url = "https://p.eagate.573.jp/game/facility/search/p/list.html?gkey=SDVX&paselif=false&finder=keyword&keyword=" + search_pref
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")
store_cnt_ = soup.find(class_="cl_search_result")
elems = soup.find_all(class_ = "cl_shop_bloc")

#計測処理時間を出力
elapsed_time = time.time() - start
print ("実行結果:{:.2f}".format(elapsed_time) + "[sec]")