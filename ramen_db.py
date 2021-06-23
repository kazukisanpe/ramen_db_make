from bs4 import BeautifulSoup    # importする
import sys
import requests
import re
import time

#実行処理時間計測開始
start = time.time()

# Webページを取得して解析する
search_pref = "宮城県"
loop_flg = 1 #loop用フラグ
page_cnt = 0 #ページカウンター
cnt = 0 #該当件数
while loop_flg:    
    page_cnt = page_cnt + 1
    load_url = "https://ramendb.supleks.jp/search?page=" + str(page_cnt) + "&state=miyagi&city=&order=point&station-id=0&tags=3"
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")
    elems = soup.find_all(class_ = "info")
    

    if page_cnt == 3:
        break

    for num in range(len(elems)):
        print(elems[num].h4)
        '''
        ramen_info = list()
        cnt = cnt + 1
        ramen_info.append(str(cnt))
        print(elems[num])
        ramen_info.append(elems[num].attrs['href']) #店舗名
        ramen_info.append(elems[num].attrs['src'] if elems[num].attrs['src'] != "" else "データなし") #所在地
        ramen_info.append(search_pref) #所在県
        ramen_info.append(elems[num].attrs['data-holiday'] if elems[num].attrs['data-holiday'] != "" else "データなし") #定休日
        ramen_info.append(elems[num].attrs['data-operationtime'] if elems[num].attrs['data-operationtime'] != "" else "データなし") #営業時間
        ramen_info.append(elems[num].attrs['data-telno'] if elems[num].attrs['data-telno'] != "" else "データなし") #電話番号
        ramen_info.append(elems[num].attrs['data-latitude'] if elems[num].attrs['data-latitude'] != "" else "データなし") #緯度
        ramen_info.append(elems[num].attrs['data-longitude'] if elems[num].attrs['data-longitude'] != "" else "データなし") #経度
        '''
        

#計測処理時間を出力
elapsed_time = time.time() - start
print ("実行結果:{:.2f}".format(elapsed_time) + "[sec]")