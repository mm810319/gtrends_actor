import json
import csv
import os



def open_file_json(file):
    output_data=[]
    for f in file:
        with open(f,"r",encoding="utf-8") as op_f:
            input_data=json.load(op_f)
            for data in input_data:
                output_data.append(data)
        op_f.close()
    return output_data

def open_file_csv(file):
    output_data=[]
    for f in file:
        with open(f,"r",encoding="utf-8") as op_f:
            input_data=csv.reader(op_f)
            count = 0
            for data in input_data:
                if count == 0:
                    count += 1
                    continue
                output_data.append(data)
        op_f.close()
    return output_data

# test
# j_file=["./in_put_json/actor_trends.json","./in_put_json/actor_trends_10000-12959.json"]
# actor_count=open_file_json(j_file)
# print(actor_count[12595])
#
# movie_list_csv=[]
# movie_csv_file=os.listdir("./input_moviedata")
# for movie in movie_csv_file:
#     movie="./input_moviedata/"+movie
#     movie_list_csv.append(movie)
#
# movie_list=open_file_csv(movie_list_csv)
# print(os.listdir("./input_moviedata"))
# print(movie_list[0])
# print(movie_list[-1])
#
# movie2act_list_csv=[]
# movie2act_csv_file=os.listdir("./Movie_Actor_Name")
# for movie in movie2act_csv_file:
#     movie="./Movie_Actor_Name/"+movie
#     movie2act_list_csv.append(movie)
#
# movie2act_list=open_file_csv(movie2act_list_csv)
# print(os.listdir("./Movie_Actor_Name"))
# print(movie2act_list[0])
# print(movie2act_list[-1])
