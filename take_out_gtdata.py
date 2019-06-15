import json

def month(m):
    mon={
        "Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,
        "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12
    }
    return mon.get(m)

def take_out(movie,released,timming="front",in_week=0,in_month=0):
    if in_month !=0:
        in_week+=4*in_month

    if timming=="next":
        in_week*=-1
    if "error" not in movie:
        r_year=int(released.split(" ")[-1])
        r_mon=released.split(" ")[-2]
        r_mon=month(r_mon)
        r_day=int(released.split(" ")[0])

        #print(count,r_year,r_mon,r_day)


        node_day=0
        day_count=0

        for m_data in movie["data"]:
            if int(m_data["date"][:4]) ==r_year and int(m_data["date"][5:7]) ==r_mon:
                    if node_day<r_day:
                        node_day=int(m_data["date"][-2:])
                        node_count=day_count
            day_count+=1

        #node_data= movie["data"][node_count]
        start_week=node_count-in_week

        out_put=0
        if timming =="front":
            for out_index in range(start_week,node_count):
                #print(movie["data"][out_index],movie["Actor_name"],released)
                out_put+=int(movie["data"][out_index]["Count"])
            #print("{},{},上映前{}周:搜尋總數:{}".format(movie["Actor_name"],released,in_week,out_put))
        if timming == "next":
            for out_index in range(node_count,start_week):
                #print(movie["data"][out_index],movie["Actor_name"],released)
                out_put += int(movie["data"][out_index]["Count"])
            #print("{},{},上映後{}周:搜尋總數:{}".format(movie["Actor_name"], released, abs(in_week), out_put))

        return out_put
    else :
        return "error"

def actor_count_col(actor_list,imdbID,actor_count,released,timming,week,month):
    count_sum=0
    for act in actor_list:
        if act[0] == imdbID:
            # print(act[1])
            actor=act[1]
            p_count=0
            for row in actor_count:
                if row["Actor_ID"]==actor:

                    try:
                        count =take_out(row,released,timming,week,month)
                        if count=="error":
                            count=0
                        p_count+=1
                    except:
                        count=0
                        p_count += 1
                    count_sum+=count
                    avg=count_sum/p_count
                    return avg




#
# with open("g_trends_scoreimdb2012.json","r") as t:
#     data=json.load(t)
# t.close()
#
# p=take_out(data[471],"next",1,0)
# print(p)
