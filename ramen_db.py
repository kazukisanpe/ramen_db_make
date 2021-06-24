from bs4 import BeautifulSoup    # importする
import sys
import requests
import re
import time

#実行処理時間計測開始
start = time.time()

#引数を取得
args = sys.argv
search_pref = args[1]

if "東京" == search_pref:
    search_pref = search_pref + "都"
elif "京都" == search_pref or "大阪" == search_pref:
    search_pref = search_pref + "府"
print(search_pref)

#都道府県ローマ字辞書データ
pref_dic = [
    ['北海道','hokkaido'],
    ['青森県','aomori'],
    ['岩手県','iwate'],
    ['秋田県','akita'],
    ['宮城県','miyagi'],
    ['山形県','yamagata'],
    ['福島県','fukushima'],
    ['茨城県','ibaraki'],
    ['栃木県','tochigi'],
    ['群馬県','gunma'],
    ['埼玉県','saitama'],
    ['千葉県','chiba'],
    ['東京都','tokyo'],
    ['神奈川県','kanagawa'],
    ['新潟県','niigata'],
    ['富山県','toyama'],
    ['石川県','ishikawa'],
    ['福井県','fukui'],
    ['山梨県','yamanashi'],
    ['長野県','nagano'],
    ['岐阜県','gifu'],
    ['静岡県','shizuoka'],
    ['愛知県','aichi'],
    ['滋賀県','shiga'],
    ['京都府','kyoto'],
    ['大阪府','osaka'],
    ['兵庫県','hyogo'],
    ['奈良県','nara'],
    ['三重県','mie'],
    ['和歌山県','wakayama'],
    ['鳥取県','tottori'],
    ['島根県','shimane'],
    ['岡山県','okayama'],
    ['広島県','hiroshima'],
    ['山口県','yamaguchi'],
    ['徳島県','tokushima'],
    ['香川県','kagawa'],
    ['愛媛県','ehime'],
    ['高知県','kochi'],
    ['福岡県','fukuoka'],
    ['佐賀県','saga'],
    ['長崎県','nagasaki'],
    ['大分県','oita'],
    ['熊本県','kumamoto'],
    ['宮崎県','miyazaki'],
    ['鹿児島県','kagoshima'],
    ['沖縄県','okinawa']
    ]

for num in range(len(pref_dic)):
    if search_pref == pref_dic[num][0]:
        search_pref = pref_dic[num][1]

page_cnt = 0 #ページカウンター
cnt = 0 #該当件数
while 1:    
    page_cnt = page_cnt + 1
    load_url = "https://ramendb.supleks.jp/search?page=" + str(page_cnt) + "&state=" + search_pref + "&city=&order=point&station-id=0&tags=3"
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")
    elems = soup.find_all(class_ = "info")
    if len(elems) == 0:
        break
    print(str(page_cnt) + "ページ目")


    for num in range(len(elems)):
        #print(elems[num].h4.text) #店名
        status_plate_retire = elems[num].find(class_ = "status_plate") #閉店情報取得
        if status_plate_retire == None:
            pass
        else:
            print(status_plate_retire.text + "しました")

        load_url = "https://ramendb.supleks.jp" + elems[num].h4.a['href'] #詳細ページURL
        html = requests.get(load_url)
        soup = BeautifulSoup(html.content, "html.parser")
        #ramen_photo = soup.find_all(id="shop-head")
        elems_detail = soup.find_all(id = "data-table") #elemsだとループのレンジ取ってるのでおかしくなる
        if len(elems) == 0:
            print("データがありません")
            break

        for num_detail in range(len(elems_detail)):
            cnt = cnt + 1 #件数
            print(str(cnt) + "件目")
            print("店舗名：" + elems_detail[num_detail].find(itemprop='name').text) #店名
            #addressに郵便番号、住所、移転先が混じってしまう
            address = elems_detail[num_detail].find(itemprop='address').text.split(" ")
            #郵便番号の有無を判定
            if address[0][0:1] != "〒":
                address_number = "情報なし"
                address_place = address[0]
            else:
                address_number = address[0]
                address_place_ = address[1] #address_place_には移転先情報も混じっている可能性あり
            #移転先情報を"このお店は"で分割
            moved_or_place = address_place_.split("このお店は")
            #移転先情報の有無を判定
            if len(moved_or_place) == 1:
                address_place = moved_or_place[0] #住所のみ
                moved_info = ""
                moved_flg = 0
            else:
                address_place = moved_or_place[0] #住所
                moved_info = moved_or_place[1] #移転先
                moved_flg = 1

            print("営業時間：" + "まだ取得できてません許してください")
            print("郵便番号：" + address_number)
            print("住所：" + address_place)
            if moved_flg == 1: 
                print("移転情報：" + moved_info)
            print("電話番号：" + elems_detail[num_detail].find(itemprop='telephone').text)
            print("")

        '''
        ramen_info = list()
        cnt = cnt 1
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