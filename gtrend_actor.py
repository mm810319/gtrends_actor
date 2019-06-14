from pytrends.request import TrendReq #API
import json
import csv
# import time
# import random
# import requests
# from bs4 import BeautifulSoup

#將演員清單存成一個list
def take_actor_data(input_file):
    actor = []
    with open(input_file,"r",encoding="utf-8")as op_f:
        actor_data=csv.reader(op_f)
        for a in actor_data:
            actor.append(a)
    op_f.close()
    return actor

#提出list中每一筆的演員編號跟名稱,並各自存成list
def take_actor_id_name(actor_data):
    actor_id=[]
    actor_name = []

    for a in actor_data:
        actor_id.append(a[0])
        actor_name.append(a[1])
    return actor_id,actor_name

#主要程式
def go_to_do(proxies,input_count=1):
   #開檔案提取要輸入的資料
    input_file = "Main_Actor.csv"
    actor_data = take_actor_data(input_file)
    actor_id, actor_name = take_actor_id_name(actor_data)
   #初始值設定
    a_count = 0
    global b_count
    b_count=input_count
    out_file_name="actor_trends.json"
    #從輸入筆數(input_count)開始
    for actor in actor_name:
       # time.sleep(random.randint(3, 8))
        if a_count < input_count:
            a_count+=1
            continue
        #使用Api建立instance:  tz參數是時區 360為美國時區
        pytrend = TrendReq(tz=360,proxies=proxies)
        kw_list=[actor]
       #超過五年單位會變成月,因為要以周為單位所以將時間分成四個區段
        timeframe=["2004-01-01 2007-12-31","2008-01-01 2011-12-31","2012-01-01 2015-12-31","2016-01-01 2019-12-31"]
        out_data = []
        print("====開始第{}筆====".format(a_count))
        t_count=20
        for t in timeframe:
            #time.sleep(random.randint(2,8))
            #因使用proxy本身就換延遲所以不用sleep
            #搜尋使用的參數,其中cat=34 為電影類別,requests跟爬資料都是在此函式 執行
            pytrend.build_payload(kw_list=kw_list,cat=34,timeframe=t,geo='US',gprop='')
            #使用api的interest_over_time方法去取的Count的資料 ，用get是因為我們只對Count欄位有興趣
            data=pytrend.interest_over_time().get(kw_list)
            try:
                #col預設名稱為電影名稱，不方便以後取值使用，因此將col名稱一致改為count
                data.rename(columns={data.columns[0]: "Count"}, inplace=True)
                # 預設是dataframe的格式，轉成json用陣列處理
                preload = json.loads(data.to_json(orient='table'))['data']
                for p in preload:
                    p['date']=p['date'][0:10]#時間欄位格式到秒 ，改為只到日
                    out_data.append(p)
            except:
                print("{}%完成,沒值,區間:{}".format(t_count,t))
                t_count += 20
                continue
            print("{}%完成,有值,區間:{}".format(t_count,t))
           # time.sleep(random.randint(2, 5))
            t_count+=20
        #設定要輸出的字典
        output = dict([("Actor_ID", actor_id[a_count]), ("Actor_name", actor), ("data", out_data)])
        #輸出成 json
        with open(out_file_name,"a",encoding="utf-8") as out_f:
            if a_count==1:
                out_f.write("["+json.dumps(output)+"\n")
            else :
                out_f.write(','+json.dumps(output)+"\n")
        out_f.close()
        print("\n==第{}筆完成,演員:{},ID:{}==".format(a_count, actor, actor_id[a_count]))
        a_count += 1

        b_count = a_count #break時紀錄第幾筆開始

    with open(out_file_name, "a", encoding="utf-8") as out_f:
        out_f.write("]")
    out_f.close()
    global  complete_all
    complete_all=1

class CompleteError(Exception):
    pass

#此函示是為了ip被斷後要換新ip重連（要先把API本身的換IP關掉，API的崇廉實測有問題）
def rp_do(count,op_ip_list=None,ip_index=0):
    #沒輸入PROXY時，預設為使用本身IP
    if op_ip_list!=None:
        ip_list=op_ip_list[ip_index]
    else:
        ip_list=[]
    #完成時跳出COMPLETE ERROR
    #斷線時使用下一個IP重連
    try:
        go_to_do(ip_list,input_count=count)

        if complete_all==1:
            raise CompleteError('COMPLETE')

    except CompleteError:
        print("complete")
    except:
        count = b_count
        ip_index += 1
        print("ip被斷重連使用新IP-({}):{}".format(ip_index,ip_list))
        rp_do(count,op_ip_list,ip_index)
#開PROXY列表的函示,op參數為從第幾個IP開始抓
def open_ip_list(filename,op=0):
    op_ip_list = []
    ip_count=0
    with open(filename, "r", encoding="utf-8")as op_f:

        ipdata =csv.reader(op_f)
        for ip in ipdata:
            if ip_count<op:
                ip_count+=1
                continue
            op_ip_list.append(ip)
    op_f.close()
    return op_ip_list

def main():

    op_ip_list=open_ip_list("proxy4.csv")
    rp_do(1,op_ip_list=op_ip_list)
main()
