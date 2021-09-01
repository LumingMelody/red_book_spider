import time


def timestamp_to_format(timestamp=None, format='%Y-%m-%d %H:%M:%S'):
    # try:
    if timestamp:
        time_tuple = time.localtime(timestamp)
        print('time_tuple:', time_tuple)
        # print('type(time_tuple):',type(time_tuple))
        res = time.strftime(format, time_tuple)
    else:
        res = time.strftime(format)
    return res
    # except:
    #     print('error')


tss1 = '2021-05-27'
# 转为时间数组
timeArray = time.strptime(tss1, "%Y-%m-%d")
# print timeArray
# # timeArray可以调用tm_year等
# print timeArray.tm_year   # 2013
# 转为时间戳
timeStamp = int(time.mktime(timeArray))
print(timeStamp)  # 1381419600
