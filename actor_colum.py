from inputdata import open_file_json,open_file_csv
import json
import csv
import os
from take_out_gtdata import take_out,actor_count_col
import pandas as pd

#演員GOOLE_Trends資料
j_file=["./in_put_json/actor_trends.json","./in_put_json/actor_trends_10000-12959.json"]
actor_count=open_file_json(j_file)
#電影資料
movie_list_csv=[]
movie_csv_file=os.listdir("./input_moviedata")
for movie in movie_csv_file:
    movie="./input_moviedata/"+movie
    movie_list_csv.append(movie)
movie_list=open_file_csv(movie_list_csv)
#電影對應演員表
movie2act_list_csv=[]
movie2act_csv_file=os.listdir("./m2a")
for movie in movie2act_csv_file:
    movie="./m2a/"+movie
    movie2act_list_csv.append(movie)
movie2act_list=open_file_csv(movie2act_list_csv)
output_file="actor_avg_trend.csv"
c=["index","imdbID","Title","rleased","2_mon_ago","1_mon_ago","2_week_ago","1_week_ago","2_mon_later","1_mon_later","2_week_later","1_week_later"]
with open(output_file, "a", encoding="utf-8", newline='') as op_f:
    writer = csv.writer(op_f)
    writer.writerow(c)
op_f.close()
m_count=0

for movie in movie_list:
    col_list=[]
    imdbID = movie[0]
    title = movie[1]
    released = movie[17]
    count_sum=0
    output_2m_ago = actor_count_col(movie2act_list,imdbID,actor_count,released,"front",0,2)
    output_1m_ago = actor_count_col(movie2act_list, imdbID, actor_count, released, "front", 0, 1)
    output_2w_ago = actor_count_col(movie2act_list, imdbID, actor_count, released, "front", 2, 0)
    output_1w_ago = actor_count_col(movie2act_list, imdbID, actor_count, released, "front", 1, 0)
    output_2m_later = actor_count_col(movie2act_list, imdbID, actor_count, released, "next", 0, 2)
    output_1m_later = actor_count_col(movie2act_list, imdbID, actor_count, released, "next", 0, 1)
    output_2w_later = actor_count_col(movie2act_list, imdbID, actor_count, released, "next", 2, 0)
    output_1w_later = actor_count_col(movie2act_list, imdbID, actor_count, released, "next", 1, 0)

    s = pd.Series([m_count,imdbID,title , released,output_2m_ago,output_1m_ago,output_2w_ago,output_1w_ago,
                   output_2m_later, output_1m_later,output_2w_later,output_1w_later] ,index=c)
    with open(output_file,"a",encoding="utf-8",newline='') as op_f:
        writer = csv.writer(op_f)
        writer.writerow(s)
    op_f.close()
    print(m_count)
    # if m_count == b_count:
    #     break
    m_count+=1




