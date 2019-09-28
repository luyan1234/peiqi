import os
import datetime
dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print(dir)
#行数 23291028,太大了也
def Getlines(name):#获得行数
    count = 0
    for index, line in enumerate(open(name, 'r')):
        count += 1
    print(count)

def cut(name,size):#路径名和每个文件的大小，单位是行数
    i = 0
    findex = 0
    with open(name,'r')as f:
        subdir = dir+'/'+'data/raw/tianchi_fresh_comp_train_user'+str(findex)+'.csv'
        if not os.path.exists(subdir):
            file = open(subdir,'w')
            wr  =True
        else:
            wr = False
        for line in f:
            # print(line)
            if wr:
                file.write(line)
            i+=1
            if i>=size:
                if wr:
                    file.close()
                i = 0
                findex+=1
                subdir = dir + '/' + 'data/raw/tianchi_fresh_comp_train_user' + str(findex) + '.csv'
                if not os.path.exists(subdir):
                    file = open(subdir, 'w')
                    wr  = True
def SortByTime(timeseries):
    import operator
    import functools
    def cmp_datetime(a, b):
        a_datetime = datetime.datetime.strptime(a, '%Y-%m-%d %H')
        b_datetime = datetime.datetime.strptime(b, '%Y-%m-%d %H')

        if a_datetime > b_datetime:
            return -1
        elif a_datetime < b_datetime:
            return 1
        else:
            return 0

    res = sorted(timeseries, key=functools.cmp_to_key(cmp_datetime),reverse=True)
    print(res)

#先弄100万行，后续用pickle搞
# cut(dir+'/'+'data/raw/tianchi_fresh_comp_train_user.csv',1000000)
# Getlines(dir+'/'+'data/raw/tianchi_fresh_comp_train_user.csv')
SortByTime(['2017-09-21 02', '2017-09-15 23', '2017-09-18 04'])