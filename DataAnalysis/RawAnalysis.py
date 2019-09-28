import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
from sklearn import linear_model
from sklearn.ensemble import  RandomForestRegressor

absdir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))#获取当前父文件夹路径
print(absdir)
userdir = absdir+'/'+'data/raw/'+'tianchi_fresh_comp_train_user0.csv'
itemdir = absdir+'/'+'data/raw/'+'tianchi_fresh_comp_train_item.csv'

#---------------------------------------数据初步分析-------------------------------------------
def DataDes(user,item):
    from project.DataAnalysis.PLOT import PlotBar
    curdir = os.path.abspath(os.path.dirname(__file__))

    #首先整体描述数据
    if not os.path.exists(curdir + '/TotalDescribe.txt'):
        f = open(curdir + '/TotalDescribe.txt', 'w')
        user_des = str(user_csv.describe())
        item_des = str(item_csv.describe())
        res = str(user_des)
        res = "userdes:\n" + user_des + "\n" + "itemdes:\n" + item_des + "\n" + "user_csv.head:\n" + str(
            user_csv.head()) + \
              "\n" + "item_csv.head:\n" + str(item_csv.head())
        f.write(res)
        f.close()
        print(res)
    else:
        print('描述文件已存在')
        with open(curdir + '/TotalDescribe.txt', 'r')as f:
            res = f.read()
            print(res)


    #分析用户id有多少重复
    #多少个用户
    usercount = len(user['user_id'].unique())
    print('----------有%d个用户信息'%(usercount))

    #这些用户买了多少商品0000000
    itemcount = len(user['item_id'].unique())
    print('----------有%d个商品信息' % (itemcount))

    #之后分析用户四种行为各自占比 浏览、收藏、加购物车、购买，对应取值分别是1、2、3、4
    behaviorDistribution = user['behavior_type'].value_counts()
    #不难发现多部分都是白嫖，真正买的微乎其微
    list_user_behavior_type = behaviorDistribution.tolist()
    print(list_user_behavior_type)

    Y = list_user_behavior_type
    X = ["浏览","收藏","加购物车","购买"]
    # X = [i for i in range(1,5)]
    #PlotBar("用户行为分布情况",X,Y)



    #时间分布
    year  = []
    for i in range(len(user['time'])):
        # print(user['time'][i])
        eachtime = str(user['time'][i])
        eachyear = eachtime.split()[0]
        year.append(eachyear)
    dfyear = DataFrame(year)
    user['year'] = dfyear
    year_count = user['year'].value_counts()
    list_year_and_day = year_count.tolist()
    #print(type(year_count))
    X = year_count.index
    #print(X)
    Y = list_year_and_day
    #PlotBar("用户产生行为的日期分布情况",X,Y)
    print('----------------------------------数据分析结束---------------------------------------')


#数据加载
def LoadData():
    print("-----------------------------------数据加载---------------------------------------")
    user_csv = pd.read_csv(userdir)
    item_csv = pd.read_csv(itemdir)
    return user_csv,item_csv




#提取特征
def extract_feature(user,item):
    from  project.Utils.PrintInfo import curline
    import time
    import datetime
    #用户id与各种行为的对应关系
    print('\n\n\n\n--------------------------提取特征-------------------------------------')


    #user_visit = user.iloc[:,[1,2,3]][user[user.T.index[0]]=='10001082']
    user_id_set = user['user_id'].unique()
    #print(user_id_set) #用户id集合
    curline(info= '开始分析每个用户每种行为的个数',isstart=True)
    totaldict  ={}
    for each in user_id_set:
         tmpdict = {}
         tmplist = []
         each_user_visit = user.loc[(user['user_id'] == each )]
         print(each_user_visit['time'])
         #浏览
         each_user_read_count = each_user_visit.loc[ (each_user_visit['behavior_type']==1)].shape[0]
         #收藏
         each_user_colection_count = each_user_visit.loc[each_user_visit['behavior_type'] == 2].shape[0]
         #加购物车
         each_user_cart_count = each_user_visit.loc[each_user_visit['behavior_type'] == 3].shape[0]
         #购买
         each_user_buy_count = each_user_visit.loc[ each_user_visit['behavior_type']==4].shape[0]
         tmplist.extend([each_user_read_count,each_user_colection_count,each_user_cart_count,each_user_buy_count])
         totaldict[each] = tmplist
    user_behavior_count_df  = (pd.DataFrame(totaldict)).T
    print(user_behavior_count_df) #输出每个用户对应的行为量


    # curline(info='',isstart=False)
    # for each in user_id_dict:




    curline(info= '开始分析日期情况个数',isstart=True)
    #将用户的浏览时间按日期排序
    timelist = []
    # for i in range(len(user['time'])):
    #      print(user['time'][i])
    #      striptime = str(user['time'][i])
    #      strippedtime = '-'.join(striptime.split())
    #      timelist.append(strippedtime)
    # dftime = DataFrame(timelist)
    # t1 = time.strptime('2014-12-03 01', "%Y-%m-%d %H")
    # t2 = time.strptime('2004-12-03 04', "%Y-%m-%d %H")
    # date1 = datetime.datetime(t1[0], t1[1], t1[2])
    # date2 = datetime.datetime(t2[0], t2[1], t2[2])
    # print(date1-date2)
    # curline(info='', isstart=False)



    curline(info='开始分析用户地理位置', isstart=True)
    geo_null_count = user['user_geohash'].isnull().sum()
    print('缺失值有%d个'%(geo_null_count))
    drropped_geo = user['user_geohash'].dropna().tolist()
    drropped_geo_set = set(drropped_geo)
    print('一共有%d个地方'%(len(drropped_geo_set)))
    # for each in drropped_geo_set:
    #     print(each+' '+ str(drropped_geo.count(each)))
    # print(user_visit)
    curline(info='', isstart=False)



    curline(info='开始分析商品种类', isstart=True)

if __name__=='__main__':
    user_csv,item_csv = LoadData()
    #DataDes(user_csv,item_csv)
    extract_feature(user_csv,item_csv)