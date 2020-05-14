import pymysql
import redis, json, time
import numpy as np
import matplotlib.pyplot as plt
from pymysql import *

#   redis数据转存mysql
def saveData():
    # redis数据库链接
    redis_client = redis.StrictRedis(host="106.12.213.43", port=6379, db=0, password='cyy19970502')
    # mysql数据库链接
    # mysql_client = connect(host="127.0.0.1", user="root", password="mysql", database="sina", port=3306, charset="uft8")
    mysql_client = connect(host="127.0.0.1", user="root", password="123456",
                     database="douban", port=3306, charset='utf8')
    cursor = mysql_client.cursor()
    i = 1
    while True:
        time.sleep(1)
        data = redis_client.blpop(["douban_book:items"], timeout=4)
        if data is None:
            print("break")
            break
        source,data = redis_client.blpop(["douban_book:items"], timeout=4)
        item = json.loads(data.decode())
        print("source===========", source)
        print("item===========", item)
        sql = "insert into url(bookName,author,press,originalName,pressYear,pageNum,price,binding,isbn,translator,publisher,rating,ratingSum,series,kind) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = [item["bookName"], item["author"], item["press"], item["originalName"], item["pressYear"],
                  item["pageNum"], item["price"], item["binding"], item["isbn"], item["translator"], item["publisher"],
                  item["rating"], item["ratingSum"], item["series"], item["kind"]]
        cursor.execute(sql, params)
        mysql_client.commit()
        i += 1

#   连接数据库，返回所得数据
def operateMysql(sql):
    conn = pymysql.connect(
        host='localhost',
        user="root",
        passwd="123456",
        database="douban",
        charset='utf8mb4',
    )
    cursor = conn.cursor()
    cursor.execute(sql)
    all_data = cursor.fetchall()
    conn.commit()
    conn.close()
    return all_data

#   清洗数据库价格数据并以柱状图显示
def operatePrice():
    price = {'<30':0, '30-60':0, '60-90':0, '90-120':0, '120-150':0, '150-180':0, '180-210':0, '>210':0}
    mysql = "select price from url where price<>'None';"
    result = operateMysql(mysql)
    for number in result:
        priceStr = ''
        for char in number[0]:
            if char.isdigit() or char == '.':
                priceStr += char
            elif char == '，':
                priceStr += '.'
        try:
            priceNum = float(priceStr.strip())
        except ValueError:
            continue
        if 'AUD' in number[0]:  # 澳元
            priceNum *= 4.8091
        elif 'NT$' in number[0] or 'NTD' in number[0] or 'TWD' in number[0]:  # 新台币
            priceNum *= 0.2312
        elif 'JPY' in number[0] or '円（税別）' in number[0]:  # 日元
            priceNum *= 0.06520
        elif '£' in number[0]:  # 英镑
            priceNum *= 9.0934
        elif '€' in number[0]:  # 欧元
            priceNum *= 9.0934
        elif 'SEK' in number[0]:  # 瑞典克朗
            priceNum *= 0.7257
        elif '円＋税' in number[0]:  # 日元
            priceNum *= 0.06520 * 1.08
        elif 'USD' in number[0]:  # 美元
            priceNum *= 7.092
        if priceNum < 30:
            price['<30'] +=1
        elif 30 <= priceNum < 60:
            price['30-60'] += 1
        elif 60 <= priceNum < 90:
            price['60-90'] += 1
        elif 90 <= priceNum < 120:
            price['90-120'] += 1
        elif 120 <= priceNum < 150:
            price['120-150'] += 1
        elif 150 <= priceNum < 180:
            price['150-180'] += 1
        elif 180 <= priceNum < 210:
            price['180-210'] += 1
        elif priceNum >= 210:
            price['>210'] += 1
    value = list(price.values())
    key = list(price.keys())
    pictureZhu(key, value)
    return price

# 价位柱状图
def pictureZhu(key,value):
    for rect in plt.bar(range(len(key)),value,color='rgb',tick_label=key):
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2. - 0.2,1.01*height,'%s'%int(height))
    plt.title('豆瓣图书价位分布', fontproperties='SimHei')
    plt.show()

#   清洗数据库评价数据并以柱状图显示
def operateRating():
    mysql = "select rating,ratingSum from url where rating<>'None' and ratingSum<>'None';"
    result = operateMysql(mysql)
    rating = []
    ratingSum = []
    for number in result:
        rating.append(float(number[0].strip()))
        ratingSum.append(float(number[1].strip()))
    pictureSan(ratingSum,rating)

#   评论散点图
def pictureSan(x,y):
    plt.scatter(x,y,s=10)
    plt.title('评论分数散点分布', fontsize=24, fontproperties='SimHei')
    plt.xlabel('评论人数', fontsize=14, fontproperties='SimHei')
    plt.ylabel('评分', fontsize=14, fontproperties='SimHei')
    plt.show()

def operateKind():
    kind = {'movie':0,'book':0,'music':0,'drama':0,'else':0}
    mysql = "select kind from url;"
    result = operateMysql(mysql)
    dataLength = len(result)
    for number in result:
        if number[0] == 'book':
            kind['book'] += 1
        elif number[0] == 'movie':
            kind['movie'] += 1
        elif number[0] == 'music':
            kind['music'] += 1
        elif number[0] == 'drama':
            kind['drama'] += 1
        else:
            kind['else'] += 1
    value = list(kind.values())
    key = list(kind.keys())
    for index in range(len(value)):
        value[index] = round(value[index]/dataLength,2)
    pictureBing(key, value)



# 跳转比例饼状图
def pictureBing(key,value):
    explode = (0.1, 0.3, 0.1, 0.1, 0.1)
    plt.pie(value, explode=explode, labels=key, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.title('请求跳转比例', fontproperties='SimHei')
    plt.show()


if __name__ == '__main__':
    saveData()
    operatePrice()
    operateRating()
    operateKind()

